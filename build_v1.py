# -*- coding: utf-8 -*-
"""ХРОНОХРОМ — расписание 10-Л, СУНЦ МГУ. Сборка PDF."""
import os, sys
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import LESSON_TIMES, INTERVALS, FAMILY, WEEK, CLASSROOM

BASE = os.path.dirname(os.path.abspath(__file__))
FDIR = os.path.join(BASE, 'fonts')
OUT = os.path.join(BASE, 'out', 'v1-raspisanie-10L-SUNC-MGU.pdf')

W, H = 1190.55, 841.89           # A3 landscape
M = 56.0

for name, fn in [
    ('Disp', 'Unbounded-800.ttf'), ('DispMid', 'Unbounded-600.ttf'),
    ('Sans', 'Manrope-400.ttf'), ('SansMid', 'Manrope-600.ttf'),
    ('SansBold', 'Manrope-800.ttf'),
    ('Mono', 'JetBrainsMono-Regular.ttf'), ('MonoBold', 'JetBrainsMono-Bold.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FDIR, fn)))

INK      = HexColor('#0A0D13')
INK_UP   = HexColor('#11161F')
INK_LINE = HexColor('#1E2635')
PAPER    = HexColor('#EEF2F8')
AMBER    = HexColor('#FFC53D')
MUTED    = HexColor('#66748C')
MUTED2   = HexColor('#3F4A5D')

DAY_START, DAY_END = 8 * 60 + 45, 16 * 60 + 45
SPAN = float(DAY_END - DAY_START)


def mix(a, b, t):
    return Color(a.red + (b.red - a.red) * t, a.green + (b.green - a.green) * t,
                 a.blue + (b.blue - a.blue) * t)


def hhmm(m):
    return '%02d:%02d' % (m // 60, m % 60)


def tracked(c, txt, x, y, font, size, tr, color, align='l'):
    c.setFont(font, size); c.setFillColor(color)
    ws = [pdfmetrics.stringWidth(ch, font, size) for ch in txt]
    total = sum(ws) + tr * max(0, len(txt) - 1)
    if align == 'c': x -= total / 2.0
    elif align == 'r': x -= total
    for ch, w in zip(txt, ws):
        c.drawString(x, y, ch); x += w + tr
    return total


def tw(txt, font, size, tr):
    return sum(pdfmetrics.stringWidth(ch, font, size) for ch in txt) + tr * max(0, len(txt) - 1)


def ground(c):
    c.setFillColor(INK); c.rect(0, 0, W, H, stroke=0, fill=1)


def hairline(c, x1, y, x2, color=INK_LINE, w=0.6):
    c.setStrokeColor(color); c.setLineWidth(w); c.line(x1, y, x2, y)


def folio(c, left, right):
    tracked(c, left, M, M - 22, 'Mono', 6.6, 1.5, MUTED2)
    tracked(c, right, W - M, M - 22, 'Mono', 6.6, 1.5, MUTED2, align='r')


def running_head(c, right_txt):
    tracked(c, 'СУНЦ МГУ · ШКОЛА-ИНТЕРНАТ ИМЕНИ А. Н. КОЛМОГОРОВА', M, H - M - 4,
            'Mono', 6.8, 1.9, MUTED2)
    tracked(c, right_txt, W - M, H - M - 4, 'Mono', 6.8, 1.9, MUTED2, align='r')


def title(c, word, tail):
    tracked(c, word, M, H - 148, 'Disp', 52, 2.5, PAPER)
    tracked(c, tail, M + tw(word, 'Disp', 52, 2.5) + 32, H - 140, 'Mono', 9, 2.2, MUTED)
    hairline(c, M, H - 172, W - M, MUTED2, 0.5)


def day_blocks(day):
    return [(LESSON_TIMES[l0][0], LESSON_TIMES[l1][1], fam, nm, note, t, r, l0, l1)
            for l0, l1, fam, nm, note, t, r in day[2]]


def day_facts(day):
    b = day_blocks(day)
    slots = sum(x[8] - x[7] + 1 for x in b)
    return slots, slots * 45, b[0][0], b[-1][1]


def meals_in_day():
    out = []
    for kind, nm, a, b in INTERVALS:
        if kind != 'meal': continue
        a2, b2 = max(a, DAY_START), min(b, DAY_END)
        if b2 - a2 >= 10:
            out.append((nm, a2, b2))
    return out


# ── мини-карта недели ───────────────────────────────────────────────────────
def week_map(c, x, y, w, h, active=None, gap=5.0):
    colw = w / 6.0
    for di, day in enumerate(WEEK):
        cx = x + di * colw
        on = (active is None) or (di == active)
        tracked(c, day[1].upper(), cx + (colw - gap) / 2.0, y + h + 9,
                'MonoBold' if on else 'Mono', 7.4, 1.6,
                PAPER if on else MUTED2, align='c')
        c.setFillColor(INK_UP if on else mix(INK, INK_UP, 0.55))
        c.rect(cx, y, colw - gap, h, stroke=0, fill=1)
        for hh in range(9, 17):
            yy = y + h - (hh * 60 - DAY_START) / SPAN * h
            hairline(c, cx, yy, cx + colw - gap, mix(INK, PAPER, 0.06), 0.35)
        for (m0, m1, fam, *_rest) in day_blocks(day):
            by = y + h - (m1 - DAY_START) / SPAN * h
            bh = (m1 - m0) / SPAN * h
            col = HexColor(FAMILY[fam][0])
            c.setFillColor(col if on else mix(INK, col, 0.36))
            c.rect(cx, by, colw - gap, bh, stroke=0, fill=1)


# ── 01 · обложка ────────────────────────────────────────────────────────────
def page_cover(c):
    ground(c)
    running_head(c, 'I СЕМЕСТР 2026/27')

    sx = M + 40
    sw = W - M - sx
    sy, sh = 112.0, 292.0
    colw = sw / 6.0
    gap = 11.0

    for hh in range(9, 17):
        yy = sy + sh - (hh * 60 - DAY_START) / SPAN * sh
        hairline(c, sx - 8, yy, sx + sw - gap, mix(INK, PAPER, 0.09), 0.4)
        tracked(c, '%02d' % hh, sx - 14, yy - 3, 'Mono', 7.4, 0.8, MUTED2, align='r')

    for di, day in enumerate(WEEK):
        cx = sx + di * colw
        c.setFillColor(INK_UP)
        c.rect(cx, sy, colw - gap, sh, stroke=0, fill=1)
        for hh in range(9, 17):
            yy = sy + sh - (hh * 60 - DAY_START) / SPAN * sh
            hairline(c, cx, yy, cx + colw - gap, mix(INK, PAPER, 0.07), 0.4)
        for (m0, m1, fam, *_r) in day_blocks(day):
            by = sy + sh - (m1 - DAY_START) / SPAN * sh
            bh = (m1 - m0) / SPAN * sh
            c.setFillColor(HexColor(FAMILY[fam][0]))
            c.rect(cx, by, colw - gap, bh, stroke=0, fill=1)
        tracked(c, '0%d' % (di + 1), cx + (colw - gap) / 2, sy + sh + 12, 'Mono',
                7.2, 1.4, MUTED2, align='c')
        tracked(c, day[0].upper(), cx + (colw - gap) / 2, sy - 21, 'Mono', 7.6, 2.2,
                MUTED, align='c')
        nsl = sum(l1 - l0 + 1 for l0, l1, *_ in day[2])
        tracked(c, '%d %s' % (nsl, 'УРОКА' if nsl in (2, 3, 4) else 'УРОКОВ'),
                cx + (colw - gap) / 2, sy - 35, 'Mono', 6.6, 1.6, MUTED2, align='c')
    hairline(c, sx - 8, sy - 50, W - M, MUTED2, 0.5)

    tracked(c, '10-Л', M - 6, 486, 'Disp', 186, -4, PAPER)
    wq = tw('10-Л', 'Disp', 186, -4)
    tx = M + wq + 32
    tracked(c, 'РАСПИСАНИЕ', tx, 600, 'DispMid', 29, 4, AMBER)
    tracked(c, 'УЧЕБНЫХ ЗАНЯТИЙ', tx, 561, 'DispMid', 29, 4, mix(INK, PAPER, 0.55))
    hairline(c, tx + 2, 541, W - M, MUTED2, 0.5)
    tracked(c, 'I СЕМЕСТР 2026/27', tx, 514, 'Mono', 8.4, 2.4, MUTED)
    tracked(c, 'КАБИНЕТ 40', tx + 190, 514, 'Mono', 8.4, 2.4, MUTED)
    tracked(c, '38 УРОКОВ В НЕДЕЛЮ', tx + 330, 514, 'Mono', 8.4, 2.4, MUTED)
    tracked(c, 'ХРОНОХРОМ · ВРЕМЯ, РАЗЛОЖЕННОЕ В СПЕКТР', W - M, 486, 'Mono', 7.6,
            2.6, MUTED2, align='r')

    folio(c, 'ИСТОЧНИК: INTERNAT.MSU.RU', '01')


# ── 02 · звонки ─────────────────────────────────────────────────────────────
def page_bells(c):
    ground(c)
    running_head(c, 'РИТМ ДНЯ · 02')
    title(c, 'ЗВОНКИ', 'ЕДИНАЯ СЕТКА ДЛЯ ВСЕХ КЛАССОВ · 8 УРОКОВ ПО 45 МИНУТ')

    rows = [('lesson', str(n), 'урок', a, b) for n, (a, b) in sorted(LESSON_TIMES.items())]
    rows += [(k, '', nm, a, b) for k, nm, a, b in INTERVALS]
    rows.sort(key=lambda r: r[3])

    y = H - 226
    for kind, num, nm, a, b in rows:
        L = kind == 'lesson'
        col = PAPER if L else (AMBER if kind == 'meal' else MUTED2)
        rowh = 36.0 if L else 24.0
        if L:
            c.setFillColor(INK_UP); c.rect(M, y - 9, W - 2 * M, rowh - 7, stroke=0, fill=1)
            c.setFillColor(AMBER); c.rect(M, y - 9, 3.2, rowh - 7, stroke=0, fill=1)
        tracked(c, num, M + 22, y, 'Disp', 21, 0, PAPER)
        tracked(c, nm.upper(), M + 74, y + (3 if L else 0),
                'SansBold' if L else 'Mono', 15 if L else 8.6, 2.6 if L else 2.0, col)
        tracked(c, hhmm(a), 470, y + (3 if L else 0), 'MonoBold' if L else 'Mono',
                17 if L else 10, 0.6, col)
        tracked(c, '—', 548, y + (3 if L else 0), 'Mono', 11, 0, MUTED2)
        tracked(c, hhmm(b), 574, y + (3 if L else 0), 'MonoBold' if L else 'Mono',
                17 if L else 10, 0.6, col)
        tracked(c, '%d мин' % (b - a), 700, y + (3 if L else 0), 'Mono',
                10 if L else 8.6, 0.8, MUTED if L else MUTED2)
        bx = 782.0
        scale = (W - M - bx) / 60.0
        c.setFillColor(col if L else mix(INK, col, 0.5))
        c.rect(bx, y + (1 if L else 0), (b - a) * scale, 7 if L else 3, stroke=0, fill=1)
        y -= rowh

    hairline(c, M, y + 6, W - M, MUTED2, 0.5)
    tracked(c, 'ПОЛДНИК В ИСТОЧНИКЕ НАЧИНАЕТСЯ В 16:40 — НА ПЯТЬ МИНУТ РАНЬШЕ КОНЦА 8-ГО УРОКА',
            M, y - 18, 'Mono', 7.2, 1.6, MUTED2)
    folio(c, 'ЗВОНКИ · ВСЕ КЛАССЫ', '02')


# ── 03–08 · дни ─────────────────────────────────────────────────────────────
def page_day(c, di):
    day = WEEK[di]
    blocks = day_blocks(day)
    slots, mins, m0, m1 = day_facts(day)

    ground(c)
    running_head(c, '%s · %02d' % (day[0].upper(), di + 3))
    word = day[0].upper()
    tracked(c, word, M, H - 148, 'Disp', 52, 2.5, PAPER)
    tail = '%d %s' % (slots, 'УРОКА' if slots in (2, 3, 4) else 'УРОКОВ')
    x2 = M + tw(word, 'Disp', 52, 2.5) + 32
    xh, yh = x2, H - 140
    xh += tracked(c, tail, xh, yh, 'MonoBold', 9, 2.2, AMBER) + 13
    xh += tracked(c, '·', xh, yh, 'Mono', 9, 0, MUTED2) + 13
    xh += tracked(c, '%s — %s' % (hhmm(m0), hhmm(m1)), xh, yh, 'Mono', 9, 2.2, MUTED) + 13
    xh += tracked(c, '·', xh, yh, 'Mono', 9, 0, MUTED2) + 13
    tracked(c, '%d Ч %02d МИН' % (mins // 60, mins % 60), xh, yh, 'Mono', 9, 2.2, MUTED)
    hairline(c, M, H - 172, W - M, MUTED2, 0.5)

    ty, th = 100.0, H - 172 - 34 - 100.0
    ax0, ax1 = M + 54, 942.0
    META = 132.0

    def yp(m):
        return ty + th - (m - DAY_START) / SPAN * th

    for hh in range(9, 17):
        yy = yp(hh * 60)
        hairline(c, ax0 - 6, yy, ax1, mix(INK, PAPER, 0.085), 0.4)
        tracked(c, '%02d' % hh, ax0 - 14, yy - 3, 'Mono', 8.6, 0.8, MUTED2, align='r')

    for nm, a, b in meals_in_day():
        yb, yt = yp(b), yp(a)
        c.setFillColor(mix(INK, AMBER, 0.13))
        c.rect(ax0, yb, ax1 - ax0, yt - yb, stroke=0, fill=1)
        tracked(c, nm.upper(), ax1 - 10, yb + (yt - yb) / 2 - 3, 'Mono', 7, 1.8,
                mix(INK, AMBER, 0.62), align='r')

    for (bm0, bm1, fam, name, note, teach, room, l0, l1) in blocks:
        col = HexColor(FAMILY[fam][0])
        yb, yt = yp(bm1), yp(bm0)
        bh = yt - yb
        c.setFillColor(col)
        c.roundRect(ax0, yb + 2, ax1 - ax0, bh - 4, 5, stroke=0, fill=1)

        # мета-полоса: каждый урок отдельным телом, перемены — провалы в чернила
        for n in range(l0, l1 + 1):
            a, b = LESSON_TIMES[n]
            sb, st = yp(b), yp(a)
            c.setFillColor(mix(col, INK, 0.15))
            c.rect(ax0 + 2, sb + 2, META, st - sb - 4, stroke=0, fill=1)
            ic2 = mix(col, INK, 0.72)
            tracked(c, str(n), ax0 + 16, st - 22, 'Disp', 15, 0, mix(col, INK, 0.55))
            tracked(c, hhmm(a), ax0 + 44, st - 16, 'MonoBold', 8.6, 0.7, ic2)
            tracked(c, hhmm(b), ax0 + 44, st - 27, 'Mono', 8.6, 0.7, mix(col, INK, 0.5))

        ic = mix(col, INK, 0.88)
        nx = ax0 + META + 44
        ns = 28 if bh > 92 else 21
        cy = yb + bh / 2
        tracked(c, name, nx, cy - ns * 0.34, 'SansBold', ns, 0.4, ic)
        if note:
            tracked(c, note.upper(), nx + tw(name, 'SansBold', ns, 0.4) + 16,
                    cy - 3.4, 'Mono', 7.6, 1.6, mix(col, INK, 0.48))
        rx = ax1 - 22
        if room:
            tracked(c, room, rx, cy - 6, 'MonoBold', 13, 1.2, ic, align='r')
            tracked(c, 'КАБ.', rx - tw(room, 'MonoBold', 13, 1.2) - 9, cy - 5, 'Mono',
                    6.6, 1.4, mix(col, INK, 0.46), align='r')
        if teach:
            tracked(c, teach, rx, cy - 23, 'SansMid', 10, 0.5, mix(col, INK, 0.62),
                    align='r')

    busy = set()
    for b in blocks:
        busy.update(range(b[7], b[8] + 1))
    for n in range(1, 9):
        if n in busy: continue
        a, b = LESSON_TIMES[n]
        yb, yt = yp(b), yp(a)
        c.setStrokeColor(INK_LINE); c.setDash(2, 4); c.setLineWidth(0.7)
        c.roundRect(ax0, yb + 2, ax1 - ax0, yt - yb - 4, 5, stroke=1, fill=0)
        c.setDash()
        tracked(c, str(n), ax0 + 16, yb + (yt - yb) / 2 - 4, 'Disp', 15, 0, MUTED2)
        tracked(c, 'СВОБОДНО', ax0 + META + 44, yb + (yt - yb) / 2 - 3, 'Mono', 7.8,
                2.6, MUTED2)

    week_map(c, 988, ty, W - M - 988, th, active=di)
    tracked(c, 'НЕДЕЛЯ', 988, ty + th + 24, 'Mono', 7, 2.4, MUTED2)
    folio(c, '10-Л · %s · КАБ. 40' % word, '%02d' % (di + 3))


# ── 09 · неделя ─────────────────────────────────────────────────────────────
def page_week(c):
    ground(c)
    running_head(c, 'НЕДЕЛЯ ЦЕЛИКОМ · 09')
    title(c, 'НЕДЕЛЯ', '38 УРОКОВ · 6 ДНЕЙ · 28 Ч 30 МИН')

    ty, th = 96.0, H - 172 - 44 - 96.0
    ax0, ax1 = M + 124, W - M
    colw = (ax1 - ax0) / 6.0
    gap = 7.0

    def yp(m):
        return ty + th - (m - DAY_START) / SPAN * th

    for n in range(1, 9):
        a, b = LESSON_TIMES[n]
        yb, yt = yp(b), yp(a)
        hairline(c, M + 46, yt, ax1, mix(INK, PAPER, 0.07), 0.4)
        tracked(c, str(n), M + 52, (yb + yt) / 2 - 5, 'Disp', 13, 0, MUTED)
        tracked(c, hhmm(a), M + 72, (yb + yt) / 2 + 1, 'Mono', 7.4, 0.6, MUTED)
        tracked(c, hhmm(b), M + 72, (yb + yt) / 2 - 9, 'Mono', 7.4, 0.6, MUTED2)
    hairline(c, M + 46, yp(DAY_END), ax1, mix(INK, PAPER, 0.07), 0.4)

    for nm, a, b in meals_in_day():
        yb, yt = yp(b), yp(a)
        c.setFillColor(mix(INK, AMBER, 0.12))
        c.rect(ax0, yb, ax1 - ax0 - gap, yt - yb, stroke=0, fill=1)
        c.setFillColor(mix(INK, AMBER, 0.5))
        c.rect(M, yb, 3, yt - yb, stroke=0, fill=1)
        tracked(c, nm.upper(), M + 8, (yb + yt) / 2 - 3, 'Mono', 6.4, 1.2,
                mix(INK, AMBER, 0.72))

    for di, day in enumerate(WEEK):
        cx = ax0 + di * colw
        tracked(c, day[0].upper(), cx + (colw - gap) / 2, ty + th + 18, 'DispMid',
                12.5, 2.2, PAPER, align='c')
        c.setFillColor(INK_UP)
        c.rect(cx, ty, colw - gap, th, stroke=0, fill=1)
        for (bm0, bm1, fam, name, note, teach, room, l0, l1) in day_blocks(day):
            col = HexColor(FAMILY[fam][0])
            yb, yt = yp(bm1), yp(bm0)
            bh = yt - yb
            c.setFillColor(col)
            c.roundRect(cx, yb + 1.5, colw - gap, bh - 3, 3.5, stroke=0, fill=1)
            ic = mix(col, INK, 0.88)
            fs, avail = 12.5, colw - gap - 20
            while max(pdfmetrics.stringWidth(w, 'SansBold', fs) for w in name.split()) > avail:
                fs -= 0.5
            lines, cur = [], ''
            for w in name.split():
                t = (cur + ' ' + w).strip()
                if pdfmetrics.stringWidth(t, 'SansBold', fs) <= avail: cur = t
                else: lines.append(cur); cur = w
            lines.append(cur)
            yy = yb + bh / 2 + (len(lines) - 1) * (fs * 0.56) - fs * 0.34
            for ln in lines:
                tracked(c, ln, cx + (colw - gap) / 2, yy, 'SansBold', fs, 0.2, ic, align='c')
                yy -= fs * 1.14
            if room and bh > 42:
                tracked(c, room, cx + (colw - gap) / 2, yb + 9, 'Mono', 7.6, 1.0,
                        mix(col, INK, 0.5), align='c')
            if teach and bh > 76:
                tracked(c, teach, cx + (colw - gap) / 2, yt - 16, 'SansMid', 7.6, 0.3,
                        mix(col, INK, 0.56), align='c')
            if note and bh > 76:
                tracked(c, note.upper(), cx + (colw - gap) / 2, yb + 20, 'Mono', 6.4,
                        1.4, mix(col, INK, 0.46), align='c')
    folio(c, '10-Л · I СЕМЕСТР 2026/27', '09')


# ── 10 · спектр ─────────────────────────────────────────────────────────────
def page_legend(c):
    ground(c)
    running_head(c, 'СПЕКТР ПРЕДМЕТОВ · 10')
    title(c, 'СПЕКТР', 'ЧАСЫ ПО ПРЕДМЕТАМ ЗА НЕДЕЛЮ · 1 УРОК = 45 МИНУТ')

    tally = {}
    for day in WEEK:
        for l0, l1, fam, *_ in day[2]:
            tally[fam] = tally.get(fam, 0) + (l1 - l0 + 1)
    order = sorted(tally.items(), key=lambda kv: (-kv[1], FAMILY[kv[0]][1]))
    top = max(v for _, v in order)

    y, rowh = H - 222, 33.5
    bx = M + 306
    bw = W - M - 46 - bx
    for fam, n in order:
        col = HexColor(FAMILY[fam][0])
        c.setFillColor(col); c.roundRect(M, y - 5, 20, 19, 3, stroke=0, fill=1)
        tracked(c, FAMILY[fam][1].upper(), M + 36, y, 'SansBold', 12.5, 2.0, PAPER)
        c.setFillColor(mix(INK, col, 0.15)); c.roundRect(bx, y - 5, bw, 19, 3, stroke=0, fill=1)
        c.setFillColor(col); c.roundRect(bx, y - 5, bw * n / float(top), 19, 3, stroke=0, fill=1)
        for k in range(n):
            c.setFillColor(mix(col, INK, 0.74))
            c.circle(bx + bw * (k + 0.5) / float(top), y + 4.5, 2.0, stroke=0, fill=1)
        tracked(c, str(n), bx - 16, y, 'Disp', 14, 0, col, align='r')
        tracked(c, '%d:%02d' % (n * 45 // 60, n * 45 % 60), W - M, y, 'Mono', 9.6,
                0.8, MUTED, align='r')
        y -= rowh

    hairline(c, M, y + 8, W - M, MUTED2, 0.5)
    tracked(c, 'ВСЕГО', M + 36, y - 18, 'Disp', 14, 2.4, PAPER)
    tracked(c, '38 УРОКОВ', bx, y - 18, 'MonoBold', 10.5, 2.0, AMBER)
    tracked(c, '28 Ч 30 МИН', W - M, y - 18, 'Mono', 9.6, 0.8, MUTED, align='r')

    # лента недели: 38 уроков подряд
    ry, rh = 118.0, 46.0
    total = sum(sum(l1 - l0 + 1 for l0, l1, *_ in d[2]) for d in WEEK)
    dgap = 12.0
    unit = (W - 2 * M - dgap * 5) / float(total)
    x = M
    for di, day in enumerate(WEEK):
        d0 = x
        for l0, l1, fam, name, *_ in day[2]:
            n = l1 - l0 + 1
            c.setFillColor(HexColor(FAMILY[fam][0]))
            c.roundRect(x + 1, ry, unit * n - 2, rh, 2.5, stroke=0, fill=1)
            x += unit * n
        tracked(c, day[0].upper(), (d0 + x) / 2, ry - 15, 'Mono', 6.8, 1.8, MUTED, align='c')
        x += dgap
    tracked(c, 'ЛЕНТА НЕДЕЛИ · КАЖДЫЙ СЕГМЕНТ — ОДИН УРОК', M, ry + rh + 12, 'Mono',
            7, 2.4, MUTED2)
    tracked(c, 'ДАННЫЕ: INTERNAT.MSU.RU · РАСПИСАНИЕ НА I СЕМЕСТР 2026/27 · КОЛОНКА 10-Л',
            W - M, ry + rh + 12, 'Mono', 7, 1.8, MUTED2, align='r')
    folio(c, 'ХРОНОХРОМ', '10')


def main():
    c = rl_canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle('Расписание 10-Л · СУНЦ МГУ · I семестр 2026/27')
    c.setAuthor('internat.msu.ru')
    c.setSubject('Хронохром — расписание учебных занятий 10-Л')
    page_cover(c); c.showPage()
    page_bells(c); c.showPage()
    for di in range(6):
        page_day(c, di); c.showPage()
    page_week(c); c.showPage()
    page_legend(c); c.showPage()
    c.save()
    print('OK →', OUT, os.path.getsize(OUT), 'bytes')


if __name__ == '__main__':
    main()
