# Script para configurar repositório GitHub para DD-AI System
# Execute este script no diretório raiz do projeto

Write-Host "🚀 Configurando repositório GitHub para DD-AI System" -ForegroundColor Green
Write-Host "=" * 60

# Verificar se Git está instalado
try {
    git --version | Out-Null
    Write-Host "✅ Git encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não encontrado. Instale o Git primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend_github")) {
    Write-Host "❌ Execute este script no diretório raiz do projeto DD-AI-Standalone" -ForegroundColor Red
    exit 1
}

# Inicializar repositório Git
Write-Host "📁 Inicializando repositório Git..." -ForegroundColor Yellow
git init

# Adicionar arquivos
Write-Host "📝 Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Commit inicial
Write-Host "💾 Fazendo commit inicial..." -ForegroundColor Yellow
git commit -m "🎉 Initial commit: DD-AI System v3.0.0

- Backend FastAPI com IA avançada
- Frontend React com interface integrada
- Modelo FinBERT-PT-BR para análise de riscos
- Integração com SQL Server e API Brasil
- Documentação completa"

Write-Host "✅ Repositório local configurado!" -ForegroundColor Green

# Instruções para GitHub
Write-Host ""
Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Crie um novo repositório no GitHub:" -ForegroundColor White
Write-Host "   - Vá para https://github.com/new" -ForegroundColor White
Write-Host "   - Nome: dd-ai-system" -ForegroundColor White
Write-Host "   - Descrição: Sistema de Due Diligence com IA Avançada" -ForegroundColor White
Write-Host "   - Público ou Privado (sua escolha)" -ForegroundColor White
Write-Host "   - NÃO inicialize com README (já temos um)" -ForegroundColor White
Write-Host ""
Write-Host "2. Conecte o repositório local ao GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/SEU-USUARIO/dd-ai-system.git" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Faça push para o GitHub:" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Configure GitHub Pages (opcional):" -ForegroundColor White
Write-Host "   - Vá para Settings > Pages" -ForegroundColor White
Write-Host "   - Source: Deploy from a branch" -ForegroundColor White
Write-Host "   - Branch: main, folder: /docs" -ForegroundColor White
Write-Host ""

# Verificar estrutura
Write-Host "📁 Estrutura do projeto:" -ForegroundColor Cyan
Get-ChildItem -Directory | ForEach-Object {
    Write-Host "   📂 $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "📄 Arquivos principais:" -ForegroundColor Cyan
Get-ChildItem -File | Where-Object { $_.Name -match "\.(md|txt|py|json)$" } | ForEach-Object {
    Write-Host "   📄 $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 Configuração concluída! Siga os próximos passos acima." -ForegroundColor Green
