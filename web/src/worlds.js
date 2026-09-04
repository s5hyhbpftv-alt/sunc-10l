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

const lum = (h) => {
  const [r, g, b] = hex(h).map((v) => {
    const x = v / 255
    return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

// Контраст по WCAG: по светлой краске печатаем чернилами, по тёмной — сливками.
const ratio = (a, b) => {
  const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m)
  return (x + 0.05) / (y + 0.05)
}
const readable = (paint, light, dark) =>
  ratio(light, paint) >= ratio(dark, paint) ? light : dark

export const WORLDS = {
  ink: {
    id: 'ink',
    label: 'Чернила',
    hint: 'тёмное издание',
    swatch: '#0A0D13',
    paintKey: 'ink',
    onBlock: (c) => readable(c, mix(c, '#EEF2F8', 0.92), mix(c, '#0A0D13', 0.9)),
    soft: (c) => mix(WORLDS.ink.onBlock(c), c, 0.3),
    meta: (c) => mix(c, '#0A0D13', 0.15),
    // краска, читаемая прямо по фону страницы
    onPage: (c) => c,
    vars: {
      '--bg': '#0A0D13',
      '--panel': '#11161F',
      '--line': '#1E2635',
      '--text': '#EEF2F8',
      '--muted': '#7C8AA3',
      '--faint': '#5C6A80',
      '--accent': '#FF5C93',
      '--amber': '#FFC53D',
      '--eat': '#FFC53D',
      '--wash': 'rgba(255,197,61,.11)',
      '--free': '#5C6A80',
      '--shadow': '0 14px 30px -18px rgba(0,0,0,.9)',
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
    onBlock: (c) => readable(c, '#EFE2C6', '#2A211A'),
    soft: (c) => mix(WORLDS.kraft.onBlock(c), c, 0.3),
    meta: (c) => mix(c, '#2A211A', 0.26),
    // по бумаге чистая краска слишком светлая — уводим её к чернилам
    onPage: (c) => mix(c, '#2A211A', 0.55),
    vars: {
      '--bg': '#C9A87D',
      '--panel': 'rgba(42,33,26,.075)',
      '--line': 'rgba(42,33,26,.24)',
      '--text': '#2A211A',
      '--muted': '#4A3B2C',
      '--faint': '#4F4030',
      '--accent': '#7A2029',
      '--amber': '#C8821C',
      '--eat': '#5A3A0C',
      '--wash': 'rgba(42,33,26,.09)',
      '--free': '#4F4030',
      '--shadow': '0 10px 22px -16px rgba(42,33,26,.7)',
      '--disp': "'IBM Plex Serif', Georgia, serif",
      '--sans': "'IBM Plex Serif', Georgia, serif",
      '--mono': "'IBM Plex Mono', ui-monospace, monospace",
      '--dispW': '700',
      '--radius': '0px',
    },
  },
}
