import json

BASE = '/home/jovyan/src'

# Создаём dist_table.svg - таблица категорного взгляда (замена markdown-таблицы)
dist_table_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="220" font-family="monospace,'JetBrains Mono',Arial,sans-serif">
  <rect width="700" height="220" fill="#0f172a" rx="8"/>

  <!-- Заголовок -->
  <rect x="0" y="0" width="700" height="36" fill="#1e293b" rx="8"/>
  <rect x="0" y="28" width="700" height="8" fill="#1e293b"/>
  <text x="350" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">Kategornyj vzglyad: edinaya kartina</text>

  <!-- Zagolovki kolonok -->
  <rect x="10" y="44" width="215" height="28" fill="#172554" rx="4"/>
  <text x="117" y="62" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Kontseptsiya</text>

  <rect x="235" y="44" width="215" height="28" fill="#172554" rx="4"/>
  <text x="342" y="62" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Kategornyj ob"ekt</text>

  <rect x="460" y="44" width="228" height="28" fill="#172554" rx="4"/>
  <text x="574" y="62" text-anchor="middle" font-size="11" font-weight="bold" fill="#60a5fa">Kategornyj morfizm</text>

  <!-- Stroka 1 -->
  <rect x="10" y="80" width="215" height="28" fill="#1e293b" rx="3"/>
  <text x="117" y="98" text-anchor="middle" font-size="11" fill="#a78bfa">Pi-ischislenie</text>
  <rect x="235" y="80" width="215" height="28" fill="#1e293b" rx="3"/>
  <text x="342" y="98" text-anchor="middle" font-size="10" fill="#94a3b8">tipy kanalov</text>
  <rect x="460" y="80" width="228" height="28" fill="#1e293b" rx="3"/>
  <text x="574" y="98" text-anchor="middle" font-size="10" fill="#94a3b8">protsessy</text>

  <!-- Stroka 2 -->
  <rect x="10" y="116" width="215" height="28" fill="#172554" rx="3"/>
  <text x="117" y="134" text-anchor="middle" font-size="11" fill="#a78bfa">Cloud Haskell</text>
  <rect x="235" y="116" width="215" height="28" fill="#172554" rx="3"/>
  <text x="342" y="134" text-anchor="middle" font-size="10" fill="#94a3b8">aktory (ProcessId)</text>
  <rect x="460" y="116" width="228" height="28" fill="#172554" rx="3"/>
  <text x="574" y="134" text-anchor="middle" font-size="10" fill="#94a3b8">soobshcheniya</text>

  <!-- Stroka 3 -->
  <rect x="10" y="152" width="215" height="28" fill="#1e293b" rx="3"/>
  <text x="117" y="170" text-anchor="middle" font-size="11" fill="#a78bfa">CRDT</text>
  <rect x="235" y="152" width="215" height="28" fill="#1e293b" rx="3"/>
  <text x="342" y="170" text-anchor="middle" font-size="10" fill="#94a3b8">sostoyaniya uzlov</text>
  <rect x="460" y="152" width="228" height="28" fill="#1e293b" rx="3"/>
  <text x="574" y="170" text-anchor="middle" font-size="10" fill="#94a3b8">merge (polureshyotka)</text>

  <!-- Stroka 4 -->
  <rect x="10" y="188" width="215" height="28" fill="#172554" rx="3"/>
  <text x="117" y="206" text-anchor="middle" font-size="11" fill="#a78bfa">MapReduce</text>
  <rect x="235" y="188" width="215" height="28" fill="#172554" rx="3"/>
  <text x="342" y="206" text-anchor="middle" font-size="10" fill="#94a3b8">shardy dannykh</text>
  <rect x="460" y="188" width="228" height="28" fill="#172554" rx="3"/>
  <text x="574" y="206" text-anchor="middle" font-size="10" fill="#94a3b8">mapper o reducer</text>
</svg>'''

with open(f'{BASE}/dist_table.svg', 'w', encoding='utf-8') as f:
    f.write(dist_table_svg)
print("dist_table.svg создан")

# Правим ноутбук - заменяем markdown-таблицу на SVG
nb_path = f'{BASE}/DistributedHaskell.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
cell12 = cells[12]
src = ''.join(cell12['source']) if isinstance(cell12['source'], list) else cell12['source']

# Заменяем markdown-таблицу на ссылку на SVG
new_src = '## \U0001f535\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u043d\u044b\u0439 \u0432\u0437\u0433\u043b\u044f\u0434: \u0435\u0434\u0438\u043d\u0430\u044f \u043a\u0430\u0440\u0442\u0438\u043d\u0430\n\n![Kategornyj vzglyad](dist_table.svg)\n\n**\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0438\u0434\u0435\u0438:**\n- CRDT = join-\u043f\u043e\u043b\u0443\u0440\u0435\u0448\u0451\u0442\u043a\u0430: \u0441\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435 \u0433\u0430\u0440\u0430\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043e \u0430\u043b\u0433\u0435\u0431\u0440\u0430\u0438\u0447\u0435\u0441\u043a\u0438\n- Process \u043c\u043e\u043d\u0430\u0434\u0430 = kleisli-\u0441\u0442\u0440\u0435\u043b\u043a\u0430: `a -> Process b`\n- MapReduce = \u0444\u0443\u043d\u043a\u0442\u043e\u0440 + \u043a\u0430\u0442\u0430\u043c\u043e\u0440\u0444\u0438\u0437\u043c\n- TChan/TQueue = \u043a\u0430\u043d\u0430\u043b \u0432 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 Proc\n\n![\u041b\u0430\u043d\u0434\u0448\u0430\u0444\u0442 \u0440\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0451\u043d\u043d\u044b\u0445 \u0432\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439](dist_landscape.svg)'

cells[12]['source'] = new_src

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Ноутбук сохранён")
