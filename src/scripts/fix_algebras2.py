import json, re

BASE = '/home/jovyan/src'

# Читаем ноутбук
with open(f'{BASE}/AlgebrasCoalgebras.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 11 — большая секция, в ней ASCII-диаграмма коммутативного квадрата
# Заменим ASCII-блок на SVG-ссылку
src11 = ''.join(cells[11]['source']) if isinstance(cells[11]['source'], list) else cells[11]['source']

# Находим ASCII-блок с диаграммой и заменяем
old_block = """### 🌟Диаграмма (коммутативный квадрат)

```
Fix F  --cata alg-->  A
  |                   |
unFix               alg
  |                   |
F(Fix F) -fmap(cata)-> F A
```"""

new_block = """### 🌟Диаграмма (коммутативный квадрат)

![Диаграмма F-алгебры](falgebra_universal.svg)"""

if old_block in src11:
    src11_new = src11.replace(old_block, new_block)
    cells[11]['source'] = src11_new
    print("Ячейка 11: ASCII-блок заменён на SVG")
else:
    # Пробуем найти фрагмент для точной идентификации
    print("Точная строка не найдена, ищем альтернативу...")
    # Попробуем через regex - найдём блок ```...Fix F...```
    pattern = r'### 🌟Диаграмма \(коммутативный квадрат\)\n\n```\n[\s\S]*?```'
    match = re.search(pattern, src11)
    if match:
        src11_new = src11[:match.start()] + new_block + src11[match.end():]
        cells[11]['source'] = src11_new
        print("Ячейка 11: Заменено через regex")
    else:
        print("НЕ НАЙДЕНО! Текущее содержимое вокруг диаграммы:")
        idx = src11.find('Fix F')
        if idx >= 0:
            print(repr(src11[idx-50:idx+200]))

with open(f'{BASE}/AlgebrasCoalgebras.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Сохранено")
