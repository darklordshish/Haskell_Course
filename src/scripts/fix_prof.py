import json

BASE = '/home/jovyan/src'

# Создаём prof_dimap.svg - диаграмма квадрата профунктора
prof_dimap_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="300" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="580" height="300" fill="#0f172a" rx="10"/>
  <text x="290" y="28" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Profunctor: dimap kak kvadrat</text>
  <text x="290" y="46" text-anchor="middle" font-size="10" fill="#94a3b8">Hask^op x Hask -&gt; Hask</text>

  <!-- Uzly kvadrata -->
  <rect x="40" y="70" width="160" height="44" rx="6" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="120" y="88" text-anchor="middle" font-size="11" fill="#60a5fa">p a b</text>
  <text x="120" y="104" text-anchor="middle" font-size="10" fill="#94a3b8">(istochnik)</text>

  <rect x="380" y="70" width="160" height="44" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="460" y="88" text-anchor="middle" font-size="11" fill="#34d399">p a&#39; b&#39;</text>
  <text x="460" y="104" text-anchor="middle" font-size="10" fill="#94a3b8">(tseli)</text>

  <rect x="40" y="200" width="160" height="44" rx="6" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="120" y="218" text-anchor="middle" font-size="11" fill="#a78bfa">p a&#39; b</text>
  <text x="120" y="234" text-anchor="middle" font-size="10" fill="#94a3b8">(posle lmap)</text>

  <!-- Strelki -->
  <!-- Verkh: p a b -> p a' b' -->
  <line x1="200" y1="92" x2="378" y2="92" stroke="#fb923c" stroke-width="2" marker-end="url(#arr)"/>
  <text x="290" y="82" text-anchor="middle" font-size="10" fill="#fb923c">dimap f g</text>

  <!-- Levo nizh: p a b -> p a' b (lmap f) -->
  <line x1="120" y1="114" x2="120" y2="198" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr2)"/>
  <text x="85" y="162" text-anchor="middle" font-size="9" fill="#60a5fa">lmap f</text>
  <text x="85" y="175" text-anchor="middle" font-size="9" fill="#94a3b8">f: a&#39;-&gt;a</text>

  <!-- Nizh: p a' b -> p a' b' (rmap g) -->
  <line x1="200" y1="222" x2="378" y2="100" stroke="#34d399" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr3)"/>
  <text x="310" y="175" text-anchor="middle" font-size="9" fill="#34d399">rmap g</text>
  <text x="310" y="188" text-anchor="middle" font-size="9" fill="#94a3b8">g: b-&gt;b&#39;</text>

  <!-- Strelka vverhu sleva: f: a'->a (kontravariant) -->
  <text x="290" y="140" text-anchor="middle" font-size="10" fill="#94a3b8">(Hask^op: strelki obratny)</text>
  <text x="290" y="155" text-anchor="middle" font-size="10" fill="#e2e8f0">dimap f g = rmap g . lmap f</text>

  <!-- Marker strelok -->
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#fb923c"/>
    </marker>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#60a5fa"/>
    </marker>
    <marker id="arr3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#34d399"/>
    </marker>
  </defs>

  <!-- Zakony -->
  <rect x="20" y="258" width="540" height="32" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="290" y="271" text-anchor="middle" font-size="10" fill="#e2e8f0">Zakon 1: dimap id id = id</text>
  <text x="290" y="284" text-anchor="middle" font-size="10" fill="#e2e8f0">Zakon 2: dimap (f.g) (h.i) = dimap g h . dimap f i</text>
</svg>'''

with open(f'{BASE}/prof_dimap.svg', 'w', encoding='utf-8') as f:
    f.write(prof_dimap_svg)
print("prof_dimap.svg создан")

# Правим ноутбук
nb_path = f'{BASE}/Profunctors.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
cell5 = cells[5]
src5 = ''.join(cell5['source']) if isinstance(cell5['source'], list) else cell5['source']
print(f"Ячейка 5 тип: {cell5['cell_type']}")
print(repr(src5[:200]))

# Ячейка 5 - заменяем ASCII диаграмму на SVG
new_src5 = '## \U0001f534\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u0437\u0433\u043b\u044f\u0434: `Hask^op x Hask -> Hask`\n\n\u041f\u0440\u043e\u0444\u0443\u043d\u043a\u0442\u043e\u0440 `p` \u2014 \u044d\u0442\u043e \u0444\u0443\u043d\u043a\u0442\u043e\u0440 \u0438\u0437 **\u043f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0439** `Hask^op x Hask` \u0432 `Hask`:\n\n![Profunctor dimap kvadrat](prof_dimap.svg)\n\n**\u0417\u0430\u043a\u043e\u043d\u044b \u043f\u0440\u043e\u0444\u0443\u043d\u043a\u0442\u043e\u0440\u0430:**\n- `dimap id id = id`\n- `dimap (f . g) (h . i) = dimap g h . dimap f i`'

cells[5]['source'] = new_src5
print("Ячейка 5 заменена")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Ноутбук сохранён")
