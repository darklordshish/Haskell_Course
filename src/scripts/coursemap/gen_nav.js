// gen_nav.js [--check] — генерирует NAV-ячейку в конце каждого ноутбука курса
// из единого порядка course_order.js. Идемпотентен. NAV руками не править.
const fs = require('fs'), path = require('path');
const order = require('./course_order');
const NB = path.join(__dirname, '..', '..', 'notebooks');
const src = c => Array.isArray(c.source) ? c.source.join('') : c.source;
const isNav = c => c.cell_type === 'markdown' && /\*\*(← Предыдущий|Следующий)/.test(src(c));

function navText(i) {
  const prev = i > 0 ? order[i - 1] : null;
  const next = i < order.length - 1 ? order[i + 1] : null;
  const link = o => `[${o.title}](${o.file}.ipynb)`;
  const parts = [];
  if (prev) parts.push(`**← Предыдущий:** ${link(prev)}`);
  if (next) parts.push(`**Следующий →** ${link(next)}`);
  return `---\n\n${parts.join('  |  ')}\n`;
}

const checkOnly = process.argv.includes('--check');
let changed = 0;
order.forEach((o, i) => {
  const p = path.join(NB, o.file + '.ipynb');
  if (!fs.existsSync(p)) throw new Error('нет ноутбука: ' + o.file);
  const nb = JSON.parse(fs.readFileSync(p, 'utf8'));
  // последняя NAV-ячейка (исторически — всегда последняя ячейка)
  let idx = -1;
  nb.cells.forEach((c, k) => { if (isNav(c)) idx = k; });
  const want = navText(i);
  if (idx < 0) { // NAV нет — добавляем в конец
    nb.cells.push({ cell_type: 'markdown', metadata: {}, source: want.split(/(?<=\n)/) });
    changed++;
    if (!checkOnly) fs.writeFileSync(p, JSON.stringify(nb, null, 1) + '\n');
    return;
  }
  if (src(nb.cells[idx]) !== want) {
    nb.cells[idx].source = want.split(/(?<=\n)/);
    changed++;
    if (!checkOnly) fs.writeFileSync(p, JSON.stringify(nb, null, 1) + '\n');
  }
});
console.log((checkOnly ? 'would change: ' : 'updated: ') + changed);
