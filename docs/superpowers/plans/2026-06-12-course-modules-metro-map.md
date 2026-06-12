# План: модульная структура курса + карта-схема метро

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development или superpowers:executing-plans. Спека: `docs/superpowers/specs/2026-06-12-course-modules-metro-map-design.md`.

**Goal:** README.ipynb перестроен по модулям 0–VI, ASCII-граф заменён на генерируемую SVG-карту курса в стиле схемы метро.

**Architecture:** `src/scripts/coursemap/build_map.js` — данные дерева (линии/станции/пересадки) + рендер SVG → `src/notebooks/course_map.svg` (ASCII-only). `src/scripts/coursemap/restructure_readme.js` — разовая перестройка README.ipynb. Контент ноутбуков не трогается, кроме NAV-ссылок Adjunctions/KanExtensions при противоречии новому порядку.

**Tech Stack:** Node.js, Jupyter (контейнер уже поднят, bind-mount `src`).

**Палитра (из утверждённого мокапа v3):** база `#8a93a3`, жёлтая `#d9a441`/название `#b8862e`, синяя `#5872c9`, красная `#c4625f`, развилка `#0f172a`, вторичный текст `#64748b`, фон станций `#ffffff`.

---

### Task 0: Ветка

- [ ] `git checkout master; git pull; git checkout -b course-map`

### Task 1: Генератор карты

**Files:** Create `src/scripts/coursemap/build_map.js`

- [ ] Записать генератор (UTF-8 без BOM, но содержимое и так ASCII):

