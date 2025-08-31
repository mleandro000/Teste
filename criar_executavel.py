#!/usr/bin/env python3
"""
🚀 GERADOR DE EXECUTÁVEL - Advanced DD-AI v2.1
==============================================

Script para criar executável standalone do DD-AI para Windows 11 64-bit
usando PyInstaller. Não requer Python instalado na máquina final.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def instalar_pyinstaller():
    """Instala PyInstaller se não estiver disponível"""
    try:
        import PyInstaller
        print("✅ PyInstaller já instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar PyInstaller")
            return False

def criar_spec_file():
    """Cria arquivo .spec customizado para o executável"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Arquivos de dados necessários
datas = [
    ('advanced_financial_bert.py', '.'),
    ('enhanced_news_monitor.py', '.'),
]

# Imports ocultos necessários
hiddenimports = [
    'torch',
    'transformers',
    'peft',
    'bitsandbytes',
    'fastapi',
    'uvicorn',
    'pandas',
    'numpy',
    'requests',
    'beautifulsoup4',
    'pyodbc',
    'sklearn',
    'accelerate',
    'datasets',
    'evaluate',
]

a = Analysis(
    ['sql_api.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'jupyter', 'notebook', 'IPython'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DD-AI-Backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='dd-ai-icon.ico' if os.path.exists('dd-ai-icon.ico') else None,
)
'''
    
    with open('dd-ai.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Arquivo .spec criado")

def otimizar_build():
    """Otimizações para reduzir tamanho do executável"""
    exclusoes = [
        '--exclude-module=matplotlib',
        '--exclude-module=jupyter',
        '--exclude-module=notebook', 
        '--exclude-module=IPython',
        '--exclude-module=sphinx',
        '--exclude-module=pytest',
        '--exclude-module=setuptools',
    ]
    return exclusoes

def criar_executavel():
    """Cria o executável principal"""
    print("🔨 Criando executável...")
    
    # Limpar builds anteriores
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Criar arquivo spec
    criar_spec_file()
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'dd-ai.spec'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável criado com sucesso!")
            print("📁 Localização: dist/DD-AI-Backend.exe")
            return True
        else:
            print("❌ Erro ao criar executável:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante build: {str(e)}")
        return False

def criar_launcher():
    """Cria launcher simples para o executável"""
    launcher_content = '''@echo off
chcp 65001 >nul
echo.
echo 🚀 DD-AI STANDALONE - EXECUTÁVEL WINDOWS
echo ========================================
echo.

echo ✅ Iniciando Advanced DD-AI v2.1...
echo.
echo 🔧 Backend: http://localhost:8001
echo 📊 Docs API: http://localhost:8001/docs
echo.
echo 💡 Para interface web, execute: frontend\\npm run dev
echo 🌐 Acesse: http://localhost:3000
echo.
echo 🛑 Para parar: Ctrl+C
echo.

DD-AI-Backend.exe

pause
'''
    
    with open('dist/Executar-DD-AI.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Launcher criado: dist/Executar-DD-AI.bat")

def criar_instalador_portatil():
    """Cria versão portátil com Python embarcado"""
    print("📦 Criando versão portátil...")
    
    portatil_dir = Path("dist/DD-AI-Portatil")
    portatil_dir.mkdir(exist_ok=True)
    
    # Copiar arquivos essenciais
    arquivos_copiar = [
        'sql_api.py',
        'advanced_financial_bert.py', 
        'enhanced_news_monitor.py',
        'requirements-standalone.txt',
        'LEIA-ME.md'
    ]
    
    for arquivo in arquivos_copiar:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, portatil_dir)
    
    # Criar script de execução portátil
    script_portatil = '''@echo off
chcp 65001 >nul
echo.
echo 🚀 DD-AI PORTÁTIL - Windows 11 64-bit
echo ====================================
echo.

:: Verificar se Python está disponível
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado no sistema!
    echo.
    echo 📥 OPÇÕES:
    echo    1. Instalar Python: https://python.org/downloads
    echo    2. Usar versão executável: DD-AI-Backend.exe
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado - iniciando DD-AI...
echo.

:: Instalar dependências se necessário
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    call venv\\Scripts\\activate.bat
    pip install -r requirements-standalone.txt
) else (
    call venv\\Scripts\\activate.bat
)

echo 🚀 Iniciando servidor...
python sql_api.py

pause
'''
    
    with open(portatil_dir / 'Executar-Portatil.bat', 'w', encoding='utf-8') as f:
        f.write(script_portatil)
    
    print("✅ Versão portátil criada: dist/DD-AI-Portatil/")

def main():
    """Função principal"""
    print("🚀 CRIADOR DE EXECUTÁVEL DD-AI v2.1")
    print("=" * 40)
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('sql_api.py'):
        print("❌ sql_api.py não encontrado!")
        print("💡 Execute este script no diretório DD-AI-Standalone")
        return False
    
    # Instalar PyInstaller
    if not instalar_pyinstaller():
        return False
    
    print("\n🎯 OPÇÕES DE BUILD:")
    print("1. 📦 Executável único (recomendado)")
    print("2. 🔧 Versão portátil com Python")
    print("3. 🚀 Ambas as versões")
    
    escolha = input("\nEscolha (1-3): ").strip()
    
    sucesso = True
    
    if escolha in ['1', '3']:
        print("\n" + "="*50)
        print("📦 CRIANDO EXECUTÁVEL ÚNICO")
        print("="*50)
        
        if criar_executavel():
            criar_launcher()
            print("✅ Executável criado com sucesso!")
        else:
            sucesso = False
    
    if escolha in ['2', '3']:
        print("\n" + "="*50)
        print("🔧 CRIANDO VERSÃO PORTÁTIL")
        print("="*50)
        
        criar_instalador_portatil()
    
    if sucesso:
        print("\n🎉 BUILD CONCLUÍDO!")
        print("\n📁 Arquivos gerados em: dist/")
        print("\n🚀 Para distribuir:")
        print("   • Executável: dist/DD-AI-Backend.exe + Executar-DD-AI.bat")
        print("   • Portátil: dist/DD-AI-Portatil/ (pasta completa)")
        print("\n💡 REQUISITOS NA MÁQUINA FINAL:")
        print("   • Windows 11 64-bit")
        print("   • Conexão com internet (para APIs)")
        print("   • 4GB+ RAM (para modelo IA)")
        
    return sucesso

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
