const fs = require('fs'), path = require('path');
const md = (id, src) => ({ cell_type: 'markdown', id, metadata: {}, source: src.replace(/\n$/, '').split(/(?<=\n)/) });
const code = (id, src) => ({ cell_type: 'code', id, metadata: {}, outputs: [], execution_count: null, source: src.replace(/\n$/, '').split(/(?<=\n)/) });
const SECTIONS = [
  ['intro',     'Set^op: переверни стрелки', false],
  ['limits',    '(Ко)пределы и mono/epi в Set^op', false],
  ['notccc',    'Не декартово замкнута, не топос', false],
  ['caba',      'A. Что это: Set^op &#8771; CABA', true],
  ['partitions','B1. Субобъекты = разбиения (логики нет)', true],
  ['coheyting', 'B2-3. Ко-Гейтинг, граница, двойное отрицание', true],
  ['dualities', 'C1. Пространства против алгебр', false],
  ['cps',       'C2-3. CPS-мост: Op, Cont, применения', true],
];
const cells = [];
cells.push(code('setup', ':set -XScopedTypeVariables -XRankNTypes\nimport Data.List (sort, nub, subsequences)\nputStrLn "\\x2705 SETUP OK"'));
cells.push(md('header', '# 🪞 Категория `Set^op`\n\nОдин странный объект — три взгляда. Всё в сравнении с `Set`.'));
let toc = '## 📌 Содержание\n\n| # | Раздел | О чём |\n|---|--------|-------|\n';
const tocRows = [
  ['Ствол', 'переверни стрелки; (ко)пределы; не CCC/не топос'],
  ['A', 'Set^op &#8771; CABA: powerset, предикат-трансформеры'],
  ['B', 'логика: разбиения, ко-Гейтинг, граница, &#172;&#172;'],
  ['C', 'пространства vs алгебры; CPS-мост (Op, Cont)'],
];
for (const [a, b] of tocRows) toc += `| ${a} | ${b} | |\n`;
cells.push(md('toc', toc));
for (const [slug, title, hasCode] of SECTIONS) {
  cells.push(md('setop_' + slug + '_md', `---\n\n<a id="setop-${slug}"></a>\n## ${title}\n\n_(заполняется)_`));
  if (hasCode) cells.push(code('setop_' + slug + '_hs', `-- Haskell (${slug}): заполняется`));
}
cells.push(md('nav', '---\n\n**Этюд вне ствола.** См. также [Duality.ipynb](Duality.ipynb), [Toposes.ipynb](Toposes.ipynb), [KanExtensions.ipynb](KanExtensions.ipynb).'));
const nb = { cells, metadata: { kernelspec: { display_name: 'Haskell', language: 'haskell', name: 'haskell' }, language_info: { name: 'haskell', version: '8.10' } }, nbformat: 4, nbformat_minor: 5 };
fs.writeFileSync(path.join(__dirname, '..', '..', 'notebooks', 'SetOp.ipynb'), JSON.stringify(nb, null, 1) + '\n');
console.log('каркас SetOp.ipynb собран:', cells.length, 'ячеек');
