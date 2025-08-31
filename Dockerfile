# Advanced DD-AI v2.1 - Standalone Docker
# =======================================

FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js para frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Criar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements-standalone.txt .
RUN pip install --no-cache-dir -r requirements-standalone.txt

# Copiar código backend
COPY *.py ./

# Copiar frontend
COPY frontend/ ./frontend/

# Instalar dependências frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Voltar para diretório principal
WORKDIR /app

# Expor portas
EXPOSE 8001 3000

# Criar script de inicialização
RUN echo '#!/bin/bash\n\
# Iniciar backend em segundo plano\n\
python sql_api.py &\n\
\n\
# Aguardar backend\n\
sleep 5\n\
\n\
# Iniciar frontend\n\
cd frontend && npm run preview &\n\
\n\
# Manter container rodando\n\
wait' > start.sh && chmod +x start.sh

# Comando padrão
CMD ["./start.sh"]

# Labels para metadados
LABEL name="dd-ai-standalone"
LABEL version="2.1"
LABEL description="Advanced Due Diligence AI - Standalone"
