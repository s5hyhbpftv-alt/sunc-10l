import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages отдаёт сайт из подпапки — отсюда base
export default defineConfig({
  base: process.env.BASE_PATH || '/sunc-10l/',
  plugins: [react()],
  build: { outDir: 'dist', assetsDir: 'assets' },
})
