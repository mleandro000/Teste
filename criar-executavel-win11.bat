@echo off
chcp 65001 >nul
title DD-AI - Criador de Executável Windows 11
color 0B

echo.
echo 🔨 DD-AI STANDALONE - GERADOR DE EXECUTÁVEL
echo ==========================================
echo 🎯 Criando versão standalone para Windows 11 64-bit
echo.

:: Verificar se estamos no diretório correto
if not exist "sql_api.py" (
    echo ❌ Arquivo sql_api.py não encontrado!
    echo 💡 Execute este script no diretório DD-AI-Standalone
    pause
    exit /b 1
)

echo ✅ Arquivos principais encontrados
echo.

:: Verificar PyInstaller
echo 📦 Verificando PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller disponível
echo.

:: Limpar builds anteriores
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo 🎯 OPÇÕES DE BUILD:
echo.
echo [1] 📦 Executável único (1 arquivo, ~200MB)
echo [2] 🗂️  Executável + arquivos (pasta, ~150MB) 
echo [3] 🔧 Versão desenvolvimento (com console)
echo [4] 🚀 Todas as versões
echo.

set /p "opcao=Escolha uma opção (1-4): "

if "%opcao%"=="1" goto :build_onefile
if "%opcao%"=="2" goto :build_onedir
if "%opcao%"=="3" goto :build_dev
if "%opcao%"=="4" goto :build_all
echo ❌ Opção inválida
pause
exit /b 1

:build_onefile
echo.
echo 📦 CRIANDO EXECUTÁVEL ÚNICO...
echo.
pyinstaller --onefile --windowed --name "DD-AI-Backend" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    --exclude-module matplotlib ^
    --exclude-module jupyter ^
    sql_api.py

goto :create_launcher

:build_onedir
echo.
echo 🗂️  CRIANDO EXECUTÁVEL + ARQUIVOS...
echo.
pyinstaller --onedir --windowed --name "DD-AI-Backend" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    --exclude-module matplotlib ^
    --exclude-module jupyter ^
    sql_api.py

goto :create_launcher

:build_dev
echo.
echo 🔧 CRIANDO VERSÃO DESENVOLVIMENTO...
echo.
pyinstaller --onefile --console --name "DD-AI-Backend-Dev" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    sql_api.py

goto :create_launcher

:build_all
echo.
echo 🚀 CRIANDO TODAS AS VERSÕES...
echo.

echo [1/3] Executável único...
pyinstaller --onefile --windowed --name "DD-AI-Backend" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    --exclude-module matplotlib ^
    --exclude-module jupyter ^
    sql_api.py

echo [2/3] Executável + arquivos...
pyinstaller --onedir --windowed --name "DD-AI-Backend-Dir" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    --exclude-module matplotlib ^
    --exclude-module jupyter ^
    sql_api.py

echo [3/3] Versão desenvolvimento...
pyinstaller --onefile --console --name "DD-AI-Backend-Dev" ^
    --add-data "advanced_financial_bert.py;." ^
    --add-data "enhanced_news_monitor.py;." ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    sql_api.py

goto :create_launcher

:create_launcher
echo.
echo 🔗 Criando scripts de execução...

:: Launcher principal
echo @echo off > "dist\Executar-DD-AI.bat"
echo chcp 65001 ^>nul >> "dist\Executar-DD-AI.bat"
echo title DD-AI v2.1 - Advanced Due Diligence AI >> "dist\Executar-DD-AI.bat"
echo color 0A >> "dist\Executar-DD-AI.bat"
echo. >> "dist\Executar-DD-AI.bat"
echo echo 🚀 DD-AI v2.1 - INICIANDO... >> "dist\Executar-DD-AI.bat"
echo echo ============================= >> "dist\Executar-DD-AI.bat"
echo echo. >> "dist\Executar-DD-AI.bat"
echo echo ✅ Backend: http://localhost:8001 >> "dist\Executar-DD-AI.bat"
echo echo 📊 API Docs: http://localhost:8001/docs >> "dist\Executar-DD-AI.bat"
echo echo 🌐 Frontend: Execute npm run dev na pasta frontend >> "dist\Executar-DD-AI.bat"
echo echo. >> "dist\Executar-DD-AI.bat"
echo echo 🛑 Para parar: Ctrl+C >> "dist\Executar-DD-AI.bat"
echo echo. >> "dist\Executar-DD-AI.bat"
echo if exist "DD-AI-Backend.exe" ( >> "dist\Executar-DD-AI.bat"
echo     DD-AI-Backend.exe >> "dist\Executar-DD-AI.bat"
echo ^) else if exist "DD-AI-Backend-Dir\DD-AI-Backend-Dir.exe" ( >> "dist\Executar-DD-AI.bat"
echo     DD-AI-Backend-Dir\DD-AI-Backend-Dir.exe >> "dist\Executar-DD-AI.bat"
echo ^) else ( >> "dist\Executar-DD-AI.bat"
echo     echo ❌ Executável não encontrado >> "dist\Executar-DD-AI.bat"
echo     pause >> "dist\Executar-DD-AI.bat"
echo ^) >> "dist\Executar-DD-AI.bat"

