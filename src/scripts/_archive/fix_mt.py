import json, re

nb_path = '/home/jovyan/src/MonadTransformers.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

def get_src(cell):
    s = cell['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(cell, text):
    cell['source'] = text

# 1. Убираем HLint display_data варнинги из outputs
cleaned = 0
for i, cell in enumerate(cells):
    if cell['cell_type'] != 'code': continue
    new_outputs = []
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'display_data':
            data = out.get('data', {})
            txt = ''.join(data.get('text/plain', []))
            # HLint подсказки содержат "Found:" и "Why not:"
            if 'Found:' in txt and 'Why not:' in txt:
                cleaned += 1
                continue  # пропускаем этот output
        new_outputs.append(out)
    cell['outputs'] = new_outputs
print(f'Убрано HLint-подсказок: {cleaned}')

# 2. Находим ячейку с "order_diagram" и исправляем ссылку
for i, cell in enumerate(cells):
    if cell['cell_type'] != 'markdown': continue
    src = get_src(cell)
    if 'order_diagram' in src:
        # Заменяем ![order_diagram] на правильную ссылку на SVG
        new_src = src.replace('![order_diagram]', '![Порядок трансформеров](mt_order.svg)')
        if new_src != src:
            set_src(cell, new_src)
            print(f'Ячейка {i}: исправлена ссылка на order_diagram -> mt_order.svg')
        break

# 3. Находим ASCII-диаграмму в "Резюме" (T1 (T2 m) a со стрелками) и заменяем на SVG
for i, cell in enumerate(cells):
    if cell['cell_type'] != 'markdown': continue
    src = get_src(cell)
    if 'T1 (T2 m) a' in src and '^' in src:
        # Заменяем ASCII-блок на SVG
        new_src = re.sub(
            r'```\nT1 \(T2 m\) a[\s\S]*?```',
            '![Внешний/внутренний трансформер](mt_layers.svg)',
            src
        )
        if new_src != src:
            set_src(cell, new_src)
            print(f'Ячейка {i}: ASCII-диаграмма заменена на mt_layers.svg')
        break

nb['cells'] = cells
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('MonadTransformers.ipynb сохранён')
