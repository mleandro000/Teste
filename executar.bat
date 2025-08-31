@echo off
chcp 65001 >nul
echo.
echo 🚀 DD-AI STANDALONE - EXECUÇÃO AUTOMÁTICA
echo ==========================================
echo.

:: Verificar se as dependências estão instaladas
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Dependências não instaladas!
    echo 💡 Execute primeiro: instalar.bat
    pause
    exit /b 1
)

echo ✅ Dependências verificadas
echo.
echo 🚀 Iniciando Advanced DD-AI v2.1...
echo.

:: Matar processos existentes (se houver)
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

echo 🔧 Limpando processos anteriores...
timeout /t 2 /nobreak >nul

:: Iniciar backend em segundo plano
echo 🐍 Iniciando backend (Python)...
start /b python sql_api.py

:: Aguardar backend inicializar
echo ⏳ Aguardando backend inicializar...
timeout /t 5 /nobreak >nul

:: Testar se backend está rodando
curl -s http://127.0.0.1:8001/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend não iniciou corretamente
    echo 💡 Verifique se a porta 8001 está livre
    pause
    exit /b 1
)

echo ✅ Backend funcionando
echo.

:: Iniciar frontend
echo 🌐 Iniciando frontend (React)...
cd frontend
start /b npm run dev

echo ⏳ Aguardando frontend inicializar...
timeout /t 8 /nobreak >nul

echo.
echo 🎉 SISTEMA INICIADO COM SUCESSO!
echo.
echo 🌐 Acesse: http://localhost:3000
echo 🔧 API Backend: http://localhost:8001
echo 📊 Documentação: http://localhost:8001/docs
echo.
echo 📋 Funcionalidades disponíveis:
echo    ✅ Análise de risco por CNPJ
echo    ✅ Monitoramento de notícias
echo    ✅ Compliance CVM/BACEN
echo    ✅ Relatórios automatizados
echo.
echo 🛑 Para parar: Ctrl+C ou feche esta janela
echo.

:: Abrir navegador automaticamente
start http://localhost:3000

echo 💡 Sistema rodando em segundo plano...
echo 📊 Monitore os logs para acompanhar o funcionamento
echo.
pause
