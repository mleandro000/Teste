#!/usr/bin/env python3
"""
🚀 BATCH ANALYSIS - Advanced DD-AI v2.1
=======================================

Sistema para análise em lote de CNPJs extraídos de queries SQL.

Fluxo:
1. 📊 Executa query SQL e extrai CNPJs
2. 🔍 Enriquece cada CNPJ via API Brasil
3. 📰 Busca notícias sobre cada empresa
4. 🧠 Analisa risco com IA
5. 📋 Gera relatório consolidado

Entrada: Query SQL ou lista de CNPJs
Saída: Relatório completo de análise de risco
"""

import requests
import json
import re
import time
import pyodbc
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import concurrent.futures
from pathlib import Path

@dataclass
class BatchAnalysisRequest:
    """Requisição de análise em lote"""
    cnpjs: List[str]
    connection_details: Optional[Dict] = None
    sql_query: Optional[str] = None
    include_news: bool = True
    include_enrichment: bool = True
    max_concurrent: int = 5
    output_format: str = "json"  # json, markdown, excel

@dataclass
class CompanyBatchResult:
    """Resultado da análise de uma empresa"""
    cnpj: str
    razao_social: str
    enrichment_data: Dict
    news_analysis: List[Dict]
    risk_assessment: Dict
    final_risk_score: float
    processing_time: float
    errors: List[str]

