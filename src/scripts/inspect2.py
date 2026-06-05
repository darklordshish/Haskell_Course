import json

def show_last(path, n=5):
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f"=== {path} LAST {n} ===")
    for i, c in enumerate(cells[-n:]):
        src = ''.join(c['source'])
        print(f"Cell {len(cells)-n+i} [{c['cell_type']}]: {repr(src[:150])}")

for name in ['FunctorHierarchy', 'Comonads', 'YonedaLemma']:
    show_last(f'{name}.ipynb', 3)
    print()
