import json

for name in ['Comonads', 'YonedaLemma', 'MetaProgramming']:
    with open(f'{name}.ipynb', encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f"=== {name} FIRST 4 ===")
    for i, c in enumerate(cells[:4]):
        src = ''.join(c['source'])
        print(f"  Cell {i} [{c['cell_type']}]: {repr(src[:200])}")
    print()
