import json

BASE = '/home/jovyan/src'

# ===== 1. cm_comonad_pairs.svg - таблица дуальных пар =====
cm_pairs_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="260" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="700" height="260" fill="#0f172a" rx="8"/>
  <text x="350" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Konkretnye dual&#39;nye pary: Monada vs Komonada</text>

  <!-- Zagolovki -->
  <rect x="10" y="36" width="220" height="26" rx="4" fill="#172554"/>
  <text x="120" y="53" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">MONADA</text>
  <rect x="240" y="36" width="220" height="26" rx="4" fill="#172554"/>
  <text x="350" y="53" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">KOMONADA</text>
  <rect x="470" y="36" width="220" height="26" rx="4" fill="#172554"/>
  <text x="580" y="53" text-anchor="middle" font-size="11" font-weight="bold" fill="#94a3b8">Otkuda</text>

  <!-- Stroki -->
  <rect x="10" y="68" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="120" y="85" text-anchor="middle" font-size="11" fill="#60a5fa">Maybe</text>
  <rect x="240" y="68" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="350" y="85" text-anchor="middle" font-size="10" fill="#94a3b8">net dual&#39;a (Maybe &#8775; kom.)</text>
  <rect x="470" y="68" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="580" y="85" text-anchor="middle" font-size="9" fill="#94a3b8">net chistogo dual&#39;a</text>

  <rect x="10" y="100" width="220" height="28" rx="3" fill="#172554"/>
  <text x="120" y="117" text-anchor="middle" font-size="11" fill="#60a5fa">Either e</text>
  <rect x="240" y="100" width="220" height="28" rx="3" fill="#172554"/>
  <text x="350" y="117" text-anchor="middle" font-size="10" fill="#94a3b8">net dual&#39;a</text>
  <rect x="470" y="100" width="220" height="28" rx="3" fill="#172554"/>
  <text x="580" y="117" text-anchor="middle" font-size="9" fill="#94a3b8">net chistogo dual&#39;a</text>

  <rect x="10" y="132" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="120" y="149" text-anchor="middle" font-size="11" fill="#60a5fa">[] (List)</text>
  <rect x="240" y="132" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="350" y="149" text-anchor="middle" font-size="11" fill="#34d399">NonEmpty*</text>
  <rect x="470" y="132" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="580" y="149" text-anchor="middle" font-size="9" fill="#94a3b8">chastichno (Stream)</text>

  <rect x="10" y="164" width="220" height="28" rx="3" fill="#172554"/>
  <text x="120" y="181" text-anchor="middle" font-size="11" fill="#60a5fa">State s</text>
  <rect x="240" y="164" width="220" height="28" rx="3" fill="#172554"/>
  <text x="350" y="181" text-anchor="middle" font-size="11" fill="#34d399">Store s</text>
  <rect x="470" y="164" width="220" height="28" rx="3" fill="#172554"/>
  <text x="580" y="181" text-anchor="middle" font-size="9" fill="#94a3b8">(-&gt;s) &#8868; (s-&gt;)</text>

  <rect x="10" y="196" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="120" y="213" text-anchor="middle" font-size="11" fill="#60a5fa">Reader r</text>
  <rect x="240" y="196" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="350" y="213" text-anchor="middle" font-size="11" fill="#34d399">Env r</text>
  <rect x="470" y="196" width="220" height="28" rx="3" fill="#1e293b"/>
  <text x="580" y="213" text-anchor="middle" font-size="9" fill="#94a3b8">&#916; &#8868; &#928; (diagonal-produced)</text>

  <rect x="10" y="228" width="220" height="26" rx="3" fill="#172554"/>
  <text x="120" y="244" text-anchor="middle" font-size="11" fill="#60a5fa">Writer w</text>
  <rect x="240" y="228" width="220" height="26" rx="3" fill="#172554"/>
  <text x="350" y="244" text-anchor="middle" font-size="11" fill="#34d399">Traced w</text>
  <rect x="470" y="228" width="220" height="26" rx="3" fill="#172554"/>
  <text x="580" y="244" text-anchor="middle" font-size="9" fill="#94a3b8">w -> a (Monoid w)</text>
