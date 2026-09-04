# -*- coding: utf-8 -*-
"""Данные книги → JSON для веб-версии. Один источник на печать и на сайт."""
import os, sys, json
ЗДЕСЬ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ЗДЕСЬ)
from data import LESSON_TIMES, INTERVALS, FAMILY, WEEK

import importlib.util
спец = importlib.util.spec_from_file_location('кн', os.path.join(ЗДЕСЬ, 'книга-крафт.py'))
# краски и знаки берём из крафтовой книги, не дублируя их руками
КРАСКА = {
    'math': '#C8821C', 'phys': '#1F7F3C', 'chem': '#C33A48', 'bio':  '#C55A1D',
    'lit':  '#7A4A86', 'rus':  '#A76E96', 'hist': '#3E5C86', 'soc':  '#7A705F',
    'eng':  '#17806E', 'inf':  '#86913A', 'obzr': '#5C6320', 'pe':   '#3B4A72',
}
ЗНАК = {
    'math': 'Мт', 'phys': 'Фз', 'chem': 'Хм', 'bio': 'Бл', 'lit': 'Лт', 'rus': 'Рс',
    'hist': 'Ис', 'soc': 'Оз', 'eng': 'Ан', 'inf': 'Иф', 'obzr': 'Бз', 'pe': 'Фр',
}

данные = {
    'lessons': {str(k): list(v) for k, v in LESSON_TIMES.items()},
    'intervals': [{'kind': k, 'name': n, 'a': a, 'b': b} for k, n, a, b in INTERVALS],
    'family': {k: {'ink': v[0], 'kraft': КРАСКА[k], 'symbol': ЗНАК[k], 'title': v[1]}
               for k, v in FAMILY.items()},
    'week': [{'name': d[0], 'short': d[1],
              'blocks': [{'l0': b[0], 'l1': b[1], 'fam': b[2], 'name': b[3],
                          'note': b[4], 'teacher': b[5], 'room': b[6]} for b in d[2]]}
             for d in WEEK],
}

путь = os.path.join(ЗДЕСЬ, 'web', 'src', 'data.json')
os.makedirs(os.path.dirname(путь), exist_ok=True)
with open(путь, 'w', encoding='utf-8') as f:
    json.dump(данные, f, ensure_ascii=False, indent=1)
print('ОК →', путь, os.path.getsize(путь), 'байт')
