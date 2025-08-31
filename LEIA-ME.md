# 🚀 DD-AI Standalone - Advanced Due Diligence AI

## 📋 Visão Geral

Esta é a versão **standalone** do Advanced DD-AI v2.1, contendo apenas os arquivos essenciais para funcionamento completo do sistema de análise de risco financeiro.

## 📁 Estrutura do Projeto

```
DD-AI-Standalone/
├── 🐍 Backend (Python)
│   ├── sql_api.py                     # API principal FastAPI
│   ├── advanced_financial_bert.py     # Motor de IA
│   ├── enhanced_news_monitor.py       # Monitor de notícias
│   └── requirements.txt               # Dependências Python
├── 🌐 Frontend (React)
│   ├── src/                          # Código fonte React
│   ├── package.json                  # Dependências Node.js
│   ├── vite.config.ts               # Configuração build
│   └── index.html                   # Página principal
├── 📊 Documentação
│   ├── LEIA-ME.md                    # Este arquivo
│   ├── PROJECT_OVERVIEW.md           # Visão geral técnica
│   └── apresentacao_dd_ai.html       # Apresentação interativa
└── 🚀 Scripts de Execução
    ├── instalar.bat                  # Instalação automática
    ├── executar.bat                  # Execução rápida
    └── requirements-standalone.txt   # Dependências mínimas
```

## 🎯 O que Este Projeto Faz

### ✅ **Funcionalidades Principais**
1. **🔍 Análise de Risco por CNPJ**: Enriquecimento via API Brasil + Análise IA
2. **📰 Monitoramento de Notícias**: Busca e análise automática de notícias
3. **🧠 Inteligência Artificial**: FinBERT-PT-BR com otimização QLoRA
4. **📊 Relatórios Avançados**: Scores de risco e recomendações
5. **🛡️ Compliance**: Verificação CVM/BACEN automática

### 🎯 **Casos de Uso**
- **Due Diligence Empresarial**: Análise de contrapartes e fornecedores
- **Compliance Financeiro**: Monitoramento de transações e alertas
- **Gestão de Risco**: Avaliação contínua de exposições
- **Auditoria**: Identificação de anomalias e red flags

## 🔧 Como Instalar e Executar

### 📋 **Pré-requisitos**
- Windows 10/11
- Conexão com internet
- SQL Server (opcional, para funcionalidades avançadas)

### 🚀 **Opção 1: Instalação Automática (Recomendada)**
```bash
# 1. Execute o instalador
instalar.bat

# 2. Execute o sistema
executar.bat
```

### 🛠️ **Opção 2: Instalação Manual**
```bash
# 1. Instalar Python 3.8+ (se não tiver)
# Baixar de: https://python.org/downloads

# 2. Instalar dependências do backend
pip install -r requirements.txt

# 3. Instalar Node.js (se não tiver)
# Baixar de: https://nodejs.org

# 4. Instalar dependências do frontend
cd frontend
npm install

# 5. Executar backend
python sql_api.py

# 6. Executar frontend (nova janela)
cd frontend
npm run dev
```

## 🌟 **Opções para Executar SEM Python Instalado**

### 1. **🐳 Docker (Recomendado)**
```bash
# Criar Dockerfile personalizado
docker build -t dd-ai-standalone .
docker run -p 8001:8001 -p 3000:3000 dd-ai-standalone
```

### 2. **📦 PyInstaller (Executável)**
```bash
# Gerar executável Windows
pip install pyinstaller
pyinstaller --onefile --windowed sql_api.py
```

### 3. **☁️ Portable Python**
- Baixar Python portable
- Incluir no pacote do projeto
- Executar via batch script

### 4. **🌐 Versão Web**
- Deploy na nuvem (Heroku, AWS, Azure)
- Acesso via navegador apenas
- Zero instalação local

## ⚡ Execução Rápida

### 🎯 **Teste Básico (5 minutos)**
```python
# 1. Executar backend
python sql_api.py

# 2. Testar API (outro terminal)
curl http://localhost:8001/api/health

# 3. Análise de CNPJ
python enhanced_news_monitor.py
```