:: Copiar frontend se existir
if exist "frontend" (
    echo 📁 Copiando frontend...
    xcopy "frontend" "dist\frontend" /E /I /Q >nul
)

:: Copiar documentação
echo 📄 Copiando documentação...
if exist "LEIA-ME.md" copy "LEIA-ME.md" "dist\" >nul
if exist "PROJECT_OVERVIEW.md" copy "PROJECT_OVERVIEW.md" "dist\" >nul
if exist "apresentacao_dd_ai.html" copy "apresentacao_dd_ai.html" "dist\" >nul

:: Criar README para distribuição
echo # 🚀 DD-AI v2.1 - Versão Executável > "dist\README-EXECUTAVEL.txt"
echo. >> "dist\README-EXECUTAVEL.txt"
echo INSTALAÇÃO: >> "dist\README-EXECUTAVEL.txt"
echo 1. Extrair todos os arquivos >> "dist\README-EXECUTAVEL.txt"
echo 2. Executar: Executar-DD-AI.bat >> "dist\README-EXECUTAVEL.txt"
echo. >> "dist\README-EXECUTAVEL.txt"
echo REQUISITOS: >> "dist\README-EXECUTAVEL.txt"
echo - Windows 11 64-bit >> "dist\README-EXECUTAVEL.txt"
echo - 4GB+ RAM >> "dist\README-EXECUTAVEL.txt"
echo - Conexão com internet >> "dist\README-EXECUTAVEL.txt"
echo. >> "dist\README-EXECUTAVEL.txt"
echo PORTAS UTILIZADAS: >> "dist\README-EXECUTAVEL.txt"
echo - Backend: 8001 >> "dist\README-EXECUTAVEL.txt"
echo - Frontend: 3000 >> "dist\README-EXECUTAVEL.txt"

echo.
echo ✅ Build concluído!
echo.

:: Verificar arquivos criados
echo 📊 ARQUIVOS GERADOS:
echo.
if exist "dist\DD-AI-Backend.exe" (
    for %%I in ("dist\DD-AI-Backend.exe") do echo ✅ Executável único: %%~zI bytes
)
if exist "dist\DD-AI-Backend-Dir" (
    echo ✅ Versão com arquivos: dist\DD-AI-Backend-Dir\
)
if exist "dist\DD-AI-Backend-Dev.exe" (
    for %%I in ("dist\DD-AI-Backend-Dev.exe") do echo ✅ Versão dev: %%~zI bytes
)

echo.
echo 🎯 COMO DISTRIBUIR:
echo.
echo 📦 Para usuário final:
echo    1. Compactar pasta 'dist' inteira
echo    2. Usuário executa: Executar-DD-AI.bat
echo    3. Não precisa Python instalado!
echo.
echo 💡 TESTANDO:
echo    👉 cd dist
echo    👉 Executar-DD-AI.bat
echo.

:: Oferecer para testar
set /p "testar=🧪 Testar agora? (s/n): "
if /i "%testar%"=="s" (
    cd dist
    echo 🚀 Iniciando teste...
    start Executar-DD-AI.bat
)

echo.
echo 🎉 PROCESSO CONCLUÍDO!
echo 📁 Todos os arquivos estão em: dist\
echo.
pause
