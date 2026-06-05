import json, re

need = ['FunctorHierarchy','Comonads','Profunctors','Optics','YonedaLemma',
        'MetaProgramming','Concurrency','DistributedHaskell','GPUHaskell']

for name in need:
    with open(f'{name}.ipynb', encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f'=== {name} ===')
    for i, c in enumerate(cells):
        src = ''.join(c['source'])
        # H1
        if src.startswith('# '):
            print(f'  H1 (cell {i}): {src.splitlines()[0]}')
        # H2
        elif src.startswith('## '):
            first_line = src.splitlines()[0]
            print(f'  H2 (cell {i}): {first_line}')
