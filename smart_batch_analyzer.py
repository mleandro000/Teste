#!/usr/bin/env python3
"""
🧠 SMART BATCH ANALYZER - Advanced DD-AI v2.1
==============================================

Sistema inteligente que detecta automaticamente o tipo de dados
e escolhe a estratégia de análise adequada:

1. 📊 CNPJ → Enriquecimento + Busca por Razão Social
2. 🏢 Razão Social → Busca direta nos motores
3. 🔄 Misto → Detecta e processa adequadamente

Estratégias:
- AUTO_DETECT: Detecta automaticamente o tipo
- CNPJ_ONLY: Força enriquecimento via CNPJ
- COMPANY_NAME_ONLY: Usa apenas nomes de empresas
- HYBRID: Usa ambos quando disponível
"""

import requests
import json
import re
import time
import pyodbc
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures

class AnalysisStrategy(Enum):
    AUTO_DETECT = "auto_detect"
    CNPJ_ONLY = "cnpj_only"
    COMPANY_NAME_ONLY = "company_name_only"
    HYBRID = "hybrid"

class DataType(Enum):
    CNPJ = "cnpj"
    COMPANY_NAME = "company_name"
    MIXED = "mixed"
    UNKNOWN = "unknown"

@dataclass
class DataItem:
    """Item de dados para análise"""
    original_value: str
    data_type: DataType
    cnpj: Optional[str] = None
    company_name: Optional[str] = None
    confidence: float = 0.0
    source_column: Optional[str] = None

@dataclass
class SmartBatchRequest:
    """Requisição inteligente de análise em lote"""
    data_items: List[Union[str, Dict[str, str]]]  # Lista de CNPJs, nomes ou dict com colunas
    analysis_strategy: AnalysisStrategy = AnalysisStrategy.AUTO_DETECT
    include_news: bool = True
    include_enrichment: bool = True
    max_concurrent: int = 5
    sql_query: Optional[str] = None
    connection_details: Optional[Dict] = None
    column_mapping: Optional[Dict[str, str]] = None  # {"cnpj_col": "ID_UNICO", "name_col": "RAZAO_SOCIAL"}

@dataclass
class SmartAnalysisResult:
    """Resultado da análise inteligente"""
    original_data: DataItem
    enrichment_data: Dict
    company_name_used: str
    news_analysis: List[Dict]
    risk_assessment: Dict
    final_risk_score: float
    processing_time: float
    strategy_used: str
    errors: List[str]

