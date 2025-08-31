from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import traceback
import asyncio
import threading

# Import Advanced DD-AI v2.1
try:
    from advanced_financial_bert import AdvancedFinancialBERT, RiskAssessmentResult
    ADVANCED_AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Advanced AI not available: {e}")
    ADVANCED_AI_AVAILABLE = False

# Versão atualizada para refletir as mudanças de design
app = FastAPI(title="DD-AI SQL Server API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Temporariamente para debug
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS Pydantic ---

# ALTERADO: Modelo reutilizável para os detalhes da conexão
class ConnectionDetails(BaseModel):
    server: str
    database: str
    port: int = 1433
    use_windows_auth: bool = True
    username: Optional[str] = None
    password: Optional[str] = None

# ALTERADO: Requisição de query agora inclui os detalhes da conexão
class QueryRequest(BaseModel):
    connection: ConnectionDetails
    query: str

# NOVO: Modelos para análise avançada de risco
class RiskAnalysisRequest(BaseModel):
    text: str
    include_explanation: bool = True
    connection: Optional[ConnectionDetails] = None

class RiskAnalysisResponse(BaseModel):
    success: bool
    risk_level: str
    confidence_score: float
    risk_factors: List[str]
    compliance_flags: List[str]
    explanation: str
    financial_entities: Dict[str, List[str]]
    regulatory_alerts: List[str]
    model_info: Dict[str, Any]
    
# --- INICIALIZAÇÃO GLOBAL ---

# Inicializar modelo avançado DD-AI v2.1
advanced_bert_model = None
if ADVANCED_AI_AVAILABLE:
    try:
        print("🚀 Inicializando Advanced DD-AI v2.1...")
        advanced_bert_model = AdvancedFinancialBERT(use_qlora=True)
        print("✅ Advanced DD-AI v2.1 inicializado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Advanced AI: {e}")
        advanced_bert_model = None

# --- FUNÇÕES AUXILIARES ---

# NOVO: Função centralizada para criar a string de conexão de forma segura
def get_db_connection_string(details: ConnectionDetails) -> str:
    """Cria a string de conexão a partir dos detalhes fornecidos."""
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={details.server},{details.port};DATABASE={details.database};"
    if details.use_windows_auth:
        conn_str += "Trusted_Connection=yes;"
    elif details.username and details.password:
        conn_str += f"UID={details.username};PWD={details.password};"
    else:
        # Lança um erro se a autenticação SQL for escolhida sem credenciais
        raise ValueError("Para autenticação SQL, username e password são obrigatórios.")
    return conn_str

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {
        "message": "DD-AI SQL Server API",
        "status": "running",
        "version": "3.0.0"
    }

# ALTERADO: Endpoint para testar a conexão. Recebe os detalhes diretamente.
@app.post("/api/test-connection")
async def test_connection(request: ConnectionDetails):
    """Endpoint para testar a conexão com o SQL Server."""
    try:
        conn_str = get_db_connection_string(request)
        # Timeout baixo para testes rápidos
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION, DB_NAME()")
        result = cursor.fetchone()
        conn.close()
        
        return {
            "success": True,
            "message": "Conexão estabelecida com sucesso!",
            "server_version": result[0].split(' - ')[0] if result else "Unknown",
            "database": result[1] if result else "Unknown"
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=400, 
            detail=f"Erro na conexão: {str(e)}"
        )

# ALTERADO: Endpoint para executar query. Recebe a query e a conexão.
@app.post("/api/execute-query")
async def execute_query(request: QueryRequest):
    """Endpoint para executar queries SQL. ATENÇÃO: Risco de SQL Injection."""
    try:
        conn_str = get_db_connection_string(request.connection)
        conn = pyodbc.connect(conn_str, timeout=20)
        cursor = conn.cursor()
        
        cursor.execute(request.query)
        
        # Se a query for um SELECT, retorna os dados
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            conn.close()
            return {
                "success": True,
                "columns": columns,
                "data": data,
                "row_count": len(data)
            }
        # Se for INSERT, UPDATE, DELETE, etc.
        else:
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            return {
                "success": True,
                "message": f"Query executada com sucesso. {affected_rows} linhas afetadas."
            }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=400, 
            detail=f"Erro ao executar a query: {str(e)}"
        )

# ALTERADO: Endpoint para listar tabelas. Agora é POST para receber os detalhes da conexão.
@app.post("/api/tables")
async def get_tables(request: ConnectionDetails):
    """Lista todas as tabelas (com seus schemas) do banco de dados especificado."""
    try:
        conn_str = get_db_connection_string(request)
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        # Retorna no formato "schema.tabela"
        tables = [f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}" for row in cursor.fetchall()]
        conn.close()
        
        return {"success": True, "tables": tables}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=400, 
            detail=f"Erro ao listar tabelas: {str(e)}"
        )