</svg>'''

with open(f'{BASE}/cm_comonad_pairs.svg', 'w', encoding='utf-8') as f:
    f.write(cm_pairs_svg)
print("cm_comonad_pairs.svg создан")

# ===== 2. cm_final.svg - итоговая диаграмма комонад =====
cm_final_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="380" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="680" height="380" fill="#0f172a" rx="10"/>
  <text x="340" y="28" text-anchor="middle" font-size="14" font-weight="bold" fill="#e2e8f0">Ierarkhiya komonad v Haskell</text>

  <!-- Endofunctor W (vershina) -->
  <rect x="220" y="45" width="240" height="50" rx="6" fill="#1e293b" stroke="#a78bfa" stroke-width="2"/>
  <text x="340" y="65" text-anchor="middle" font-size="12" font-weight="bold" fill="#a78bfa">Comonad W</text>
  <text x="340" y="82" text-anchor="middle" font-size="9" fill="#94a3b8">extract, extend, duplicate</text>
  <text x="340" y="95" text-anchor="middle" font-size="9" fill="#94a3b8">W : Hask -&gt; Hask</text>

  <!-- Strelki -->
  <line x1="290" y1="95" x2="155" y2="140" stroke="#334155" stroke-width="1.5"/>
  <line x1="340" y1="95" x2="340" y2="140" stroke="#334155" stroke-width="1.5"/>
  <line x1="390" y1="95" x2="525" y2="140" stroke="#334155" stroke-width="1.5"/>

  <!-- Uroveny 2 -->
  <rect x="60" y="140" width="165" height="50" rx="5" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="142" y="160" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">Store s</text>
  <text x="142" y="175" text-anchor="middle" font-size="9" fill="#94a3b8">s -&gt; a, s</text>
  <text x="142" y="188" text-anchor="middle" font-size="9" fill="#94a3b8">(dual&#39; State)</text>

  <rect x="257" y="140" width="165" height="50" rx="5" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="340" y="160" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">Env r</text>
  <text x="340" y="175" text-anchor="middle" font-size="9" fill="#94a3b8">(r, a)</text>
  <text x="340" y="188" text-anchor="middle" font-size="9" fill="#94a3b8">(dual&#39; Reader)</text>

  <rect x="455" y="140" width="165" height="50" rx="5" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="537" y="160" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">Traced w</text>
  <text x="537" y="175" text-anchor="middle" font-size="9" fill="#94a3b8">w -&gt; a</text>
  <text x="537" y="188" text-anchor="middle" font-size="9" fill="#94a3b8">(dual&#39; Writer)</text>

  <!-- Uroveny 3 -->
  <line x1="142" y1="190" x2="142" y2="240" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="340" y1="190" x2="340" y2="240" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="537" y1="190" x2="537" y2="240" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>

  <rect x="50" y="240" width="180" height="40" rx="4" fill="#172554" stroke="#60a5fa" stroke-width="1.2"/>
  <text x="140" y="255" text-anchor="middle" font-size="10" fill="#60a5fa">Stream</text>
  <text x="140" y="270" text-anchor="middle" font-size="9" fill="#94a3b8">beskon. posledovatel&#39;nost&#39;</text>

  <rect x="255" y="240" width="170" height="40" rx="4" fill="#172554" stroke="#60a5fa" stroke-width="1.2"/>
  <text x="340" y="255" text-anchor="middle" font-size="10" fill="#60a5fa">NonEmpty</text>
  <text x="340" y="270" text-anchor="middle" font-size="9" fill="#94a3b8">nepostoyannyj spisok</text>

  <rect x="458" y="240" width="170" height="40" rx="4" fill="#172554" stroke="#60a5fa" stroke-width="1.2"/>
  <text x="543" y="255" text-anchor="middle" font-size="10" fill="#60a5fa">Zipper</text>
  <text x="543" y="270" text-anchor="middle" font-size="9" fill="#94a3b8">fokusirovka na pozitsii</text>

  <!-- Zakony -->
  <rect x="20" y="305" width="640" height="62" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="340" y="322" text-anchor="middle" font-size="11" font-weight="bold" fill="#e2e8f0">Zakony komonady</text>
  <text x="340" y="340" text-anchor="middle" font-size="10" fill="#94a3b8">extract . extend f = f</text>
  <text x="340" y="355" text-anchor="middle" font-size="10" fill="#94a3b8">extend extract = id</text>
  <text x="340" y="362" text-anchor="middle" font-size="9" fill="#94a3b8">extend f . extend g = extend (f . extend g)</text>
</svg>'''

with open(f'{BASE}/cm_final.svg', 'w', encoding='utf-8') as f:
    f.write(cm_final_svg)
print("cm_final.svg создан")

# ===== 3. Правим Comonads.ipynb =====
nb_path = f'{BASE}/Comonads.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 80 - таблица дуальных пар
src80 = ''.join(cells[80]['source']) if isinstance(cells[80]['source'], list) else cells[80]['source']
if '\u041c\u041e\u041d\u0410\u0414\u0410' in src80 or 'MONADA' in src80:
    new_src80 = '## 11.5 \u041a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u044b\u0435 \u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u0440\u044b\n\n![Dual&#39;nye pary](cm_comonad_pairs.svg)'
    cells[80]['source'] = new_src80
    print("Ячейка 80 заменена")

# Ячейка 82 - итоговая диаграмма
new_src82 = '## 11.6 \u0418\u0442\u043e\u0433\u043e\u0432\u0430\u044f \u0434\u0438\u0430\u0433\u0440\u0430\u043c\u043c\u0430\n\n![\u0418\u0435\u0440\u0430\u0440\u0445\u0438\u044f \u043a\u043e\u043c\u043e\u043d\u0430\u0434](cm_final.svg)'
cells[82]['source'] = new_src82
print("Ячейка 82 заменена")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Comonads.ipynb сохранён")
