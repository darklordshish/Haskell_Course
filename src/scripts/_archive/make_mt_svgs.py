import json

# SVG 1: mt_layers.svg — схема внешнего/внутреннего трансформера
# T1 (T2 m) a: внешний T1 содержит внутренний T2
layers_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="220" viewBox="0 0 560 220">
  <rect width="560" height="220" fill="#0f172a" rx="12"/>
  <text x="280" y="28" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="15" fill="#94a3b8">T1 (T2 m) a -- struktura steka</text>

  <!-- Внешний блок T1 -->
  <rect x="30" y="50" width="500" height="140" rx="8" fill="#1e293b" stroke="#60a5fa" stroke-width="2"/>
  <text x="50" y="75" font-family="monospace,JetBrains Mono,Arial" font-size="14" fill="#60a5fa" font-weight="bold">T1  (vneshnij)</text>
  <text x="50" y="95" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#64748b">pri sboe T1 -- vse soderzhimoe T2 i m ischezaet</text>

  <!-- Внутренний блок T2 -->
  <rect x="70" y="108" width="420" height="65" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="2"/>
  <text x="90" y="133" font-family="monospace,JetBrains Mono,Arial" font-size="14" fill="#34d399" font-weight="bold">T2  (vnutrennij)</text>
  <text x="90" y="153" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#64748b">pri sboe T1 -- vyzhivaet; pri sboe T2 -- m sohranyaetsya</text>

  <!-- Стрелка-подсказка -->
  <text x="50" y="200" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#fb923c">Pravilo: chitaj stek snazhi vnutr -- eto poryadok poter pri sboe</text>
</svg>'''

with open('/home/jovyan/src/mt_layers.svg', 'w', encoding='utf-8') as f:
    f.write(layers_svg)
print('mt_layers.svg создан')

# SVG 2: mt_order.svg — диаграмма что теряется при сбое трансформера
# Показывает два стека: MaybeT(State s) vs StateT s Maybe
order_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
  <rect width="640" height="360" fill="#0f172a" rx="12"/>
  <text x="320" y="28" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="15" fill="#e2e8f0" font-weight="bold">Chto teryaetsya pri sboe: poryadok transformerov</text>

  <!-- Левая колонка: MaybeT (State s) -->
  <rect x="20" y="45" width="280" height="180" rx="8" fill="#1e293b" stroke="#60a5fa" stroke-width="2"/>
  <text x="160" y="68" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="13" fill="#60a5fa" font-weight="bold">MaybeT (State s) a</text>
  <!-- MaybeT outer -->
  <rect x="35" y="80" width="250" height="130" rx="6" fill="#0f172a" stroke="#fb923c" stroke-width="2"/>
  <text x="160" y="100" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#fb923c">MaybeT  (vneshnij)</text>
  <!-- State inner -->
  <rect x="50" y="110" width="220" height="85" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="160" y="130" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#34d399">State s  (vnutrennij)</text>
  <text x="160" y="150" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#94a3b8">s -&gt; (Maybe a, s)</text>
  <text x="160" y="170" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#34d399">sostoyanie VSEGDA vozvrashaetsya</text>
  <text x="160" y="185" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="10" fill="#64748b">dazhe pri neudache</text>

  <text x="160" y="248" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#34d399">Sboj: Maybe schitaetsya snaruzhi</text>
  <text x="160" y="265" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#94a3b8">State vyzhivaet</text>

  <!-- Правая колонка: StateT s Maybe -->
  <rect x="340" y="45" width="280" height="180" rx="8" fill="#1e293b" stroke="#a78bfa" stroke-width="2"/>
  <text x="480" y="68" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="13" fill="#a78bfa" font-weight="bold">StateT s Maybe a</text>
  <!-- StateT outer -->
  <rect x="355" y="80" width="250" height="130" rx="6" fill="#0f172a" stroke="#fb923c" stroke-width="2"/>
  <text x="480" y="100" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#fb923c">StateT s  (vneshnij)</text>
  <!-- Maybe inner -->
  <rect x="370" y="110" width="220" height="85" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.5"/>
  <text x="480" y="130" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#f87171">Maybe  (vnutrennij)</text>
  <text x="480" y="150" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#94a3b8">s -&gt; Maybe (a, s)</text>
  <text x="480" y="170" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#f87171">sostoyanie TERYAETSYA pri sboe</text>
  <text x="480" y="185" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="10" fill="#64748b">Nothing = net rezultata I sostoyaniya</text>

  <text x="480" y="248" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#f87171">Sboj: Maybe vnutri StateT</text>
  <text x="480" y="265" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="11" fill="#94a3b8">State ischezaet vmeste s nim</text>

  <!-- Нижняя подсказка -->
  <line x1="20" y1="295" x2="620" y2="295" stroke="#334155" stroke-width="1"/>
  <text x="320" y="318" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#60a5fa">Vneshnij transformator opredelyaet semantiku sboev</text>
  <text x="320" y="340" text-anchor="middle" font-family="monospace,JetBrains Mono,Arial" font-size="12" fill="#94a3b8">Chitaj stek snazhi vnutr: vneshnij &gt; vnutrennij po vliyaniyu</text>
</svg>'''

with open('/home/jovyan/src/mt_order.svg', 'w', encoding='utf-8') as f:
    f.write(order_svg)
print('mt_order.svg создан')

# Теперь исправим ссылку на order_diagram в ноутбуке (ищем разные форматы)
nb_path = '/home/jovyan/src/MonadTransformers.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

for i, cell in enumerate(cells):
    if cell['cell_type'] != 'markdown': continue
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    if 'order_diagram' in src:
        print(f"Найдено в ячейке {i}:", repr(src[:200]))
        new_src = src.replace('![order_diagram]', '![Порядок трансформеров](mt_order.svg)')
        # Также обработаем случай без скобок
        import re
        new_src = re.sub(r'!\[order_diagram\](?:\([^)]*\))?', '![Порядок трансформеров](mt_order.svg)', new_src)
        cell['source'] = new_src
        print(f"Исправлено -> mt_order.svg")
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Сохранено')
