// gen_headers.js [--check] [--index] — шапки "Зависимости" в ноутбуках.
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', '..', 'notebooks');
const dict = JSON.parse(fs.readFileSync(path.join(__dirname, 'dictionary.json'), 'utf8'));
const src = c => Array.isArray(c.source) ? c.source.join('') : c.source;

function pkgOf(mod) {
  if (dict.libModules.includes(mod)) return null; // lib, не пакет
  let best = dict.packages._default, bestLen = 0;
  for (const [pre, pkg] of Object.entries(dict.packages))
    if (pre !== '_default' && (mod === pre || mod.startsWith(pre + '.')) && pre.length > bestLen)
      { best = pkg; bestLen = pre.length; }
  return best;
}

function analyze(nb) {
  const exts = new Set(), pkgs = new Set(), libs = new Set();
  for (const c of nb.cells) {
    if (c.cell_type !== 'code') continue;
    const s = src(c);
    for (const m of s.match(/-X(\w+)/g) || []) exts.add(m.slice(2));
    for (const m of s.match(/^import\s+(?:qualified\s+)?([A-Z][\w.]*)/gm) || []) {
      const mod = m.replace(/^import\s+(qualified\s+)?/, '');
      const p = pkgOf(mod);
      if (p === null) libs.add(mod); else pkgs.add(p);
    }
  }
  return { exts: [...exts].sort(), pkgs: [...pkgs].sort(), libs: [...libs].sort() };
}

function header({ exts, pkgs, libs }) {
  const missing = exts.filter(e => !dict.extensions[e]);
  if (missing.length) throw new Error('Нет в словаре: ' + missing.join(', '));
  const lines = ['> **\u{1F4E6} Зависимости**\n'];
  if (pkgs.length) lines.push('> **Пакеты:** ' + pkgs.map(p => '`' + p + '`').join(', ') + '\n');
  if (libs.length) lines.push('> **Библиотека курса:** ' + libs.map(m => '`' + m + '`').join(', ') + ' (`src/lib`)\n');
  if (exts.length) lines.push('> **Расширения:** ' + exts.map(e => {
    const d = dict.extensions[e];
    return '`' + e + '` — ' + d.blurb + ' ([→](Extensions.ipynb#' + d.anchor + '))';
  }).join(' · ') + '\n');
  return lines;
}

const checkOnly = process.argv.includes('--check');
const indexMode = process.argv.includes('--index');
const index = {};
let changed = 0;
for (const f of fs.readdirSync(ROOT).filter(f => f.endsWith('.ipynb'))) {
  const p = path.join(ROOT, f);
  const nb = JSON.parse(fs.readFileSync(p, 'utf8'));
  const a = analyze(nb);
  if (indexMode) { for (const e of a.exts) (index[e] = index[e] || []).push(f); continue; }
  if (!a.exts.length && !a.pkgs.length && !a.libs.length) continue; // DesignShowcase
  if (f === 'Extensions.ipynb') continue;
  const cell = { cell_type: 'markdown', id: 'deps_header', metadata: {}, source: header(a) };
  const i = nb.cells.findIndex(c => c.id === 'deps_header');
  const before = JSON.stringify(nb.cells[i >= 0 ? i : -1]);
  if (i >= 0) nb.cells[i] = cell;
  else {
    const t = nb.cells.findIndex(c => c.cell_type === 'markdown');
    nb.cells.splice(t < 0 ? 0 : t + 1, 0, cell);
  }
  if (JSON.stringify(cell) !== before) {
    changed++;
    if (!checkOnly) fs.writeFileSync(p, JSON.stringify(nb, null, 1) + '\n');
  }
}
if (indexMode) console.log(JSON.stringify(index, null, 2));
else {
  console.log((checkOnly ? 'would change: ' : 'updated: ') + changed);
  if (checkOnly && changed) process.exit(1);
}