# NOVO: Endpoint para análise avançada de risco financeiro
@app.post("/api/analyze-risk", response_model=RiskAnalysisResponse)
async def analyze_financial_risk(request: RiskAnalysisRequest):
    """
    Análise avançada de risco financeiro usando DD-AI v2.1 com FinBERT-PT-BR e QLoRA
    
    Features:
    - Análise de texto em português brasileiro
    - Detecção de compliance CVM/BACEN
    - Identificação de red flags regulatórios
    - Explicação detalhada com IA
    """
    if not ADVANCED_AI_AVAILABLE or advanced_bert_model is None:
        raise HTTPException(
            status_code=503,
            detail="Advanced DD-AI v2.1 não está disponível. Instale as dependências: pip install peft bitsandbytes accelerate"
        )
    
    try:
        # Executar análise em thread separada para não bloquear
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: advanced_bert_model.analyze_risk(
                request.text, 
                request.include_explanation
            )
        )
        
        # Obter informações do modelo para auditoria
        model_info = advanced_bert_model.get_model_info()
        
        return RiskAnalysisResponse(
            success=True,
            risk_level=result.risk_level,
            confidence_score=result.confidence_score,
            risk_factors=result.risk_factors,
            compliance_flags=result.compliance_flags,
            explanation=result.explanation,
            financial_entities=result.financial_entities,
            regulatory_alerts=result.regulatory_alerts,
            model_info=model_info
        )
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise de risco: {str(e)}"
        )

# NOVO: Endpoint para análise de dados do SQL Server
@app.post("/api/analyze-sql-data")
async def analyze_sql_data(request: QueryRequest):
    """
    Executa query SQL e analisa os resultados com DD-AI v2.1
    Combina acesso a dados com análise avançada de risco
    """
    if not ADVANCED_AI_AVAILABLE or advanced_bert_model is None:
        raise HTTPException(
            status_code=503,
            detail="Advanced DD-AI v2.1 não está disponível"
        )
    
    try:
        # Executar query SQL
        conn_str = get_db_connection_string(request.connection)
        conn = pyodbc.connect(conn_str, timeout=20)
        cursor = conn.cursor()
        
        cursor.execute(request.query)
        
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            conn.close()
            
            # Analisar cada linha de dados
            analyses = []
            for row in data[:10]:  # Limitar a 10 registros para performance
                # Converter dados em texto para análise
                text_data = " ".join([f"{k}: {v}" for k, v in row.items() if v is not None])
                
                # Executar análise de risco
                loop = asyncio.get_event_loop()
                risk_analysis = await loop.run_in_executor(
                    None,
                    lambda: advanced_bert_model.analyze_risk(text_data, False)
                )
                
                analyses.append({
                    "row_data": row,
                    "risk_analysis": {
                        "risk_level": risk_analysis.risk_level,
                        "confidence": risk_analysis.confidence_score,
                        "risk_factors": risk_analysis.risk_factors,
                        "compliance_flags": risk_analysis.compliance_flags
                    }
                })
            
            return {
                "success": True,
                "query_results": {
                    "columns": columns,
                    "total_rows": len(data),
                    "analyzed_rows": len(analyses)
                },
                "risk_analyses": analyses,
                "summary": {
                    "high_risk_count": sum(1 for a in analyses if a["risk_analysis"]["risk_level"] in ["ALTO", "CRÍTICO"]),
                    "total_analyzed": len(analyses)
                }
            }
        else:
            conn.commit()
            conn.close()
            return {
                "success": True,
                "message": "Query executada (não SELECT), análise não aplicável"
            }
            
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise SQL: {str(e)}"
        )

