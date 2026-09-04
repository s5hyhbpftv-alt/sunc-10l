import { useEffect, useRef, useState } from 'react'
import { WORLDS } from './worlds'
import { Signet } from './Marks'
import { D, hhmm, skl, nowState, lessonsOf, dayIndex } from './lib'

const RING = ['chem', 'math', 'inf', 'phys', 'eng', 'lit']
const BASE = import.meta.env.BASE_URL

const ИЗДАНИЯ = [
  { file: 'pdf/10L-chernila.pdf', title: 'Чернильная книга', meta: 'A4 · 12 полос · 143 КБ' },
  { file: 'pdf/10L-kraft.pdf', title: 'Крафтовое издание', meta: 'A4 · 12 полос · 1,1 МБ' },
  { file: 'pdf/10L-plakat-a3.pdf', title: 'Настенный разворот', meta: 'A3 · 10 полос · 125 КБ' },
]

const склонМин = (n) => {
  const d = n % 10, s = n % 100
  if (d === 1 && s !== 11) return 'минута'
  if (d >= 2 && d <= 4 && (s < 12 || s > 14)) return 'минуты'
  return 'минут'
}

export default function Pocket() {
  const [worldId, setWorldId] = useState(() => {
    const q = new URLSearchParams(location.search).get('world')
    if (q && WORLDS[q]) return q
    try { return localStorage.getItem('world') || 'ink' } catch (e) { return 'ink' }
  })
  const world = WORLDS[worldId] || WORLDS.ink
  const paint = (k) => D.family[k][world.paintKey]

  const [tick, setTick] = useState(() => new Date())
  useEffect(() => {
    const t = setInterval(() => setTick(new Date()), 15000)
    return () => clearInterval(t)
  }, [])

  const live = nowState(tick)
  const today = dayIndex(tick)
  const [pick, setPick] = useState(today)
  const day = D.week[pick ?? 0]
  const list = lessonsOf(day)
  const isToday = pick === today

  useEffect(() => {
    document.documentElement.dataset.world = worldId
    Object.entries(world.vars).forEach(([k, v]) => document.documentElement.style.setProperty(k, v))
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) meta.setAttribute('content', world.vars['--bg'])
    try { localStorage.setItem('world', worldId) } catch (e) { /* приватное окно */ }
  }, [worldId, world])

  // предложение установки: браузер даёт его один раз, придерживаем до нажатия
  const prompt = useRef(null)
  const [canInstall, setCanInstall] = useState(false)
  useEffect(() => {
    const h = (e) => { e.preventDefault(); prompt.current = e; setCanInstall(true) }
    window.addEventListener('beforeinstallprompt', h)
    return () => window.removeEventListener('beforeinstallprompt', h)
  }, [])
  const install = async () => {
    if (!prompt.current) return
    prompt.current.prompt()
    await prompt.current.userChoice
    prompt.current = null
    setCanInstall(false)
  }

  return (
    <>
      <div className="ground" aria-hidden="true"
           style={worldId === 'kraft' ? { backgroundImage: `url(${BASE}kraft.jpg)` } : undefined} />

      <div className="pocket">
        <header className="phead">
          <Signet size={44} colors={RING.map(paint)}
                  inner={worldId === 'ink' ? '#EEF2F8' : '#2A211A'}
                  ink={worldId === 'ink' ? '#EEF2F8' : '#2A211A'}
                  font={worldId === 'ink' ? 'Unbounded' : 'IBM Plex Serif'} />
          <div className="phead-t">
            <b>10-Л</b>
            <i>{tick.toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })}</i>
          </div>
          <span className="sp" />
          <span className="switch">
            {Object.values(WORLDS).map((w) => (
              <button key={w.id} className={w.id === worldId ? 'on' : ''}
                      onClick={() => setWorldId(w.id)} aria-label={w.label}>
                <i style={{ background: w.swatch }} />
              </button>
            ))}
          </span>
        </header>

        <Card live={live} world={world} paint={paint} />

        <nav className="pdays">
          {D.week.map((d, i) => (
            <button key={d.short} className={i === pick ? 'on' : ''} onClick={() => setPick(i)}>
              {d.short}
              {i === today && <u />}
            </button>
          ))}
        </nav>

        <ol className="plist">
          {day.blocks.map((b, i) => {
            const from = D.lessons[b.l0][0]
            const to = D.lessons[b.l1][1]
            const active = isToday && live.kind === 'lesson' && live.cur.block === b
            return (
              <li key={i} className={active ? 'on' : ''}>
                <span className="n">{b.l0 === b.l1 ? b.l0 : `${b.l0}–${b.l1}`}</span>
                <span className="t">{hhmm(from)}<i>{hhmm(to)}</i></span>
                <span className="chip" style={{ background: paint(b.fam) }} />
                <span className="nm">
                  {b.name}
                  {b.teacher && <i>{b.teacher}</i>}
                </span>
                <span className="room">{b.room || '—'}</span>
              </li>
            )
          })}
        </ol>

        <p className="pepi">{day.epigraph}</p>

        <section className="pdl">
          <h2>Забрать с собой</h2>
          <p className="phint">Скачанный файл остаётся доступным и без сети.</p>
          {ИЗДАНИЯ.map((и) => (
            <a key={и.file} href={BASE + и.file} download>
              <span className="pdl-t">{и.title}</span>
              <span className="pdl-m">{и.meta}</span>
              <span className="pdl-a" aria-hidden="true">↓</span>
            </a>
          ))}
        </section>

        <footer className="pfoot">
          {canInstall && (
            <button className="pinstall" onClick={install}>Установить на телефон</button>
          )}
          <a href={BASE}>Полная версия расписания</a>
          <span>{D.texts['студия']}</span>
        </footer>
      </div>
    </>
  )
}

