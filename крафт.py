# -*- coding: utf-8 -*-
"""Крафтовая бумага: волокно, крапины, выцветание к краям.

Лист печатается один раз в `assets/kraft.jpg` и дальше только подкладывается —
пересчитывать шум на каждую полосу незачем, а зерно должно быть одним и тем же
на всей книге, как у настоящей пачки бумаги.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ОСНОВА = (201, 168, 125)          # крафт при дневном свете
Ш, В = 1654, 2339                 # А4 при 200 dpi — зерна хватает, вес разумный


def лист(путь, seed=7, ширина=Ш, высота=В):
    if os.path.exists(путь):
        return путь
    rng = np.random.default_rng(seed)

    # масса листа: ровный тон, мелкое зерно и еле заметная неравномерность
    мелкий = rng.random((высота // 30 + 2, ширина // 30 + 2))
    разводы = np.asarray(Image.fromarray((мелкий * 255).astype('uint8'))
                         .resize((ширина, высота), Image.BICUBIC), dtype=float)
    разводы = (разводы - разводы.mean()) / (разводы.std() + 1e-6)
    поле = разводы * 2.2 + rng.normal(0, 4.6, (высота, ширина))

    холст = np.empty((высота, ширина, 3), dtype=float)
    for i, c in enumerate(ОСНОВА):
        холст[:, :, i] = c + поле * (0.92 + 0.10 * i)

    # выцветание к краям: лист лежал на свету
    yy, xx = np.mgrid[0:высота, 0:ширина]
    r = (((xx - ширина / 2) / (ширина / 2)) ** 2 +
         ((yy - высота / 2) / (высота / 2)) ** 2)
    холст += (r * -8.0)[:, :, None]

    im = Image.fromarray(np.clip(холст, 0, 255).astype('uint8'), 'RGB').convert('RGBA')

    # волокна: длинные полупрозрачные штрихи, светлее и темнее массы
    волокна = Image.new('RGBA', (ширина, высота), (0, 0, 0, 0))
    d = ImageDraw.Draw(волокна)
    for _ in range(11000):
        x, y = int(rng.integers(0, ширина)), int(rng.integers(0, высота))
        L = float(rng.integers(10, 80))
        a = rng.normal(0.0, 0.55) + (0.0 if rng.random() < 0.5 else 1.5708)
        св = rng.random() < 0.52
        t = int(rng.integers(14, 30))
        alpha = int(rng.integers(16, 42))
        цв = tuple(int(min(255, max(0, c + (t if св else -t)))) for c in ОСНОВА)
        d.line([(x, y), (x + L * np.cos(a), y + L * np.sin(a))],
               fill=цв + (alpha,), width=1)
    im = Image.alpha_composite(im, волокна.filter(ImageFilter.GaussianBlur(0.35)))

    # крапины: тёмные включения древесины
    точки = Image.new('RGBA', (ширина, высота), (0, 0, 0, 0))
    d = ImageDraw.Draw(точки)
    for _ in range(1600):
        x, y = int(rng.integers(0, ширина)), int(rng.integers(0, высота))
        s = int(rng.integers(1, 4))
        t = int(rng.integers(22, 55))
        цв = tuple(int(max(0, c - t)) for c in ОСНОВА)
        d.ellipse([x, y, x + s, y + s], fill=цв + (int(rng.integers(70, 150)),))
    im = Image.alpha_composite(im, точки)

    im.convert('RGB').save(путь, 'JPEG', quality=90, optimize=True)
    return путь


if __name__ == '__main__':
    здесь = os.path.dirname(os.path.abspath(__file__))
    п = лист(os.path.join(здесь, 'assets', 'kraft.jpg'))
    print('ОК →', п, os.path.getsize(п), 'байт')
