// restructure_readme.js — разовая перестройка src/README.ipynb по модулям 0–VI
// (спека docs/superpowers/specs/2026-06-12-course-modules-metro-map-design.md).
const fs = require('fs'), path = require('path');
const P = path.join(__dirname, '..', '..', 'README.ipynb');
const nb = JSON.parse(fs.readFileSync(P, 'utf8'));
const get = c => Array.isArray(c.source) ? c.source.join('') : c.source;
const set = (c, s) => { c.source = s.split(/(?<=\n)/); };
const byId = id => {
  const c = nb.cells.find(c => c.id === id);
  if (!c) throw new Error('нет ячейки ' + id);
  return c;
};
const cardOf = name => {
  const c = nb.cells.find(c => get(c).includes('**Файл:** [`' + name + '.ipynb`]'));
  if (!c) throw new Error('нет карточки ' + name);
  return c;
};

// ---- Op 1: Содержание ----
set(byId('f97907eb'), `📌 Содержание

| # | Ноутбук | Уровень |
|---|---------|---------|
| **Модуль 0 — Старт** | | |
| 0.1 | [⚙️ Расширения GHC: бриф](notebooks/Extensions.ipynb) | \u{1F7E2} начальный |
| 0.2 | [\u{1F393} Базовый Haskell](notebooks/BaseHaskell.ipynb) | \u{1F7E2} начальный |
| 0.3 | [\u{1F9EE} Типы как алгебра](notebooks/TypeAlgebra.ipynb) | \u{1F7E2} нач/сред |
| **Модуль I — Функторы** | | |
| I.1 | [\u{1F53A} Иерархия функторов](notebooks/FunctorHierarchy.ipynb) | \u{1F7E1} нач/сред |
| I.2 | [\u{1F300} Foldable & Traversable](notebooks/FoldableTraversable.ipynb) | \u{1F7E0} сред/+ |
| **Модуль II — Эффекты** | | |
| II.1 | [\u{1F5FA}️ Монады](notebooks/Monads.ipynb) | \u{1F7E1} средний |
| II.2 | [\u{1F527} Трансформеры монад](notebooks/MonadTransformers.ipynb) | \u{1F7E1} средний |
| II.3 | [\u{1FA9E} Комонады](notebooks/Comonads.ipynb) | \u{1F7E0} сред/+ |
| II.4 | [⭐ Трансформеры комонад](notebooks/ComonadTransformers.ipynb) | \u{1F7E0} сред/+ |
| **Модуль III — Структуры и оптики** | | |
| III.1 | [\u{1F3D7}️ Алгебры и Коалгебры](notebooks/AlgebrasCoalgebras.ipynb) | \u{1F534} продвин. |
| III.2 | [↔️ Профункторы](notebooks/Profunctors.ipynb) | \u{1F534} продвин. |
| III.3 | [\u{1F50D} Оптики](notebooks/Optics.ipynb) | \u{1F534} продвин. |
| III.4 | [\u{1F3AF} Arrows](notebooks/Arrows.ipynb) | ⚫ эксперт. |
| **Модуль IV — Теория категорий** | | |
| IV.1 | [∀ Лемма Ёнеды](notebooks/YonedaLemma.ipynb) | \u{1F534} продвин. |
| IV.2 | [\u{1F517} Сопряжения](notebooks/Adjunctions.ipynb) | ⚫ эксперт. |
| IV.3 | [\u{1F52D} Расширения Кана](notebooks/KanExtensions.ipynb) | ⚫ эксперт. |
| **Модуль V — Практика** | | |
| V.1 | [\u{1F52E} Метапрограммирование](notebooks/MetaProgramming.ipynb) | ⚫ эксперт. |
| V.2 | [\u{1F9F5} Конкурентность](notebooks/Concurrency.ipynb) | \u{1F534} сред/продв. |
| V.3 | [\u{1F310} Distributed Haskell](notebooks/DistributedHaskell.ipynb) | ⚫ эксперт. |
| V.4 | [\u{1F680} GPU / Accelerate](notebooks/GPUHaskell.ipynb) | ⚫ специал. |
| **Модуль VI — Топосы и неопределённость** | | |
| VI.1 | [\u{1F30F} Топосы](notebooks/Toposes.ipynb) | ⚫ эксперт. |
| VI.2 | [❓ Неопределённость](notebooks/Uncertainty.ipynb) | ⚫ эксперт. |
| VI.3 | [\u{1F9EE} Теория Пытьева](notebooks/SubjectiveModeling.ipynb) | ⚫ эксперт. |
`);

