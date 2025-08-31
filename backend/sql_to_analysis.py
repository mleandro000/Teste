#!/usr/bin/env python3
"""
🚀 SQL TO ANALYSIS - Fluxo Automático Completo
==============================================

Automatiza o fluxo completo:
1. Query SQL → CNPJs
2. Enriquecimento via API Brasil
3. Busca de notícias
4. Análise de risco com IA
5. Relatório consolidado
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any

class SQLToAnalysis:
    def __init__(self, api_url: str = "http://127.0.0.1:8001"):
        self.api_url = api_url
        
    def execute_sql_query(self, connection_details: Dict, query: str) -> List[str]:
        """
        Executa query SQL e retorna lista de CNPJs
        """
        print(f"🔍 Executando query SQL...")
        print(f"📊 Query: {query}")
        
        payload = {
            "connection": connection_details,
            "query": query
        }
        
        try:
            response = requests.post(f"{self.api_url}/api/execute-query", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    data = result.get('data', [])
                    cnpjs = []
                    
                    # Extrair CNPJs dos resultados
                    for row in data:
                        if isinstance(row, dict):
                            # Procurar por colunas que podem conter CNPJs
                            for key, value in row.items():
                                if isinstance(value, str) and self._is_cnpj(value):
                                    cnpjs.append(value)
                        elif isinstance(row, list) and len(row) > 0:
                            # Se for lista, pegar o primeiro valor
                            value = row[0]
                            if isinstance(value, str) and self._is_cnpj(value):
                                cnpjs.append(value)
                    
                    print(f"✅ Query executada com sucesso!")
                    print(f"📊 CNPJs encontrados: {len(cnpjs)}")
                    return cnpjs
                else:
                    print(f"❌ Erro na query: {result.get('error', 'Erro desconhecido')}")
                    return []
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erro de conexão: {str(e)}")
            return []
    
    def _is_cnpj(self, value: str) -> bool:
        """Verifica se uma string é um CNPJ válido"""
        import re
        cnpj_pattern = re.compile(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}')
        return bool(cnpj_pattern.match(value))
    
    def enrich_cnpjs(self, cnpjs: List[str]) -> List[Dict]:
        """
        Enriquece CNPJs via API Brasil
        """
        print(f"\n🌐 Enriquecendo {len(cnpjs)} CNPJs via API Brasil...")
        
        enriched_data = []
        
        for i, cnpj in enumerate(cnpjs, 1):
            print(f"   📊 {i}/{len(cnpjs)}: {cnpj}")
            
            try:
                # Limpar CNPJ (remover pontos e traços)
                clean_cnpj = ''.join(filter(str.isdigit, cnpj))
                url = f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}"
                
                response = requests.get(url, timeout=10)
                
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
                        'data_abertura': data.get('data_inicio_atividade', ''),
                        'enrichment_success': True
                    })
                    print(f"      ✅ {data.get('razao_social', 'N/A')}")
                else:
                    enriched_data.append({
                        'cnpj': cnpj,
                        'razao_social': f'CNPJ {cnpj}',
                        'enrichment_success': False,
                        'error': f'API retornou {response.status_code}'
                    })
                    print(f"      ❌ Erro: {response.status_code}")
                    
            except Exception as e:
                enriched_data.append({
                    'cnpj': cnpj,
                    'razao_social': f'CNPJ {cnpj}',
                    'enrichment_success': False,
                    'error': str(e)
                })
                print(f"      ❌ Erro: {str(e)}")
            
            # Pausa para não sobrecarregar a API
            time.sleep(0.5)
        
        return enriched_data
    
    def search_news(self, company_name: str) -> List[Dict]:
        """
        Busca notícias sobre a empresa (simulado por enquanto)
        """
        # Simulação de busca de notícias
        # Em produção, integrar com APIs reais (Google News, etc.)
        
        news_data = [
            {
                'title': f'Notícia sobre {company_name}',
                'url': 'https://exemplo.com/noticia1',
                'content': f'Análise de mercado para {company_name}...',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'relevance': 0.8
            },
            {
                'title': f'Relatório financeiro {company_name}',
                'url': 'https://exemplo.com/noticia2', 
                'content': f'Dados financeiros recentes de {company_name}...',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'relevance': 0.9
            }
        ]
        
        return news_data
    
    def analyze_risk(self, company_data: Dict, news_data: List[Dict]) -> Dict:
        """
        Analisa risco da empresa usando IA
        """
        print(f"🧠 Analisando risco para: {company_data.get('razao_social', 'N/A')}")
        
        # Construir texto para análise
        analysis_text = f"""
        Análise de risco para empresa:
        
        Dados da empresa:
        - Razão Social: {company_data.get('razao_social', 'N/A')}
        - CNPJ: {company_data.get('cnpj', 'N/A')}
        - Situação: {company_data.get('situacao', 'N/A')}
        - Atividade: {company_data.get('atividade_principal', 'N/A')}
        - Porte: {company_data.get('porte', 'N/A')}
        - Capital Social: R$ {company_data.get('capital_social', 0)}
        - Localização: {company_data.get('municipio', '')}/{company_data.get('uf', '')}
        
        Notícias recentes:
        """
        
        for news in news_data:
            analysis_text += f"\n- {news.get('title', '')}: {news.get('content', '')[:200]}..."
        
        # Chamar API de análise
        payload = {"text": analysis_text}
        
        try:
            response = requests.post(f"{self.api_url}/api/analyze-risk", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'risk_level': result.get('risk_level', 'MÉDIO'),
                    'confidence': result.get('confidence', 0),
                    'explanation': result.get('explanation', ''),
                    'compliance_flags': result.get('compliance_flags', []),
                    'regulatory_alerts': result.get('regulatory_alerts', [])
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
    
    def process_complete_flow(self, connection_details: Dict, query: str) -> Dict:
        """
        Executa o fluxo completo: SQL → Enriquecimento → Notícias → Análise
        """
        print("🚀 INICIANDO FLUXO COMPLETO DE ANÁLISE")
        print("=" * 60)
        
        start_time = time.time()
        
        # 1. Executar query SQL
        cnpjs = self.execute_sql_query(connection_details, query)
        
        if not cnpjs:
            return {
                'success': False,
                'error': 'Nenhum CNPJ encontrado na query'
            }
        
        # 2. Enriquecer dados
        enriched_data = self.enrich_cnpjs(cnpjs)
        
        # 3. Buscar notícias e analisar risco
        results = []
        
        for company_data in enriched_data:
            print(f"\n📊 Processando: {company_data.get('razao_social', 'N/A')}")
            
            # Buscar notícias
            news_data = self.search_news(company_data.get('razao_social', ''))
            
            # Analisar risco
            risk_analysis = self.analyze_risk(company_data, news_data)
            
            # Compilar resultado
            result = {
                'company_data': company_data,
                'news_data': news_data,
                'risk_analysis': risk_analysis,
                'processing_time': time.time() - start_time
            }
            
            results.append(result)
            
            print(f"   ✅ Risco: {risk_analysis.get('risk_level', 'N/A')}")
        
        # 4. Gerar relatório consolidado
        total_time = time.time() - start_time
        
        # Estatísticas
        successful_enrichments = len([r for r in enriched_data if r.get('enrichment_success')])
        successful_analyses = len([r for r in results if r['risk_analysis'].get('success')])
        
        risk_levels = [r['risk_analysis'].get('risk_level', 'MÉDIO') for r in results if r['risk_analysis'].get('success')]
        risk_counts = {}
        for level in risk_levels:
            risk_counts[level] = risk_counts.get(level, 0) + 1
        
        consolidated_report = {
            'success': True,
            'metadata': {
                'query_executed': query,
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
                'avg_processing_time': f"{total_time/len(cnpjs):.2f}s por empresa"
            }
        }
        
        return consolidated_report

def main():
    """Função principal para teste"""
    print("🚀 SQL TO ANALYSIS - Teste do Fluxo Completo")
    print("=" * 50)
    
    # Configuração de conexão (usar os dados do seu SQL Server)
    connection_details = {
        "server": "DESKTOP-T9HKFSQ\\SQLEXPRESS",
        "database": "Projeto_Dev", 
        "port": 1433
    }
    
    # Query que você executou
    query = "SELECT TOP 10 ID_UNICO FROM dbo.FIDC_BALANCO_MENSAL"
    
    # Criar instância e executar fluxo
    analyzer = SQLToAnalysis()
    
    try:
        results = analyzer.process_complete_flow(connection_details, query)
        
        if results['success']:
            print(f"\n🎉 FLUXO COMPLETO EXECUTADO COM SUCESSO!")
            print(f"📊 Empresas analisadas: {results['summary']['companies_analyzed']}")
            print(f"📈 Taxa de enriquecimento: {results['summary']['enrichment_success_rate']}")
            print(f"🧠 Taxa de análise: {results['summary']['analysis_success_rate']}")
            print(f"⏱️ Tempo médio: {results['summary']['avg_processing_time']}")
            
            print(f"\n📋 DISTRIBUIÇÃO DE RISCO:")
            for risk_level, count in results['risk_distribution'].items():
                print(f"   {risk_level}: {count} empresas")
            
            # Salvar relatório
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analise_completa_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Relatório salvo em: {filename}")
            
        else:
            print(f"❌ Erro no fluxo: {results.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
