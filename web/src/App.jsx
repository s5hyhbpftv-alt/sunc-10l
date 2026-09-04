import { useEffect, useRef, useState } from 'react'
import { WORLDS } from './worlds'
import { Signet, Cubes } from './Marks'
import { D, hhmm, skl, dayStats } from './lib'
import Spectrum from './sections/Spectrum'
import DayTape from './sections/DayTape'
import Bells from './sections/Bells'
import Elements from './sections/Elements'
import Studio from './Studio'

const RING_KEYS = ['chem', 'math', 'inf', 'phys', 'eng', 'lit']
const SUNC = ['chem', 'math', 'hist']
const BASE = import.meta.env.BASE_URL

const СКАЧАТЬ = [
  {
    href: BASE + 'pdf/10L-chernila.pdf',
    title: 'Чернильное издание',
    text: 'Двенадцать полос по тёмному. Неделя светится на них, как индикатор, которому только что подняли pH.',
    tag: 'A4 · 12 полос',
  },
  {
    href: BASE + 'pdf/10L-kraft.pdf',
    title: 'Крафтовое издание',
    text: 'То же самое, отпечатанное землистыми красками по обёрточной бумаге из-под реактивов. Со штампом и следом стакана.',
    tag: 'A4 · 12 полос',
  },
  {
    href: BASE + 'pdf/10L-plakat-a3.pdf',
    title: 'Настенный разворот',
    text: 'Тот же разбор в альбомном A3: когда неделю нужно повесить над столом, а не листать.',
    tag: 'A3 · 10 полос',
  },
  {
    href: 'https://internat.msu.ru/structure/departments/for-students/schedule/',
    title: 'Исходное вещество',
    text: 'Заводской файл интерната, из которого всё это выпарено. Меняется каждый семестр — сверяйтесь.',
    tag: 'internat.msu.ru',
    out: true,
  },
]