# NOVO: Endpoint para informações do modelo
@app.get("/api/model-info")
async def get_model_info():
    """Retorna informações detalhadas do modelo DD-AI v2.1 para auditoria"""
    if not ADVANCED_AI_AVAILABLE or advanced_bert_model is None:
        return {
            "available": False,
            "message": "Advanced DD-AI v2.1 não está disponível"
        }
    
    try:
        model_info = advanced_bert_model.get_model_info()
        return {
            "available": True,
            "model_info": model_info
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

# NOVO: Endpoint para análise integrada SQL → Enriquecimento → IA
@app.post("/api/sql-to-analysis")
async def sql_to_analysis(request: QueryRequest) -> Dict[str, Any]:
    """
    Executa query SQL e faz análise completa automaticamente:
    1. Executa query SQL
    2. Extrai CNPJs dos resultados
    3. Enriquece dados via API Brasil
    4. Busca notícias (simulado)
    5. Análise de risco com IA
    6. Relatório consolidado
    """
    if not ADVANCED_AI_AVAILABLE or advanced_bert_model is None:
        raise HTTPException(status_code=503, detail="Advanced AI module not available")
    
    try:
        import time
        import requests
        from datetime import datetime
        import re
        
        start_time = time.time()
        
        # 1. Executar query SQL
        connection_string = get_db_connection_string(request.connection)
        cnx = pyodbc.connect(connection_string)
        cursor = cnx.cursor()
        
        cursor.execute(request.query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        
        # Extrair CNPJs dos resultados
        cnpjs = []
        cnpj_pattern = re.compile(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}')
        
        for row in rows:
            for value in row:
                if isinstance(value, str) and cnpj_pattern.match(value):
                    cnpjs.append(value)
                    break  # Pegar apenas o primeiro CNPJ por linha
        
        cursor.close()
        cnx.close()
        
        if not cnpjs:
            return {
                'success': False,
                'error': 'Nenhum CNPJ encontrado na query'
            }
        
        # 2. Enriquecer dados via API Brasil
        enriched_data = []
        for cnpj in cnpjs:
            try:
                clean_cnpj = ''.join(filter(str.isdigit, cnpj))
                response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    enriched_data.append({
                        'cnpj': cnpj,
                        'razao_social': data.get('razao_social', ''),
                        'nome_fantasia': data.get('nome_fantasia', ''),
                        'situacao': data.get('descricao_situacao_cadastral', ''),
                        'atividade_principal': data.get('cnae_fiscal_descricao', ''),
                        'porte': data.get('porte', ''),
                        'capital_social': data.get('capital_social', 0),
                        'municipio': data.get('municipio', ''),
                        'uf': data.get('uf', ''),
                        'enrichment_success': True
                    })
                else:
                    enriched_data.append({
                        'cnpj': cnpj,
                        'razao_social': f'CNPJ {cnpj}',
                        'enrichment_success': False
                    })
                    
                time.sleep(0.3)  # Rate limiting
                
            except Exception:
                enriched_data.append({
                    'cnpj': cnpj,
                    'razao_social': f'CNPJ {cnpj}',
                    'enrichment_success': False
                })
        
        # 3. Análise de risco para cada empresa
        results = []
        for company_data in enriched_data:
            # Simular notícias (em produção, integrar APIs reais)
            news_data = [
                {
                    'title': f'Análise financeira de {company_data.get("razao_social", "")}',
                    'content': f'Relatório corporativo sobre {company_data.get("razao_social", "")} indicando performance no setor financeiro...',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'relevance': 0.85
                }
            ]
            
            # Análise de risco com IA
            analysis_text = f"""
            Análise de risco corporativo:
            
            Dados da empresa:
            - Razão Social: {company_data.get('razao_social', 'N/A')}
            - CNPJ: {company_data.get('cnpj', 'N/A')}
            - Situação Cadastral: {company_data.get('situacao', 'N/A')}
            - Atividade Principal: {company_data.get('atividade_principal', 'N/A')}
            - Porte Empresarial: {company_data.get('porte', 'N/A')}
            - Capital Social: R$ {company_data.get('capital_social', 0)}
            - Localização: {company_data.get('municipio', '')}/{company_data.get('uf', '')}
            
            Contexto de notícias:
            {news_data[0]['content'][:300]}...
            
            Avalie o risco financeiro considerando compliance regulatório brasileiro.
            """
            
            risk_result = advanced_bert_model.analyze_risk(analysis_text)
            
            results.append({
                'company_data': company_data,
                'news_data': news_data,
                'risk_analysis': {
                    'success': True,
                    'risk_level': risk_result.risk_level,
                    'confidence': risk_result.confidence_score,
                    'explanation': risk_result.explanation,
                    'compliance_flags': risk_result.compliance_flags,
                    'regulatory_alerts': risk_result.regulatory_alerts
                },
                'processing_time': time.time() - start_time
            })
        
        # 4. Compilar relatório final
        total_time = time.time() - start_time
        successful_enrichments = len([r for r in enriched_data if r.get('enrichment_success')])
        successful_analyses = len(results)
        
        risk_levels = [r['risk_analysis']['risk_level'] for r in results]
        risk_counts = {}
        for level in risk_levels:
            risk_counts[level] = risk_counts.get(level, 0) + 1
        
        return {
            'success': True,
            'metadata': {
                'query_executed': request.query,
                'total_cnpjs': len(cnpjs),
                'successful_enrichments': successful_enrichments,
                'successful_analyses': successful_analyses,
                'total_processing_time': total_time,
                'analysis_date': datetime.now().isoformat()
            },
            'risk_distribution': risk_counts,
            'results': results,
            'summary': {
                'companies_analyzed': len(results),
                'enrichment_success_rate': f"{(successful_enrichments/len(cnpjs)*100):.1f}%",
                'analysis_success_rate': f"{(successful_analyses/len(cnpjs)*100):.1f}%",
                'avg_processing_time': f"{total_time/len(cnpjs):.2f}s"
            }
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro na análise integrada: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando DD-AI SQL Server API v3.0.0 na porta 8001...")
    print("🌐 Endpoints disponíveis:")
    print("   - POST /api/test-connection")
    print("   - POST /api/execute-query") 
    print("   - POST /api/tables")
    print("   🆕 DD-AI v2.1 Advanced Features:")
    print("   - POST /api/analyze-risk (Análise de risco financeiro)")
    print("   - POST /api/analyze-sql-data (Query + Análise IA)")
    print("   - POST /api/sql-to-analysis (Query → Enriquecimento → IA) ⭐ NOVO!")
    print("   - GET  /api/model-info (Informações do modelo)")
    
    if ADVANCED_AI_AVAILABLE and advanced_bert_model:
        print("✅ Advanced DD-AI v2.1 com QLoRA ativo")
    else:
        print("⚠️ Advanced DD-AI v2.1 não disponível")
        
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")