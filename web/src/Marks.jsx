// Знаки рисуются формулой, а не картинкой: одна геометрия на оба мира.
const S3 = Math.sqrt(3) / 2

// Печатка: шесть цветных рёбер — шесть учебных дней, внутри кольца — класс.
export function Signet({ size = 120, colors, inner = '#EEF2F8', ink, font, label = '10Л' }) {
  const R = size / 2.44
  const pad = R * 0.2
  const box = 2 * (R + pad)
  const c = R + pad
  const r = R * 0.62
  const pts = [...Array(6)].map((_, i) => [
    c + R * Math.sin((Math.PI / 3) * i),
    c - R * Math.cos((Math.PI / 3) * i),
  ])
  return (
    <svg viewBox={`0 0 ${box} ${box}`} width={size} height={size} role="img"
         aria-label="10-Л, химический класс">
      <g fill="none" strokeLinecap="round" strokeWidth={R * 0.132}>
        {pts.map((p, i) => {
          const q = pts[(i + 1) % 6]
          return <path key={i} d={`M${p[0]} ${p[1]} L${q[0]} ${q[1]}`} stroke={colors[i]} />
        })}
      </g>
      <circle cx={c} cy={c} r={r} fill="none" stroke={inner} strokeWidth={R * 0.085} />
      <text x={c} y={c} textAnchor="middle" dominantBaseline="central"
            fontFamily={font} fontWeight="800" fontSize={r * 0.66}
            letterSpacing={r * -0.012} fill={ink || inner}>{label}</text>
    </svg>
  )
}

// Эмблема СУНЦ: три изометрических куба. Ось Y в SVG идёт вниз, поэтому
// верхний ряд сидит на r, а не на 2.5r — иначе синий уезжает за край.
export function Cubes({ size = 34, colors = ['#FF0C19', '#FFE000', '#00AEE8'], line = '#1B1211' }) {
  const r = size / 3.5
  const s = r * S3
  const w = 4 * s
  const lw = Math.max(0.5, r * 0.15)
  const pad = lw / 2
  const ox = w / 2
  const oy = r
  const cubes = [
    [-s, 0, colors[0]],
    [s, 0, colors[1]],
    [0, 1.5 * r, colors[2]],
  ]
  return (
    <svg
      viewBox={`${-pad} ${-pad} ${w + 2 * pad} ${size + 2 * pad}`}
      width={w + 2 * pad}
      height={size + 2 * pad}
      role="img"
      aria-label="СУНЦ МГУ"
    >
      <g stroke={line} strokeWidth={lw} strokeLinejoin="round" strokeLinecap="round">
        {cubes.map(([dx, dy, col], i) => {
          const cx = ox + dx
          const cy = oy + dy
          const P = {
            T: [cx, cy - r], UR: [cx + s, cy - r / 2], LR: [cx + s, cy + r / 2],
            B: [cx, cy + r], LL: [cx - s, cy + r / 2], UL: [cx - s, cy - r / 2],
          }
          const poly = [P.T, P.UR, P.LR, P.B, P.LL, P.UL].map((p) => p.join(',')).join(' ')
          return (
            <g key={i}>
              <polygon points={poly} fill={col} />
              {[P.T, P.LL, P.LR].map((p, k) => (
                <path key={k} d={`M${cx} ${cy} L${p[0]} ${p[1]}`} fill="none" />
              ))}
            </g>
          )
        })}
      </g>
    </svg>
  )
}
