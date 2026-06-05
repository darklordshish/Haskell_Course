import json

def show_cells(path, max_cells=8):
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f"=== {path} ({len(cells)} cells) ===")
    for i, c in enumerate(cells[:max_cells]):
        src = ''.join(c['source'])
        print(f"Cell {i} [{c['cell_type']}]: {repr(src[:120])}")
    print()

show_cells('FunctorHierarchy.ipynb')
