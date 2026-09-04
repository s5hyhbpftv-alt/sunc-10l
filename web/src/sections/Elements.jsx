import { D, tally } from '../lib'

// Состав недели, разложенный клетками, как элементы в таблице.
export default function Elements({ world }) {
  const rows = tally()
  const max = rows[0][1]
  return (
    <div className="elements">
      {rows.map(([fam, n]) => {
        const paint = D.family[fam][world.paintKey]
        const onPage = world.onPage(paint)
        const hours = `${Math.floor((n * 45) / 60)}:${String((n * 45) % 60).padStart(2, '0')}`
        return (
          <div key={fam} className="cell" style={{ borderColor: paint }}>
            <div className="cap" style={{ background: paint, color: world.onBlock(paint) }}>
              <span>{n}</span><span>{hours}</span>
            </div>
            <div className="sym" style={{ color: onPage }}>{D.family[fam].symbol}</div>
            <div className="name">{D.family[fam].title}</div>
            <div className="bar"><b style={{ width: `${(n / max) * 100}%`, background: onPage }} /></div>
          </div>
        )
      })}
    </div>
  )
}