class BatchAnalyzer:
    def __init__(self, api_base_url: str = "http://127.0.0.1:8001"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DD-AI-BatchAnalyzer/2.1'
        })
        
    def extract_cnpjs_from_sql_result(self, sql_results: List[Dict]) -> List[str]:
        """
        Extrai CNPJs de resultados SQL
        """
        cnpjs = []
        
        for row in sql_results:
            for key, value in row.items():
                if isinstance(value, str):
                    # Buscar padrões de CNPJ
                    cnpj_matches = re.findall(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}', value)
                    cnpjs.extend(cnpj_matches)
        
        # Limpar e validar CNPJs
        valid_cnpjs = []
        for cnpj in set(cnpjs):  # Remove duplicatas
            clean_cnpj = re.sub(r'[^\d]', '', cnpj)
            if len(clean_cnpj) == 14:
                valid_cnpjs.append(cnpj)
        
        return valid_cnpjs
    
    def execute_sql_and_extract_cnpjs(self, connection_details: Dict, query: str) -> List[str]:
        """
        Executa query SQL e extrai CNPJs automaticamente
        """
        try:
            print(f"🔍 Executando query SQL...")
            
            # Construir string de conexão
            if connection_details.get('use_windows_auth', True):
                conn_str = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={connection_details['server']};
                DATABASE={connection_details['database']};
                Trusted_Connection=yes;
                """
            else:
                conn_str = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={connection_details['server']};
                DATABASE={connection_details['database']};
                UID={connection_details['username']};
                PWD={connection_details['password']};
                """
            
            # Executar query
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                
                # Obter colunas
                columns = [column[0] for column in cursor.description]
                
                # Obter dados
                rows = cursor.fetchall()
                
                # Converter para lista de dicionários
                results = []
                for row in rows:
                    results.append(dict(zip(columns, row)))
                
                print(f"✅ Query executada: {len(results)} registros")
                
                # Extrair CNPJs
                cnpjs = self.extract_cnpjs_from_sql_result(results)
                print(f"🔍 CNPJs encontrados: {len(cnpjs)}")
                
                return cnpjs, results
                
        except Exception as e:
            print(f"❌ Erro na execução SQL: {str(e)}")
            raise
    
    def enrich_company_data(self, cnpj: str) -> Dict:
        """
        Enriquece dados da empresa via API Brasil
        """
        try:
            clean_cnpj = re.sub(r'[^\d]', '', cnpj)
            url = f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'cnpj': data.get('cnpj', cnpj),
                    'razao_social': data.get('razao_social', ''),
                    'nome_fantasia': data.get('nome_fantasia', ''),
                    'situacao': data.get('descricao_situacao_cadastral', ''),
                    'atividade_principal': data.get('cnae_fiscal_descricao', ''),
                    'porte': data.get('porte', ''),
                    'capital_social': data.get('capital_social', 0),
                    'municipio': data.get('municipio', ''),
                    'uf': data.get('uf', ''),
                    'data_abertura': data.get('data_inicio_atividade', ''),
                    'telefone': data.get('ddd_telefone_1', '')
                }
            else:
                return {
                    'success': False,
                    'cnpj': cnpj,
                    'error': f'API Brasil retornou {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'cnpj': cnpj,
                'error': str(e)
            }
    
    def search_company_news(self, company_name: str, days_back: int = 30) -> List[Dict]:
        """
        Busca notícias sobre a empresa
        """
        try:
            # Usar o enhanced_news_monitor
            from enhanced_news_monitor import EnhancedNewsMonitor
            
            monitor = EnhancedNewsMonitor(self.api_base_url)
            news_data = monitor.search_google_news(company_name, days_back)
            
            # Processar notícias
            processed_news = []
            for news_item in news_data[:5]:  # Limitar a 5 notícias
                content = monitor.extract_news_content(news_item.get('link', ''))
                
                processed_news.append({
                    'title': news_item.get('title', ''),
                    'url': news_item.get('link', ''),
                    'source': news_item.get('source', ''),
                    'date': news_item.get('pubDate', ''),
                    'content': content[:500] + "..." if len(content) > 500 else content
                })
            
            return processed_news
            
        except Exception as e:
            print(f"⚠️ Erro na busca de notícias para {company_name}: {str(e)}")
            return []
    
    def analyze_company_risk(self, company_data: Dict, news_data: List[Dict]) -> Dict:
        """
        Analisa risco da empresa usando IA
        """
        try:
            # Construir texto para análise
            analysis_text = f"""
            Empresa: {company_data.get('razao_social', 'N/A')}
            CNPJ: {company_data.get('cnpj', 'N/A')}
            Situação: {company_data.get('situacao', 'N/A')}
            Atividade: {company_data.get('atividade_principal', 'N/A')}
            Porte: {company_data.get('porte', 'N/A')}
            Capital Social: R$ {company_data.get('capital_social', 0)}
            
            Notícias recentes:
            """
            
            for news in news_data[:3]:  # Incluir até 3 notícias
                analysis_text += f"\n- {news.get('title', '')}: {news.get('content', '')[:200]}..."
            
            # Chamar API de análise
            payload = {"text": analysis_text}
            
            response = requests.post(
                f"{self.api_base_url}/api/analyze-risk",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Calcular score numérico
                risk_scores = {
                    'BAIXO': 25,
                    'MÉDIO': 50,
                    'ALTO': 75,
                    'CRÍTICO': 90
                }
                
                risk_level = result.get('risk_level', 'MÉDIO')
                base_score = risk_scores.get(risk_level, 50)
                
                # Ajustar score baseado em fatores
                if company_data.get('situacao', '').upper() != 'ATIVA':
                    base_score += 20
                
                if len(news_data) > 3:
                    base_score += 10  # Muitas notícias podem indicar problemas
                
                final_score = min(base_score, 100)
                
                return {
                    'success': True,
                    'risk_level': risk_level,
                    'risk_score': final_score,
                    'confidence': result.get('confidence', 0),
                    'explanation': result.get('explanation', ''),
                    'compliance_flags': result.get('compliance_flags', []),
                    'regulatory_alerts': result.get('regulatory_alerts', []),
                    'factors': {
                        'base_risk': risk_level,
                        'situation_penalty': 20 if company_data.get('situacao', '').upper() != 'ATIVA' else 0,
                        'news_penalty': 10 if len(news_data) > 3 else 0
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'API retornou {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_single_company(self, cnpj: str, include_news: bool = True, 
                             include_enrichment: bool = True) -> CompanyBatchResult:
        """
        Processa uma única empresa
        """
        start_time = time.time()
        errors = []
        
        print(f"🔍 Processando: {cnpj}")
        
        # 1. Enriquecimento
        enrichment_data = {}
        if include_enrichment:
            enrichment_data = self.enrich_company_data(cnpj)
            if not enrichment_data.get('success', False):
                errors.append(f"Enriquecimento falhou: {enrichment_data.get('error', 'Erro desconhecido')}")
        
        razao_social = enrichment_data.get('razao_social', f'Empresa {cnpj}')
        
        # 2. Busca de notícias
        news_data = []
        if include_news and enrichment_data.get('success', False):
            news_data = self.search_company_news(razao_social)
            if not news_data:
                errors.append("Nenhuma notícia encontrada")
        
        # 3. Análise de risco
        risk_data = self.analyze_company_risk(enrichment_data, news_data)
        if not risk_data.get('success', False):
            errors.append(f"Análise de risco falhou: {risk_data.get('error', 'Erro desconhecido')}")
        
        processing_time = time.time() - start_time
        
        return CompanyBatchResult(
            cnpj=cnpj,
            razao_social=razao_social,
            enrichment_data=enrichment_data,
            news_analysis=news_data,
            risk_assessment=risk_data,
            final_risk_score=risk_data.get('risk_score', 50),
            processing_time=processing_time,
            errors=errors
        )
    
    def process_batch(self, request: BatchAnalysisRequest) -> Dict:
        """
        Processa lote de empresas
        """
        print(f"🚀 INICIANDO ANÁLISE EM LOTE")
        print(f"📊 CNPJs para processar: {len(request.cnpjs)}")
        print("=" * 60)
        
        start_time = time.time()
        results = []
        
        # Processar com concorrência limitada
        with concurrent.futures.ThreadPoolExecutor(max_workers=request.max_concurrent) as executor:
            # Submeter tarefas
            futures = {
                executor.submit(
                    self.process_single_company, 
                    cnpj, 
                    request.include_news, 
                    request.include_enrichment
                ): cnpj for cnpj in request.cnpjs
            }
            
            # Coletar resultados
            for future in concurrent.futures.as_completed(futures):
                cnpj = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Progress
                    progress = len(results) / len(request.cnpjs) * 100
                    print(f"📊 Progresso: {progress:.1f}% ({len(results)}/{len(request.cnpjs)})")
                    
                except Exception as e:
                    print(f"❌ Erro ao processar {cnpj}: {str(e)}")
                    results.append(CompanyBatchResult(
                        cnpj=cnpj,
                        razao_social=f"Erro: {cnpj}",
                        enrichment_data={},
                        news_analysis=[],
                        risk_assessment={},
                        final_risk_score=0,
                        processing_time=0,
                        errors=[str(e)]
                    ))
        
        total_time = time.time() - start_time
        
        # Gerar estatísticas
        successful_results = [r for r in results if not r.errors]
        risk_scores = [r.final_risk_score for r in successful_results]
        
        stats = {
            'total_processed': len(results),
            'successful': len(successful_results),
            'failed': len(results) - len(successful_results),
            'total_time': total_time,
            'avg_time_per_company': total_time / len(results) if results else 0,
            'avg_risk_score': sum(risk_scores) / len(risk_scores) if risk_scores else 0,
            'high_risk_companies': len([r for r in successful_results if r.final_risk_score >= 70]),
            'risk_distribution': {
                'baixo': len([r for r in successful_results if r.final_risk_score < 40]),
                'medio': len([r for r in successful_results if 40 <= r.final_risk_score < 70]),
                'alto': len([r for r in successful_results if r.final_risk_score >= 70])
            }
        }
        
        # Compilar resultado final
        batch_result = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_cnpjs': len(request.cnpjs),
                'processing_time': total_time,
                'include_news': request.include_news,
                'include_enrichment': request.include_enrichment
            },
            'statistics': stats,
            'companies': [asdict(result) for result in results],
            'summary': {
                'companies_analyzed': len(results),
                'avg_risk_score': stats['avg_risk_score'],
                'high_risk_count': stats['high_risk_companies'],
                'processing_efficiency': f"{len(results) / (total_time / 60):.1f} empresas/min"
            }
        }
        
        return batch_result
    
    def save_results(self, results: Dict, filename: str = None, format: str = "json") -> str:
        """
        Salva resultados em arquivo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_analysis_{timestamp}"
        
        if format == "json":
            filepath = f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            filepath = f"{filename}.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._generate_markdown_report(results))
        
        print(f"💾 Resultados salvos em: {filepath}")
        return filepath
    
    def _generate_markdown_report(self, results: Dict) -> str:
        """
        Gera relatório em markdown
        """
        metadata = results['metadata']
        stats = results['statistics']
        companies = results['companies']
        
        report = f"""# 📊 Relatório de Análise em Lote - DD-AI v2.1