```js
// build_map.js — генерирует src/notebooks/course_map.svg (схема метро курса).
// Правки карты — только здесь. ASCII-only внутри SVG (правило курса).
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', '..', 'notebooks', 'course_map.svg');

const C = { base: '#8a93a3', yellow: '#d9a441', yellowName: '#b8862e',
  blue: '#5872c9', blueDark: '#3d4f8f', red: '#c4625f',
  hub: '#0f172a', text: '#0f172a', sub: '#64748b', bg: '#ffffff' };

// y-координаты станций; пересадка: mix = цвет второго кольца; terminus: плашка
const trunk = [
  { n: 'Extensions', y: 104 }, { n: 'BaseHaskell', y: 152 }, { n: 'TypeAlgebra', y: 200 },
  { n: 'FunctorHierarchy', y: 260 }, { n: 'FoldableTraversable', y: 308 },
  { n: 'Monads', y: 368 }, { n: 'MonadTransformers', y: 412 }, { n: 'Comonads', y: 456 },
];
const yellow = [
  { n: 'AlgebrasCoalgebras', y: 616 }, { n: 'Profunctors', y: 676 },
  { n: 'Optics', y: 736 }, { n: 'Arrows', y: 800, mix: C.blue },
];
const blue = [
  { n: 'YonedaLemma', y: 616 }, { n: 'Adjunctions', y: 676 }, { n: 'KanExtensions', y: 736 },
];
const red = [
  { n: 'MetaProgramming', y: 616 }, { n: 'Concurrency', y: 676, mix: C.base },
  { n: 'DistributedHaskell', y: 736 }, { n: 'GPUHaskell', y: 788, terminus: true },
];
const finals = [
  { n: 'Toposes', y: 858 }, { n: 'Uncertainty', y: 912, mix: C.base },
  { n: 'SubjectiveModeling', y: 968, mix: C.yellow, terminus: true, labelRight: true },
];
const TX = 350, YX = 150, RX = 570; // x ствола/жёлтой/красной

const esc = s => s; // имена ASCII; кириллицы нет по построению
function station(x, st, color, side) {
  const right = st.labelRight || side === 'right';
  const lx = right ? x + 22 : x - 22, anchor = right ? 'start' : 'end';
  const cls = st.mix ? 'stb' : 'st';
  let s = '';
  if (st.mix) {
    s += `<circle cx="${x}" cy="${st.y}" r="9" class="stn" stroke="${color}"/>` +
         `<circle cx="${x}" cy="${st.y}" r="4.5" fill="none" stroke="${st.mix}" stroke-width="3"/>`;
  } else {
    s += `<circle cx="${x}" cy="${st.y}" r="7" class="stn" stroke="${color}"/>`;
  }
  s += `<text x="${lx}" y="${st.y + 5}" text-anchor="${anchor}" class="${cls}">${esc(st.n)}</text>`;
  if (st.terminus) s += `<rect x="${x - 7}" y="${st.y + 16}" width="14" height="4.5" rx="2.25" fill="${color}"/>`;
  return s;
}

const body = `
<path class="ln" stroke="${C.base}" d="M${TX} 96 V500"/>
<path class="ln" stroke="${C.yellow}" d="M${TX} 500 C${TX} 560 ${YX} 540 ${YX} 600 V940 C${YX} 1006 254 1014 341 976"/>
<path class="ln" stroke="${C.blue}" d="M${TX} 500 V968"/>
<path class="ln" stroke="${C.red}" d="M${TX} 500 C${TX} 560 ${RX} 540 ${RX} 600 V790"/>
<text x="${TX + 22}" y="100" class="line-name" fill="#6b7484">BASE</text>
<text x="${YX}" y="572" class="line-name" fill="${C.yellowName}" text-anchor="middle">STRUCTURES &amp; OPTICS</text>
<text x="${TX + 22}" y="572" class="line-name" fill="${C.blue}">CATEGORY THEORY</text>
<text x="${RX + 22}" y="572" class="line-name" fill="${C.red}">PRACTICE</text>
<text x="${TX + 22}" y="850" class="line-name" fill="${C.blueDark}">TOPOSES &amp;</text>
<text x="${TX + 22}" y="866" class="line-name" fill="${C.blueDark}">UNCERTAINTY</text>
${trunk.map(s => station(TX, s, C.base, 'left')).join('\n')}
<circle cx="${TX}" cy="500" r="10" class="stn" stroke="${C.hub}"/>
<text x="${TX - 26}" y="494" text-anchor="end" class="stb">ComonadTransformers</text>
${yellow.map(s => station(YX, s, C.yellow, 'left')).join('\n')}
${blue.map(s => station(TX, s, C.blue, 'right')).join('\n')}
${red.map(s => station(RX, s, C.red, 'right')).join('\n')}
${finals.map(s => station(TX, s, C.blue, 'left')).join('\n')}
<g transform="translate(656 96)">
<rect x="-18" y="-24" width="222" height="220" rx="12" fill="none" stroke="#e2e8f0"/>
<text x="0" y="0" class="line-name" fill="${C.sub}">LEGEND</text>
<g transform="translate(0 28)">
<path class="ln" stroke="${C.base}" stroke-width="5" d="M0 0 H30"/><text x="42" y="4" class="sub">base of the course</text>
<path class="ln" stroke="${C.yellow}" stroke-width="5" d="M0 26 H30"/><text x="42" y="30" class="sub">structures &amp; optics</text>
<path class="ln" stroke="${C.blue}" stroke-width="5" d="M0 52 H30"/><text x="42" y="56" class="sub">category theory</text>
<path class="ln" stroke="${C.red}" stroke-width="5" d="M0 78 H30"/><text x="42" y="82" class="sub">practice</text>
<circle cx="15" cy="110" r="8" class="stn" stroke="${C.blue}"/>
<circle cx="15" cy="110" r="4" fill="none" stroke="${C.yellow}" stroke-width="2.5"/>
<text x="42" y="114" class="sub">interchange = topic mix</text>
<circle cx="15" cy="138" r="8" class="stn" stroke="${C.hub}"/>
<text x="42" y="142" class="sub">fork of the branches</text>
<text x="0" y="170" class="sub">further along the line = harder</text>
</g></g>`;

const svg = `<svg viewBox="0 0 880 1100" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Segoe UI', system-ui, sans-serif">
<title>Course map</title>
<desc>Metro-style map: gray base line, yellow structures, blue category theory, red practice. Interchange stations mix topics.</desc>
<style>
.st { font-size: 14px; font-weight: 450; fill: ${C.text}; }
.stb { font-size: 14px; font-weight: 650; fill: ${C.text}; }
.line-name { font-size: 11.5px; font-weight: 700; letter-spacing: .12em; }
.sub { font-size: 11px; fill: ${C.sub}; }
.ln { fill: none; stroke-linecap: round; stroke-width: 7; }
.stn { fill: ${C.bg}; stroke-width: 3.5; }
</style>
${body}
</svg>
`;

if (/[^\x00-\x7F]/.test(svg)) { console.error('NOT ASCII-ONLY'); process.exit(1); }
fs.writeFileSync(OUT, svg);
console.log('course_map.svg written, bytes: ' + svg.length);
```

