import json, re

BASE = '/home/jovyan/src'

with open(f'{BASE}/AlgebrasCoalgebras.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 11 — большая секция, найдём ASCII-блок через regex
src11 = ''.join(cells[11]['source']) if isinstance(cells[11]['source'], list) else cells[11]['source']

# Паттерн: ищем строку с Диаграмма + коммутативный + блок кода с Fix F
pattern = r'(##+ [^\n]*[Дд]иаграмма[^\n]*\(коммутативный квадрат\))\n\n```\n[\s\S]*?```'
match = re.search(pattern, src11)
if match:
    old_text = match.group(0)
    header = match.group(1)
    new_text = f"{header}\n\n![Диаграмма F-алгебры](falgebra_universal.svg)"
    src11_new = src11.replace(old_text, new_text)
    cells[11]['source'] = src11_new
    print("OK: ASCII заменён на SVG")
    print(f"Было: {repr(old_text[:80])}")
else:
    print("НЕ НАЙДЕНО через regex")
    # Покажем все вхождения Диаграмма
    for m in re.finditer(r'Диаграмма', src11):
        print(repr(src11[m.start()-3:m.start()+60]))

with open(f'{BASE}/AlgebrasCoalgebras.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Сохранено")
