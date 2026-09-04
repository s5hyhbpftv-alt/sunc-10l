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
