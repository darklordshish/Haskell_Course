// fill_section.js <slug> — вписывает содержимое раздела в Duality.ipynb.
// Источники: src/scripts/duality/<slug>_md.txt (markdown + inline SVG) и <slug>_hs.txt (Haskell).
// Инлайновые <svg> ВЫНОСЯТСЯ в файлы src/diagrams/duality/<slug>_<n>.svg, а в ячейку
// markdown подставляется ссылка ![..](../diagrams/duality/..) — JupyterLab вырезает инлайновый
// <svg> из markdown, а внешние картинки показывает (конвенция курса). Идемпотентно.
const fs = require('fs'), path = require('path');
const slug = process.argv[2];
if (!slug) { console.error('usage: node fill_section.js <slug>'); process.exit(1); }
const NB = path.join(__dirname, '..', '..', 'notebooks', 'Duality.ipynb');
const DIAGRAMS = path.join(__dirname, '..', '..', 'diagrams', 'duality');
const mdPath = path.join(__dirname, slug + '_md.txt');
const hsPath = path.join(__dirname, slug + '_hs.txt');
const nb = JSON.parse(fs.readFileSync(NB, 'utf8'));
const toLines = s => s.replace(/\n$/, '').split(/(?<=\n)/);
fs.mkdirSync(DIAGRAMS, { recursive: true });

// markdown: вынести каждый <svg> в файл, заменить ссылкой
let mdText = fs.readFileSync(mdPath, 'utf8');
let n = 0;
mdText = mdText.replace(/<svg[\s\S]*?<\/svg>/g, (svg) => {
  n++;
  const bad = (svg.replace(/&#\d+;/g, '').match(/[^\x00-\x7F]/g) || []);
  if (bad.length) { console.error('НЕ-ASCII в SVG #' + n + ' раздела ' + slug + ': ' + [...new Set(bad)].join(' ')); process.exit(1); }
  const name = `${slug}_${n}.svg`;
  fs.writeFileSync(path.join(DIAGRAMS, name), svg + '\n');
  return `![${slug} fig.${n}](../diagrams/duality/${name})`;
});

const setLines = (id, text, isCode) => {
  const cell = nb.cells.find(c => c.id === id);
  if (!cell) throw new Error('нет ячейки ' + id);
  cell.source = toLines(text);
  if (isCode) { cell.outputs = []; cell.execution_count = null; }
};
setLines('dual_' + slug + '_md', mdText, false);
setLines('dual_' + slug + '_hs', fs.readFileSync(hsPath, 'utf8'), true);

fs.writeFileSync(NB, JSON.stringify(nb, null, 1) + '\n');
console.log(`раздел ${slug} вписан (md+hs), ${n} SVG вынесено в diagrams/duality/`);
