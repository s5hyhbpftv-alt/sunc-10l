import { D, hhmm } from '../lib'

export default function Bells() {
  const rows = Object.entries(D.lessons)
    .map(([n, [a, b]]) => ({ lesson: true, n, name: 'урок', a, b }))
    .concat(D.intervals.map((v) => ({ lesson: false, n: '', name: v.name, a: v.a, b: v.b, eat: v.kind === 'meal' })))
    .sort((x, y) => x.a - y.a)
  return (
    <div className="bells">
      {rows.map((r, i) => (
        <div key={i} className={'brow' + (r.lesson ? ' les' : r.eat ? ' eat' : '')}>
          <span className="no">{r.n}</span>
          <span className="nm">{r.name}</span>
          <span className="t">{hhmm(r.a)}</span>
          <span className="dash">—</span>
          <span className="t">{hhmm(r.b)}</span>
          <span className="du">{r.b - r.a} мин</span>
        </div>
      ))}
    </div>
  )
}
