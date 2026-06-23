import json, hashlib

def cid(s):
    return 'cmp' + hashlib.md5(s.encode()).hexdigest()[:8]

def md_cell(src):
    lines = src.split('\n')
    source = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type":"markdown","id":cid(src),"metadata":{},"source":source}

with open('Adjunctions.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# 1) Удалить мусорную cell 0 если это не SETUP
c0 = ''.join(cells[0]['source'])
if cells[0]['cell_type'] == 'code' and 'import json' in c0 and ':set' not in c0:
    cells.pop(0)
    print('Removed junk cell 0')

# Пересчитаем индекс cell 8 (теперь может быть 7)
# Найдём ячейку с ASCII-диаграммой треугольных тождеств
ascii_idx = None
for i, c in enumerate(cells):
    src = ''.join(c['source'])
    if c['cell_type'] == 'markdown' and '\\___' in src and 'id _' in src:
        ascii_idx = i
        break

if ascii_idx is None:
    print('ASCII diagram cell not found!')
else:
    print(f'Found ASCII diagram at cell {ascii_idx}')
    old_src = ''.join(cells[ascii_idx]['source'])
    print('Old cell preview:', old_src[:100])

# SVG треугольных тождеств
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="260"
     viewBox="0 0 700 260"
     font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <!-- Background -->
  <rect width="700" height="260" fill="#0f172a" rx="8"/>

  <!-- Title -->
  <text x="350" y="28" text-anchor="middle" fill="#f1f5f9" font-size="15" font-weight="bold">
    Triangle Identities (Triangular Equations)
  </text>

  <!-- TOP ROW: F(a) -> F(GF(a)) -> F(a) -->
  <!-- Nodes -->
  <rect x="30" y="55" width="70" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="65" y="77" text-anchor="middle" fill="#60a5fa" font-size="13">F(a)</text>

  <rect x="290" y="55" width="110" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="345" y="77" text-anchor="middle" fill="#a78bfa" font-size="13">F(G(F(a)))</text>

  <rect x="590" y="55" width="70" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="625" y="77" text-anchor="middle" fill="#60a5fa" font-size="13">F(a)</text>

  <!-- Arrows top row -->
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#60a5fa"/>
    </marker>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#34d399"/>
    </marker>
  </defs>

  <line x1="102" y1="72" x2="287" y2="72" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="195" y="65" text-anchor="middle" fill="#94a3b8" font-size="11">F(eta_a)</text>

  <line x1="403" y1="72" x2="587" y2="72" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="495" y="65" text-anchor="middle" fill="#94a3b8" font-size="11">eps_{F(a)}</text>

  <!-- id arc top -->
  <path d="M 100 90 Q 350 140 588 90" fill="none" stroke="#34d399" stroke-width="1.5"
        stroke-dasharray="5,3" marker-end="url(#arr2)"/>
  <text x="350" y="135" text-anchor="middle" fill="#34d399" font-size="12" font-style="italic">id_{F(a)}</text>

  <!-- BOTTOM ROW: G(b) -> G(F(G(b))) -> G(b) -->
  <rect x="30" y="185" width="70" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="65" y="207" text-anchor="middle" fill="#60a5fa" font-size="13">G(b)</text>

  <rect x="290" y="185" width="110" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="345" y="207" text-anchor="middle" fill="#a78bfa" font-size="13">G(F(G(b)))</text>

  <rect x="590" y="185" width="70" height="34" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="625" y="207" text-anchor="middle" fill="#60a5fa" font-size="13">G(b)</text>

  <!-- Arrows bottom row -->
  <line x1="102" y1="202" x2="287" y2="202" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="195" y="195" text-anchor="middle" fill="#94a3b8" font-size="11">eta_{G(b)}</text>

  <line x1="403" y1="202" x2="587" y2="202" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="495" y="195" text-anchor="middle" fill="#94a3b8" font-size="11">G(eps_b)</text>

  <!-- id arc bottom -->
  <path d="M 100 220 Q 350 255 588 220" fill="none" stroke="#34d399" stroke-width="1.5"
        stroke-dasharray="5,3" marker-end="url(#arr2)"/>
  <text x="350" y="252" text-anchor="middle" fill="#34d399" font-size="12" font-style="italic">id_{G(b)}</text>
</svg>'''

# Сохраняем SVG-файл
with open('adj_triangle.svg', 'w', encoding='utf-8') as f:
    f.write(SVG)
print('Written adj_triangle.svg')

# Заменяем ASCII-блок на SVG в ячейке
if ascii_idx is not None:
    old_src = ''.join(cells[ascii_idx]['source'])
    # Найдём блок от "### Схема" до конца ASCII
    # Заменим весь блок ``` ... ``` на ссылку на SVG
    import re
    new_src = re.sub(
        r'### Схема\n```\n.*?```',
        '### Схема\n\n![Треугольные тождества сопряжения](adj_triangle.svg)',
        old_src,
        flags=re.DOTALL
    )
    if new_src != old_src:
        cells[ascii_idx] = md_cell(new_src)
        print(f'Replaced ASCII diagram in cell {ascii_idx} with SVG reference')
    else:
        print('WARNING: regex did not match, showing old_src snippet:')
        # Попробуем найти ``` блок
        idx1 = old_src.find('```\n')
        idx2 = old_src.find('\n```', idx1+1)
        print(repr(old_src[idx1:idx2+4]))

nb['cells'] = cells

with open('Adjunctions.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f'Saved Adjunctions.ipynb ({len(cells)} cells)')
