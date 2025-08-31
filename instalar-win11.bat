@echo off
chcp 65001 >nul
title DD-AI Standalone - Instalador Windows 11
color 0A

echo.
echo ██████╗ ██████╗       █████╗ ██╗    ██╗██╗███╗   ██╗██╗   ██╗
echo ██╔══██╗██╔══██╗     ██╔══██╗██║    ██║██║████╗  ██║╚██╗ ██╔╝
echo ██║  ██║██║  ██║     ███████║██║ █╗ ██║██║██╔██╗ ██║ ╚████╔╝ 
echo ██║  ██║██║  ██║     ██╔══██║██║███╗██║██║██║╚██╗██║  ╚██╔╝  
echo ██████╔╝██████╔╝     ██║  ██║╚███╔███╔╝██║██║ ╚████║   ██║   
echo ╚═════╝ ╚═════╝      ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   
echo.
echo 🚀 ADVANCED DD-AI v2.1 - INSTALADOR WINDOWS 11 64-BIT
echo =====================================================
echo 🇧🇷 Sistema de Análise de Risco Financeiro Brasileiro
echo.

:: Verificar se é Windows 11
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo 🖥️  Sistema detectado: Windows %VERSION%

:: Verificar arquitetura
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ Arquitetura: 64-bit
) else (
    echo ❌ Erro: Requer Windows 64-bit
    pause
    exit /b 1
)

echo.
echo 📋 VERIFICANDO PRÉ-REQUISITOS...
echo.

:: Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 INSTALAÇÃO AUTOMÁTICA DO PYTHON:
    echo    Baixando Python 3.11 para Windows 11...
    
    :: Baixar Python automaticamente
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}"
    
    if exist "python-installer.exe" (
        echo ✅ Download concluído, instalando...
        start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del python-installer.exe
        
        :: Verificar novamente
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ Instalação do Python falhou
            echo 💡 Instale manualmente: https://python.org/downloads
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Falha no download do Python
        echo 💡 Verifique sua conexão com internet
        pause
        exit /b 1
    )
)

python --version
echo ✅ Python OK

:: Verificar Node.js
echo.
echo [2/4] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado!
    echo.
    echo 📥 INSTALAÇÃO AUTOMÁTICA DO NODE.JS:
    echo    Baixando Node.js LTS para Windows 11...
    
    :: Baixar Node.js
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nodejs.org/dist/v18.19.0/node-v18.19.0-x64.msi' -OutFile 'nodejs-installer.msi'}"
    
    if exist "nodejs-installer.msi" (
        echo ✅ Download concluído, instalando...
        start /wait msiexec /i nodejs-installer.msi /quiet
        del nodejs-installer.msi
        
        :: Atualizar PATH
        call refreshenv >nul 2>&1
        
        :: Verificar novamente
        node --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ Instalação do Node.js falhou
            echo 💡 Instale manualmente: https://nodejs.org
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Falha no download do Node.js
        pause
        exit /b 1
    )
)

node --version
echo ✅ Node.js OK

:: Verificar conectividade
echo.
echo [3/4] Testando conectividade...
ping -n 1 google.com >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Sem conexão com internet
    echo 💡 Verifique sua conexão
    pause
    exit /b 1
)
echo ✅ Internet OK

:: Verificar espaço em disco
echo.
echo [4/4] Verificando espaço em disco...
for /f "tokens=3" %%a in ('dir /-c %SystemDrive%\ ^| find "bytes free"') do set freespace=%%a
echo ✅ Espaço disponível verificado

echo.
echo 🎯 PRÉ-REQUISITOS ATENDIDOS!
echo.
echo 📦 INSTALANDO DEPENDÊNCIAS...
echo.

:: Atualizar pip
echo ⬆️  Atualizando pip...
python -m pip install --upgrade pip

:: Instalar dependências Python
echo 📊 Instalando dependências de IA e análise...
pip install -r requirements-standalone.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências Python
    echo 💡 Verifique o arquivo requirements-standalone.txt
    pause
    exit /b 1
)

echo ✅ Dependências Python instaladas

:: Instalar dependências do frontend
echo.
echo 🌐 Instalando dependências do frontend...
cd frontend
npm install --silent
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências Node.js
    pause
    exit /b 1
)

echo ✅ Dependências frontend instaladas

:: Voltar ao diretório principal
cd ..

:: Testar instalação
echo.
echo 🧪 TESTANDO INSTALAÇÃO...
echo.

:: Teste rápido do backend
echo 🐍 Testando backend...
timeout /t 2 /nobreak >nul
python -c "import fastapi, torch, transformers; print('✅ Imports OK')"
if %errorlevel% neq 0 (
    echo ❌ Erro nos imports do Python
    pause
    exit /b 1
)

:: Teste do frontend
echo 🌐 Testando frontend...
cd frontend
npm run build >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Erro no build do frontend
    pause
    exit /b 1
)
cd ..

echo.
echo 🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo.
echo 📋 SISTEMA INSTALADO:
echo    ✅ Backend: Python + FastAPI + IA
echo    ✅ Frontend: React + TypeScript
echo    ✅ Dependências: Todas as bibliotecas
echo    ✅ Modelos IA: FinBERT-PT-BR + QLoRA
echo.
echo 🚀 COMO USAR:
echo    👉 Execute: executar.bat
echo    🌐 Acesse: http://localhost:3000
echo    🔧 API: http://localhost:8001
echo.
echo 💡 FUNCIONALIDADES:
echo    📊 Análise de risco por CNPJ
echo    📰 Monitoramento de notícias
echo    🛡️ Compliance CVM/BACEN
echo    📋 Relatórios automatizados
echo.
echo ⚡ PERFORMANCE ESPERADA:
echo    🧠 IA: ~300ms por análise
echo    📊 Enriquecimento: ~500ms por CNPJ
echo    💾 RAM: 2-4GB (modelo carregado)
echo.

:: Criar atalho na área de trabalho
echo 🔗 Criando atalho na área de trabalho...
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\DD-AI v2.1.lnk"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%CD%\executar.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Advanced DD-AI v2.1 - Análise de Risco Financeiro'; $Shortcut.Save()}"

if exist "%shortcut%" (
    echo ✅ Atalho criado na área de trabalho
) else (
    echo ⚠️ Não foi possível criar atalho
)

echo.
echo 🎯 PRONTO PARA USO!
echo.
echo 📞 SUPORTE:
echo    📖 Documentação: LEIA-ME.md
echo    🌐 Apresentação: apresentacao_dd_ai.html
echo    📊 Overview: PROJECT_OVERVIEW.md
echo.

pause
