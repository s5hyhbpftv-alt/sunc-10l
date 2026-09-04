import data from './data.json'

export const D = data
export const START = 8 * 60 + 45
export const END = 16 * 60 + 45
export const SPAN = END - START

export const hhmm = (m) =>
  `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`
export const pct = (m) => ((m - START) / SPAN) * 100
export const skl = (n) => (n > 1 && n < 5 ? 'урока' : 'уроков')

export const dayStats = (day) => {
  const slots = day.blocks.reduce((s, b) => s + b.l1 - b.l0 + 1, 0)
  const first = D.lessons[day.blocks[0].l0][0]
  const last = D.lessons[day.blocks[day.blocks.length - 1].l1][1]
  return { slots, mins: slots * 45, first, last }
}

export const meals = D.intervals
  .filter((v) => v.kind === 'meal')
  .map((v) => ({ ...v, a: Math.max(v.a, START), b: Math.min(v.b, END) }))
  .filter((v) => v.b - v.a >= 10)

export const tally = () => {
  const t = {}
  D.week.forEach((d) => d.blocks.forEach((b) => (t[b.fam] = (t[b.fam] || 0) + b.l1 - b.l0 + 1)))
  return Object.entries(t).sort((a, b) => b[1] - a[1] || D.family[a[0]].title.localeCompare(D.family[b[0]].title))
}

export const TOTAL = D.week.reduce((s, d) => s + d.blocks.reduce((k, b) => k + b.l1 - b.l0 + 1, 0), 0)

// ── что происходит прямо сейчас ─────────────────────────────────────────────
// Возвращает одно из состояний дня: до начала, урок, промежуток, всё кончилось,
// выходной. Промежуток знает своё имя — перемена, обед или второй завтрак.
export const dayIndex = (d) => {
  const wd = d.getDay()
  return wd >= 1 && wd <= 6 ? wd - 1 : null
}

export const lessonsOf = (day) => {
  const out = []
  day.blocks.forEach((b) => {
    for (let n = b.l0; n <= b.l1; n++) {
      const [from, to] = D.lessons[n]
      out.push({ n, from, to, block: b })
    }
  })
  return out.sort((a, b) => a.from - b.from)
}

const gapName = (from, to) => {
  const meal = D.intervals.find((v) => v.kind === 'meal' && v.a <= from && v.b >= to)
  if (meal) return meal.name
  return to - from <= 15 ? 'перемена' : 'окно'
}

export function nowState(now = new Date()) {
  const di = dayIndex(now)
  if (di === null) return { kind: 'weekend' }
  const day = D.week[di]
  const list = lessonsOf(day)
  const m = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60

  if (m < list[0].from) return { kind: 'before', di, day, next: list[0], list }
  const last = list[list.length - 1]
  if (m > last.to) return { kind: 'after', di, day, list }

  const cur = list.find((l) => m >= l.from && m <= l.to)
  if (cur) {
    return {
      kind: 'lesson', di, day, list, cur,
      left: Math.max(0, Math.ceil(cur.to - m)),
      progress: (m - cur.from) / (cur.to - cur.from),
      next: list.find((l) => l.from > cur.to) || null,
    }
  }
  const prev = [...list].reverse().find((l) => l.to <= m)
  const next = list.find((l) => l.from >= m)
  return {
    kind: 'gap', di, day, list, next,
    name: gapName(prev.to, next.from),
    left: Math.max(0, Math.ceil(next.from - m)),
    progress: (m - prev.to) / (next.from - prev.to),
  }
}
