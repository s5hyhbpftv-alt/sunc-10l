import { D, START, END, SPAN, hhmm, pct, meals } from '../lib'

// Лента дня: высота полосы равна длительности, провал в левой колонке —
// перемена внутри сдвоенного урока.
export default function DayTape({ world, day }) {
  const hours = [...Array(8)].map((_, i) => i + 9)
  const busy = new Set()
  day.blocks.forEach((b) => { for (let n = b.l0; n <= b.l1; n++) busy.add(n) })
  const free = [...Array(8)].map((_, i) => i + 1).filter((n) => !busy.has(n))

  const now = new Date()
  const wd = now.getDay()
  const mins = now.getHours() * 60 + now.getMinutes()
  const isToday = wd >= 1 && wd <= 6 && D.week[wd - 1].name === day.name
  const showNow = isToday && mins >= START && mins <= END

  return (
    <div className="tape">
      {hours.map((h) => (
        <div key={h} className="hr" style={{ top: `${pct(h * 60)}%` }}>
          <i>{String(h).padStart(2, '0')}</i>
        </div>
      ))}

      {meals.map((v) => (
        <div key={v.name} className="wash"
             style={{ top: `${pct(v.a)}%`, height: `${((v.b - v.a) / SPAN) * 100}%` }}>
          <span>{v.name}</span>
        </div>
      ))}

      {day.blocks.map((b, i) => {
        const paint = D.family[b.fam][world.paintKey]
        const a = D.lessons[b.l0][0]
        const z = D.lessons[b.l1][1]
        const on = world.onBlock(paint)
        const soft = world.soft(paint)
        const meta = world.meta(paint)
        const lessons = []
        for (let n = b.l0; n <= b.l1; n++) lessons.push(n)
        // в одиночном уроке две строки справа не помещаются по высоте
        const single = b.l0 === b.l1
        return (
          <div key={i} className="blk"
               style={{ top: `${pct(a)}%`, height: `${((z - a) / SPAN) * 100}%`,
                        background: paint, animationDelay: `${i * 80}ms` }}>
            <div className="meta">
              {lessons.map((n) => {
                const [la, lb] = D.lessons[n]
                return (
                  <u key={n} style={{ top: `${((la - a) / (z - a)) * 100}%`,
                                      height: `${((lb - la) / (z - a)) * 100}%`,
                                      background: meta }}>
                    <em style={{ color: on }}>{n}</em>
                    <s style={{ color: on }}>{hhmm(la)}<br />{hhmm(lb)}</s>
                  </u>
                )
              })}
            </div>
            <div className="body">
              <div className="left">
                <span className="nm" style={{ color: on }}>{b.name}</span>
                {b.note && <span className="note" style={{ color: soft }}>{b.note}</span>}
              </div>
              <div className={'right' + (single ? ' inline' : '')}>
                {b.room && (
                  <div className="room" style={{ color: on }}>
                    <i style={{ color: soft }}>каб.</i>{b.room}
                  </div>
                )}
                {b.teacher && <div className="tch" style={{ color: soft }}>{b.teacher}</div>}
              </div>
            </div>
          </div>
        )
      })}

      {free.map((n) => {
        const [a, b] = D.lessons[n]
        return (
          <div key={n} className="free"
               style={{ top: `${pct(a)}%`, height: `${((b - a) / SPAN) * 100}%` }}>
            <em>{n}</em><s>окно</s>
          </div>
        )
      })}

      {showNow && (
        <div className="now" style={{ top: `${pct(mins)}%` }}><b>сейчас {hhmm(mins)}</b></div>
      )}
    </div>
  )
}
