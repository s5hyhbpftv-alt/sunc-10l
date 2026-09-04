import { useEffect, useRef, useState } from 'react'
import { D, START, SPAN, pct, skl } from '../lib'

export default function Spectrum({ world, active, onPick, height = 'clamp(180px,24vw,320px)' }) {
  const box = useRef(null)
  const [lit, setLit] = useState(false)
  useEffect(() => {
    const el = box.current
    if (!el) return
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => e.isIntersecting && (setLit(true), io.disconnect())),
      { threshold: 0.2 }
    )
    io.observe(el)
    return () => io.disconnect()
  }, [])
  const hours = [...Array(8)].map((_, i) => i + 9)
  return (
    <div ref={box}>
      <div className="spectrum" style={{ '--sh': height }}>
        <div className="hours">
          {hours.map((h) => (
            <i key={h} style={{ top: `${pct(h * 60)}%` }}>{String(h).padStart(2, '0')}</i>
          ))}
        </div>
        {D.week.map((day, di) => (
          <button
            key={day.short}
            className={'col' + (di === active ? ' on' : '')}
            onClick={() => onPick(di)}
            aria-label={day.name}
          >
            {hours.map((h) => (
              <u key={h} style={{ top: `${pct(h * 60)}%` }} />
            ))}
            {day.blocks.map((b, i) => {
              const a = D.lessons[b.l0][0]
              const z = D.lessons[b.l1][1]
              return (
                <b
                  key={i}
                  style={{
                    top: `${pct(a)}%`,
                    height: `${((z - a) / SPAN) * 100}%`,
                    background: D.family[b.fam][world.paintKey],
                    transform: lit ? 'none' : 'scaleY(0)',
                    transitionDelay: `${di * 80 + i * 60}ms`,
                  }}
                />
              )
            })}
          </button>
        ))}
      </div>
      <div className="caps">
        <div />
        {D.week.map((day) => {
          const n = day.blocks.reduce((s, b) => s + b.l1 - b.l0 + 1, 0)
          return (
            <div key={day.short}>
              <div className="d">{day.name}</div>
              <div className="n">{n} {skl(n)}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
