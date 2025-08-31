# 🔧 Backend - DD-AI System

API FastAPI para análise de riscos financeiros com IA avançada.

## 📁 Estrutura

```
backend/
├── sql_api.py                    # API principal
├── advanced_financial_bert.py    # Modelo de IA
├── test_backend_simple.py        # Testes de conectividade
├── sql_to_analysis.py           # Script de análise completa
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

## 🚀 Instalação

### 1. Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar
```bash
python sql_api.py
```

## 🌐 Endpoints

### Básicos
- `GET /` - Teste de conectividade
- `POST /api/test-connection` - Teste conexão SQL
- `POST /api/execute-query` - Executar query SQL
- `POST /api/tables` - Listar tabelas

### Avançados (IA)
- `POST /api/analyze-risk` - Análise de risco
- `POST /api/analyze-sql-data` - Query + Análise IA
- `POST /api/sql-to-analysis` - Análise completa ⭐
- `GET /api/model-info` - Informações do modelo

## 🧪 Testes

### Teste de Conectividade
```bash
python test_backend_simple.py
```

### Teste Manual
```bash
# Teste básico
curl http://localhost:8001/

# Teste de conexão SQL
curl -X POST http://localhost:8001/api/test-connection \
  -H "Content-Type: application/json" \
  -d '{
    "server": "DESKTOP-T9HKFSQ\\SQLEXPRESS",
    "database": "Projeto_Dev",
    "use_windows_auth": true
  }'
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
SQL_SERVER=DESKTOP-T9HKFSQ\SQLEXPRESS
SQL_DATABASE=Projeto_Dev
API_PORT=8001
```

### Conexão SQL Server
- **Driver:** ODBC Driver 17 for SQL Server
- **Autenticação:** Windows Authentication
- **Porta:** 1433 (padrão)

## 📊 Exemplo de Uso

### Análise Completa
```python
import requests

# Dados de conexão
connection_data = {
    "server": "DESKTOP-T9HKFSQ\\SQLEXPRESS",
    "database": "Projeto_Dev",
    "use_windows_auth": True
}

# Query para análise
query_data = {
    "connection": connection_data,
    "query": "SELECT TOP 5 CNPJ, RazaoSocial FROM Empresas"
}

# Executar análise
response = requests.post(
    "http://localhost:8001/api/sql-to-analysis",
    json=query_data
)

print(response.json())
```

## 🧠 Modelo de IA

### FinBERT-PT-BR
- **Base:** neuralmind/bert-base-portuguese-cased
- **Fine-tuning:** QLoRA para eficiência
- **Tarefa:** Classificação de riscos financeiros

### Classes de Risco
- **Baixo:** 0-25%
- **Moderado:** 26-50%
- **Alto:** 51-75%
- **Crítico:** 76-100%

## 🔒 Segurança

- Validação de dados com Pydantic
- Sanitização de queries SQL
- CORS configurado
- Autenticação Windows

## 📝 Logs

O sistema gera logs detalhados para:
- Conexões SQL
- Execução de queries
- Análises de IA
- Erros e exceções

## 🐛 Troubleshooting

### Erro de Conexão SQL
1. Verificar se o SQL Server está rodando
2. Confirmar credenciais Windows
3. Testar driver ODBC

### Erro de IA
1. Verificar dependências PyTorch
2. Confirmar modelo carregado
3. Verificar memória disponível

### Erro de Porta
1. Verificar se porta 8001 está livre
2. Parar processos conflitantes
3. Alterar porta se necessário
