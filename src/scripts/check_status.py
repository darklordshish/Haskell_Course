import json, os

nbs = [
    'BaseHaskell', 'TypeAlgebra', 'FunctorHierarchy', 'Monads', 'MonadTransformers',
    'Comonads', 'FoldableTraversable', 'AlgebrasCoalgebras', 'Profunctors', 'Optics',
    'YonedaLemma', 'KanExtensions', 'Adjunctions', 'MetaProgramming',
    'Concurrency', 'DistributedHaskell', 'GPUHaskell'
]

for nb_name in nbs:
    path = f'{nb_name}.ipynb'
    if not os.path.exists(path):
        print(f'MISSING: {nb_name}')
        continue
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    first_src = ''.join(cells[0]['source']) if cells else ''
    has_setup = ':set' in first_src and 'putStrLn' in first_src
    all_src = ' '.join(''.join(c['source']) for c in cells)
    has_toc = 'Содержание' in all_src
    has_nav = 'Предыдущий' in all_src or 'Следующий' in all_src
    # Заголовок H1
    h1_cells = [c for c in cells if c['cell_type']=='markdown' and ''.join(c['source']).startswith('# ')]
    h1 = ''.join(h1_cells[0]['source'])[:60] if h1_cells else 'NO H1'
    ok = 'OK' if (has_setup and has_toc and has_nav) else 'NEED'
    print(f'{ok} | {nb_name:25s} | cells={len(cells):3d} | setup={has_setup} toc={has_toc} nav={has_nav}')