// ---- Op 2: Карта ----
set(byId('a5550535'), `---

## \u{1F5FA}️ Карта курса

![course map](notebooks/course_map.svg)

**Легенда:** серая линия — база курса (Старт → Функторы → Эффекты); жёлтая — структуры и оптики; синяя — теория категорий (продолжается в Топосы и неопределённость); красная — практика. Станция с двумя кольцами — пересадка: ноутбук смешивает темы двух линий (Arrows = структуры × ТК, Concurrency = практика × эффекты, Uncertainty = ТК × эффекты, SubjectiveModeling = ТК × структуры). Чёрный узел — развилка после ComonadTransformers. Дальше по линии — сложнее. Карта генерируется \`scripts/coursemap/build_map.js\` — руками не править.
`);

// ---- Op 4+5: заголовки и пререквизиты карточек ----
const heads = {
  Extensions: '## 0.1 ⚙️ Расширения GHC: бриф',
  BaseHaskell: '## 0.2 \u{1F393} Базовый Haskell',
  TypeAlgebra: '## 0.3 \u{1F9EE} Типы как алгебра',
  FunctorHierarchy: '## I.1 \u{1F53A} Иерархия функторов',
  FoldableTraversable: '## I.2 \u{1F300} Foldable & Traversable',
  Monads: '## II.1 \u{1F5FA}️ Монады',
  MonadTransformers: '## II.2 \u{1F527} Трансформеры монад',
  Comonads: '## II.3 \u{1FA9E} Комонады',
  ComonadTransformers: '## II.4 ⭐ Трансформеры комонад',
  AlgebrasCoalgebras: '## III.1 \u{1F3D7}️ Алгебры и Коалгебры',
  Profunctors: '## III.2 ↔️ Профункторы',
  Optics: '## III.3 \u{1F50D} Оптики',
  Arrows: '## III.4 \u{1F3AF} Arrows',
  YonedaLemma: '## IV.1 ∀ Лемма Ёнеды',
  Adjunctions: '## IV.2 \u{1F517} Сопряжения',
  KanExtensions: '## IV.3 \u{1F52D} Расширения Кана',
  MetaProgramming: '## V.1 \u{1F52E} Метапрограммирование',
  Concurrency: '## V.2 \u{1F9F5} Конкурентность и параллелизм',
  DistributedHaskell: '## V.3 \u{1F310} Distributed Haskell',
  GPUHaskell: '## V.4 \u{1F680} GPU / Accelerate',
  Toposes: '## VI.1 \u{1F30F} Топосы, Пучки и Логика Классификатора',
  Uncertainty: '## VI.2 ❓ Неопределённость & Случайность',
  SubjectiveModeling: '## VI.3 \u{1F9EE} Теория Субъективного Моделирования',
};
const order = Object.keys(heads);
for (const name of order) {
  const c = cardOf(name);
  const lines = get(c).split('\n');
  const i = lines.findIndex(l => l.startsWith('## '));
  if (i < 0) throw new Error('нет заголовка в карточке ' + name);
  lines[i] = heads[name];
  set(c, lines.join('\n'));
}
const fixPrereq = (name, val) => {
  const c = cardOf(name);
  const lines = get(c).split('\n');
  const i = lines.findIndex(l => l.startsWith('**Предварительно:**'));
  if (i < 0) throw new Error('нет пререквизитов в ' + name);
  lines[i] = '**Предварительно:** ' + val;
  set(c, lines.join('\n'));
};
// F&T переехал в модуль I (до монад) — убираем ссылку вперёд на Monads
fixPrereq('FoldableTraversable', '[FunctorHierarchy.ipynb](notebooks/FunctorHierarchy.ipynb)');
fixPrereq('Adjunctions', '[YonedaLemma.ipynb](notebooks/YonedaLemma.ipynb)');
fixPrereq('KanExtensions', '[Adjunctions.ipynb](notebooks/Adjunctions.ipynb), [MonadTransformers.ipynb](notebooks/MonadTransformers.ipynb)');