export default function App() {
  // мир можно закрепить ссылкой: ?world=kraft
  const [worldId, setWorldId] = useState(() => {
    const q = new URLSearchParams(location.search).get('world')
    if (q && WORLDS[q]) return q
    try { return localStorage.getItem('world') || 'ink' } catch (e) { return 'ink' }
  })
  const world = WORLDS[worldId] || WORLDS.ink
  const paint = (k) => D.family[k][world.paintKey]

  const today = () => {
    const wd = new Date().getDay()
    return wd >= 1 && wd <= 6 ? wd - 1 : 0
  }
  const [day, setDay] = useState(today)
  const [playing, setPlaying] = useState(true)
  const timer = useRef(null)

  useEffect(() => {
    document.documentElement.dataset.world = worldId
    Object.entries(world.vars).forEach(([k, v]) => document.documentElement.style.setProperty(k, v))
    try { localStorage.setItem('world', worldId) } catch (e) { /* приватное окно */ }
  }, [worldId, world])

  useEffect(() => {
    clearInterval(timer.current)
    if (playing) timer.current = setInterval(() => setDay((d) => (d + 1) % 6), 4600)
    return () => clearInterval(timer.current)
  }, [playing, day])

  const pick = (d) => { setPlaying(false); setDay(d) }
  const cur = D.week[day]
  const st = dayStats(cur)

  return (
    <>
      <div className="ground" aria-hidden="true"
           style={worldId === 'kraft' ? { backgroundImage: `url(${BASE}kraft.jpg)` } : undefined} />

      <header>
        <nav className="nav">
          <span className="sunc">
            <Cubes size={30} colors={SUNC.map(paint)} line={worldId === 'ink' ? '#0A0D13' : '#2A211A'} />
            <span>
              <b>СУНЦ МГУ</b>
              <i>им. А. Н. Колмогорова</i>
            </span>
          </span>
          <span className="sp" />
          <a href="#hromatogramma" className="hide">Хроматограмма</a>
          <a href="#proba">Проба дня</a>
          <a href="#hronometrazh" className="hide">Хронометраж</a>
          <a href="#ottiski">Оттиски</a>
          <a href={BASE + 'app.html'} className="app">Приложение</a>
          <span className="switch">
            {Object.values(WORLDS).map((w) => (
              <button key={w.id} className={w.id === worldId ? 'on' : ''}
                      onClick={() => setWorldId(w.id)} title={w.hint}>
                <i style={{ background: w.swatch }} />{w.label}
              </button>
            ))}
          </span>
        </nav>
      </header>

      <main className="wrap">
        <section className="hero">
          <div className="lock">
            <Signet size={186} colors={RING_KEYS.map(paint)}
                    inner={worldId === 'ink' ? '#EEF2F8' : '#2A211A'}
                    ink={worldId === 'ink' ? '#EEF2F8' : '#2A211A'}
                    font={worldId === 'ink' ? 'Unbounded' : 'IBM Plex Serif'} />
            <div className="lockText">
              <p className="band"><span>Химический класс</span></p>
              <h1>Неделя,<br />разложенная<br />на фракции</h1>
              <p className="sub">
                Тридцать восемь уроков поставлены в шесть колонок. Полоса тем выше, чем
                дольше держится предмет, и цвет у каждого свой — читается быстрее, чем
                подпись под ним. Двадцать восемь с половиной часов в неделю,
                свой кабинет — сороковой.
              </p>
            </div>
          </div>
        </section>

        <div className="rule" />

        <section id="hromatogramma">
          <h2>Хроматограмма</h2>
          <p className="lede">
            Шесть проб, поставленных в понедельник и снятых в субботу. Нажмите на колонку —
            она развернётся в ленту.
          </p>
          <Spectrum world={world} active={day} onPick={pick} />
        </section>

        <div className="rule" />

        <section id="proba">
          <div className="dayhead">
            <h2 className="dayname">{cur.name}</h2>
            <span className="facts">
              <b>{st.slots} {skl(st.slots)}</b>
              <em>·</em>{hhmm(st.first)} — {hhmm(st.last)}
              <em>·</em>{Math.floor(st.mins / 60)} ч {String(st.mins % 60).padStart(2, '0')} мин
            </span>
          </div>
          <p className="epigraph">{cur.epigraph}</p>
          <div className="bar">
            {D.week.map((d, i) => (
              <button key={d.short} className={i === day ? 'on' : ''} onClick={() => pick(i)}>
                {d.short}
              </button>
            ))}
            <span className="sp" />
            <button onClick={() => setPlaying((p) => !p)} className={playing ? 'on' : ''}>
              {playing ? '▮▮ стоп' : '▶ листать'}
            </button>
          </div>
          <DayTape world={world} day={cur} />
        </section>

        <div className="rule" />

        <section id="hronometrazh" className="two">
          <div>
            <h2>Хронометраж</h2>
            <p className="lede">
              Единственная константа в этой лаборатории: сорок пять минут реакции,
              десять на промывку. Один раз в день — пятьдесят, и это обед.
            </p>
            <Bells />
            <p className="note">
              В источнике полдник начинается в 16:40 — на пять минут раньше, чем кончается
              восьмой урок. Оставлено как есть.
            </p>
          </div>
          <div>
            <h2>Состав</h2>
            <p className="lede">
              Что показал элементный анализ недели: доля каждого предмета,
              выраженная в уроках и часах.
            </p>
            <Elements world={world} />
          </div>
        </section>

        <div className="rule" />

        <section id="ottiski">
          <h2>Оттиски</h2>
          <p className="lede">Четыре способа вынести эту неделю из лаборатории.</p>
          <div className="dl">
            {СКАЧАТЬ.map((d) => (
              <a key={d.href} href={d.href}
                 {...(d.out ? { target: '_blank', rel: 'noopener' } : { download: true })}>
                <span className="tag">{d.tag}</span>
                <b>{d.title}</b>
                <span className="txt">{d.text}</span>
              </a>
            ))}
          </div>
        </section>

        <footer>
          <span className="sunc">
            <Cubes size={34} colors={SUNC.map(paint)} line={worldId === 'ink' ? '#0A0D13' : '#2A211A'} />
          </span>
          <span className="note">
            Данные: internat.msu.ru, колонка 10-Л. Границы сдвоенных блоков сняты
            по рамкам ячеек и сверены с изображением расписания.
          </span>
          <span className="note">
            <a href={BASE + 'app.html'}>Карманное расписание</a> · Хронохром · 2026
          </span>
        </footer>

        <Studio />
      </main>
    </>
  )
}
