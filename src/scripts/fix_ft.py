import json

BASE = '/home/jovyan/src'

# ===== 1. Создаём ft_foldable.svg (тёмная тема) =====
ft_foldable_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="740" height="360" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="740" height="360" fill="#0f172a" rx="10"/>
  <text x="370" y="32" text-anchor="middle" font-size="15" font-weight="bold" fill="#e2e8f0">Foldable vs Traversable</text>

  <!-- Foldable (sleva) -->
  <rect x="20" y="50" width="330" height="200" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="185" y="78" text-anchor="middle" font-size="13" font-weight="bold" fill="#60a5fa">Foldable t</text>
  <text x="185" y="96" text-anchor="middle" font-size="10" fill="#94a3b8">t a -> [a]  (svortyvanie v spisok)</text>

  <rect x="40" y="105" width="290" height="40" rx="5" fill="#172554" stroke="#1d4ed8" stroke-width="1"/>
  <text x="185" y="122" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">foldMap :: Monoid m =&gt; (a -&gt; m) -&gt; t a -&gt; m</text>
  <text x="185" y="138" text-anchor="middle" font-size="10" fill="#93c5fd">(gomomorfizm v monoid)</text>

  <rect x="40" y="153" width="290" height="40" rx="5" fill="#172554" stroke="#1d4ed8" stroke-width="1"/>
  <text x="185" y="170" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">foldr :: (a -&gt; b -&gt; b) -&gt; b -&gt; t a -&gt; b</text>
  <text x="185" y="186" text-anchor="middle" font-size="10" fill="#93c5fd">(strukturnaya rekursiya)</text>

  <text x="185" y="220" text-anchor="middle" font-size="10" fill="#94a3b8">sum, product, length, elem, toList, ...</text>
  <text x="185" y="235" text-anchor="middle" font-size="10" fill="#94a3b8">Tree, [], Maybe, Map, Set, Seq</text>

  <text x="185" y="255" text-anchor="middle" font-size="11" font-weight="bold" fill="#f59e0b">t a -&gt; b</text>
  <text x="185" y="272" text-anchor="middle" font-size="10" fill="#fbbf24">slomat formu</text>

  <!-- Traversable (sprava) -->
  <rect x="390" y="50" width="330" height="200" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="555" y="78" text-anchor="middle" font-size="13" font-weight="bold" fill="#34d399">Traversable t</text>
  <text x="555" y="96" text-anchor="middle" font-size="10" fill="#94a3b8">t a -&gt; f (t b)  (obkhod s effektami)</text>

  <rect x="410" y="105" width="290" height="40" rx="5" fill="#052e16" stroke="#16a34a" stroke-width="1"/>
  <text x="555" y="122" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">traverse :: (a -&gt; f b) -&gt; t a -&gt; f (t b)</text>
  <text x="555" y="138" text-anchor="middle" font-size="10" fill="#6ee7b7">trebuet: Applicative f</text>

  <rect x="410" y="153" width="290" height="40" rx="5" fill="#052e16" stroke="#16a34a" stroke-width="1"/>
  <text x="555" y="170" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">sequenceA :: t (f a) -&gt; f (t a)</text>
  <text x="555" y="186" text-anchor="middle" font-size="10" fill="#6ee7b7">(kommutatsiya s effektom)</text>

  <text x="555" y="220" text-anchor="middle" font-size="10" fill="#94a3b8">mapM, forM, mapAccumL, ...</text>
  <text x="555" y="235" text-anchor="middle" font-size="10" fill="#94a3b8">trebuet: Functor + Foldable</text>

  <text x="555" y="255" text-anchor="middle" font-size="11" font-weight="bold" fill="#f59e0b">t a -&gt; f (t b)</text>
  <text x="555" y="272" text-anchor="middle" font-size="10" fill="#fbbf24">sokhranit formu + effekt</text>

  <!-- Svyaz -->
  <line x1="350" y1="150" x2="390" y2="150" stroke="#a78bfa" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="370" y="143" text-anchor="middle" font-size="9" fill="#a78bfa">sil-</text>
  <text x="370" y="155" text-anchor="middle" font-size="9" fill="#a78bfa">nee</text>

  <!-- Nizhniye formuly -->
  <rect x="20" y="295" width="700" height="50" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="370" y="315" text-anchor="middle" font-size="10" fill="#e2e8f0">fmap f = runIdentity . traverse (Identity . f)</text>
  <text x="370" y="333" text-anchor="middle" font-size="10" fill="#e2e8f0">foldMap f = getConst . traverse (Const . f)</text>
