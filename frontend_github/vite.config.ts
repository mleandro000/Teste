import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: path.resolve(__dirname, '.'), // Define a raiz do projeto como o diretório atual
  server: {
    port: 3000,
    host: '127.0.0.1',
    strictPort: false // Permite usar outra porta se 3000 estiver ocupada
  },
  build: {
    outDir: './dist', // Define a pasta de saída para o build
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  },
  // Configuração para evitar problemas de escopo
  publicDir: 'public',
  // Ignorar arquivos que não são do projeto React
  optimizeDeps: {
    exclude: ['nicegui', 'torch', 'playwright']
  }
})