- [ ] Запуск: `node src/scripts/coursemap/build_map.js` → `course_map.svg written, ...` (без `NOT ASCII-ONLY`).
- [ ] Детерминизм: повторный запуск, `git status` — файл не меняется после первого коммита (или `git diff --quiet src/notebooks/course_map.svg` после повторного запуска).
- [ ] XML well-formed: `node -e "const s=require('fs').readFileSync('src/notebooks/course_map.svg','utf8'); if(!s.includes('</svg>'))throw 1; const open=(s.match(/<(circle|text|rect|path)/g)||[]).length; console.log('elements:',open)"` (элементов ≥ 60) + открыть `http://localhost:8889/files/notebooks/course_map.svg` (вручную или curl → 200).
- [ ] Визуально сверить с мокапом v3 (подписи не пересекают линии: ствол/финал/жёлтая — слева, синяя/красная — справа, SubjectiveModeling — справа).
- [ ] Commit: `git add src/scripts/coursemap/build_map.js src/notebooks/course_map.svg; git commit -m "map: генератор и course_map.svg (схема метро)"`

### Task 2: Реструктуризация README.ipynb

**Files:** Create `src/scripts/coursemap/restructure_readme.js`; Modify `src/README.ipynb`

Скрипт читает `src/README.ipynb`, находит ячейки по содержимому/id и выполняет операции ниже. Карточки находить по подстроке `**Файл:** [\`<Name>.ipynb\`]` в source. После всех операций — `JSON.stringify(nb, null, 1) + '\n'`.

- [ ] **Op 1 — Содержание.** Ячейку с `📌 Содержание` заменить целиком на:

```markdown
📌 Содержание

| # | Ноутбук | Уровень |
|---|---------|---------|
| **Модуль 0 — Старт** | | |
| 0.1 | [⚙️ Расширения GHC: бриф](notebooks/Extensions.ipynb) | 🟢 начальный |
| 0.2 | [🎓 Базовый Haskell](notebooks/BaseHaskell.ipynb) | 🟢 начальный |
| 0.3 | [🧮 Типы как алгебра](notebooks/TypeAlgebra.ipynb) | 🟢 нач/сред |
| **Модуль I — Функторы** | | |
| I.1 | [🔺 Иерархия функторов](notebooks/FunctorHierarchy.ipynb) | 🟡 нач/сред |
| I.2 | [🌀 Foldable & Traversable](notebooks/FoldableTraversable.ipynb) | 🟠 сред/+ |
| **Модуль II — Эффекты** | | |
| II.1 | [🗺️ Монады](notebooks/Monads.ipynb) | 🟡 средний |
| II.2 | [🔧 Трансформеры монад](notebooks/MonadTransformers.ipynb) | 🟡 средний |
| II.3 | [🫞 Комонады](notebooks/Comonads.ipynb) | 🟠 сред/+ |
| II.4 | [⭐ Трансформеры комонад](notebooks/ComonadTransformers.ipynb) | 🟠 сред/+ |
| **Модуль III — Структуры и оптики** | | |
| III.1 | [🏗️ Алгебры и Коалгебры](notebooks/AlgebrasCoalgebras.ipynb) | 🔴 продвин. |
| III.2 | [↔️ Профункторы](notebooks/Profunctors.ipynb) | 🔴 продвин. |
| III.3 | [🔍 Оптики](notebooks/Optics.ipynb) | 🔴 продвин. |
| III.4 | [🎯 Arrows](notebooks/Arrows.ipynb) | ⚫ эксперт. |
| **Модуль IV — Теория категорий** | | |
| IV.1 | [∀ Лемма Ёнеды](notebooks/YonedaLemma.ipynb) | 🔴 продвин. |
| IV.2 | [🔗 Сопряжения](notebooks/Adjunctions.ipynb) | ⚫ эксперт. |
| IV.3 | [🔭 Расширения Кана](notebooks/KanExtensions.ipynb) | ⚫ эксперт. |
| **Модуль V — Практика** | | |
| V.1 | [🔮 Метапрограммирование](notebooks/MetaProgramming.ipynb) | ⚫ эксперт. |
| V.2 | [🧵 Конкурентность](notebooks/Concurrency.ipynb) | 🔴 сред/продв. |
| V.3 | [🌐 Distributed Haskell](notebooks/DistributedHaskell.ipynb) | ⚫ эксперт. |
| V.4 | [🚀 GPU / Accelerate](notebooks/GPUHaskell.ipynb) | ⚫ специал. |
| **Модуль VI — Топосы и неопределённость** | | |
| VI.1 | [🌏 Топосы](notebooks/Toposes.ipynb) | ⚫ эксперт. |
| VI.2 | [❓ Неопределённость](notebooks/Uncertainty.ipynb) | ⚫ эксперт. |
| VI.3 | [🧮 Теория Пытьева](notebooks/SubjectiveModeling.ipynb) | ⚫ эксперт. |
```

