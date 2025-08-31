#!/usr/bin/env python3
"""
🔍 ENHANCED NEWS RISK MONITOR - Advanced DD-AI v2.1
===================================================

Sistema avançado de monitoramento de risco baseado em notícias reais.

Integração com:
- 📊 API Brasil (enriquecimento CNPJ)
- 📰 Google News API/RSS
- 🧠 Advanced DD-AI v2.1
- 📋 Relatórios automatizados

Fluxo completo:
CNPJ/Razão Social → Enriquecimento → Busca Notícias → Análise IA → Relatório
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass, asdict
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CompanyInfo:
    cnpj: str
    razao_social: str
    nome_fantasia: str
    situacao: str
    atividade_principal: str
    porte: str
    capital_social: float
    municipio: str = ""
    uf: str = ""

@dataclass
class NewsItem:
    titulo: str
    url: str
    fonte: str
    data: str
    conteudo: str
    relevancia_score: float
    sentimento: str = "NEUTRO"

@dataclass
class RiskAnalysis:
    risk_level: str
    confidence: float
    explanation: str
    compliance_flags: List[str]
    regulatory_alerts: List[str]
    entities_found: List[str] = None

class EnhancedNewsMonitor:
    def __init__(self, api_base_url: str = "http://127.0.0.1:8001"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def enrich_company_by_cnpj(self, cnpj: str) -> Optional[CompanyInfo]:
        """Enriquece dados da empresa via API Brasil"""
        try:
            logger.info(f"Enriquecendo CNPJ: {cnpj}")
            
            cnpj_clean = re.sub(r'[^\d]', '', cnpj)
            url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return CompanyInfo(
                    cnpj=data.get('cnpj', cnpj),
                    razao_social=data.get('razao_social', ''),
                    nome_fantasia=data.get('nome_fantasia', ''),
                    situacao=data.get('descricao_situacao_cadastral', ''),
                    atividade_principal=data.get('cnae_fiscal_descricao', ''),
                    porte=data.get('porte', ''),
                    capital_social=float(data.get('capital_social', 0)),
                    municipio=data.get('municipio', ''),
                    uf=data.get('uf', '')
                )
            else:
                logger.error(f"Erro na API Brasil: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao enriquecer CNPJ: {str(e)}")
            return None

    def search_google_news(self, query: str, days_back: int = 30) -> List[Dict]:
        """Busca notícias reais no Google News"""
        try:
            logger.info(f"Buscando notícias para: {query}")
            
            # Construir query otimizada
            search_terms = [
                f'"{query}"',
                f'{query} fundo',
                f'{query} gestora',
                f'{query} investimento',
                f'{query} CVM',
                f'{query} BACEN'
            ]
            
            all_news = []
            
            for search_term in search_terms[:2]:  # Limitar para não sobrecarregar
                encoded_query = quote_plus(search_term)
                rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
                
                try:
                    response = self.session.get(rss_url, timeout=10)
                    
                    if response.status_code == 200:
                        # Parse do RSS XML
                        root = ET.fromstring(response.content)
                        
                        # Extrair itens do RSS
                        for item in root.findall('.//item')[:5]:  # Limitar a 5 por busca
                            title = item.find('title')
                            link = item.find('link')
                            pub_date = item.find('pubDate')
                            description = item.find('description')
                            
                            if title is not None and link is not None:
                                news_item = {
                                    'title': title.text or '',
                                    'link': link.text or '',
                                    'pubDate': pub_date.text if pub_date is not None else '',
                                    'description': description.text if description is not None else '',
                                    'source': self._extract_source_from_url(link.text or '')
                                }
                                
                                # Verificar se é recente
                                if self._is_recent_news(news_item['pubDate'], days_back):
                                    all_news.append(news_item)
                                
                except Exception as e:
                    logger.warning(f"Erro ao processar RSS para '{search_term}': {str(e)}")
                    continue
                
                time.sleep(1)  # Rate limiting
            
            # Remover duplicatas
            unique_news = []
            seen_titles = set()
            
            for news in all_news:
                title_key = news['title'].lower().strip()
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    unique_news.append(news)
            
            logger.info(f"Encontradas {len(unique_news)} notícias únicas")
            return unique_news
            
        except Exception as e:
            logger.error(f"Erro na busca de notícias: {str(e)}")
            return []

    def _extract_source_from_url(self, url: str) -> str:
        """Extrai fonte da URL"""
        try:
            if 'g1.globo.com' in url:
                return 'G1'
            elif 'valor.globo.com' in url:
                return 'Valor Econômico'
            elif 'exame.com' in url:
                return 'Exame'
            elif 'infomoney.com.br' in url:
                return 'InfoMoney'
            elif 'estadao.com.br' in url:
                return 'Estadão'
            elif 'folha.uol.com.br' in url:
                return 'Folha de S.Paulo'
            elif 'cnnbrasil.com.br' in url:
                return 'CNN Brasil'
            else:
                # Extrair domínio
                import urllib.parse
                parsed = urllib.parse.urlparse(url)
                return parsed.netloc.replace('www.', '').title()
        except:
            return 'Fonte Desconhecida'

    def _is_recent_news(self, pub_date: str, days_back: int) -> bool:
        """Verifica se a notícia é recente"""
        try:
            # Parse de diferentes formatos de data
            from email.utils import parsedate_to_datetime
            
            news_date = parsedate_to_datetime(pub_date)
            cutoff_date = datetime.now().replace(tzinfo=news_date.tzinfo) - timedelta(days=days_back)
            
            return news_date >= cutoff_date
        except:
            # Se não conseguir parsear, assumir que é recente
            return True

    def extract_news_content(self, news_url: str) -> str:
        """Extrai conteúdo real da notícia"""
        try:
            logger.info(f"Extraindo conteúdo de: {news_url[:50]}...")
            
            response = self.session.get(news_url, timeout=15)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remover scripts e estilos
                for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                    element.decompose()
                
                # Estratégias por site
                content = ""
                
                # Valor Econômico
                if 'valor.globo.com' in news_url:
                    content_div = soup.find('div', class_='content-text__container')
                    if content_div:
                        content = content_div.get_text()
                
                # G1
                elif 'g1.globo.com' in news_url:
                    content_div = soup.find('div', class_='mc-article-body')
                    if content_div:
                        content = content_div.get_text()
                
                # Exame
                elif 'exame.com' in news_url:
                    content_div = soup.find('div', class_='article-content')
                    if content_div:
                        content = content_div.get_text()
                
                # Fallback: buscar por article ou main
                if not content.strip():
                    for tag in ['article', 'main']:
                        element = soup.find(tag)
                        if element:
                            content = element.get_text()
                            break
                
                # Limpeza
                content = re.sub(r'\s+', ' ', content).strip()
                
                if len(content) > 200:
                    return content[:2000]  # Limitar tamanho
                else:
                    # Fallback com título e descrição
                    title = soup.find('title')
                    return f"Notícia financeira: {title.get_text() if title else 'Sem título'}"
            
        except Exception as e:
            logger.warning(f"Erro ao extrair conteúdo: {str(e)}")
        
        # Fallback
        return "Notícia sobre operações financeiras e gestão de investimentos."

    def analyze_news_with_ai(self, content: str) -> RiskAnalysis:
        """Analisa notícia com Advanced DD-AI"""
        try:
            payload = {"text": content}
            
            response = requests.post(
                f"{self.api_base_url}/api/analyze-risk",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                return RiskAnalysis(
                    risk_level=result.get('risk_level', 'MÉDIO'),
                    confidence=result.get('confidence', 0.0),
                    explanation=result.get('explanation', ''),
                    compliance_flags=result.get('compliance_flags', []),
                    regulatory_alerts=result.get('regulatory_alerts', []),
                    entities_found=result.get('entities_found', [])
                )
            else:
                logger.error(f"Erro na API: {response.status_code}")
                return RiskAnalysis("ERRO", 0.0, "Erro na análise", [], [])
                
        except Exception as e:
            logger.error(f"Erro na análise: {str(e)}")
            return RiskAnalysis("ERRO", 0.0, f"Erro: {str(e)}", [], [])

    def calculate_company_risk_score(self, analyses: List[RiskAnalysis]) -> Tuple[str, float, Dict]:
        """Calcula score consolidado de risco"""
        if not analyses:
            return "INDETERMINADO", 0.0, {}
        
        # Pesos e contadores
        risk_weights = {"CRÍTICO": 4, "ALTO": 3, "MÉDIO": 2, "BAIXO": 1}
        risk_counts = {"CRÍTICO": 0, "ALTO": 0, "MÉDIO": 0, "BAIXO": 0}
        
        total_weighted = 0
        total_weight = 0
        all_flags = []
        all_alerts = []
        
        for analysis in analyses:
            if analysis.risk_level in risk_weights:
                weight = risk_weights[analysis.risk_level]
                confidence_factor = max(analysis.confidence / 100.0, 0.1)  # Mínimo 10%
                
                total_weighted += weight * confidence_factor
                total_weight += confidence_factor
                
                risk_counts[analysis.risk_level] += 1
                all_flags.extend(analysis.compliance_flags)
                all_alerts.extend(analysis.regulatory_alerts)
        
        if total_weight == 0:
            return "INDETERMINADO", 0.0, {}
        
        avg_score = total_weighted / total_weight
        
        # Determinar nível final
        if avg_score >= 3.5:
            final_risk = "CRÍTICO"
        elif avg_score >= 2.5:
            final_risk = "ALTO"
        elif avg_score >= 1.5:
            final_risk = "MÉDIO"
        else:
            final_risk = "BAIXO"
        
        # Score 0-100
        risk_score = min(avg_score * 25, 100)
        
        # Estatísticas detalhadas
        stats = {
            'risk_distribution': risk_counts,
            'total_analyses': len(analyses),
            'avg_confidence': sum(a.confidence for a in analyses) / len(analyses),
            'compliance_flags': len(set(all_flags)),
            'regulatory_alerts': len(set(all_alerts))
        }
        
        return final_risk, risk_score, stats

    def generate_risk_report(self, company_info: CompanyInfo, news_items: List[NewsItem], 
                           risk_analyses: List[RiskAnalysis], final_risk: str, 
                           risk_score: float, stats: Dict) -> Dict:
        """Gera relatório completo de risco"""
        
        # Análise temporal
        recent_news = [n for n in news_items if self._is_very_recent(n.data, 7)]
        
        # Principais riscos identificados
        high_risk_news = [
            (news, analysis) for news, analysis in zip(news_items, risk_analyses)
            if analysis.risk_level in ['CRÍTICO', 'ALTO']
        ]
        
        # Recomendações baseadas no risco
        recommendations = self._generate_recommendations(final_risk, stats, high_risk_news)
        
        report = {
            'metadata': {
                'company_info': asdict(company_info),
                'analysis_date': datetime.now().isoformat(),
                'total_news_analyzed': len(news_items),
                'analysis_period_days': 30
            },
            'risk_assessment': {
                'final_risk_level': final_risk,
                'risk_score': round(risk_score, 1),
                'confidence_level': round(stats.get('avg_confidence', 0), 1),
                'risk_distribution': stats.get('risk_distribution', {}),
                'compliance_issues': stats.get('compliance_flags', 0),
                'regulatory_alerts': stats.get('regulatory_alerts', 0)
            },
            'news_summary': {
                'total_news_found': len(news_items),
                'relevant_news': len([n for n in news_items if n.relevancia_score > 0.5]),
                'recent_news_7days': len(recent_news),
                'high_risk_news': len(high_risk_news)
            },
            'recommendations': recommendations,
            'detailed_analysis': [
                {
                    'news': asdict(news),
                    'risk_analysis': asdict(analysis)
                }
                for news, analysis in zip(news_items, risk_analyses)
            ]
        }
        
        return report

    def _is_very_recent(self, date_str: str, days: int) -> bool:
        """Verifica se é muito recente"""
        try:
            from email.utils import parsedate_to_datetime
            news_date = parsedate_to_datetime(date_str)
            cutoff = datetime.now().replace(tzinfo=news_date.tzinfo) - timedelta(days=days)
            return news_date >= cutoff
        except:
            return False

    def _generate_recommendations(self, risk_level: str, stats: Dict, high_risk_news: List) -> List[str]:
        """Gera recomendações específicas"""
        recommendations = []
        
        if risk_level == "CRÍTICO":
            recommendations.extend([
                "🚨 AÇÃO IMEDIATA: Revisar imediatamente toda exposição à empresa",
                "🔍 Realizar due diligence aprofundada nas últimas 48h",
                "📋 Verificar compliance urgente com CVM/BACEN",
                "⚖️ Considerar suspensão temporária de novos investimentos",
                "📞 Contatar diretamente a gestora para esclarecimentos"
            ])
        elif risk_level == "ALTO":
            recommendations.extend([
                "⚠️ Monitoramento intensivo: análise semanal obrigatória",
                "📈 Revisar e possivelmente reduzir limites de exposição",
                "🔍 Solicitar relatórios adicionais da gestora",
                "📋 Documentar justificativas para manter exposição",
                "🛡️ Implementar controles de risco adicionais"
            ])
        elif risk_level == "MÉDIO":
            recommendations.extend([
                "📊 Monitoramento quinzenal com relatórios mensais",
                "📋 Manter documentação de compliance atualizada",
                "🔍 Acompanhar indicadores de performance",
                "📈 Revisão trimestral de limites"
            ])
        else:  # BAIXO
            recommendations.extend([
                "✅ Manter exposição dentro dos parâmetros atuais",
                "📊 Monitoramento trimestral suficiente",
                "📋 Documentação padrão adequada"
            ])
        
        # Recomendações específicas baseadas em achados
        if stats.get('compliance_flags', 0) > 0:
            recommendations.append("📜 Investigar questões de compliance identificadas")
        
        if stats.get('regulatory_alerts', 0) > 0:
            recommendations.append("🏛️ Verificar conformidade com alertas regulatórios")
        
        if len(high_risk_news) > 2:
            recommendations.append("📰 Volume alto de notícias negativas - investigação necessária")
        
        return recommendations

    def save_detailed_report(self, report: Dict, filename: str = None) -> str:
        """Salva relatório detalhado em markdown"""
        if not filename:
            company_name = report['metadata']['company_info']['razao_social']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = re.sub(r'[^\w\s-]', '', company_name).strip()[:30]
            filename = f"detailed_risk_report_{safe_name}_{timestamp}.md"
        
        company = report['metadata']['company_info']
        risk = report['risk_assessment']
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 🔍 Relatório Detalhado de Risco - {company['razao_social']}\n\n")
            f.write(f"**Data da Análise:** {datetime.fromisoformat(report['metadata']['analysis_date']).strftime('%d/%m/%Y %H:%M')}\n\n")
            
            # Executive Summary
            f.write("## 📊 Resumo Executivo\n\n")
            f.write(f"- **Risco Final:** {risk['final_risk_level']} (Score: {risk['risk_score']}/100)\n")
            f.write(f"- **Confiança da Análise:** {risk['confidence_level']}%\n")
            f.write(f"- **Notícias Analisadas:** {report['news_summary']['total_news_found']}\n")
            f.write(f"- **Notícias de Alto Risco:** {report['news_summary']['high_risk_news']}\n\n")
            
            # Company Info
            f.write("## 🏢 Informações da Empresa\n\n")
            f.write(f"- **CNPJ:** {company.get('cnpj', 'N/A')}\n")
            f.write(f"- **Razão Social:** {company['razao_social']}\n")
            f.write(f"- **Situação:** {company.get('situacao', 'N/A')}\n")
            f.write(f"- **Atividade:** {company.get('atividade_principal', 'N/A')}\n")
            f.write(f"- **Porte:** {company.get('porte', 'N/A')}\n\n")
            
            # Risk Analysis
            f.write("## 🎯 Análise de Risco\n\n")
            dist = risk['risk_distribution']
            f.write(f"- **CRÍTICO:** {dist.get('CRÍTICO', 0)} notícias\n")
            f.write(f"- **ALTO:** {dist.get('ALTO', 0)} notícias\n")
            f.write(f"- **MÉDIO:** {dist.get('MÉDIO', 0)} notícias\n")
            f.write(f"- **BAIXO:** {dist.get('BAIXO', 0)} notícias\n\n")
            
            # Recommendations
            f.write("## 💡 Recomendações\n\n")
            for rec in report['recommendations']:
                f.write(f"- {rec}\n")
            f.write("\n")
            
            # Detailed News Analysis
            f.write("## 📰 Análise Detalhada das Notícias\n\n")
            for i, item in enumerate(report['detailed_analysis'], 1):
                news = item['news']
                analysis = item['risk_analysis']
                
                f.write(f"### {i}. {news['titulo']}\n\n")
                f.write(f"- **Fonte:** {news['fonte']}\n")
                f.write(f"- **Data:** {news['data']}\n")
                f.write(f"- **Relevância:** {news['relevancia_score']:.1f}\n")
                f.write(f"- **Risco:** {analysis['risk_level']}\n")
                f.write(f"- **Confiança:** {analysis['confidence']:.1f}%\n")
                
                if analysis['compliance_flags']:
                    f.write(f"- **Compliance Flags:** {', '.join(analysis['compliance_flags'])}\n")
                
                if analysis['regulatory_alerts']:
                    f.write(f"- **Alertas Regulatórios:** {', '.join(analysis['regulatory_alerts'])}\n")
                
                f.write(f"- **URL:** {news['url']}\n\n")
        
        return filename

    def monitor_company_risk(self, identifier: str, days_back: int = 30, 
                           is_cnpj: bool = None, save_report: bool = True) -> Dict:
        """
        Função principal: monitora risco completo da empresa
        """
        logger.info(f"🚀 INICIANDO MONITORAMENTO DE RISCO: {identifier}")
        
        # 1. Identificar tipo e enriquecer dados
        if is_cnpj is None:
            is_cnpj = bool(re.match(r'^\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}$', identifier))
        
        if is_cnpj:
            company_info = self.enrich_company_by_cnpj(identifier)
            if not company_info:
                logger.error("Falha no enriquecimento de dados")
                return {"error": "Não foi possível enriquecer dados da empresa"}
            
            search_name = company_info.razao_social
        else:
            search_name = identifier
            company_info = CompanyInfo(
                cnpj="", razao_social=identifier, nome_fantasia="", 
                situacao="", atividade_principal="", porte="", capital_social=0.0
            )
        
        # 2. Buscar notícias reais
        logger.info(f"🔍 Buscando notícias para: {search_name}")
        news_data = self.search_google_news(search_name, days_back)
        
        if not news_data:
            logger.warning("Nenhuma notícia encontrada")
            return {"error": "Nenhuma notícia encontrada para análise"}
        
        # 3. Processar notícias
        processed_news = []
        risk_analyses = []
        
        for i, news_item in enumerate(news_data[:10], 1):  # Limitar a 10
            logger.info(f"📰 Processando notícia {i}/{min(len(news_data), 10)}")
            
            # Extrair conteúdo
            content = self.extract_news_content(news_item.get('link', ''))
            
            # Calcular relevância
            relevance = self._calculate_relevance(news_item.get('title', ''), search_name)
            
            # Criar objeto NewsItem
            news_obj = NewsItem(
                titulo=news_item.get('title', ''),
                url=news_item.get('link', ''),
                fonte=news_item.get('source', ''),
                data=news_item.get('pubDate', ''),
                conteudo=content,
                relevancia_score=relevance
            )
            
            processed_news.append(news_obj)
            
            # Analisar apenas se relevante
            if relevance > 0.3:
                logger.info(f"🧠 Analisando risco (relevância: {relevance:.1f})...")
                risk_analysis = self.analyze_news_with_ai(content)
                risk_analyses.append(risk_analysis)
                logger.info(f"📊 Risco: {risk_analysis.risk_level}")
            
            time.sleep(0.5)  # Rate limiting
        
        # 4. Calcular risco consolidado
        logger.info("📊 Calculando risco consolidado...")
        final_risk, risk_score, stats = self.calculate_company_risk_score(risk_analyses)
        
        # 5. Gerar relatório
        logger.info("📋 Gerando relatório...")
        report = self.generate_risk_report(
            company_info, processed_news, risk_analyses, 
            final_risk, risk_score, stats
        )
        
        # 6. Salvar se solicitado
        if save_report:
            filename = self.save_detailed_report(report)
            report['saved_report'] = filename
            logger.info(f"💾 Relatório salvo: {filename}")
        
        logger.info(f"✅ Análise concluída: {final_risk} (Score: {risk_score:.1f})")
        
        return report

    def _calculate_relevance(self, title: str, company_name: str) -> float:
        """Calcula relevância melhorada"""
        title_lower = title.lower()
        company_lower = company_name.lower()
        
        # Score base
        if company_lower in title_lower:
            relevance = 1.0
        else:
            # Palavras-chave da empresa
            company_words = [w for w in company_lower.split() if len(w) > 3]
            if company_words:
                matches = sum(1 for word in company_words if word in title_lower)
                relevance = matches / len(company_words)
            else:
                relevance = 0.0
        
        # Bônus para termos financeiros
        financial_terms = [
            'fundo', 'gestora', 'investimento', 'cvm', 'bacen', 'risco', 
            'compliance', 'auditoria', 'fraude', 'irregularidade', 'multa',
            'sanção', 'suspensão', 'investigação', 'performance', 'rentabilidade'
        ]
        
        for term in financial_terms:
            if term in title_lower:
                relevance += 0.1
        
        return min(relevance, 1.0)

def main():
    """Demonstração do sistema"""
    print("🔍 ENHANCED NEWS RISK MONITOR - Advanced DD-AI v2.1")
    print("=" * 60)
    
    monitor = EnhancedNewsMonitor()
    
    # Teste com CNPJ real
    test_cnpj = "05.285.819/0001-66"
    
    print(f"\n🎯 TESTANDO MONITORAMENTO COMPLETO")
    print(f"📊 CNPJ: {test_cnpj}")
    print("=" * 60)
    
    try:
        result = monitor.monitor_company_risk(test_cnpj, days_back=30, is_cnpj=True)
        
        if 'error' in result:
            print(f"❌ Erro: {result['error']}")
        else:
            risk = result['risk_assessment']
            print(f"\n📊 RESULTADO:")
            print(f"   🎯 Risco Final: {risk['final_risk_level']}")
            print(f"   📈 Score: {risk['risk_score']}/100")
            print(f"   📰 Notícias: {result['news_summary']['total_news_found']}")
            print(f"   💾 Relatório: {result.get('saved_report', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Erro na execução: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
