import json

with open('Monads.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

# Ищем TOC-ячейку
for i, c in enumerate(cells[:10]):
    src = ''.join(c['source'])
    if 'Содержание' in src:
        print(f'TOC found at cell {i}:')
        print(src)
        break