- [ ] **Op 2 — Карта.** Ячейку `## 🗺️ Карта тем` (ASCII-блок) заменить на:

```markdown
---

## 🗺️ Карта курса

![course map](notebooks/course_map.svg)

**Легенда:** серая линия — база курса (Старт → Функторы → Эффекты); жёлтая — структуры и оптики; синяя — теория категорий (продолжается в Топосы и неопределённость); красная — практика. Станция с двумя кольцами — пересадка: ноутбук смешивает темы двух линий (Arrows = структуры × ТК, Concurrency = практика × эффекты, Uncertainty = ТК × эффекты, SubjectiveModeling = ТК × структуры). Чёрный узел — развилка после ComonadTransformers. Дальше по линии — сложнее. Карта генерируется `scripts/coursemap/build_map.js` — руками не править.
```

- [ ] **Op 3 — Порядок карточек.** Переставить markdown-карточки (ячейки с `**Файл:**`) в порядок: Extensions (`readme_ext_card`), BaseHaskell, TypeAlgebra, FunctorHierarchy, FoldableTraversable, Monads, MonadTransformers, Comonads, ComonadTransformers, AlgebrasCoalgebras, Profunctors, Optics, Arrows, YonedaLemma, Adjunctions, KanExtensions, MetaProgramming, Concurrency, DistributedHaskell, GPUHaskell, Toposes, Uncertainty, SubjectiveModeling. Карточки идут сплошным блоком после ячейки карты (Op 2), перед сводной таблицей.
- [ ] **Op 4 — Заголовки карточек.** В каждой карточке первую строку `## <старый номер+эмодзи> <название>` заменить на `## <новый номер> <эмодзи> <название>` по нумерации Op 1 (например `## 1️⃣3️⃣ 🔭 Расширения Кана` → `## IV.3 🔭 Расширения Кана`; `## 0️⃣ ⚙️ Расширения GHC: бриф` → `## 0.1 ⚙️ Расширения GHC: бриф`). Реализация: regex `^## .*?(?=[А-ЯA-Z⚙🎓🧮🔺🌀🗺🔧🫞⭐🏗↔🔍🎯∀🔗🔭🔮🧵🌐🚀🌏❓])` не надёжен — проще таблица соответствий «имя файла → новый заголовок» в скрипте, первая строка карточки заменяется целиком.
- [ ] **Op 5 — Пререквизиты.** В карточке Adjunctions строку `**Предварительно:** [KanExtensions.ipynb](notebooks/KanExtensions.ipynb)` заменить на `**Предварительно:** [YonedaLemma.ipynb](notebooks/YonedaLemma.ipynb)`. В карточке KanExtensions: `**Предварительно:** [YonedaLemma.ipynb](notebooks/YonedaLemma.ipynb), [MonadTransformers.ipynb](notebooks/MonadTransformers.ipynb)` → `**Предварительно:** [Adjunctions.ipynb](notebooks/Adjunctions.ipynb), [MonadTransformers.ipynb](notebooks/MonadTransformers.ipynb)` (точные старые строки сверить по факту, менять только имена ноутбуков).
- [ ] **Op 6 — Сводная таблица.** В ячейке `## 📊 Сводная таблица` строки перегруппировать по модулям с теми же разделителями `| **Модуль …** | | | | | |` и номерами 0.1–VI.3 (данные строк — ячейки/SVG/статус — не менять). Итоговую строку оставить: 23 ноутбука, 83 SVG (карта курса не считается — она вне ноутбуков), 906 ячеек.
- [ ] **Op 7 — Удаления.** Удалить ячейку `## 🔄 Граф зависимостей` (ASCII) и хвостовые мусорные ячейки (markdown `## ` пустые, raw-пустышка, code-пустышки в конце файла — всё после сводной таблицы, что не содержит контента).
- [ ] Запуск скрипта; JSON-валидность; проверка: `node -e` — все 23 имени `*.ipynb` встречаются в README.ipynb, ячейки `deps_header` нет (README не ноутбук курса), число карточек = 23.
- [ ] Открыть README.ipynb в Jupyter (Reload from Disk), проверить рендер карты и таблиц.
- [ ] Commit: `git add src/README.ipynb src/scripts/coursemap/restructure_readme.js; git commit -m "map: README.ipynb — модули 0–VI, карта-метро вместо ASCII-графа"`

