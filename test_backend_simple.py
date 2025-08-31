#!/usr/bin/env python3
"""
Teste simples do backend para diagnóstico
"""

import sys
import os

def test_imports():
    """Testa se todas as dependências estão disponíveis"""
    print("🔍 Testando imports...")
    
    try:
        import fastapi
        print("✅ FastAPI OK")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import pyodbc
        print("✅ PyODBC OK")
    except ImportError as e:
        print(f"❌ PyODBC: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn OK")
    except ImportError as e:
        print(f"❌ Uvicorn: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("✅ Pydantic OK")
    except ImportError as e:
        print(f"❌ Pydantic: {e}")
        return False
    
    return True

def test_advanced_ai():
    """Testa se o módulo de IA avançada está disponível"""
    print("\n🧠 Testando Advanced AI...")
    
    try:
        from advanced_financial_bert import AdvancedFinancialBERT
        print("✅ Advanced Financial BERT OK")
        return True
    except ImportError as e:
        print(f"❌ Advanced Financial BERT: {e}")
        return False

def test_sql_connection():
    """Testa conexão básica com SQL Server"""
    print("\n🗄️ Testando conexão SQL...")
    
    try:
        import pyodbc
        
        # Dados de conexão
        server = "DESKTOP-T9HKFSQ\\SQLEXPRESS"
        database = "Projeto_Dev"
        
        # String de conexão
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        
        # Tentar conectar
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Teste simples
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print("✅ Conexão SQL OK")
        print(f"   Versão: {version[0][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Conexão SQL: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 DIAGNÓSTICO DO BACKEND DD-AI")
    print("=" * 50)
    
    # Teste 1: Imports
    if not test_imports():
        print("\n❌ FALHA: Imports básicos não funcionaram")
        return False
    
    # Teste 2: Advanced AI
    ai_ok = test_advanced_ai()
    
    # Teste 3: SQL Connection
    sql_ok = test_sql_connection()
    
    print("\n📊 RESUMO DOS TESTES:")
    print(f"   Imports básicos: ✅")
    print(f"   Advanced AI: {'✅' if ai_ok else '❌'}")
    print(f"   Conexão SQL: {'✅' if sql_ok else '❌'}")
    
    if ai_ok and sql_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("   O backend deve funcionar corretamente.")
        return True
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM:")
        if not ai_ok:
            print("   - Advanced AI não disponível (funcionalidades limitadas)")
        if not sql_ok:
            print("   - Conexão SQL falhou (verificar configuração)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
