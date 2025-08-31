#!/usr/bin/env python3
"""
📖 EXEMPLO DE USO INTELIGENTE - Advanced DD-AI v2.1
==================================================

Demonstra como usar o sistema inteligente para diferentes cenários:

1. 📊 Query SQL que retorna CNPJs
2. 🏢 Query SQL que retorna Razões Sociais
3. 🔄 Query SQL com dados mistos (CNPJ + Nome)
4. 📝 Lista manual de empresas

Este exemplo mostra como o sistema automaticamente detecta
o tipo de dados e escolhe a melhor estratégia de análise.
"""

import requests
import json
from datetime import datetime

class ExemploUsoInteligente:
    def __init__(self, api_url: str = "http://127.0.0.1:8001"):
        self.api_url = api_url
    
    def testar_deteccao_automatica(self):
        """
        Testa a detecção automática de tipos de dados
        """
        print("🔍 TESTE 1: DETECÇÃO AUTOMÁTICA DE TIPOS")
        print("=" * 50)
        
        # Dados mistos para teste
        dados_teste = [
            "05.285.819/0001-66",                    # CNPJ
            "XP Asset Management",                   # Nome empresa
            "Itaú Unibanco Holding S.A.",          # Nome empresa
            "05.753.599/0001-58",                   # CNPJ
            "CATERPILLAR FUNDO DE INVESTIMENTO",    # Nome empresa
            "11.222.333/0001-81",                   # CNPJ
            "Verde Asset Management"                 # Nome empresa
        ]
        
        payload = {"data_items": dados_teste}
        
        try:
            response = requests.post(f"{self.api_url}/api/detect-data-type", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("📊 RESULTADOS DA DETECÇÃO:")
                for deteccao in resultado["detections"]:
                    tipo = deteccao["detected_type"]
                    confianca = deteccao["confidence"]
                    valor = deteccao["original_value"]
                    
                    emoji = "🔢" if tipo == "cnpj" else "🏢" if tipo == "company_name" else "❓"
                    print(f"   {emoji} {valor:<30} → {tipo.upper()} ({confianca:.1%})")
                
                print(f"\n📈 RESUMO:")
                print(f"   CNPJs: {resultado['summary']['CNPJ']}")
                print(f"   Nomes: {resultado['summary']['COMPANY_NAME']}")
                print(f"   Desconhecidos: {resultado['summary']['UNKNOWN']}")
                
                print(f"\n💡 RECOMENDAÇÃO:")
                rec = resultado["recommendations"]
                print(f"   Estratégia: {rec['primary']}")
                print(f"   Motivo: {rec['reason']}")
                
                return True
            else:
                print(f"❌ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def exemplo_query_cnpjs(self):
        """
        Exemplo: Query SQL que retorna CNPJs
        """
        print("\n🔢 TESTE 2: ANÁLISE DE QUERY COM CNPJs")
        print("=" * 50)
        
        # Simular dados de uma query SQL com CNPJs
        dados_cnpjs = [
            "05.285.819/0001-66",
            "05.753.599/0001-58", 
            "05.754.060/0001-13"
        ]
        
        payload = {
            "data_items": dados_cnpjs,
            "analysis_strategy": "cnpj_only",  # Forçar estratégia de enriquecimento
            "include_news": True,
            "include_enrichment": True,
            "max_concurrent": 3
        }
        
        try:
            print("🚀 Iniciando análise com estratégia CNPJ_ONLY...")
            response = requests.post(f"{self.api_url}/api/smart-batch-analysis", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("✅ ANÁLISE CONCLUÍDA!")
                print(f"📊 Empresas processadas: {resultado['summary']['companies_analyzed']}")
                print(f"📈 Score médio de risco: {resultado['summary']['avg_risk_score']:.1f}/100")
                print(f"⚡ Eficiência: {resultado['summary']['processing_efficiency']}")
                
                print(f"\n🏢 EMPRESAS ANALISADAS:")
                for i, empresa in enumerate(resultado['results'], 1):
                    nome = empresa['company_name_used']
                    score = empresa['final_risk_score']
                    estrategia = empresa['strategy_used']
                    
                    emoji = "🟢" if score < 40 else "🟡" if score < 70 else "🔴"
                    print(f"   {i}. {nome:<40} {emoji} {score:.1f}/100 ({estrategia})")
                
                return True
            else:
                print(f"❌ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def exemplo_query_nomes(self):
        """
        Exemplo: Query SQL que retorna Razões Sociais
        """
        print("\n🏢 TESTE 3: ANÁLISE DE QUERY COM NOMES DE EMPRESAS")
        print("=" * 50)
        
        # Simular dados de uma query SQL com nomes
        dados_nomes = [
            "XP Asset Management",
            "Itaú Asset Management", 
            "Verde Asset Management",
            "CATERPILLAR FUNDO DE INVESTIMENTO",
            "IDEAL EDUCACAO FUNDO"
        ]
        
        payload = {
            "data_items": dados_nomes,
            "analysis_strategy": "company_name_only",  # Forçar estratégia de busca por nome
            "include_news": True,
            "include_enrichment": False,  # Não precisa enriquecer via CNPJ
            "max_concurrent": 3
        }
        
        try:
            print("🚀 Iniciando análise com estratégia COMPANY_NAME_ONLY...")
            response = requests.post(f"{self.api_url}/api/smart-batch-analysis", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("✅ ANÁLISE CONCLUÍDA!")
                print(f"📊 Empresas processadas: {resultado['summary']['companies_analyzed']}")
                print(f"📈 Score médio de risco: {resultado['summary']['avg_risk_score']:.1f}/100")
                
                print(f"\n📰 ESTRATÉGIA UTILIZADA:")
                for estrategia, stats in resultado['strategy_performance'].items():
                    if stats['count'] > 0:
                        print(f"   {estrategia}: {stats['count']} empresas, {stats['success_rate']:.1f}% sucesso")
                
                print(f"\n🏢 EMPRESAS ANALISADAS:")
                for i, empresa in enumerate(resultado['results'], 1):
                    nome = empresa['company_name_used']
                    score = empresa['final_risk_score']
                    noticias = len(empresa['news_analysis'])
                    
                    emoji = "🟢" if score < 40 else "🟡" if score < 70 else "🔴"
                    print(f"   {i}. {nome:<40} {emoji} {score:.1f}/100 ({noticias} notícias)")
                
                return True
            else:
                print(f"❌ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def exemplo_dados_mistos(self):
        """
        Exemplo: Dados mistos (CNPJ + Nome) com estratégia híbrida
        """
        print("\n🔄 TESTE 4: ANÁLISE HÍBRIDA COM DADOS MISTOS")
        print("=" * 50)
        
        # Simular resultados de query SQL com colunas mistas
        dados_mistos = [
            {"cnpj": "05.285.819/0001-66", "razao_social": "IDEAL EDUCACAO FUNDO"},
            {"cnpj": "", "razao_social": "XP Asset Management"},  # Só nome
            {"cnpj": "05.753.599/0001-58", "razao_social": ""},  # Só CNPJ
            {"cnpj": "05.754.060/0001-13", "razao_social": "CATERPILLAR FUNDO"}  # Ambos
        ]
        
        payload = {
            "data_items": dados_mistos,
            "analysis_strategy": "hybrid",  # Estratégia híbrida
            "include_news": True,
            "include_enrichment": True,
            "max_concurrent": 2,
            "column_mapping": {
                "cnpj_col": "cnpj",
                "name_col": "razao_social"
            }
        }
        
        try:
            print("🚀 Iniciando análise com estratégia HÍBRIDA...")
            response = requests.post(f"{self.api_url}/api/smart-batch-analysis", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("✅ ANÁLISE HÍBRIDA CONCLUÍDA!")
                print(f"📊 Items processados: {resultado['summary']['companies_analyzed']}")
                
                print(f"\n🎯 DISTRIBUIÇÃO POR ESTRATÉGIA:")
                for estrategia, count in resultado['strategy_distribution'].items():
                    print(f"   {estrategia}: {count} items")
                
                print(f"\n📊 PERFORMANCE POR ESTRATÉGIA:")
                for estrategia, stats in resultado['strategy_performance'].items():
                    if stats['count'] > 0:
                        print(f"   {estrategia}:")
                        print(f"      Processados: {stats['count']}")
                        print(f"      Taxa de sucesso: {stats['success_rate']:.1f}%")
                        print(f"      Score médio: {stats['avg_score']:.1f}/100")
                
                print(f"\n🏢 RESULTADOS DETALHADOS:")
                for i, empresa in enumerate(resultado['results'], 1):
                    dados_orig = empresa['original_data']
                    nome = empresa['company_name_used']
                    score = empresa['final_risk_score']
                    estrategia = empresa['strategy_used']
                    erros = empresa['errors']
                    
                    emoji = "🟢" if score < 40 else "🟡" if score < 70 else "🔴"
                    status = "❌" if erros else "✅"
                    
                    print(f"   {i}. {status} {nome:<35} {emoji} {score:.1f}/100")
                    print(f"      Dados originais: {dados_orig['original_value'][:50]}...")
                    print(f"      Estratégia: {estrategia}")
                    if erros:
                        print(f"      Erros: {'; '.join(erros[:2])}")
                
                return True
            else:
                print(f"❌ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def exemplo_auto_detect(self):
        """
        Exemplo: Detecção automática da melhor estratégia
        """
        print("\n🧠 TESTE 5: DETECÇÃO AUTOMÁTICA DE ESTRATÉGIA")
        print("=" * 50)
        
        # Dados variados para testar auto-detecção
        dados_variados = [
            "05.285.819/0001-66",          # CNPJ
            "XP Asset Management",         # Nome
            "05.753.599/0001-58",         # CNPJ
            "Itaú Asset Management",      # Nome
            "Verde Asset Management"       # Nome
        ]
        
        payload = {
            "data_items": dados_variados,
            "analysis_strategy": "auto_detect",  # Deixar o sistema escolher
            "include_news": True,
            "include_enrichment": True,
            "max_concurrent": 3
        }
        
        try:
            print("🚀 Iniciando análise com AUTO_DETECT...")
            response = requests.post(f"{self.api_url}/api/smart-batch-analysis", json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                
                print("✅ ANÁLISE AUTO-DETECTADA CONCLUÍDA!")
                print(f"🎯 Estratégia escolhida: {resultado['summary']['most_used_strategy']}")
                print(f"📊 Empresas analisadas: {resultado['summary']['companies_analyzed']}")
                print(f"📈 Score médio: {resultado['summary']['avg_risk_score']:.1f}/100")
                
                print(f"\n🤖 COMO O SISTEMA DECIDIU:")
                for estrategia, count in resultado['strategy_distribution'].items():
                    if count > 0:
                        print(f"   {estrategia.replace('_', ' ').title()}: {count} items")
                
                return True
            else:
                print(f"❌ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def executar_todos_exemplos(self):
        """
        Executa todos os exemplos em sequência
        """
        print("🎯 DEMONSTRAÇÃO COMPLETA - Sistema Inteligente de Análise")
        print("=" * 70)
        print("🚀 O sistema detecta automaticamente se você tem:")
        print("   📊 CNPJs → Enriquece via API Brasil + busca notícias")
        print("   🏢 Nomes → Busca direta por notícias")
        print("   🔄 Mistos → Escolhe a melhor estratégia para cada item")
        print("=" * 70)
        
        testes = [
            ("Detecção Automática", self.testar_deteccao_automatica),
            ("Análise por CNPJs", self.exemplo_query_cnpjs),
            ("Análise por Nomes", self.exemplo_query_nomes),
            ("Análise Híbrida", self.exemplo_dados_mistos),
            ("Auto-Detecção", self.exemplo_auto_detect)
        ]
        
        resultados = []
        
        for nome, teste_func in testes:
            try:
                print(f"\n⏱️ Iniciando: {nome}")
                sucesso = teste_func()
                resultados.append((nome, sucesso))
                
                if sucesso:
                    print(f"✅ {nome} - SUCESSO")
                else:
                    print(f"❌ {nome} - FALHA")
                
                # Pausa entre testes
                import time
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ {nome} - ERRO: {str(e)}")
                resultados.append((nome, False))
        
        # Resumo final
        print("\n" + "=" * 70)
        print("📊 RESUMO DOS TESTES")
        print("=" * 70)
        
        sucessos = 0
        for nome, sucesso in resultados:
            status = "✅ PASSOU" if sucesso else "❌ FALHOU"
            print(f"   {nome:<25} {status}")
            if sucesso:
                sucessos += 1
        
        taxa_sucesso = (sucessos / len(resultados)) * 100
        print(f"\n🎯 Taxa de Sucesso: {sucessos}/{len(resultados)} ({taxa_sucesso:.1f}%)")
        
        if taxa_sucesso >= 80:
            print("🏆 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        elif taxa_sucesso >= 60:
            print("✅ Sistema funcionando bem")
        else:
            print("⚠️ Sistema precisa de ajustes")
        
        return resultados

def main():
    """Função principal"""
    print("📖 EXEMPLO DE USO INTELIGENTE - Advanced DD-AI v2.1")
    print("=" * 60)
    print("🎯 Este exemplo demonstra como o sistema funciona com diferentes tipos de dados:")
    print()
    
    exemplo = ExemploUsoInteligente()
    
    # Verificar se a API está disponível
    try:
        response = requests.get(f"{exemplo.api_url}/")
        if response.status_code == 200:
            print("✅ API DD-AI conectada e funcionando")
            print()
            
            # Executar demonstração completa
            exemplo.executar_todos_exemplos()
            
        else:
            print("❌ API não está respondendo corretamente")
            print("💡 Certifique-se de que o backend está rodando: python sql_api.py")
            
    except Exception as e:
        print(f"❌ Erro de conexão com a API: {str(e)}")
        print("💡 Verifique se o backend está rodando em http://127.0.0.1:8001")

if __name__ == "__main__":
    main()
