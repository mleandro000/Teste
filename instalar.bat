@echo off
chcp 65001 >nul
echo.
echo 🚀 DD-AI STANDALONE - INSTALADOR AUTOMÁTICO
echo =============================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 Por favor, instale Python 3.8+ de: https://python.org/downloads
    echo    ✅ Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado:
python --version

:: Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado!
    echo.
    echo 📥 Por favor, instale Node.js de: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js encontrado:
node --version

echo.
echo 📦 Instalando dependências do backend...
echo.

:: Instalar dependências Python
pip install -r requirements-standalone.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências Python
    pause
    exit /b 1
)

echo.
echo ✅ Backend instalado com sucesso!
echo.
echo 📦 Instalando dependências do frontend...
echo.

:: Navegar para frontend e instalar
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências Node.js
    pause
    exit /b 1
)

cd ..

echo.
echo ✅ Frontend instalado com sucesso!
echo.
echo 🎯 INSTALAÇÃO CONCLUÍDA!
echo.
echo 🚀 Para executar o sistema:
echo    👉 Execute: executar.bat
echo.
echo 📋 Ou execute manualmente:
echo    1. Backend: python sql_api.py
echo    2. Frontend: cd frontend && npm run dev
echo.
echo 🌐 Acesse: http://localhost:3000
echo.
pause
