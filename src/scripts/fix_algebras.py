import json

BASE = '/home/jovyan/src'

# ===== 1. falgebra_universal.svg - диаграмма универсального свойства =====
falg_univ_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="320" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="560" height="320" fill="#0f172a" rx="10"/>
  <text x="280" y="26" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Universal&#39;noe svojstvo nachal&#39;noj F-algebry</text>
  <text x="280" y="44" text-anchor="middle" font-size="10" fill="#94a3b8">Katamorfi zm - edinstvennaya strelka iz (&#956;F, in)</text>

  <!-- Uzly -->
  <!-- F(muF) - verkhnij levyj -->
  <rect x="30" y="70" width="150" height="44" rx="6" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="105" y="89" text-anchor="middle" font-size="11" font-weight="bold" fill="#a78bfa">F(&#956;F)</text>
  <text x="105" y="105" text-anchor="middle" font-size="9" fill="#94a3b8">primenenie funktora</text>

  <!-- muF - verkhnij pravyj -->
  <rect x="370" y="70" width="150" height="44" rx="6" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="445" y="89" text-anchor="middle" font-size="11" font-weight="bold" fill="#a78bfa">&#956;F</text>
  <text x="445" y="105" text-anchor="middle" font-size="9" fill="#94a3b8">nachal&#39;naya algebra</text>

  <!-- F(A) - nizhnij levyj -->
  <rect x="30" y="220" width="150" height="44" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="105" y="239" text-anchor="middle" font-size="11" fill="#34d399">F(A)</text>
  <text x="105" y="255" text-anchor="middle" font-size="9" fill="#94a3b8">primenenie funktora</text>

  <!-- A - nizhnij pravyj -->
  <rect x="370" y="220" width="150" height="44" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="445" y="239" text-anchor="middle" font-size="11" fill="#34d399">A</text>
  <text x="445" y="255" text-anchor="middle" font-size="9" fill="#94a3b8">nositel&#39; algebry</text>

  <!-- Strelki -->
  <!-- Verkh: F(muF) -> muF (in) -->
  <line x1="180" y1="92" x2="368" y2="92" stroke="#a78bfa" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="274" y="84" text-anchor="middle" font-size="11" font-weight="bold" fill="#a78bfa">in</text>

  <!-- Nizh: F(A) -> A (alg) -->
  <line x1="180" y1="242" x2="368" y2="242" stroke="#34d399" stroke-width="2" marker-end="url(#arr2)"/>
  <text x="274" y="234" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">alg</text>

  <!-- Levo: F(muF) -> F(A) (F(h)) -->
  <line x1="105" y1="114" x2="105" y2="218" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr3)"/>
  <text x="75" y="168" text-anchor="middle" font-size="10" fill="#60a5fa">F(h)</text>

  <!-- Pravo: muF -> A (h = cata alg) -->
  <line x1="445" y1="114" x2="445" y2="218" stroke="#fb923c" stroke-width="2" stroke-dasharray="8,4" marker-end="url(#arr4)"/>
  <text x="490" y="155" text-anchor="middle" font-size="11" font-weight="bold" fill="#fb923c">h</text>
  <text x="490" y="172" text-anchor="middle" font-size="9" fill="#fb923c">= cata alg</text>
  <text x="490" y="185" text-anchor="middle" font-size="9" fill="#94a3b8">(edinstvennaya)</text>

  <!-- Zakon -->
  <rect x="20" y="282" width="520" height="28" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="280" y="295" text-anchor="middle" font-size="10" fill="#e2e8f0">Zakon: h . in = alg . fmap h</text>
  <text x="280" y="308" text-anchor="middle" font-size="9" fill="#94a3b8">cata alg - edinstvennaya strelka delayushchaya kvadrat kommutativnym</text>

  <defs>
    <marker id="arr1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#a78bfa"/></marker>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#34d399"/></marker>
    <marker id="arr3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#60a5fa"/></marker>
    <marker id="arr4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#fb923c"/></marker>
  </defs>
</svg>'''

with open(f'{BASE}/falgebra_universal.svg', 'w', encoding='utf-8') as f:
    f.write(falg_univ_svg)
print("falgebra_universal.svg создан")

# ===== 2. recursion_schemes.svg - иерархия схем рекурсии =====
rec_schemes_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="360" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="680" height="360" fill="#0f172a" rx="10"/>
  <text x="340" y="26" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Ierarkhiya skhem rekursii</text>
  <text x="340" y="44" text-anchor="middle" font-size="10" fill="#94a3b8">Kazhdaya posleduyushchaya skhema usilyaet predydushchuyu</text>

  <!-- cata -->
  <rect x="30" y="60" width="120" height="40" rx="5" fill="#172554" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="90" y="78" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">cata</text>
  <text x="90" y="93" text-anchor="middle" font-size="9" fill="#94a3b8">Algebra</text>

  <!-- para -->
  <rect x="190" y="60" width="120" height="40" rx="5" fill="#172554" stroke="#34d399" stroke-width="1.5"/>
  <text x="250" y="78" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">para</text>
  <text x="250" y="93" text-anchor="middle" font-size="9" fill="#94a3b8">RAlgebra</text>

  <!-- ana -->
  <rect x="30" y="140" width="120" height="40" rx="5" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="90" y="158" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">ana</text>
  <text x="90" y="173" text-anchor="middle" font-size="9" fill="#94a3b8">Coalgebra</text>

  <!-- apo -->
  <rect x="190" y="140" width="120" height="40" rx="5" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="250" y="158" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">apo</text>
  <text x="250" y="173" text-anchor="middle" font-size="9" fill="#94a3b8">RCoalgebra</text>

  <!-- histo -->
  <rect x="350" y="140" width="130" height="40" rx="5" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="415" y="158" text-anchor="middle" font-size="11" font-weight="bold" fill="#a78bfa">histo</text>
  <text x="415" y="173" text-anchor="middle" font-size="9" fill="#94a3b8">CVAlgebra</text>

  <!-- futu -->
  <rect x="510" y="140" width="130" height="40" rx="5" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="575" y="158" text-anchor="middle" font-size="11" font-weight="bold" fill="#a78bfa">futu</text>
  <text x="575" y="173" text-anchor="middle" font-size="9" fill="#94a3b8">CVCoalgebra</text>

  <!-- hylo -->
  <rect x="30" y="230" width="120" height="40" rx="5" fill="#1e293b" stroke="#fb923c" stroke-width="1.5"/>
  <text x="90" y="248" text-anchor="middle" font-size="11" font-weight="bold" fill="#fb923c">hylo</text>
  <text x="90" y="263" text-anchor="middle" font-size="9" fill="#94a3b8">cata . ana</text>

  <!-- chrono -->
  <rect x="415" y="230" width="130" height="40" rx="5" fill="#1e293b" stroke="#fb923c" stroke-width="1.5"/>
  <text x="480" y="248" text-anchor="middle" font-size="11" font-weight="bold" fill="#fb923c">chrono</text>
  <text x="480" y="263" text-anchor="middle" font-size="9" fill="#94a3b8">histo . futu</text>

  <!-- Strelki -->
  <line x1="150" y1="80" x2="188" y2="80" stroke="#334155" stroke-width="1.5" marker-end="url(#sarr)"/>
  <text x="170" y="73" text-anchor="middle" font-size="8" fill="#94a3b8">+ orig.</text>

  <line x1="150" y1="160" x2="188" y2="160" stroke="#334155" stroke-width="1.5" marker-end="url(#sarr)"/>
  <text x="170" y="153" text-anchor="middle" font-size="8" fill="#94a3b8">+ exit</text>

  <line x1="310" y1="160" x2="348" y2="160" stroke="#334155" stroke-width="1.5" marker-end="url(#sarr)"/>
  <text x="330" y="153" text-anchor="middle" font-size="8" fill="#94a3b8">+ hist.</text>

  <line x1="480" y1="160" x2="508" y2="160" stroke="#334155" stroke-width="1.5" marker-end="url(#sarr)"/>
  <text x="495" y="153" text-anchor="middle" font-size="8" fill="#94a3b8">pred.</text>

  <line x1="90" y1="180" x2="90" y2="228" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#sarr)"/>
  <text x="60" y="208" text-anchor="middle" font-size="8" fill="#94a3b8">comp.</text>

  <line x1="415" y1="180" x2="440" y2="228" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#sarr)"/>

  <!-- Legenda -->
  <rect x="20" y="295" width="640" height="54" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="340" y="314" text-anchor="middle" font-size="10" font-weight="bold" fill="#e2e8f0">Gylomorfi zm: hylo alg coalg = cata alg . ana coalg</text>
  <text x="340" y="330" text-anchor="middle" font-size="9" fill="#94a3b8">(s optimizaciej: bez promezhutochnoj struktury)</text>
  <text x="340" y="345" text-anchor="middle" font-size="9" fill="#94a3b8">Razdelyaet rekursiyu i logiku: cata razrushaet, ana stroit strukturu</text>

  <defs>
    <marker id="sarr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L5,3 L0,6 Z" fill="#334155"/></marker>
  </defs>
</svg>'''

with open(f'{BASE}/recursion_schemes.svg', 'w', encoding='utf-8') as f:
    f.write(rec_schemes_svg)
print("recursion_schemes.svg создан")

# ===== 3. Правим AlgebrasCoalgebras.ipynb =====
nb_path = f'{BASE}/AlgebrasCoalgebras.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 12 - диаграмма универсального свойства
src12 = ''.join(cells[12]['source']) if isinstance(cells[12]['source'], list) else cells[12]['source']
print(f"Ячейка 12 тип: {cells[12]['cell_type']}, len: {len(src12)}")

if 'F(' in src12 and cells[12]['cell_type'] == 'markdown':
    # Сохраняем заголовок, заменяем ASCII
    new_src12 = '### \u0422\u0435\u043e\u0440\u0435\u043c\u0430 \u041b\u0430\u043c\u0431\u0435\u043a\u0430 \u0438 \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c\n\n**\u041a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u0438\u0432\u043d\u044b\u0439 \u043a\u0432\u0430\u0434\u0440\u0430\u0442** (\u0434\u0438\u0430\u0433\u0440\u0430\u043c\u043c\u0430 \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430):\n\n![Universal&#39;noe svojstvo](falgebra_universal.svg)\n\n\u0417\u0430\u043a\u043e\u043d \u043a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438: `h . in = alg . fmap h`\n\n\u0418\u043d\u044b\u043c\u0438 \u0441\u043b\u043e\u0432\u0430\u043c\u0438: **\u043a\u0430\u0442\u0430\u043c\u043e\u0440\u0444\u0438\u0437\u043c \u2014 \u044d\u0442\u043e \u0435\u0434\u0438\u043d\u0441\u0442\u0432\u0435\u043d\u043d\u0430\u044f \u0441\u0442\u0440\u0435\u043b\u043a\u0430** \u0438\u0437 (\u03bcF, in)'
    cells[12]['source'] = new_src12
    print("Ячейка 12 заменена")

# Ячейка 37 - иерархия схем рекурсии
new_src37 = '### \U0001f4d0 \u041a\u0430\u043a \u043a\u0430\u0436\u0434\u0430\u044f \u0441\u0445\u0435\u043c\u0430 \u0441\u0442\u0440\u043e\u0438\u0442\u0441\u044f \u0438\u0437 \u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0435\u0439\n\n![\u0418\u0435\u0440\u0430\u0440\u0445\u0438\u044f \u0441\u0445\u0435\u043c \u0440\u0435\u043a\u0443\u0440\u0441\u0438\u0438](recursion_schemes.svg)\n\n**\u0413\u0438\u043b\u043e\u043c\u043e\u0440\u0444\u0438\u0437\u043c** \u0441\u0432\u044f\u0437\u044b\u0432\u0430\u0435\u0442 ana \u0438 cata:\n```\nhylo alg coalg = cata alg . ana coalg  -- \u0441 \u043e\u043f\u0442\u0438\u043c\u0438\u0437\u0430\u0446\u0438\u0435\u0439: \u0431\u0435\u0437 \u043f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u043e\u0439 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u044b\n```'
cells[37]['source'] = new_src37
print("Ячейка 37 заменена")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("AlgebrasCoalgebras.ipynb сохранён")
