// build_duality_scaffold.js — каркас src/notebooks/Duality.ipynb (словарь двойственности).
// Стаб-ячейки разделов с фиксированными id; наполняются отдельными шагами по шаблону.
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', '..', 'notebooks', 'Duality.ipynb');

// разделы по порядку спеки: примитивы -> Кан-движок -> через Кан
const SECTIONS = [
  ['monoepi',      'Мономорфизм &#8611; / Эпиморфизм &#8608; (примитив)'],
  ['variance',     'Ковариантный / Контравариантный функтор (примитив)'],
  ['algcoalg',     'Алгебра / Коалгебра (примитив)'],
  ['kan',          'Расширения Кана: Lan / Ran (движок)'],
  ['limcolim',     'Пределы / Копределы через Кан'],
  ['termini',      'Терминальный / Начальный объект (J = &#8709;)'],
  ['prodcoprod',   'Произведение / Копроизведение (J = пара)'],
  ['equ',          'Уравнитель / Коуравнитель (J = параллельная пара)'],
  ['pbpo',         'Pullback / Pushout (J = коспан / спан)'],
  ['adj',          'Сопряжения: левое / правое (через Кан)'],
  ['monadcomonad', 'Монада / Комонада (через Кан)'],
];

const md = (id, text) => ({ cell_type: 'markdown', id, metadata: {}, source: text.split(/(?<=\n)/) });
const code = (id, text) => ({ cell_type: 'code', id, metadata: {}, execution_count: null, outputs: [], source: text.split(/(?<=\n)/) });

const cells = [];

cells.push(code('dual_setup',
`:set -XRankNTypes
:set -XScopedTypeVariables
:set -XTypeOperators
:set -XFlexibleInstances
:set -XFlexibleContexts
:set -XDeriveFunctor
:set -XGADTs
:set -XExistentialQuantification
putStrLn "\\x2705 SETUP OK"`));

cells.push(md('dual_title',
`# 🔄 Словарь двойственности

Парад двойственных категорных конструкций. Одна ось — обращение стрелок \`C &#8644; C^op\`.
Подача: разминка на **примитивах** &#8594; рано вводится **движок — расширения Кана** &#8594;
и дальше пределы, сопряжения, монады/комонады выводятся **через Кан**.
`));

cells.push(md('dual_motiv',
`## 0. Мотивация: что такое двойственность

**Двойственность = обращение всех стрелок.** Каждой конструкции в категории \`C\` отвечает
её зеркальное отражение в противоположной категории \`C^op\` (те же объекты, стрелки развёрнуты).
Приставка «co-» буквально значит «то же самое в \`C^op\`»: ко-предел, ко-произведение, ко-монада.

Дальше мы увидим, что бо&#769;льшая часть конструкций — **частные случаи расширений Кана**
(\`Lan\`/\`Ran\`), которые сами зеркальны друг другу. Но сперва — чистые примитивы, которые
Каном не порождаются: моно/эпи, вариантность функтора, алгебры/коалгебры.
`));

// сводная таблица
const tocRows = [
  ['Мономорфизм &#8611;', 'Эпиморфизм &#8608;', 'лево- vs право-сократимость', 'нет', 'Toposes', 'monoepi'],
  ['Ковариантный', 'Контравариантный', 'C&#8594;D vs C^op&#8594;D', 'нет', 'FunctorHierarchy', 'variance'],
  ['Алгебра F a&#8594;a', 'Коалгебра a&#8594;F a', 'неподвижные точки эндофунктора', 'нет', 'AlgebrasCoalgebras', 'algcoalg'],
  ['Lan (левое)', 'Ran (правое)', 'движок: зеркало C^op', 'сам Кан', 'KanExtensions', 'kan'],
  ['Предел', 'Копредел', 'lim=Ran, colim=Lan вдоль J&#8594;1', 'да', 'KanExtensions', 'limcolim'],
  ['Терминальный', 'Начальный', 'J = &#8709;', 'да', 'TypeAlgebra', 'termini'],
  ['Произведение &#215;', 'Копроизведение +', 'J = пара точек', 'да', 'TypeAlgebra', 'prodcoprod'],
  ['Уравнитель', 'Коуравнитель', 'J = параллельная пара', 'да', 'AlgebrasCoalgebras', 'equ'],
  ['Pullback', 'Pushout', 'J = коспан / спан', 'да', 'Toposes', 'pbpo'],
  ['Левый сопряжённый', 'Правый сопряжённый', 'F=Lan_G Id, G=Ran_F Id', 'да', 'Adjunctions', 'adj'],
  ['Монада', 'Комонада', 'Codensity=Ran f f, Density=Lan f f', 'да', 'Monads', 'monadcomonad'],
];
let toc = `## 📌 Сводная таблица\n\n| Конструкция | Двойственная | Идея | Через Кан? | Где в курсе | &#8594; |\n|---|---|---|---|---|---|\n`;
for (const [a, b, idea, kan, course, slug] of tocRows)
  toc += `| ${a} | ${b} | ${idea} | ${kan} | ${course} | [&#8594;](#dual-${slug}) |\n`;
toc += `\n_Левая колонка — прямая конструкция, правая — двойственная (приставка «co-» = обращение стрелок в \`C^op\`). Пары Lan/Ran и левый/правый сопряжённый **симметричны**: ни одна не «co-» другой._`;
cells.push(md('dual_toc', toc));

// стаб-ячейки разделов
for (const [slug, title] of SECTIONS) {
  cells.push(md(`dual_${slug}_md`,
`---

<a id="dual-${slug}"></a>
## ${title}

*Раздел в наполнении — скелет по шаблону словаря (идея &#8594; определение + универсальное
свойство &#8594; парная диаграмма &#8594; Haskell обоих &#8594; «в чём двойственность» &#8594; где в курсе).*
`));
  cells.push(code(`dual_${slug}_hs`, `-- Haskell (${slug}): заполняется`));
}

cells.push(md('dual_nav',
`---

**Справочник-приложение**, вне линейного ствола 0&#8211;VI. &#8617; [Путеводитель](README.ipynb)
`));

const nb = {
  cells,
  metadata: {
    kernelspec: { display_name: 'Haskell', language: 'haskell', name: 'haskell' },
    language_info: { name: 'haskell' },
  },
  nbformat: 4,
  nbformat_minor: 5,
};

fs.writeFileSync(OUT, JSON.stringify(nb, null, 1) + '\n');
console.log('Duality.ipynb написан, ячеек: ' + cells.length);
