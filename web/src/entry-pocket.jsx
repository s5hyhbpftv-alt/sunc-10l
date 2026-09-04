import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Pocket from './Pocket'
import './styles.css'
import './pocket.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Pocket />
  </StrictMode>
)

// Офлайн включаем только у собранной версии: в dev воркер мешает горячей замене.
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(import.meta.env.BASE_URL + 'sw.js').catch(() => {})
  })
}