</svg>'''

with open(f'{BASE}/ft_foldable.svg', 'w', encoding='utf-8') as f:
    f.write(ft_foldable_svg)
print("ft_foldable.svg создан (темная тема)")

# ===== 2. Создаём ft_compare.svg - диаграмма сравнения (категорная картина) =====
ft_compare_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="300" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="720" height="300" fill="#0f172a" rx="10"/>
  <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="bold" fill="#e2e8f0">Itogovaya Kategornaya Kartina</text>

  <!-- FOLDABLE kolonka -->
  <rect x="20" y="45" width="320" height="230" rx="8" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="180" y="68" text-anchor="middle" font-size="13" font-weight="bold" fill="#60a5fa">FOLDABLE</text>
  <line x1="20" y1="75" x2="340" y2="75" stroke="#334155"/>
  <text x="180" y="95" text-anchor="middle" font-size="11" fill="#e2e8f0">t a -&gt; b</text>
  <text x="180" y="112" text-anchor="middle" font-size="10" fill="#94a3b8">slomat formu</text>
  <line x1="40" y1="120" x2="320" y2="120" stroke="#334155" stroke-dasharray="4,2"/>
  <text x="180" y="140" text-anchor="middle" font-size="10" fill="#60a5fa">foldMap :: (a-&gt;m) -&gt; t a-&gt;m</text>
  <text x="180" y="158" text-anchor="middle" font-size="10" fill="#94a3b8">Monadicheskij: net</text>
  <text x="180" y="175" text-anchor="middle" font-size="10" fill="#94a3b8">Nuzhen: Foldable</text>
  <line x1="40" y1="185" x2="320" y2="185" stroke="#334155" stroke-dasharray="4,2"/>
  <text x="180" y="205" text-anchor="middle" font-size="11" fill="#fb923c">foldr = katamorfi zm</text>
  <text x="180" y="221" text-anchor="middle" font-size="10" fill="#94a3b8">(unichtozhaet strukturu)</text>
  <text x="180" y="243" text-anchor="middle" font-size="11" fill="#a78bfa">unfoldr = anamorfi zm</text>
  <text x="180" y="259" text-anchor="middle" font-size="10" fill="#94a3b8">(stroit strukturu)</text>

  <!-- TRAVERSABLE kolonka -->
  <rect x="380" y="45" width="320" height="230" rx="8" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="540" y="68" text-anchor="middle" font-size="13" font-weight="bold" fill="#34d399">TRAVERSABLE</text>
  <line x1="380" y1="75" x2="700" y2="75" stroke="#334155"/>
  <text x="540" y="95" text-anchor="middle" font-size="11" fill="#e2e8f0">t a -&gt; f (t b)</text>
  <text x="540" y="112" text-anchor="middle" font-size="10" fill="#94a3b8">sokhranit formu + effekt</text>
  <line x1="400" y1="120" x2="680" y2="120" stroke="#334155" stroke-dasharray="4,2"/>
  <text x="540" y="140" text-anchor="middle" font-size="10" fill="#34d399">traverse :: (a-&gt;f b) -&gt; t a-&gt;f(t b)</text>
  <text x="540" y="158" text-anchor="middle" font-size="10" fill="#94a3b8">Monadicheskij: mapM</text>
  <text x="540" y="175" text-anchor="middle" font-size="10" fill="#94a3b8">Nuzhen: Functor + Foldable</text>
  <line x1="400" y1="185" x2="680" y2="185" stroke="#334155" stroke-dasharray="4,2"/>
  <text x="540" y="205" text-anchor="middle" font-size="11" fill="#fb923c">traverse = apo-morfi zm</text>
  <text x="540" y="221" text-anchor="middle" font-size="10" fill="#94a3b8">(sokhranjaet strukturu)</text>
  <text x="540" y="243" text-anchor="middle" font-size="10" fill="#6ee7b7">sil&#39;nee foldMap</text>
  <text x="540" y="259" text-anchor="middle" font-size="10" fill="#94a3b8">(foldMap = traverse c Const)</text>
</svg>'''

with open(f'{BASE}/ft_compare.svg', 'w', encoding='utf-8') as f:
    f.write(ft_compare_svg)
print("ft_compare.svg создан")

# ===== 3. Правим ноутбук =====
nb_path = f'{BASE}/FoldableTraversable.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 52 - заменить ASCII таблицу на SVG
cell52_new = '## \U0001f9e9\u0418\u0442\u043e\u0433\u043e\u0432\u0430\u044f \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u043d\u0430\u044f \u041a\u0430\u0440\u0442\u0438\u043d\u0430\n\n![Foldable vs Traversable](ft_compare.svg)\n\n**\u041a\u043b\u044e\u0447\u0435\u0432\u0430\u044f \u0438\u043d\u0442\u0443\u0438\u0446\u0438\u044f:**\n- `Foldable` \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u0435\u0442 \u00ab\u0447\u0438\u0442\u0430\u0442\u044c\u00bb \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u044b, \u0437\u0430\u0431\u044b\u0432\u0430\u044f \u043e \u0444\u043e\u0440\u043c\u0435\n- `Traversable` \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u0435\u0442 \u00ab\u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u00bb \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0441 \u044d\u0444\u0444\u0435\u043a\u0442\u0430\u043c\u0438, **\u043f\u043e\u043c\u043d\u044f** \u0444\u043e\u0440\u043c\u0443\n- `traverse` \u0441\u0438\u043b\u044c\u043d\u0435\u0435 `foldMap` (`foldMap = traverse c Const`) \u0438 `fmap` (`fmap = traverse c Identity`)\n\n```\nfmap f    = runIdentity . traverse (Identity . f)\nfoldMap f = getConst   . traverse (Const    . f)\n```'
cells[52]['source'] = cell52_new

# Ячейка 54 - плейсхолдер "Диаграмма:" - удалить (ячейка 55 уже имеет ft_foldable.svg)
# Проверим что ячейка 54 - это плейсхолдер
src54 = ''.join(cells[54]['source']) if isinstance(cells[54]['source'], list) else cells[54]['source']
print(f"Ячейка 54: {repr(src54[:100])}")

if 'Диаграмма:' in src54 and 'ft_foldable' not in src54:
    # Удаляем ячейку-плейсхолдер
    cells.pop(54)
    print("Ячейка 54 (плейсхолдер) удалена")
else:
    print("Ячейка 54 не является плейсхолдером, оставляем")

nb['cells'] = cells

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Ноутбук сохранён")
print(f"Всего ячеек теперь: {len(cells)}")
