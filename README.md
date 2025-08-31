# 🚀 DD-AI - Sistema de Due Diligence com IA Avançada

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descrição

Sistema avançado de Due Diligence que combina análise de dados SQL Server com IA para avaliação de riscos financeiros. Utiliza modelos BERT especializados em português brasileiro e integração com APIs externas para enriquecimento de dados.

## ✨ Funcionalidades Principais

- 🔗 **Conexão SQL Server** - Interface para conexão e consultas
- 🧠 **IA Avançada** - Modelo FinBERT-PT-BR com QLoRA
- 📊 **Análise de Riscos** - Avaliação automática de riscos financeiros
- 🔍 **Enriquecimento de Dados** - Integração com API Brasil
- 📰 **Monitoramento de Notícias** - Análise de impacto de notícias
- 🎯 **Interface Integrada** - Frontend React com análise completa
- 📈 **Relatórios Detalhados** - Exportação de análises

## 🏗️ Arquitetura

```
DD-AI/
├── backend/                 # API FastAPI
│   ├── sql_api.py          # API principal
│   ├── advanced_financial_bert.py  # Modelo IA
│   └── requirements.txt    # Dependências Python
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   └── App.tsx        # Aplicação principal
│   └── package.json       # Dependências Node.js
└── docs/                  # Documentação
```

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- SQL Server
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/dd-ai-system.git
cd dd-ai-system
```

### 2. Backend (Python)
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r backend/requirements.txt

# Executar backend
cd backend
python sql_api.py
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Como Usar

### 1. Acesse a Interface
- Frontend: http://localhost:3000
- Backend: http://localhost:8001

### 2. Configure a Conexão SQL
- Servidor: `DESKTOP-T9HKFSQ\SQLEXPRESS`
- Banco: `Projeto_Dev`
- Autenticação Windows

### 3. Execute Análise Completa
1. Vá para "Análise Integrada"
2. Execute uma query SQL
3. Clique em "🚀 Executar Análise Completa"
4. Aguarde o processamento

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Backend
SQL_SERVER=DESKTOP-T9HKFSQ\SQLEXPRESS
SQL_DATABASE=Projeto_Dev
API_PORT=8001

# Frontend
VITE_API_URL=http://localhost:8001
```

### Modelo de IA
O sistema utiliza:
- **FinBERT-PT-BR** - Modelo BERT especializado em português
- **QLoRA** - Fine-tuning eficiente
- **Análise de Riscos** - Classificação automática

## 📊 Exemplos de Uso

### Query SQL para Análise
```sql
SELECT TOP 10 
    CNPJ, 
    RazaoSocial, 
    Situacao 
FROM Empresas 
WHERE Situacao = 'ATIVA'
```

### Endpoint de Análise
```bash
curl -X POST "http://localhost:8001/api/sql-to-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "connection": {
      "server": "DESKTOP-T9HKFSQ\\SQLEXPRESS",
      "database": "Projeto_Dev"
    },
    "query": "SELECT TOP 5 CNPJ, RazaoSocial FROM Empresas"
  }'
```

## 🧪 Testes

### Teste de Conectividade
```bash
python test_backend_simple.py
```

### Teste de Endpoints
```bash
# Teste básico
curl http://localhost:8001/

# Teste de conexão SQL
curl -X POST http://localhost:8001/api/test-connection \
  -H "Content-Type: application/json" \
  -d '{"server": "DESKTOP-T9HKFSQ\\SQLEXPRESS", "database": "Projeto_Dev"}'
```

## 📈 Funcionalidades Avançadas

### 1. Análise de Riscos
- Classificação automática (Baixo/Moderado/Alto/Crítico)
- Explicações detalhadas
- Flags de compliance
- Alertas regulatórios

### 2. Enriquecimento de Dados
- API Brasil para dados de CNPJ
- Informações cadastrais
- Dados financeiros
- Histórico empresarial

### 3. Monitoramento de Notícias
- Busca automática de notícias
- Análise de sentimento
- Impacto no risco
- Alertas em tempo real

## 🔒 Segurança

- Autenticação Windows para SQL Server
- CORS configurado para desenvolvimento
- Validação de dados com Pydantic
- Sanitização de queries SQL

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

- **Issues:** [GitHub Issues](https://github.com/seu-usuario/dd-ai-system/issues)
- **Documentação:** [Wiki](https://github.com/seu-usuario/dd-ai-system/wiki)
- **Email:** seu-email@exemplo.com

## 🏆 Roadmap

- [ ] Integração com mais APIs de notícias
- [ ] Dashboard de métricas em tempo real
- [ ] Exportação para PDF/Excel
- [ ] API REST completa
- [ ] Deploy em Docker
- [ ] Testes automatizados
- [ ] CI/CD Pipeline

---

**Desenvolvido com ❤️ para análise de riscos financeiros no Brasil**