**Data da Análise:** {datetime.fromisoformat(metadata['analysis_date']).strftime('%d/%m/%Y %H:%M')}
**Total de CNPJs:** {metadata['total_cnpjs']}
**Tempo de Processamento:** {metadata['processing_time']:.1f}s

## 📈 Estatísticas Gerais

- **Empresas Processadas:** {stats['total_processed']}
- **Sucessos:** {stats['successful']}
- **Falhas:** {stats['failed']}
- **Score Médio de Risco:** {stats['avg_risk_score']:.1f}/100
- **Empresas de Alto Risco:** {stats['high_risk_companies']}

### 🎯 Distribuição de Risco

- **Baixo Risco (< 40):** {stats['risk_distribution']['baixo']} empresas
- **Médio Risco (40-69):** {stats['risk_distribution']['medio']} empresas  
- **Alto Risco (≥ 70):** {stats['risk_distribution']['alto']} empresas

---

## 🏢 Detalhes por Empresa

"""
        
        for i, company in enumerate(companies, 1):
            risk_emoji = "🟢" if company['final_risk_score'] < 40 else "🟡" if company['final_risk_score'] < 70 else "🔴"
            
            report += f"""### {i}. {company['razao_social']} {risk_emoji}

- **CNPJ:** {company['cnpj']}
- **Score de Risco:** {company['final_risk_score']:.1f}/100
- **Tempo de Processamento:** {company['processing_time']:.1f}s
- **Notícias Encontradas:** {len(company['news_analysis'])}

