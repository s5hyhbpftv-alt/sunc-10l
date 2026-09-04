# -*- coding: utf-8 -*-
"""Знаки: эмблема СУНЦ МГУ (три куба) и знак класса 10-Л (бензольное кольцо).

Кольцо — шесть рёбер шести цветов: ароматическое кольцо химического класса
и одновременно шесть учебных дней недели. Внутренняя окружность — та самая
делокализация, которой в школьной тетради обозначают бензол.
"""
import math

# цвета заводской эмблемы СУНЦ (сняты пипеткой с internat.msu.ru/logo.png)
SUNC_RED, SUNC_YEL, SUNC_BLUE, SUNC_LINE = '#FF0C19', '#FFE000', '#00AEE8', '#1B1211'

# спектр кольца 10-Л: химия ведёт, дальше по кругу
RING = ['#FF5C93', '#FFC53D', '#B6E36B', '#2BD576', '#22D3EE', '#A970FF']

S3 = math.sqrt(3) / 2.0


def _hex_pts(cx, cy, r, up=True):
    """Вершины правильного шестиугольника «остриём вверх»."""
    return [(cx + r * math.sin(math.pi / 3 * i), cy + r * math.cos(math.pi / 3 * i))
            for i in range(6)] if up else None


# ── эмблема СУНЦ: три изометрических куба ───────────────────────────────────
def sunc_cubes_geometry(h):
    """h — полная высота знака. → (r, [(cx, cy, color), ...], ширина)"""
    r = h / 3.5
    s = r * S3
    cubes = [(-s, 0.0, SUNC_RED), (s, 0.0, SUNC_YEL), (0.0, -1.5 * r, SUNC_BLUE)]
    return r, cubes, 4 * s


def draw_sunc(c, x, y, h, colors=None, line=None):
    """Рисует эмблему в reportlab. (x, y) — левый нижний угол габарита.
    colors — три цвета кубов (красный, жёлтый, синий) для печати по цветной бумаге."""
    from reportlab.lib.colors import HexColor
    r, cubes, w = sunc_cubes_geometry(h)
    if colors:
        cubes = [(dx, dy, colors[i]) for i, (dx, dy, _) in enumerate(cubes)]
    s = r * S3
    ox, oy = x + w / 2.0, y + 2.5 * r
    lw = max(0.5, r * 0.15)
    c.setLineWidth(lw); c.setLineJoin(1); c.setLineCap(1)
    for dx, dy, col in cubes:
        cx, cy = ox + dx, oy + dy
        T, UR, LR = (cx, cy + r), (cx + s, cy + r / 2), (cx + s, cy - r / 2)
        B, LL, UL = (cx, cy - r), (cx - s, cy - r / 2), (cx - s, cy + r / 2)
        p = c.beginPath(); p.moveTo(*T)
        for pt in (UR, LR, B, LL, UL): p.lineTo(*pt)
        p.close()
        c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor(line or SUNC_LINE))
        c.drawPath(p, stroke=1, fill=1)
        for pt in (T, LL, LR):
            c.line(cx, cy, *pt)
    return w


def svg_sunc(h):
    r, cubes, w = sunc_cubes_geometry(h)
    s = r * S3
    # svg: ось Y вниз, поэтому верхний ряд кубов сидит на r, а не на 2.5r —
    # иначе нижний (синий) куб уезжает за нижний край картинки.
    ox, oy = w / 2.0, r
    lw = max(0.5, r * 0.15)
    pad = lw / 2.0                     # обводка не должна срезаться рамкой
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.2f %.2f %.2f %.2f" '
           'width="%.0f" height="%.0f" role="img" aria-label="СУНЦ МГУ">'
           % (-pad, -pad, w + 2 * pad, h + 2 * pad, w + 2 * pad, h + 2 * pad)]
    out.append('<g stroke="%s" stroke-width="%.2f" stroke-linejoin="round" '
               'stroke-linecap="round">' % (SUNC_LINE, lw))
    for dx, dy, col in cubes:
        cx, cy = ox + dx, oy - dy
        T, UR, LR = (cx, cy - r), (cx + s, cy - r / 2), (cx + s, cy + r / 2)
        B, LL, UL = (cx, cy + r), (cx - s, cy + r / 2), (cx - s, cy - r / 2)
        pts = ' '.join('%.2f,%.2f' % p for p in (T, UR, LR, B, LL, UL))
        out.append('<polygon points="%s" fill="%s"/>' % (pts, col))
        for pt in (T, LL, LR):
            out.append('<path d="M%.2f %.2f L%.2f %.2f" fill="none"/>' % (cx, cy, pt[0], pt[1]))
    out.append('</g></svg>')
    return '\n'.join(out)


# ── знак 10-Л: ароматическое кольцо ─────────────────────────────────────────
def draw_ring(c, cx, cy, R, mono=None, inner='#EEF2F8', colors=None):
    """Кольцо шести цветов. mono — весь знак одним цветом; colors — своя шестёрка."""
    from reportlab.lib.colors import HexColor
    ring = colors or RING
    pts = _hex_pts(cx, cy, R)
    lw = R * 0.155
    c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        c.setStrokeColor(HexColor(mono or ring[i]))
        c.line(a[0], a[1], b[0], b[1])
    c.setLineWidth(R * 0.105)
    c.setStrokeColor(HexColor(mono or inner))
    c.circle(cx, cy, R * 0.5, stroke=1, fill=0)


