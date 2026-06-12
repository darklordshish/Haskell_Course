// Разовое обновление src/README.ipynb: добавление Extensions.ipynb (нулевой ноутбук).
const fs = require('fs'), path = require('path');
const P = path.join(__dirname, '..', '..', 'README.ipynb');
const nb = JSON.parse(fs.readFileSync(P, 'utf8'));
const get = c => Array.isArray(c.source) ? c.source.join('') : c.source;
const set = (c, s) => { c.source = s.split(/(?<=\n)/); };

const edit = (idx, from, to) => {
  const s = get(nb.cells[idx]);
  if (!s.includes(from)) throw new Error('cell ' + idx + ': не найдено: ' + from.slice(0, 60));
  set(nb.cells[idx], s.replace(from, to));
};

// 1. Содержание: строка 0 перед строкой 1
edit(2, '| 1 | [\u{1F393} Базовый Haskell]',
  '| 0 | [⚙️ Расширения GHC: бриф](notebooks/Extensions.ipynb) | \u{1F7E2} начальный |\n| 1 | [\u{1F393} Базовый Haskell]');

// 2. Карта тем: Часть 0
edit(3, 'Часть I. Основы Haskell',
  'Часть 0. Подготовка\n  Extensions (0) — бриф по расширениям GHC\n\nЧасть I. Основы Haskell');

// 3. Карточка раздела — после ячейки 3 (карта тем), перед карточкой BaseHaskell
const card = `---

## 0️⃣ ⚙️ Расширения GHC: бриф

**Файл:** [\`Extensions.ipynb\`](notebooks/Extensions.ipynb)  |  **Уровень:** \u{1F7E2} начальный  |  **Ячеек:** 18  |  **Диаграмм:** —  |  **Статус:** ✅ готов

**Предварительно:** нет — это нулевой ноутбук, с него рекомендуется начинать.

О чём, зачем и в чём соль каждого из 26 расширений GHC, используемых в курсе. Каждый ноутбук содержит автогенерируемую шапку «\u{1F4E6} Зависимости» со ссылками сюда.

| Тема | Суть |
|------|------|
| Синтаксис и литералы | OverloadedStrings, LambdaCase, TupleSections |
| forall | ScopedTypeVariables, RankNTypes, ExistentialQuantification |
| Классы типов | FlexibleInstances/Contexts, MultiParamTypeClasses, InstanceSigs |
| Deriving | DeriveFunctor/Foldable/Traversable/Generic, GND |
| Уровень типов | TypeOperators, TypeFamilies, GADTs, DataKinds |
| За пределами курса | TypeApplications, BangPatterns, LinearTypes и др. |
`;
if (!nb.cells.some(c => c.id === 'readme_ext_card')) {
  nb.cells.splice(4, 0, { cell_type: 'markdown', id: 'readme_ext_card', metadata: {}, source: card.split(/(?<=\n)/) });
}

// Индексы дальше сдвинулись на +1: сводная таблица 27, граф 28
// 4. Сводная таблица: строка 0 + итоги
edit(27, '| 1 | [\u{1F393} Базовый Haskell]',
  '| 0 | [⚙️ Расширения GHC: бриф](notebooks/Extensions.ipynb) | \u{1F7E2} начальный | 18 | — | ✅ |\n| 1 | [\u{1F393} Базовый Haskell]');
edit(27, '**Итого:** 22 ноутбука готовы (0 ошибок), 83 SVG-диаграмм, 888 ячеек.',
  '**Итого:** 23 ноутбука готовы (0 ошибок), 83 SVG-диаграмм, 906 ячеек.');

// 5. Граф зависимостей
edit(28, 'BaseHaskell (1)\n|',
  'Extensions (0)\n|\nv\nBaseHaskell (1)\n|');

fs.writeFileSync(P, JSON.stringify(nb, null, 1) + '\n');
console.log('README.ipynb обновлён, ячеек: ' + nb.cells.length);