"""
            
            if company['errors']:
                report += f"- **⚠️ Erros:** {', '.join(company['errors'])}\n"
            
            if company['enrichment_data'].get('success'):
                enrich = company['enrichment_data']
                report += f"""
**Dados da Empresa:**
- Situação: {enrich.get('situacao', 'N/A')}
- Atividade: {enrich.get('atividade_principal', 'N/A')}
- Porte: {enrich.get('porte', 'N/A')}
- Capital Social: R$ {enrich.get('capital_social', 0)}
"""
            
            if company['risk_assessment'].get('success'):
                risk = company['risk_assessment']
                report += f"""
**Análise de Risco:**
- Nível: {risk.get('risk_level', 'N/A')}
- Confiança: {risk.get('confidence', 0):.1f}%
- Explicação: {risk.get('explanation', 'N/A')[:200]}...
"""
            
            report += "\n---\n\n"
        
        return report

def main():
    """Função principal para demonstração"""
    print("🚀 BATCH ANALYZER - Advanced DD-AI v2.1")
    print("=" * 50)
    
    # Exemplo de uso
    analyzer = BatchAnalyzer()
    
    # CNPJs de exemplo (dos seus resultados SQL)
    test_cnpjs = [
        "05.285.819/0001-66",
        "05.753.599/0001-58", 
        "05.754.060/0001-13"
    ]
    
    # Criar requisição
    request = BatchAnalysisRequest(
        cnpjs=test_cnpjs,
        include_news=True,
        include_enrichment=True,
        max_concurrent=3,
        output_format="json"
    )
    
    # Processar
    try:
        results = analyzer.process_batch(request)
        
        # Salvar resultados
        json_file = analyzer.save_results(results, format="json")
        md_file = analyzer.save_results(results, format="markdown")
        
        print(f"\n🎉 ANÁLISE CONCLUÍDA!")
        print(f"📊 {results['summary']['companies_analyzed']} empresas analisadas")
        print(f"📈 Score médio: {results['summary']['avg_risk_score']:.1f}/100")
        print(f"⚠️ Alto risco: {results['summary']['high_risk_count']} empresas")
        print(f"⚡ Eficiência: {results['summary']['processing_efficiency']}")
        print(f"💾 Relatórios: {json_file}, {md_file}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