### 📊 **Teste Completo (15 minutos)**
```bash
# 1. Backend + Frontend
executar.bat

# 2. Acessar http://localhost:3000
# 3. Testar conexão SQL Server
# 4. Executar análise de risco
```

## 🏆 Performance Esperada

| Métrica | Valor | Descrição |
|---------|--------|-----------|
| **Latência IA** | ~300ms | Análise de risco por texto |
| **Enriquecimento** | ~500ms | API Brasil + processamento |
| **Notícias** | ~2-5s | Busca + análise por empresa |
| **Memória** | ~2-4GB | Com modelo IA carregado |
| **CPU** | Médio | Otimização QLoRA ativa |

## 🛡️ Segurança e Compliance

### ✅ **Conformidade**
- **CVM**: Regulamentações de valores mobiliários
- **BACEN**: Normas do Banco Central
- **LGPD**: Proteção de dados pessoais
- **ESG**: Critérios ambientais e sociais

### 🔒 **Segurança**
- Conexões HTTPS obrigatórias
- Validação de inputs
- Rate limiting automático
- Logs de auditoria

## 📞 Suporte e Troubleshooting

### ❓ **Problemas Comuns**

#### 1. **"Módulo não encontrado"**
```bash
# Solução: Instalar dependências
pip install -r requirements.txt
```

#### 2. **"Porta em uso"**
```bash
# Solução: Mudar porta ou matar processo
netstat -ano | findstr :8001
taskkill /PID <numero_do_processo> /F
```

#### 3. **"Modelo IA não carrega"**
```bash
# Solução: Verificar memória e internet
python test_pytorch.py
```

#### 4. **"API Brasil falha"**
```bash
# Solução: Verificar internet e CNPJ
curl "https://brasilapi.com.br/api/cnpj/v1/11222333000181"
```

### 🔧 **Logs e Diagnóstico**
```bash
# Ver logs detalhados
python sql_api.py --debug

# Testar conexões
python enhanced_news_monitor.py --test
```

## 📈 Roadmap de Funcionalidades

### ✅ **Implementado**
- [x] Análise IA com FinBERT-PT-BR
- [x] Enriquecimento via API Brasil
- [x] Interface React responsiva
- [x] Relatórios automatizados
- [x] Compliance CVM/BACEN

### 🚧 **Em Desenvolvimento**
- [ ] Executável standalone
- [ ] Cache inteligente
- [ ] Dashboard executivo
- [ ] Alertas em tempo real
- [ ] Integração WhatsApp/Email

### 🔮 **Futuro**
- [ ] Mobile app
- [ ] API marketplace
- [ ] Multi-idiomas
- [ ] Blockchain integration

## 🎓 Exemplos de Uso

### 🏢 **Análise de Empresa**
```python
from enhanced_news_monitor import EnhancedNewsMonitor

monitor = EnhancedNewsMonitor()
resultado = monitor.monitor_company_risk("05.285.819/0001-66")
print(f"Risco: {resultado['risk_assessment']['final_risk_level']}")
```

### 📰 **Monitoramento de Notícias**
```python
# Buscar notícias sobre gestora
noticias = monitor.search_google_news("XP Asset Management")
for noticia in noticias:
    print(f"- {noticia['title']}")
```

### 🧠 **Análise de Texto**
```python
import requests

texto = "Fundo registrou perdas de R$ 1 bilhão devido a derivativos"
response = requests.post("http://localhost:8001/api/analyze-risk", 
                        json={"text": texto})
print(response.json())
```

## 📄 Licença e Créditos

**Advanced DD-AI v2.1**
- Desenvolvido para o mercado financeiro brasileiro
- Powered by FinBERT-PT-BR & QLoRA
- Compliance CVM/BACEN integrado

---

🚀 **Sistema pronto para produção!**  
🇧🇷 **Feito para o Brasil**  
⚡ **Performance otimizada**  
🛡️ **Compliance total**
