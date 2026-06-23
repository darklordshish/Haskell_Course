import json, os

BASE = '/home/jovyan/src'

def load_nb(name):
    path = os.path.join(BASE, name + '.ipynb')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f), path

def save_nb(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

def get_src(cell):
    s = cell['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(cell, text):
    cell['source'] = text

def fix_nav(nb_name, old_prev, new_prev, old_next, new_next):
    nb, path = load_nb(nb_name)
    cells = nb['cells']
    last = cells[-1]
    src = get_src(last)
    changed = False
    if old_prev and old_prev in src:
        src = src.replace(old_prev, new_prev)
        changed = True
    if old_next and old_next in src:
        src = src.replace(old_next, new_next)
        changed = True
    if changed:
        set_src(last, src)
        save_nb(nb, path)
        print(f'  {nb_name}: NAV обновлён')
        print(f'    -> {src.strip()}')
    else:
        print(f'  {nb_name}: ничего не изменилось (искал: prev={old_prev!r}, next={old_next!r})')
        print(f'    текущий NAV: {src.strip()}')

# Текущий порядок: ... YonedaLemma -> KanExtensions -> Adjunctions -> MetaProgramming ...
# Новый порядок:   ... YonedaLemma -> Adjunctions -> KanExtensions -> MetaProgramming ...

print('=== Меняем порядок: Adjunctions перед KanExtensions ===')

# YonedaLemma: Следующий KanExtensions -> Adjunctions
fix_nav('YonedaLemma',
    None, None,
    '[KanExtensions](KanExtensions.ipynb)', '[Adjunctions](Adjunctions.ipynb)')

# Adjunctions: Предыдущий KanExtensions -> YonedaLemma, Следующий MetaProgramming -> KanExtensions
fix_nav('Adjunctions',
    '[KanExtensions](KanExtensions.ipynb)', '[YonedaLemma](YonedaLemma.ipynb)',
    '[MetaProgramming](MetaProgramming.ipynb)', '[KanExtensions](KanExtensions.ipynb)')

# KanExtensions: Предыдущий YonedaLemma -> Adjunctions, Следующий Adjunctions -> MetaProgramming
fix_nav('KanExtensions',
    '[YonedaLemma](YonedaLemma.ipynb)', '[Adjunctions](Adjunctions.ipynb)',
    '[Adjunctions](Adjunctions.ipynb)', '[MetaProgramming](MetaProgramming.ipynb)')

# MetaProgramming: Предыдущий Adjunctions -> KanExtensions
fix_nav('MetaProgramming',
    '[Adjunctions](Adjunctions.ipynb)', '[KanExtensions](KanExtensions.ipynb)',
    None, None)

print('\n=== Обновляем README.ipynb ===')
# В README меняем порядок строк таблицы: строка 11 Расширения Кана <-> строка 12 Сопряжения
nb, path = load_nb('README')
cells = nb['cells']
for i, cell in enumerate(cells):
    src = get_src(cell)
    if 'Расширения Кана' in src and 'Сопряжения' in src and '|' in src:
        # Найти строки таблицы и поменять местами
        lines = src.split('\n')
        kan_idx = next((j for j, l in enumerate(lines) if 'Расширения Кана' in l and '|' in l), None)
        adj_idx = next((j for j, l in enumerate(lines) if 'Сопряжения' in l and '|' in l and 'Расширения' not in l), None)
        if kan_idx is not None and adj_idx is not None:
            # Меняем местами строки
            lines[kan_idx], lines[adj_idx] = lines[adj_idx], lines[kan_idx]
            # Обновляем нумерацию (если есть | 11 | и | 12 |)
            set_src(cell, '\n'.join(lines))
            save_nb(nb, path)
            print(f'  README ячейка {i}: строки поменяны местами')
            print(f'    Расширения Кана: строка {kan_idx}, Сопряжения: строка {adj_idx}')
            break
else:
    print('  README: ячейка с таблицей не найдена или уже правильный порядок')

print('\nГотово!')