class SmartBatchAnalyzer:
    def __init__(self, api_base_url: str = "http://127.0.0.1:8001"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DD-AI-SmartAnalyzer/2.1'
        })
        
        # Padrões para detecção
        self.cnpj_pattern = re.compile(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}')
        self.company_indicators = [
            'ltda', 'sa', 's.a.', 'ltd', 'eireli', 'mei', 'epp', 'me',
            'sociedade', 'empresa', 'companhia', 'corp', 'fundo',
            'gestora', 'asset', 'investimentos', 'participações'
        ]
    
    def detect_data_type(self, value: str) -> Tuple[DataType, float]:
        """
        Detecta automaticamente o tipo de dados
        """
        if not isinstance(value, str):
            return DataType.UNKNOWN, 0.0
        
        value_clean = value.strip().lower()
        
        # Verificar CNPJ
        cnpj_matches = self.cnpj_pattern.findall(value)
        if cnpj_matches:
            # Validar se é um CNPJ válido (14 dígitos)
            clean_cnpj = re.sub(r'[^\d]', '', cnpj_matches[0])
            if len(clean_cnpj) == 14:
                return DataType.CNPJ, 0.95
        
        # Verificar indicadores de nome de empresa
        company_score = 0
        for indicator in self.company_indicators:
            if indicator in value_clean:
                company_score += 0.2
        
        # Verificar características de nome empresarial
        if len(value_clean) > 10:  # Nomes empresariais são geralmente longos
            company_score += 0.1
        
        if any(char.isupper() for char in value):  # Nomes empresariais têm maiúsculas
            company_score += 0.1
        
        if company_score >= 0.3:
            return DataType.COMPANY_NAME, min(company_score, 0.9)
        
        return DataType.UNKNOWN, 0.1
    
    def parse_data_items(self, data_items: List[Union[str, Dict]], 
                        column_mapping: Optional[Dict] = None) -> List[DataItem]:
        """
        Converte dados de entrada em DataItems estruturados
        """
        parsed_items = []
        
        for item in data_items:
            if isinstance(item, str):
                # String simples - detectar tipo automaticamente
                data_type, confidence = self.detect_data_type(item)
                
                parsed_item = DataItem(
                    original_value=item,
                    data_type=data_type,
                    confidence=confidence
                )
                
                if data_type == DataType.CNPJ:
                    parsed_item.cnpj = item
                elif data_type == DataType.COMPANY_NAME:
                    parsed_item.company_name = item
                
                parsed_items.append(parsed_item)
                
            elif isinstance(item, dict):
                # Dicionário com colunas - usar mapeamento
                cnpj_col = column_mapping.get('cnpj_col') if column_mapping else 'cnpj'
                name_col = column_mapping.get('name_col') if column_mapping else 'razao_social'
                
                cnpj_value = item.get(cnpj_col, '')
                name_value = item.get(name_col, '')
                
                # Determinar dados disponíveis
                has_cnpj = bool(cnpj_value and self.cnpj_pattern.match(str(cnpj_value)))
                has_name = bool(name_value and len(str(name_value).strip()) > 3)
                
                if has_cnpj and has_name:
                    data_type = DataType.MIXED
                    confidence = 0.95
                elif has_cnpj:
                    data_type = DataType.CNPJ
                    confidence = 0.9
                elif has_name:
                    data_type = DataType.COMPANY_NAME
                    confidence = 0.8
                else:
                    data_type = DataType.UNKNOWN
                    confidence = 0.1
                
                parsed_item = DataItem(
                    original_value=str(item),
                    data_type=data_type,
                    cnpj=cnpj_value if has_cnpj else None,
                    company_name=name_value if has_name else None,
                    confidence=confidence,
                    source_column=f"{cnpj_col}+{name_col}" if has_cnpj and has_name else (cnpj_col if has_cnpj else name_col)
                )
                
                parsed_items.append(parsed_item)
        
        return parsed_items
    
    def choose_analysis_strategy(self, data_items: List[DataItem], 
                               requested_strategy: AnalysisStrategy) -> Dict[str, List[DataItem]]:
        """
        Escolhe a estratégia de análise baseada nos dados e preferência
        """
        if requested_strategy == AnalysisStrategy.AUTO_DETECT:
            # Analisar distribuição dos tipos de dados
            cnpj_count = len([item for item in data_items if item.data_type in [DataType.CNPJ, DataType.MIXED]])
            name_count = len([item for item in data_items if item.data_type in [DataType.COMPANY_NAME, DataType.MIXED]])
            
            if cnpj_count > name_count * 1.5:
                strategy = AnalysisStrategy.CNPJ_ONLY
            elif name_count > cnpj_count * 1.5:
                strategy = AnalysisStrategy.COMPANY_NAME_ONLY
            else:
                strategy = AnalysisStrategy.HYBRID
        else:
            strategy = requested_strategy
        
        # Organizar items por estratégia
        strategy_groups = {
            'cnpj_enrichment': [],
            'direct_name_search': [],
            'hybrid_analysis': [],
            'unknown_items': []
        }
        
        for item in data_items:
            if strategy == AnalysisStrategy.CNPJ_ONLY:
                if item.cnpj:
                    strategy_groups['cnpj_enrichment'].append(item)
                else:
                    strategy_groups['unknown_items'].append(item)
                    
            elif strategy == AnalysisStrategy.COMPANY_NAME_ONLY:
                if item.company_name:
                    strategy_groups['direct_name_search'].append(item)
                else:
                    strategy_groups['unknown_items'].append(item)
                    
            elif strategy == AnalysisStrategy.HYBRID:
                if item.data_type == DataType.MIXED:
                    strategy_groups['hybrid_analysis'].append(item)
                elif item.cnpj:
                    strategy_groups['cnpj_enrichment'].append(item)
                elif item.company_name:
                    strategy_groups['direct_name_search'].append(item)
                else:
                    strategy_groups['unknown_items'].append(item)
        
        return strategy_groups
    
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
                    'source': 'api_brasil',
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
                    'source': 'api_brasil',
                    'cnpj': cnpj,
                    'error': f'API Brasil retornou {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'source': 'api_brasil',
                'cnpj': cnpj,
                'error': str(e)
            }
    
    def search_company_news(self, company_name: str, days_back: int = 30) -> List[Dict]:
        """
        Busca notícias sobre a empresa usando nome
        """
        try:
            from enhanced_news_monitor import EnhancedNewsMonitor
            
            monitor = EnhancedNewsMonitor(self.api_base_url)
            news_data = monitor.search_google_news(company_name, days_back)
            
            processed_news = []
            for news_item in news_data[:5]:
                content = monitor.extract_news_content(news_item.get('link', ''))
                
                processed_news.append({
                    'title': news_item.get('title', ''),
                    'url': news_item.get('link', ''),
                    'source': news_item.get('source', ''),
                    'date': news_item.get('pubDate', ''),
                    'content': content[:500] + "..." if len(content) > 500 else content,
                    'relevance': self._calculate_relevance(news_item.get('title', ''), company_name)
                })
            
            # Ordenar por relevância
            processed_news.sort(key=lambda x: x['relevance'], reverse=True)
            
            return processed_news
            
        except Exception as e:
            print(f"⚠️ Erro na busca de notícias para {company_name}: {str(e)}")
            return []
    
    def _calculate_relevance(self, title: str, company_name: str) -> float:
        """Calcula relevância da notícia"""
        if not title or not company_name:
            return 0.0
        
        title_lower = title.lower()
        company_lower = company_name.lower()
        
        # Score base por menção direta
        if company_lower in title_lower:
            relevance = 1.0
        else:
            # Score por palavras-chave
            company_words = [w for w in company_lower.split() if len(w) > 3]
            matches = sum(1 for word in company_words if word in title_lower)
            relevance = matches / len(company_words) if company_words else 0.0
        
        # Bônus para termos financeiros
        financial_terms = ['fundo', 'gestora', 'investimento', 'risco', 'compliance', 'cvm', 'bacen']
        financial_bonus = sum(0.1 for term in financial_terms if term in title_lower)
        
        return min(relevance + financial_bonus, 1.0)
    
    def analyze_company_risk(self, company_data: Dict, news_data: List[Dict], 
                           strategy_used: str) -> Dict:
        """
        Analisa risco da empresa usando IA
        """
        try:
            # Construir texto para análise baseado na estratégia
            if strategy_used == 'cnpj_enrichment':
                analysis_text = f"""
                Análise via CNPJ - Dados enriquecidos:
                Empresa: {company_data.get('razao_social', 'N/A')}
                CNPJ: {company_data.get('cnpj', 'N/A')}
                Situação: {company_data.get('situacao', 'N/A')}
                Atividade: {company_data.get('atividade_principal', 'N/A')}
                Porte: {company_data.get('porte', 'N/A')}
                Capital Social: R$ {company_data.get('capital_social', 0)}
                Localização: {company_data.get('municipio', '')}/{company_data.get('uf', '')}
                """
            else:
                analysis_text = f"""
                Análise via nome da empresa:
                Empresa: {company_data.get('razao_social', company_data.get('company_name', 'N/A'))}
                Método: Busca direta por notícias e informações públicas
                """
            
            # Adicionar notícias relevantes
            if news_data:
                analysis_text += "\n\nNotícias recentes encontradas:\n"
                for news in news_data[:3]:
                    if news.get('relevance', 0) > 0.3:
                        analysis_text += f"\n- {news.get('title', '')}: {news.get('content', '')[:200]}..."
            else:
                analysis_text += "\n\nNenhuma notícia relevante encontrada no período analisado."
            
            # Chamar API de análise
            payload = {"text": analysis_text}
            
            response = requests.post(
                f"{self.api_base_url}/api/analyze-risk",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Calcular score ajustado por estratégia
                risk_scores = {'BAIXO': 25, 'MÉDIO': 50, 'ALTO': 75, 'CRÍTICO': 90}
                risk_level = result.get('risk_level', 'MÉDIO')
                base_score = risk_scores.get(risk_level, 50)
                
                # Ajustes baseados na estratégia e dados
                if strategy_used == 'cnpj_enrichment':
                    # Dados mais confiáveis do governo
                    if company_data.get('situacao', '').upper() != 'ATIVA':
                        base_score += 20
                    if company_data.get('capital_social', 0) == 0:
                        base_score += 10
                
                elif strategy_used == 'direct_name_search':
                    # Baseado apenas em notícias - menos certeza
                    confidence_penalty = 10
                    base_score += confidence_penalty
                
                # Ajuste por qualidade das notícias
                high_relevance_news = len([n for n in news_data if n.get('relevance', 0) > 0.7])
                if high_relevance_news > 2:
                    base_score += 5  # Muita exposição na mídia pode indicar problemas
                
                final_score = min(base_score, 100)
                
                return {
                    'success': True,
                    'risk_level': risk_level,
                    'risk_score': final_score,
                    'confidence': result.get('confidence', 0),
                    'explanation': result.get('explanation', ''),
                    'compliance_flags': result.get('compliance_flags', []),
                    'regulatory_alerts': result.get('regulatory_alerts', []),
                    'strategy_adjustments': {
                        'strategy_used': strategy_used,
                        'base_score': risk_scores.get(risk_level, 50),
                        'final_score': final_score,
                        'news_quality': high_relevance_news
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
    
    def process_single_item(self, data_item: DataItem, strategy: str) -> SmartAnalysisResult:
        """
        Processa um único item de dados
        """
        start_time = time.time()
        errors = []
        
        print(f"🔍 Processando: {data_item.original_value[:50]}... (Estratégia: {strategy})")
        
        # Inicializar dados
        enrichment_data = {}
        company_name_used = ""
        
        # Executar estratégia apropriada
        if strategy == 'cnpj_enrichment':
            # Enriquecer via CNPJ
            enrichment_data = self.enrich_company_data(data_item.cnpj)
            if enrichment_data.get('success'):
                company_name_used = enrichment_data.get('razao_social', '')
            else:
                errors.append(f"Enriquecimento CNPJ falhou: {enrichment_data.get('error', '')}")
                company_name_used = f"Empresa {data_item.cnpj}"
        
        elif strategy == 'direct_name_search':
            # Usar nome diretamente
            company_name_used = data_item.company_name
            enrichment_data = {
                'success': True,
                'source': 'direct_input',
                'razao_social': company_name_used,
                'method': 'direct_name_search'
            }
        
        elif strategy == 'hybrid_analysis':
            # Enriquecer CNPJ + validar com nome
            enrichment_data = self.enrich_company_data(data_item.cnpj)
            if enrichment_data.get('success'):
                company_name_used = enrichment_data.get('razao_social', '')
                # Verificar se nome bate (opcional)
                if data_item.company_name and data_item.company_name.lower() not in company_name_used.lower():
                    errors.append("Nome informado difere do encontrado via CNPJ")
            else:
                # Fallback para nome informado
                company_name_used = data_item.company_name
                enrichment_data = {
                    'success': True,
                    'source': 'fallback_to_name',
                    'razao_social': company_name_used,
                    'cnpj_error': enrichment_data.get('error', '')
                }
        
        # Buscar notícias
        news_data = []
        if company_name_used:
            news_data = self.search_company_news(company_name_used)
            if not news_data:
                errors.append("Nenhuma notícia encontrada")
        
        # Análise de risco
        risk_data = self.analyze_company_risk(enrichment_data, news_data, strategy)
        if not risk_data.get('success'):
            errors.append(f"Análise de risco falhou: {risk_data.get('error', '')}")
        
        processing_time = time.time() - start_time
        
        return SmartAnalysisResult(
            original_data=data_item,
            enrichment_data=enrichment_data,
            company_name_used=company_name_used,
            news_analysis=news_data,
            risk_assessment=risk_data,
            final_risk_score=risk_data.get('risk_score', 50),
            processing_time=processing_time,
            strategy_used=strategy,
            errors=errors
        )
    
    def process_smart_batch(self, request: SmartBatchRequest) -> Dict:
        """
        Processa lote inteligente de dados
        """
        print(f"🧠 INICIANDO ANÁLISE INTELIGENTE EM LOTE")
        print(f"📊 Items para processar: {len(request.data_items)}")
        print(f"🎯 Estratégia solicitada: {request.analysis_strategy.value}")
        print("=" * 60)
        
        start_time = time.time()
        
        # 1. Parsear e detectar tipos de dados
        parsed_items = self.parse_data_items(request.data_items, request.column_mapping)
        
        # 2. Escolher estratégia de análise
        strategy_groups = self.choose_analysis_strategy(parsed_items, request.analysis_strategy)
        
        print(f"📋 Distribuição por estratégia:")
        for strategy, items in strategy_groups.items():
            if items:
                print(f"   {strategy}: {len(items)} items")
        
        # 3. Processar cada grupo
        all_results = []
        
        # Processar enriquecimento via CNPJ
        if strategy_groups['cnpj_enrichment']:
            print(f"\n🔍 Processando {len(strategy_groups['cnpj_enrichment'])} CNPJs...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=request.max_concurrent) as executor:
                futures = {
                    executor.submit(self.process_single_item, item, 'cnpj_enrichment'): item 
                    for item in strategy_groups['cnpj_enrichment']
                }
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    all_results.append(result)
        
        # Processar busca direta por nome
        if strategy_groups['direct_name_search']:
            print(f"\n🏢 Processando {len(strategy_groups['direct_name_search'])} nomes de empresas...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=request.max_concurrent) as executor:
                futures = {
                    executor.submit(self.process_single_item, item, 'direct_name_search'): item 
                    for item in strategy_groups['direct_name_search']
                }
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    all_results.append(result)
        
        # Processar análise híbrida
        if strategy_groups['hybrid_analysis']:
            print(f"\n🔄 Processando {len(strategy_groups['hybrid_analysis'])} items híbridos...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=request.max_concurrent) as executor:
                futures = {
                    executor.submit(self.process_single_item, item, 'hybrid_analysis'): item 
                    for item in strategy_groups['hybrid_analysis']
                }
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    all_results.append(result)
        
        total_time = time.time() - start_time
        
        # 4. Gerar estatísticas
        successful_results = [r for r in all_results if not r.errors]
        risk_scores = [r.final_risk_score for r in successful_results]
        
        strategy_stats = {}
        for result in all_results:
            strategy = result.strategy_used
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {'count': 0, 'avg_score': 0, 'success_rate': 0}
            strategy_stats[strategy]['count'] += 1
        
        for strategy in strategy_stats:
            strategy_results = [r for r in all_results if r.strategy_used == strategy]
            successful_strategy = [r for r in strategy_results if not r.errors]
            if strategy_results:
                strategy_stats[strategy]['success_rate'] = len(successful_strategy) / len(strategy_results) * 100
                if successful_strategy:
                    strategy_stats[strategy]['avg_score'] = sum(r.final_risk_score for r in successful_strategy) / len(successful_strategy)
        
        # 5. Compilar resultado final
        result = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_items': len(request.data_items),
                'processing_time': total_time,
                'strategy_requested': request.analysis_strategy.value,
                'include_news': request.include_news,
                'include_enrichment': request.include_enrichment
            },
            'strategy_distribution': {
                strategy: len(items) for strategy, items in strategy_groups.items() if items
            },
            'strategy_performance': strategy_stats,
            'statistics': {
                'total_processed': len(all_results),
                'successful': len(successful_results),
                'failed': len(all_results) - len(successful_results),
                'avg_risk_score': sum(risk_scores) / len(risk_scores) if risk_scores else 0,
                'high_risk_companies': len([r for r in successful_results if r.final_risk_score >= 70]),
                'avg_processing_time': total_time / len(all_results) if all_results else 0
            },
            'results': [asdict(result) for result in all_results],
            'summary': {
                'companies_analyzed': len(all_results),
                'avg_risk_score': sum(risk_scores) / len(risk_scores) if risk_scores else 0,
                'most_used_strategy': max(strategy_stats.keys(), key=lambda k: strategy_stats[k]['count']) if strategy_stats else 'none',
                'processing_efficiency': f"{len(all_results) / (total_time / 60):.1f} items/min"
            }
        }
        
        return result

def main():
    """Demonstração do analisador inteligente"""
    print("🧠 SMART BATCH ANALYZER - Advanced DD-AI v2.1")
    print("=" * 50)
    
    analyzer = SmartBatchAnalyzer()
    
    # Dados de teste mistos
    test_data = [
        "05.285.819/0001-66",  # CNPJ
        "XP Asset Management",  # Nome da empresa
        "Itaú Asset Management",  # Nome da empresa
        {"cnpj": "05.753.599/0001-58", "razao_social": "GP AETATIS II FUNDO"},  # Dados mistos
        "CATERPILLAR FUNDO DE INVESTIMENTO"  # Nome da empresa
    ]
    
    # Criar requisição
    request = SmartBatchRequest(
        data_items=test_data,
        analysis_strategy=AnalysisStrategy.AUTO_DETECT,
        include_news=True,
        include_enrichment=True,
        max_concurrent=3
    )
    
    # Processar
    try:
        results = analyzer.process_smart_batch(request)
        
        print(f"\n🎉 ANÁLISE INTELIGENTE CONCLUÍDA!")
        print(f"📊 {results['summary']['companies_analyzed']} items analisados")
        print(f"📈 Score médio: {results['summary']['avg_risk_score']:.1f}/100")
        print(f"🎯 Estratégia mais usada: {results['summary']['most_used_strategy']}")
        print(f"⚡ Eficiência: {results['summary']['processing_efficiency']}")
        
        # Salvar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"smart_analysis_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados salvos em: {filename}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