function Card({ live, world, paint }) {
  if (live.kind === 'weekend') {
    return (
      <div className="card quiet">
        <b className="card-k">Воскресенье</b>
        <p className="card-s">Уроков нет. Ближайший — в понедельник в 08:45.</p>
      </div>
    )
  }
  if (live.kind === 'before' || live.kind === 'after') {
    const начало = live.kind === 'before'
    const b = начало ? live.next.block : null
    return (
      <div className="card quiet">
        <b className="card-k">{начало ? 'Ещё не началось' : 'На сегодня всё'}</b>
        <p className="card-s">
          {начало
            ? `Первый урок — ${b.name.toLowerCase()} в ${hhmm(live.next.from)}${b.room ? `, каб. ${b.room}` : ''}.`
            : `Сегодня было ${live.list.length} ${skl(live.list.length)}. Последний кончился в ${hhmm(live.list[live.list.length - 1].to)}.`}
        </p>
      </div>
    )
  }
  if (live.kind === 'gap') {
    const b = live.next.block
    return (
      <div className="card quiet">
        <b className="card-k">{live.name[0].toUpperCase() + live.name.slice(1)}</b>
        <p className="card-big">{live.left} <i>{склонМин(live.left)}</i></p>
        <p className="card-s">
          Дальше — {b.name.toLowerCase()} в {hhmm(live.next.from)}
          {b.room ? `, каб. ${b.room}` : ''}.
        </p>
        <span className="card-bar"><b style={{ transform: `scaleX(${live.progress})` }} /></span>
      </div>
    )
  }

  const b = live.cur.block
  const c = paint(b.fam)
  const on = world.onBlock(c)
  const soft = world.soft(c)
  return (
    <div className="card" style={{ background: c, color: on }}>
      <b className="card-k" style={{ color: soft }}>
        Сейчас · урок {live.cur.n} · до {hhmm(live.cur.to)}
      </b>
      <p className="card-nm">{b.name}</p>
      <p className="card-s" style={{ color: soft }}>
        {b.room ? `каб. ${b.room}` : 'без кабинета'}{b.teacher ? ` · ${b.teacher}` : ''}
      </p>
      <p className="card-big">{live.left} <i>{склонМин(live.left)}</i></p>
      <span className="card-bar" style={{ background: soft }}>
        <b style={{ transform: `scaleX(${live.progress})`, background: on }} />
      </span>
      {live.next && (
        <p className="card-next" style={{ color: soft }}>
          дальше {live.next.block.name.toLowerCase()} в {hhmm(live.next.from)}
        </p>
      )}
    </div>
  )
}
