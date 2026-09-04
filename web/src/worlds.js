// Два мира одной книги. Всё, чем они различаются, живёт здесь: краски,
// гарнитуры, подложка и то, каким цветом ложится текст на плашку урока.

const hex = (h) => {
  const n = parseInt(h.slice(1), 16)
  return [n >> 16, (n >> 8) & 255, n & 255]
}

export const mix = (a, b, t) => {
  const [r1, g1, b1] = hex(a), [r2, g2, b2] = hex(b)
  const k = (x, y) => Math.round(x + (y - x) * t)
  return `rgb(${k(r1, r2)},${k(g1, g2)},${k(b1, b2)})`
}

export const WORLDS = {
  ink: {
    id: 'ink',
    label: 'Чернила',
    hint: 'тёмное издание',
    swatch: '#0A0D13',
    paintKey: 'ink',
    onBlock: (c) => mix(c, '#0A0D13', 0.88),
    soft: (c) => mix(c, '#0A0D13', 0.62),
    meta: (c) => mix(c, '#0A0D13', 0.15),
    vars: {
      '--bg': '#0A0D13',
      '--panel': '#11161F',
      '--line': '#1E2635',
      '--text': '#EEF2F8',
      '--muted': '#66748C',
      '--faint': '#3F4A5D',
      '--accent': '#FF5C93',
      '--amber': '#FFC53D',
      '--wash': 'rgba(255,197,61,.11)',
      '--free': '#3F4A5D',
      '--disp': "'Unbounded', system-ui, sans-serif",
      '--sans': "'Manrope', system-ui, sans-serif",
      '--mono': "'JetBrains Mono', ui-monospace, monospace",
      '--dispW': '800',
      '--radius': '7px',
    },
  },
  kraft: {
    id: 'kraft',
    label: 'Крафт',
    hint: 'бумага из лаборатории',
    swatch: '#C9A87D',
    paintKey: 'kraft',
    onBlock: () => '#EFE2C6',
    soft: (c) => mix('#EFE2C6', c, 0.4),
    meta: (c) => mix(c, '#2A211A', 0.26),
    vars: {
      '--bg': '#C9A87D',
      '--panel': 'rgba(42,33,26,.075)',
      '--line': 'rgba(42,33,26,.24)',
      '--text': '#2A211A',
      '--muted': '#5A4A38',
      '--faint': '#8A7355',
      '--accent': '#C33A48',
      '--amber': '#C8821C',
      '--wash': 'rgba(42,33,26,.09)',
      '--free': '#8A7355',
      '--disp': "'IBM Plex Serif', Georgia, serif",
      '--sans': "'IBM Plex Serif', Georgia, serif",
      '--mono': "'IBM Plex Mono', ui-monospace, monospace",
      '--dispW': '700',
      '--radius': '0px',
    },
  },
}