def svg_ring(R, mono=None, inner='#EEF2F8', pad=None):
    pad = pad if pad is not None else R * 0.22
    size = 2 * (R + pad)
    cx = cy = R + pad
    pts = [(cx + R * math.sin(math.pi / 3 * i), cy - R * math.cos(math.pi / 3 * i))
           for i in range(6)]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
           'width="%.0f" height="%.0f" role="img" aria-label="10-Л">' % (size, size, size, size)]
    out.append('<g stroke-linecap="round" stroke-width="%.2f" fill="none">' % (R * 0.155))
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        out.append('<path d="M%.2f %.2f L%.2f %.2f" stroke="%s"/>'
                   % (a[0], a[1], b[0], b[1], mono or RING[i]))
    out.append('</g>')
    out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" '
               'stroke-width="%.2f"/>' % (cx, cy, R * 0.5, mono or inner, R * 0.105))
    out.append('</svg>')
    return '\n'.join(out)


# ── знак-печатка: кольцо с номером класса внутри ────────────────────────────
def draw_signet(c, cx, cy, R, шрифт, mono=None, colors=None,
                inner='#EEF2F8', label='10Л', ink=None):
    """Кольцо с надписью внутри: подпись класса становится частью формулы,
    а не строчкой рядом с ней. Размер кегля подбирается по хорде окружности."""
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    ring = colors or RING
    pts = _hex_pts(cx, cy, R)
    c.setLineWidth(R * 0.132); c.setLineCap(1); c.setLineJoin(1)
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        c.setStrokeColor(HexColor(mono or ring[i]))
        c.line(a[0], a[1], b[0], b[1])
    r = R * 0.62
    c.setLineWidth(R * 0.085)
    c.setStrokeColor(HexColor(mono or inner))
    c.circle(cx, cy, r, stroke=1, fill=0)

    цель = r * 1.05                      # надпись чуть шире радиуса, но внутри круга
    кегль = 10.0
    while pdfmetrics.stringWidth(label, шрифт, кегль) < цель:
        кегль += 0.25
    кегль -= 0.25
    c.setFont(шрифт, кегль)
    c.setFillColor(HexColor(mono or ink or inner))
    w = pdfmetrics.stringWidth(label, шрифт, кегль)
    c.drawString(cx - w / 2, cy - кегль * 0.35, label)


def svg_signet(R, mono=None, colors=None, inner='#EEF2F8', ink=None,
               label='10Л', font='Unbounded, system-ui, sans-serif'):
    """Печатка в SVG. Кегль подписи задаётся долей радиуса: ширину строки
    здесь не измерить, поэтому доля подобрана по отрисовке в reportlab."""
    ring = colors or RING
    pad = R * 0.2
    size = 2 * (R + pad)
    cx = cy = R + pad
    r = R * 0.62
    pts = [(cx + R * math.sin(math.pi / 3 * i), cy - R * math.cos(math.pi / 3 * i))
           for i in range(6)]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
           'width="%.0f" height="%.0f" role="img" aria-label="10-Л, химический класс">'
           % (size, size, size, size)]
    out.append('<g fill="none" stroke-linecap="round" stroke-width="%.2f">' % (R * 0.132))
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        out.append('<path d="M%.2f %.2f L%.2f %.2f" stroke="%s"/>'
                   % (a[0], a[1], b[0], b[1], mono or ring[i]))
    out.append('</g>')
    out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" '
               'stroke-width="%.2f"/>' % (cx, cy, r, mono or inner, R * 0.085))
    out.append('<text x="%.2f" y="%.2f" text-anchor="middle" dominant-baseline="central" '
               'font-family="%s" font-weight="800" font-size="%.2f" fill="%s">%s</text>'
               % (cx, cy, font, r * 0.66, mono or ink or inner, label))
    out.append('</svg>')
    return '\n'.join(out)


# ── подпись студии: «е», которая на самом деле «ё» ──────────────────────────
def draw_studio(c, txt, x, y, шрифт, кегль, тр, цвет, акцент, вырав='c'):
    """Рисует подпись, выделяя в имени букву «е».

    По-русски студия зовётся Настёна, но в латинской раскладке буквы «ё» нет.
    Две точки над «е» возвращают её на место — и заодно читаются как
    неподелённая электронная пара над атомом. Для химического класса это
    не украшение, а его собственный знак препинания.
    """
    from reportlab.pdfbase import pdfmetrics
    ш = [pdfmetrics.stringWidth(з, шрифт, кегль) for з in txt]
    всего = sum(ш) + тр * max(0, len(txt) - 1)
    if вырав == 'c': x -= всего / 2.0
    elif вырав == 'r': x -= всего

    верх = txt.upper()
    метка = верх.find('NAST')
    цель = метка + 4 if метка >= 0 else -1     # буква «е» в имени

    c.setFont(шрифт, кегль)
    курсор = x
    центр = None
    for i, (з, w) in enumerate(zip(txt, ш)):
        c.setFillColor(акцент if i == цель else цвет)
        c.drawString(курсор, y, з)
        if i == цель:
            центр = курсор + w / 2.0
        курсор += w + тр

    if центр is not None:
        r = кегль * 0.064
        c.setFillColor(акцент)
        c.circle(центр - кегль * 0.13, y + кегль * 0.86, r, stroke=0, fill=1)
        c.circle(центр + кегль * 0.13, y + кегль * 0.86, r, stroke=0, fill=1)
    return всего
