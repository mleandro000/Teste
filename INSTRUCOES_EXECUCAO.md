# 🚀 INSTRUÇÕES PARA EXECUTAR O DD-AI v3.0.0

## ⚠️ **PROBLEMAS IDENTIFICADOS:**

### **1️⃣ Backend - Erro PyTorch:**
```
ImportError: cannot import name 'LoRAConfig' from 'peft'
```
**Solução**: Precisamos corrigir a importação no arquivo `advanced_financial_bert.py`

### **2️⃣ Frontend - Build Cancelado:**
```
X [ERROR] The build was canceled
```
**Solução**: Limpar cache e reinstalar dependências

---

## 🔧 **PASSOS PARA CORRIGIR E EXECUTAR:**

### **PASSO 1: Corrigir Backend**
```bash
# 1. Ativar ambiente virtual
& "venv/Scripts/Activate.ps1"

# 2. Navegar para o diretório
cd DD-AI-Standalone

# 3. Corrigir importação (vou fazer isso agora)
# 4. Testar backend
python sql_api.py
```

### **PASSO 2: Corrigir Frontend**
```bash
# 1. Navegar para frontend
cd frontend_react

# 2. Limpar cache
npm cache clean --force

# 3. Remover node_modules
Remove-Item -Recurse -Force node_modules

# 4. Reinstalar dependências
npm install

# 5. Iniciar servidor
npm run dev
```

### **PASSO 3: Testar Sistema**
```bash
# 1. Testar backend
curl http://127.0.0.1:8001/

# 2. Testar frontend
curl http://127.0.0.1:3000/

# 3. Abrir no navegador
Start-Process "http://localhost:3000"
```

---

## 🎯 **EXECUÇÃO RÁPIDA (COMANDOS PRONTOS):**

### **Terminal 1 - Backend:**
```powershell
# Ativar ambiente e iniciar backend
& "venv/Scripts/Activate.ps1"
cd DD-AI-Standalone
python sql_api.py
```

### **Terminal 2 - Frontend:**
```powershell
# Iniciar frontend
cd frontend_react
npm run dev
```

### **Terminal 3 - Testes:**
```powershell
# Testar sistema
curl http://127.0.0.1:8001/
curl http://127.0.0.1:3000/
```

---

## 📋 **CHECKLIST DE VERIFICAÇÃO:**

### ✅ **Backend (Porta 8001):**
- [ ] Ambiente virtual ativado
- [ ] Importações corrigidas
- [ ] Servidor rodando
- [ ] API respondendo

### ✅ **Frontend (Porta 3000):**
- [ ] Dependências instaladas
- [ ] Cache limpo
- [ ] Servidor Vite rodando
- [ ] Interface carregando

### ✅ **Sistema Inteligente:**
- [ ] Detecção de CNPJs funcionando
- [ ] Análise de risco operacional
- [ ] API Brasil integrada
- [ ] Relatórios gerados

---

## 🚨 **SOLUÇÕES PARA PROBLEMAS COMUNS:**

### **Erro PyTorch:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### **Erro PEFT:**
```bash
pip uninstall peft
pip install peft==0.7.0
```

### **Erro Frontend:**
```bash
npm cache clean --force
Remove-Item -Recurse -Force node_modules
npm install
```

### **Porta Ocupada:**
```bash
# Verificar portas
netstat -an | findstr ":8001\|:3000"

# Matar processos
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*"} | Stop-Process -Force
```

---

## 🎉 **RESULTADO ESPERADO:**

### **Backend Funcionando:**
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### **Frontend Funcionando:**
```
VITE v4.5.14  ready in 375 ms
➜  Local:   http://127.0.0.1:3000/
```

### **Teste de Conectividade:**
```json
{
  "message": "DD-AI SQL Server API",
  "status": "running",
  "version": "3.0.0"
}
```

---

## 🔗 **URLS IMPORTANTES:**

- **Backend API**: http://127.0.0.1:8001
- **Frontend**: http://127.0.0.1:3000
- **Documentação API**: http://127.0.0.1:8001/docs
- **Teste de Conexão**: http://127.0.0.1:8001/api/test-connection

---

**🚀 Sistema DD-AI v3.0.0 - Advanced Financial Risk Assessment**  
**📅 Última Atualização**: 31/08/2025  
**🎯 Objetivo**: Análise inteligente de risco financeiro com dados reais do SQL Server
