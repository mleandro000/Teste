# 🎨 Frontend - DD-AI System

Interface React moderna para análise de riscos financeiros.

## 📁 Estrutura

```
frontend/
├── src/
│   ├── components/           # Componentes React
│   │   ├── IntegratedAnalysisInterface.tsx  # Interface principal
│   │   ├── ConnectionManager.tsx            # Gerenciador de conexões
│   │   └── Sidebar.tsx                      # Menu lateral
│   ├── App.tsx              # Aplicação principal
│   ├── main.tsx             # Ponto de entrada
│   └── index.css            # Estilos globais
├── package.json             # Dependências Node.js
├── vite.config.ts           # Configuração Vite
└── README.md               # Este arquivo
```

## 🚀 Instalação

### 1. Dependências
```bash
npm install
```

### 2. Executar em Desenvolvimento
```bash
npm run dev
```

### 3. Build para Produção
```bash
npm run build
```

## 🎯 Funcionalidades

### Interface Integrada
- **Conexão Automática** - Conecta ao SQL Server automaticamente
- **Query Builder** - Interface para construir consultas SQL
- **Análise Completa** - Executa todo o pipeline de análise
- **Dashboard de Resultados** - Visualização detalhada dos resultados

### Componentes Principais

#### IntegratedAnalysisInterface
- Conexão automática ao banco
- Execução de queries SQL
- Análise completa com IA
- Visualização de resultados

#### ConnectionManager
- Gerenciamento de conexões
- Teste de conectividade
- Configurações de banco

#### Sidebar
- Navegação entre módulos
- Status de conexão
- Menu responsivo

## 🎨 Tecnologias

- **React 18** - Framework principal
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Chakra UI** - Componentes de interface
- **Zustand** - Gerenciamento de estado

## 🔧 Configuração

### Variáveis de Ambiente
```bash
VITE_API_URL=http://localhost:8001
VITE_APP_TITLE=DD-AI System
```

### Configuração do Vite
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
})
```

## 📱 Interface

### Páginas Principais

#### 1. Análise Integrada
- Conexão automática
- Query pré-configurada
- Botão de análise completa
- Resultados detalhados

#### 2. Gerenciador de Conexões
- Lista de conexões
- Teste de conectividade
- Configurações avançadas

#### 3. Dashboard
- Métricas em tempo real
- Gráficos de risco
- Histórico de análises

## 🎨 Design System

### Cores
- **Primary:** #3182CE (Azul)
- **Secondary:** #38A169 (Verde)
- **Warning:** #D69E2E (Amarelo)
- **Error:** #E53E3E (Vermelho)

### Componentes
- **Cards** - Para exibição de dados
- **Tables** - Para resultados SQL
- **Charts** - Para visualizações
- **Forms** - Para configurações

## 🔌 Integração com Backend

### Endpoints Utilizados
```typescript
// Conexão
POST /api/test-connection

// Queries
POST /api/execute-query
POST /api/tables

// Análise
POST /api/sql-to-analysis
GET /api/model-info
```

### Exemplo de Uso
```typescript
import { useState } from 'react'

const [connection, setConnection] = useState({
  server: 'DESKTOP-T9HKFSQ\\SQLEXPRESS',
  database: 'Projeto_Dev',
  use_windows_auth: true
})

const testConnection = async () => {
  const response = await fetch('/api/test-connection', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(connection)
  })
  return response.json()
}
```

## 🧪 Testes

### Teste de Interface
```bash
npm run test
```

### Teste de Build
```bash
npm run build
npm run preview
```

## 🚀 Deploy

### Build para Produção
```bash
npm run build
```

### Servir Build
```bash
npm run preview
```

### Deploy no GitHub Pages
```bash
npm run deploy
```

## 🔧 Desenvolvimento

### Scripts Disponíveis
- `npm run dev` - Servidor de desenvolvimento
- `npm run build` - Build para produção
- `npm run preview` - Preview do build
- `npm run lint` - Linting do código
- `npm run test` - Executar testes

### Estrutura de Componentes
```typescript
// Componente típico
interface ComponentProps {
  title: string
  data: any[]
  onAction: (data: any) => void
}

const Component: React.FC<ComponentProps> = ({ title, data, onAction }) => {
  return (
    <Box>
      <Heading>{title}</Heading>
      {/* Conteúdo */}
    </Box>
  )
}
```

## 🐛 Troubleshooting

### Erro de CORS
1. Verificar configuração do backend
2. Confirmar URL da API
3. Verificar headers

### Erro de Build
1. Verificar dependências
2. Limpar cache: `npm run clean`
3. Reinstalar: `rm -rf node_modules && npm install`

### Erro de Conexão
1. Verificar se backend está rodando
2. Confirmar porta 8001
3. Testar endpoint manualmente

## 📝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m 'Adiciona nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request
