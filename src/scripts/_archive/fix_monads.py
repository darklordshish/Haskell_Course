import json

BASE = '/home/jovyan/src'

# ===== 1. monad_hierarchy.svg - итоговая диаграмма иерархии монад =====
monad_hier_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="480" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="720" height="480" fill="#0f172a" rx="10"/>
  <text x="360" y="28" text-anchor="middle" font-size="14" font-weight="bold" fill="#e2e8f0">Ierarkhiya monad v Haskell</text>

  <!-- Monad (vershina) -->
  <rect x="270" y="45" width="180" height="44" rx="6" fill="#1e293b" stroke="#a78bfa" stroke-width="2"/>
  <text x="360" y="63" text-anchor="middle" font-size="12" font-weight="bold" fill="#a78bfa">Monad</text>
  <text x="360" y="80" text-anchor="middle" font-size="9" fill="#94a3b8">return, &gt;&gt;=, join, &gt;=&gt;</text>

  <!-- Strelki ot Monad -->
  <line x1="310" y1="89" x2="160" y2="128" stroke="#334155" stroke-width="1.5"/>
  <line x1="360" y1="89" x2="360" y2="128" stroke="#334155" stroke-width="1.5"/>
  <line x1="410" y1="89" x2="560" y2="128" stroke="#334155" stroke-width="1.5"/>

  <!-- Uroveny 2: Maybe, Either, [] -->
  <rect x="80" y="128" width="150" height="44" rx="5" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="155" y="147" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Maybe</text>
  <text x="155" y="163" text-anchor="middle" font-size="9" fill="#94a3b8">1 + a (proval)</text>

  <rect x="280" y="128" width="160" height="44" rx="5" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="360" y="147" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Either e</text>
  <text x="360" y="163" text-anchor="middle" font-size="9" fill="#94a3b8">e + a (s ob"yasneniem)</text>

  <rect x="490" y="128" width="140" height="44" rx="5" fill="#1e293b" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="560" y="147" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">[] (List)</text>
  <text x="560" y="163" text-anchor="middle" font-size="9" fill="#94a3b8">P(a) (nedeterminizm)</text>

  <!-- Maybe -> isomorfno Either () a -->
  <text x="155" y="188" text-anchor="middle" font-size="9" fill="#94a3b8">&#8773; Either () a</text>

  <!-- Strelki ot Maybe k State/Reader/Writer -->
  <line x1="200" y1="172" x2="120" y2="248" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="360" y1="172" x2="360" y2="248" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="490" y1="172" x2="600" y2="248" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>

  <!-- Uroveny 3: State, Reader, Writer -->
  <rect x="35" y="248" width="145" height="44" rx="5" fill="#172554" stroke="#34d399" stroke-width="1.5"/>
  <text x="112" y="265" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">State s</text>
  <text x="112" y="281" text-anchor="middle" font-size="9" fill="#94a3b8">s -&gt; (a, s)</text>

  <rect x="285" y="248" width="150" height="44" rx="5" fill="#172554" stroke="#34d399" stroke-width="1.5"/>
  <text x="360" y="265" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">Reader r</text>
  <text x="360" y="281" text-anchor="middle" font-size="9" fill="#94a3b8">r -&gt; a</text>

  <rect x="540" y="248" width="145" height="44" rx="5" fill="#172554" stroke="#34d399" stroke-width="1.5"/>
  <text x="612" y="265" text-anchor="middle" font-size="11" font-weight="bold" fill="#34d399">Writer w</text>
  <text x="612" y="281" text-anchor="middle" font-size="9" fill="#94a3b8">(a, w)</text>

  <!-- RWS -->
  <line x1="112" y1="292" x2="280" y2="330" stroke="#334155" stroke-width="1.2"/>
  <line x1="360" y1="292" x2="360" y2="330" stroke="#334155" stroke-width="1.2"/>
  <line x1="612" y1="292" x2="440" y2="330" stroke="#334155" stroke-width="1.2"/>
  <rect x="290" y="330" width="140" height="34" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="360" y="354" text-anchor="middle" font-size="11" font-weight="bold" fill="#f59e0b">RWS = R+W+S</text>

  <!-- IO, ST, STM, Cont -->
  <line x1="180" y1="292" x2="60" y2="390" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="540" y1="292" x2="660" y2="390" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>

  <rect x="20" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="70" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">IO</text>
  <text x="70" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">RealWorld</text>

  <rect x="135" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="185" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">ST s</text>
  <text x="185" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">Safe mutable</text>

  <rect x="250" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="300" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">STM</text>
  <text x="300" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">Atom. transakts.</text>

  <rect x="370" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="420" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">Cont r</text>
  <text x="420" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">Prodolzheniya</text>

  <rect x="490" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="540" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">Free f</text>
  <text x="540" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">DSL/Interpret.</text>

  <rect x="605" y="390" width="100" height="36" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="655" y="406" text-anchor="middle" font-size="10" font-weight="bold" fill="#fb923c">Parser</text>
  <text x="655" y="420" text-anchor="middle" font-size="8" fill="#94a3b8">&#8773;StateT Maybe</text>

  <!-- Legenda -->
  <rect x="20" y="445" width="680" height="28" rx="4" fill="#1e293b" stroke="#334155"/>
  <text x="360" y="458" text-anchor="middle" font-size="9" fill="#94a3b8">Transformery monad: MaybeT, ExceptT, StateT, ReaderT, WriterT, ContT</text>
  <text x="360" y="469" text-anchor="middle" font-size="9" fill="#94a3b8">pozvolyayut kombinirovat effekty v odnom steke</text>
</svg>'''

with open(f'{BASE}/monad_hierarchy.svg', 'w', encoding='utf-8') as f:
    f.write(monad_hier_svg)
print("monad_hierarchy.svg создан")

# ===== 2. monad_choice.svg - таблица "Когда какую монаду выбрать?" =====
monad_choice_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="290" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="700" height="290" fill="#0f172a" rx="8"/>
  <text x="350" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Kogda kakuyu monadu vybrat?</text>

  <!-- Zagolovki -->
  <rect x="10" y="36" width="380" height="26" rx="4" fill="#172554"/>
  <text x="200" y="53" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Nuzhno...</text>
  <rect x="400" y="36" width="290" height="26" rx="4" fill="#172554"/>
  <text x="545" y="53" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Ispol&#39;zuj</text>

  <!-- Stroki -->
  <rect x="10" y="68" width="380" height="24" rx="3" fill="#1e293b"/>
  <text x="20" y="84" font-size="10" fill="#e2e8f0">Bezopasnyj dostup / poisk</text>
  <rect x="400" y="68" width="290" height="24" rx="3" fill="#1e293b"/>
  <text x="410" y="84" font-size="10" font-weight="bold" fill="#60a5fa">Maybe</text>

  <rect x="10" y="96" width="380" height="24" rx="3" fill="#172554"/>
  <text x="20" y="112" font-size="10" fill="#e2e8f0">Obrabotka oshibok s diagnostikoj</text>
  <rect x="400" y="96" width="290" height="24" rx="3" fill="#172554"/>
  <text x="410" y="112" font-size="10" font-weight="bold" fill="#60a5fa">Either e</text>

  <rect x="10" y="124" width="380" height="24" rx="3" fill="#1e293b"/>
  <text x="20" y="140" font-size="10" fill="#e2e8f0">Perebor / kombinatorika</text>
  <rect x="400" y="124" width="290" height="24" rx="3" fill="#1e293b"/>
  <text x="410" y="140" font-size="10" font-weight="bold" fill="#60a5fa">[] (List)</text>

  <rect x="10" y="152" width="380" height="24" rx="3" fill="#172554"/>
  <text x="20" y="168" font-size="10" fill="#e2e8f0">Pobochnye effekty / IO</text>
  <rect x="400" y="152" width="290" height="24" rx="3" fill="#172554"/>
  <text x="410" y="168" font-size="10" font-weight="bold" fill="#60a5fa">IO</text>

  <rect x="10" y="180" width="380" height="24" rx="3" fill="#1e293b"/>
  <text x="20" y="196" font-size="10" fill="#e2e8f0">Izmenyaemoe sostoyanie (chistoe)</text>
  <rect x="400" y="180" width="290" height="24" rx="3" fill="#1e293b"/>
  <text x="410" y="196" font-size="10" font-weight="bold" fill="#34d399">State s</text>

  <rect x="10" y="208" width="380" height="24" rx="3" fill="#172554"/>
  <text x="20" y="224" font-size="10" fill="#e2e8f0">Konfiguraciya / okruzhenie</text>
  <rect x="400" y="208" width="290" height="24" rx="3" fill="#172554"/>
  <text x="410" y="224" font-size="10" font-weight="bold" fill="#34d399">Reader r</text>

  <rect x="10" y="236" width="380" height="24" rx="3" fill="#1e293b"/>
  <text x="20" y="252" font-size="10" fill="#e2e8f0">Nakoplenie loga / metrik</text>
  <rect x="400" y="236" width="290" height="24" rx="3" fill="#1e293b"/>
  <text x="410" y="252" font-size="10" font-weight="bold" fill="#34d399">Writer w</text>

  <rect x="10" y="264" width="380" height="20" rx="3" fill="#172554"/>
  <text x="20" y="278" font-size="10" fill="#e2e8f0">Vsyo srazu: Read + Write + State</text>
  <rect x="400" y="264" width="290" height="20" rx="3" fill="#172554"/>
  <text x="410" y="278" font-size="10" font-weight="bold" fill="#f59e0b">RWS</text>
</svg>'''

with open(f'{BASE}/monad_choice.svg', 'w', encoding='utf-8') as f:
    f.write(monad_choice_svg)
print("monad_choice.svg создан")

# ===== 3. Правим ноутбук =====
nb_path = f'{BASE}/Monads.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Ячейка 136 - заменяем ASCII таблицу на SVG
new_src136 = '## 15.4 \u041a\u043e\u0433\u0434\u0430 \u043a\u0430\u043a\u0443\u044e \u043c\u043e\u043d\u0430\u0434\u0443 \u0432\u044b\u0431\u0440\u0430\u0442\u044c?\n\n![Kogda kakuyu monadu](monad_choice.svg)'
cells[136]['source'] = new_src136
print("Ячейка 136 заменена")

# Ячейка 137 - заменяем ASCII диаграмму на SVG
new_src137 = '---\n## \U0001f9e9\u0418\u0442\u043e\u0433\u043e\u0432\u0430\u044f \u0434\u0438\u0430\u0433\u0440\u0430\u043c\u043c\u0430\n\n![\u0418\u0435\u0440\u0430\u0440\u0445\u0438\u044f \u043c\u043e\u043d\u0430\u0434](monad_hierarchy.svg)\n\n**\u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u044b \u043c\u043e\u043d\u0430\u0434** (\u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u043d\u043e\u0443\u0442\u0431\u0443\u043a): MaybeT, ExceptT, StateT, ReaderT, WriterT, ContT \u2014 \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u044e\u0442 **\u043a\u043e\u043c\u0431\u0438\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c** \u044d\u0444\u0444\u0435\u043a\u0442\u044b \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u043c\u043e\u043d\u0430\u0434 \u0432 \u043e\u0434\u043d\u043e\u043c \u0441\u0442\u0435\u043a\u0435.'
cells[137]['source'] = new_src137
print("Ячейка 137 заменена")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Ноутбук сохранён")
