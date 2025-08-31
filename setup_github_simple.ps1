# Script simples para configurar repositório GitHub
Write-Host "🚀 Configurando repositório GitHub para DD-AI System" -ForegroundColor Green

# Inicializar Git
git init
git add .
git commit -m "🎉 Initial commit: DD-AI System v3.0.0"

Write-Host "✅ Repositório local configurado!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Crie repositório em: https://github.com/new" -ForegroundColor White
Write-Host "2. Execute: git remote add origin https://github.com/SEU-USUARIO/dd-ai-system.git" -ForegroundColor Yellow
Write-Host "3. Execute: git branch -M main" -ForegroundColor Yellow
Write-Host "4. Execute: git push -u origin main" -ForegroundColor Yellow
