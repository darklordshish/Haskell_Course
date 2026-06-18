// fill_section.js <slug> — вписывает содержимое раздела в Duality.ipynb.
// Источники: src/scripts/duality/<slug>_md.txt (markdown+SVG) и <slug>_hs.txt (Haskell).
// Кладёт их в ячейки dual_<slug>_md и dual_<slug>_hs. Идемпотентно.
const fs = require('fs'), path = require('path');
const slug = process.argv[2];
if (!slug) { console.error('usage: node fill_section.js <slug>'); process.exit(1); }
const NB = path.join(__dirname, '..', '..', 'notebooks', 'Duality.ipynb');
const mdPath = path.join(__dirname, slug + '_md.txt');
const hsPath = path.join(__dirname, slug + '_hs.txt');
const nb = JSON.parse(fs.readFileSync(NB, 'utf8'));
const toLines = s => s.replace(/\n$/, '').split(/(?<=\n)/);
const set = (id, file) => {
  const cell = nb.cells.find(c => c.id === id);
  if (!cell) throw new Error('нет ячейки ' + id);
  cell.source = toLines(fs.readFileSync(file, 'utf8'));
  if (cell.cell_type === 'code') { cell.outputs = []; cell.execution_count = null; }
};
set('dual_' + slug + '_md', mdPath);
set('dual_' + slug + '_hs', hsPath);
// guard: ASCII-only внутри <svg> блоков (правило курса)
const md = nb.cells.find(c => c.id === 'dual_' + slug + '_md');
const svgs = (md.source.join('').match(/<svg[\s\S]*?<\/svg>/g) || []).join('');
const bad = (svgs.replace(/&#\d+;/g, '').match(/[^\x00-\x7F]/g) || []);
if (bad.length) { console.error('НЕ-ASCII в SVG раздела ' + slug + ': ' + [...new Set(bad)].join(' ')); process.exit(1); }
fs.writeFileSync(NB, JSON.stringify(nb, null, 1) + '\n');
console.log('раздел ' + slug + ' вписан (md+hs), SVG ASCII-only ок');
