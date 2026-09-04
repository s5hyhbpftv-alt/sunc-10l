// Офлайн-слой карманного расписания.
// Оболочка кладётся в кеш при установке, всё остальное — по мере обращения.
// Скачанный однажды PDF тоже остаётся доступным без сети.
const ВЕРСИЯ = 'sunc10l-v1'
const БАЗА = new URL('./', self.location).pathname
const ОБОЛОЧКА = [
  БАЗА,
  БАЗА + 'app.html',
  БАЗА + 'index.html',
  БАЗА + 'manifest.webmanifest',
  БАЗА + 'icon-192.png',
  БАЗА + 'icon-512.png',
]

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(ВЕРСИЯ)
      .then((c) => Promise.allSettled(ОБОЛОЧКА.map((u) => c.add(u))))
      .then(() => self.skipWaiting())
  )
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k !== ВЕРСИЯ).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (e) => {
  const req = e.request
  if (req.method !== 'GET') return
  const url = new URL(req.url)
  if (url.origin !== self.location.origin) return

  // навигация: сеть вперёд, кеш как запасной выход в самолётном режиме
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req)
        .then((r) => {
          const копия = r.clone()
          caches.open(ВЕРСИЯ).then((c) => c.put(req, копия))
          return r
        })
        .catch(() => caches.match(req).then((r) => r || caches.match(БАЗА + 'app.html')))
    )
    return
  }

  // остальное: отдаём из кеша сразу, в фоне обновляем
  e.respondWith(
    caches.match(req).then((кеш) => {
      const сеть = fetch(req)
        .then((r) => {
          if (r && r.status === 200 && r.type === 'basic') {
            const копия = r.clone()
            caches.open(ВЕРСИЯ).then((c) => c.put(req, копия))
          }
          return r
        })
        .catch(() => кеш)
      return кеш || сеть
    })
  )
})