### Task 3: NAV-ячейки Adjunctions / KanExtensions

**Files:** Possibly modify `src/notebooks/Adjunctions.ipynb`, `src/notebooks/KanExtensions.ipynb` (только markdown NAV)

- [ ] Найти NAV-ячейки (markdown со ссылками «следующий/предыдущий» в начале или конце): `node`-скриптом вывести все markdown-ячейки этих двух ноутбуков, содержащие `.ipynb`.
- [ ] Если NAV говорит «KanExtensions → далее Adjunctions» или «Adjunctions ← перед этим KanExtensions» — поменять направление: после YonedaLemma идёт Adjunctions, затем KanExtensions, затем (модуль V/VI по выбору читателя — оставить ссылку на Toposes из KanExtensions, если она там есть). Менять ТОЛЬКО ссылки/подписи навигации, не контент.
- [ ] Если противоречий нет — задача закрывается без изменений (отметить в отчёте).
- [ ] JSON-валидность изменённых файлов; commit (если были изменения): `git add src/notebooks/Adjunctions.ipynb src/notebooks/KanExtensions.ipynb; git commit -m "map: NAV-ссылки под новый порядок Adjunctions → KanExtensions"`

### Task 4: ROADMAP + README.md

**Files:** Modify `src/ROADMAP.md`, `README.md`

- [ ] ROADMAP: фаза «Фаза 17 — Модульная структура курса + карта-метро» (таблица: генератор карты / course_map.svg / README.ipynb модули / NAV-фиксы / README.md). В «Критические правила» добавить: «`course_map.svg` генерируется `src/scripts/coursemap/build_map.js` — руками не править».
- [ ] README.md: в дерево файлов добавить `scripts/coursemap/` и `notebooks/course_map.svg`; абзац про модульную структуру (0 Старт, I Функторы, II Эффекты, III Структуры и оптики, IV Теория категорий, V Практика, VI Топосы и неопределённость) и рекомендуемый маршрут: ствол по порядку, после ComonadTransformers — любая ветка.
- [ ] Commit: `git add src/ROADMAP.md README.md; git commit -m "map: ROADMAP Фаза 17 + README"`

### Task 5: Финиш

- [ ] Повторный `node src/scripts/coursemap/build_map.js` → файл без изменений (`git status` чист).
- [ ] `node src/scripts/deps/gen_headers.js` → `updated: 0` (шапки не задеты).
- [ ] superpowers:finishing-a-development-branch — merge в master по выбору пользователя.
