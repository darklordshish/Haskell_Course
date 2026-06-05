import json, hashlib, re, os

def cid(s):
    return 'cmp' + hashlib.md5(s.encode()).hexdigest()[:8]

def md_cell(src):
    lines = src.split('\n')
    source = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type":"markdown","id":cid(src),"metadata":{},"source":source}

def code_cell(src):
    lines = src.split('\n')
    source = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type":"code","execution_count":None,"id":cid(src),"metadata":{},"outputs":[],"source":source}

# Навигационные ссылки для каждого ноутбука
NAV = {
    'FunctorHierarchy':   ('TypeAlgebra', 'TypeAlgebra.ipynb', 'Monads', 'Monads.ipynb'),
    'Comonads':           ('MonadTransformers', 'MonadTransformers.ipynb', 'FoldableTraversable', 'FoldableTraversable.ipynb'),
    'Profunctors':        ('AlgebrasCoalgebras', 'AlgebrasCoalgebras.ipynb', 'Optics', 'Optics.ipynb'),
    'Optics':             ('Profunctors', 'Profunctors.ipynb', 'YonedaLemma', 'YonedaLemma.ipynb'),
    'YonedaLemma':        ('Optics', 'Optics.ipynb', 'KanExtensions', 'KanExtensions.ipynb'),
    'MetaProgramming':    ('Adjunctions', 'Adjunctions.ipynb', 'Concurrency', 'Concurrency.ipynb'),
    'Concurrency':        ('MetaProgramming', 'MetaProgramming.ipynb', 'DistributedHaskell', 'DistributedHaskell.ipynb'),
    'DistributedHaskell': ('Concurrency', 'Concurrency.ipynb', 'GPUHaskell', 'GPUHaskell.ipynb'),
    'GPUHaskell':         ('DistributedHaskell', 'DistributedHaskell.ipynb', None, None),
}

def nav_src(prev_name, prev_file, next_name, next_file):
    parts = ['---\n']
    if prev_name:
        parts.append(f'**\u2190 \u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0439:** [{prev_name}]({prev_file})')
    if prev_name and next_name:
        parts.append(' \u2002|\u2002 ')
    if next_name:
        parts.append(f'**\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u2192:** [{next_name}]({next_file})')
    return ''.join(parts)

def build_toc(h2_titles):
    lines = ['\u2756\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435\n\n']
    lines.append('| # | \u0422\u0435\u043c\u0430 | \u0421\u0443\u0442\u044c |\n')
    lines.append('|---|------|------|\n')
    for i, title in enumerate(h2_titles, 1):
        # title = '## 1Functor — ...' -> strip '## N\u200b...'
        clean = re.sub(r'^##\s*', '', title).strip()
        lines.append(f'| {i} | {clean} |  |\n')
    return ''.join(lines).rstrip('\n')

NEED = ['FunctorHierarchy','Comonads','Profunctors','Optics','YonedaLemma',
        'MetaProgramming','Concurrency','DistributedHaskell','GPUHaskell']

for name in NEED:
    path = f'{name}.ipynb'
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']

    # 1) Fix SETUP: убедиться что в code cell[0] есть putStrLn "Setup done."
    c0_src = ''.join(cells[0]['source'])
    if cells[0]['cell_type'] == 'code' and 'putStrLn' not in c0_src:
        new_src = c0_src.rstrip('\n') + '\nputStrLn "Setup done."'
        cells[0] = code_cell(new_src)
        print(f'  [{name}] Added putStrLn to setup cell')

    # 2) Найти H2-заголовки (исключая "## Итоги", "## Заключение", "## Диаграмма")
    h2_titles = []
    for c in cells:
        src = ''.join(c['source'])
        if src.startswith('## ') and c['cell_type'] == 'markdown':
            first = src.splitlines()[0]
            skip = ['\u0418\u0442\u043e\u0433', '\u0417\u0430\u043a\u043b\u044e\u0447', '\u0414\u0438\u0430\u0433\u0440\u0430\u043c\u043c']
            if not any(s in first for s in skip):
                h2_titles.append(first)

    # 3) Найти H1-ячейку и вставить/обновить TOC
    h1_idx = None
    for i, c in enumerate(cells):
        src = ''.join(c['source'])
        if src.startswith('# ') and c['cell_type'] == 'markdown':
            h1_idx = i
            break

    has_toc = any('\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435' in ''.join(c['source']) for c in cells)

    if h1_idx is not None and not has_toc:
        toc_src = build_toc(h2_titles)
        toc_cell = md_cell(toc_src)
        cells.insert(h1_idx + 1, toc_cell)
        print(f'  [{name}] Inserted TOC with {len(h2_titles)} sections after H1 (cell {h1_idx})')

    # 4) Проверить/добавить навигацию в последнюю ячейку
    has_nav = any('\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0439' in ''.join(c['source']) or
                  '\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439' in ''.join(c['source']) for c in cells)
    if not has_nav and name in NAV:
        prev_n, prev_f, next_n, next_f = NAV[name]
        nav = nav_src(prev_n, prev_f, next_n, next_f)
        cells.append(md_cell(nav))
        print(f'  [{name}] Added NAV cell')

    nb['cells'] = cells

    # 5) Сохранить с ensure_ascii=False - эмодзи остаются как есть
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f'OK [{name}] saved ({len(cells)} cells)')

print('\nDone!')
