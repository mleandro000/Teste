#!/usr/bin/env python3
"""
Script para iniciar o backend de forma controlada
"""

import subprocess
import sys
import time
import requests
import os

def start_backend():
    """Inicia o backend e verifica se está funcionando"""
    print("🚀 Iniciando backend DD-AI...")
    
    # Verificar se o arquivo existe
    if not os.path.exists("sql_api.py"):
        print("❌ Arquivo sql_api.py não encontrado!")
        return False
    
    try:
        # Iniciar o processo
        print("📡 Iniciando servidor na porta 8001...")
        process = subprocess.Popen([
            sys.executable, "sql_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aguardar um pouco
        print("⏳ Aguardando inicialização...")
        time.sleep(10)
        
        # Verificar se o processo ainda está rodando
        if process.poll() is not None:
            print("❌ Processo terminou prematuramente!")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        # Testar se está respondendo
        print("🔍 Testando conectividade...")
        try:
            response = requests.get("http://127.0.0.1:8001/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend funcionando corretamente!")
                print(f"   Resposta: {response.json()}")
                return True
            else:
                print(f"❌ Backend retornou status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conectividade: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return False

def test_endpoints():
    """Testa os endpoints principais"""
    print("\n🧪 Testando endpoints...")
    
    # Teste de conexão
    try:
        data = {
            "server": "DESKTOP-T9HKFSQ\\SQLEXPRESS",
            "database": "Projeto_Dev",
            "port": 1433,
            "use_windows_auth": True
        }
        
        response = requests.post("http://127.0.0.1:8001/api/test-connection", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Endpoint /api/test-connection: OK")
            else:
                print(f"❌ Endpoint /api/test-connection: {result.get('message')}")
        else:
            print(f"❌ Endpoint /api/test-connection: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste de conexão: {e}")

if __name__ == "__main__":
    print("🔧 SCRIPT DE INICIALIZAÇÃO DO BACKEND")
    print("=" * 50)
    
    success = start_backend()
    
    if success:
        test_endpoints()
        print("\n🎉 Backend iniciado com sucesso!")
        print("   Mantenha este terminal aberto.")
        print("   Pressione Ctrl+C para parar.")
        
        try:
            # Manter o script rodando
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando backend...")
    else:
        print("\n❌ Falha ao iniciar backend!")
        sys.exit(1)