// ---- Op 6: сводная таблица ----
const sumRows = {};
for (const row of get(byId('3fcd7166')).split('\n'))
  for (const name of order)
    if (row.includes('notebooks/' + name + '.ipynb')) sumRows[name] = row;
const missing = order.filter(n => !sumRows[n]);
if (missing.length) throw new Error('нет строк сводной: ' + missing.join(','));
const renum = { Extensions: '0.1', BaseHaskell: '0.2', TypeAlgebra: '0.3',
  FunctorHierarchy: 'I.1', FoldableTraversable: 'I.2',
  Monads: 'II.1', MonadTransformers: 'II.2', Comonads: 'II.3', ComonadTransformers: 'II.4',
  AlgebrasCoalgebras: 'III.1', Profunctors: 'III.2', Optics: 'III.3', Arrows: 'III.4',
  YonedaLemma: 'IV.1', Adjunctions: 'IV.2', KanExtensions: 'IV.3',
  MetaProgramming: 'V.1', Concurrency: 'V.2', DistributedHaskell: 'V.3', GPUHaskell: 'V.4',
  Toposes: 'VI.1', Uncertainty: 'VI.2', SubjectiveModeling: 'VI.3' };
const row = n => '| ' + renum[n] + ' |' + sumRows[n].split('|').slice(2).join('|');
const mod = t => '| **' + t + '** | | | | | |';
set(byId('3fcd7166'), `---

## \u{1F4CA} Сводная таблица

| # | Ноутбук | Уровень | Ячеек | SVG | Статус |
|---|---------|---------|-------|-----|--------|
${mod('Модуль 0 — Старт')}
${['Extensions','BaseHaskell','TypeAlgebra'].map(row).join('\n')}
${mod('Модуль I — Функторы')}
${['FunctorHierarchy','FoldableTraversable'].map(row).join('\n')}
${mod('Модуль II — Эффекты')}
${['Monads','MonadTransformers','Comonads','ComonadTransformers'].map(row).join('\n')}
${mod('Модуль III — Структуры и оптики')}
${['AlgebrasCoalgebras','Profunctors','Optics','Arrows'].map(row).join('\n')}
${mod('Модуль IV — Теория категорий')}
${['YonedaLemma','Adjunctions','KanExtensions'].map(row).join('\n')}
${mod('Модуль V — Практика')}
${['MetaProgramming','Concurrency','DistributedHaskell','GPUHaskell'].map(row).join('\n')}
${mod('Модуль VI — Топосы и неопределённость')}
${['Toposes','Uncertainty','SubjectiveModeling'].map(row).join('\n')}

**Итого:** 23 ноутбука готовы (0 ошибок), 83 SVG-диаграмм, 906 ячеек.

**Обозначения уровней:** \u{1F7E2} начальный • \u{1F7E1} средний • \u{1F7E0} средний/+ • \u{1F534} продвинутый • ⚫ эксперт
`);

// ---- Op 3: порядок карточек ----
const cards = order.map(cardOf);
const cardSet = new Set(cards);
const rest = nb.cells.filter(c => !cardSet.has(c));
const mapIdx = rest.findIndex(c => c.id === 'a5550535');
nb.cells = [...rest.slice(0, mapIdx + 1), ...cards, ...rest.slice(mapIdx + 1)];

// ---- Op 7: удаления ----
// Удаляем ASCII-граф (id 0133db59) и хвостовые пустышки (пустые ячейки или одинокий «##»).
nb.cells = nb.cells.filter((c, i) => {
  if (c.id === '0133db59') return false; // граф зависимостей
  const s = get(c).trim();
  return !((s === '' || s === '##') && i > 5);
});

fs.writeFileSync(P, JSON.stringify(nb, null, 1) + '\n');
console.log('README.ipynb: ячеек ' + nb.cells.length);
