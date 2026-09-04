import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const __dirname = dirname(fileURLToPath(import.meta.url))

// GitHub Pages отдаёт сайт из подпапки — отсюда base
export default defineConfig({
  base: process.env.BASE_PATH || '/sunc-10l/',
  plugins: [react()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // две страницы: витрина и карманное приложение
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        app: resolve(__dirname, 'app.html'),
      },
    },
  },
})
