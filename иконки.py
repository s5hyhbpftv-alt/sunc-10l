# -*- coding: utf-8 -*-
"""Иконки приложения из той же геометрии, что и знак в книгах.

Рисуем знак в PDF средствами reportlab (одна правда о форме — marks.py),
растрируем pdftoppm и режем на нужные размеры. Так иконка не разъезжается
с обложками, когда меняется знак.
"""
import os, subprocess, sys
from reportlab.pdfgen import canvas as rl
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image

ЗДЕСЬ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ЗДЕСЬ)
from marks import draw_signet

ВЫХОД = os.path.join(ЗДЕСЬ, 'web', 'public')
ЧЕРНИЛА = '#0A0D13'
pdfmetrics.registerFont(TTFont('Disp', os.path.join(ЗДЕСЬ, 'fonts', 'Unbounded-800.ttf')))


def знак(путь_pdf, сторона, доля):
    """доля — какую часть квадрата занимает знак по ширине."""
    c = rl.Canvas(путь_pdf, pagesize=(сторона, сторона))
    c.setFillColor(HexColor(ЧЕРНИЛА))
    c.rect(0, 0, сторона, сторона, stroke=0, fill=1)
    # ширина шестиугольника «остриём вверх» = 2R·sin60
    R = сторона * доля / 2 / 0.8660254
    draw_signet(c, сторона / 2, сторона / 2, R, 'Disp', ink='#EEF2F8')
    c.save()


def растр(путь_pdf, сторона, путь_png):
    корень = путь_pdf[:-4]
    subprocess.run(['pdftoppm', '-png', '-r', str(72 * сторона / 512 * (512 / сторона)),
                    '-scale-to', str(сторона), путь_pdf, корень], check=True)
    готово = корень + '-1.png'
    Image.open(готово).convert('RGB').save(путь_png)
    os.remove(готово)


def главная():
    врем = os.path.join(ЗДЕСЬ, 'out', '_icon.pdf')
    os.makedirs(ВЫХОД, exist_ok=True)
    # обычная иконка: знак почти во весь квадрат
    знак(врем, 512, 0.74)
    for n in (512, 192, 180):
        имя = 'icon-%d.png' % n if n != 180 else 'apple-touch-icon.png'
        растр(врем, n, os.path.join(ВЫХОД, имя))
    # маскируемая: система обрежет углы, поэтому знак ужимаем в безопасную зону
    знак(врем, 512, 0.56)
    растр(врем, 512, os.path.join(ВЫХОД, 'icon-maskable-512.png'))
    os.remove(врем)
    print('ОК → иконки в', ВЫХОД)


if __name__ == '__main__':
    главная()
