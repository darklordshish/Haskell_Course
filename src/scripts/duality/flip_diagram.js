// Зеркалит парные диаграммы в <slug>_md.txt: меняет местами левый и правый
// столбцы (прямая конструкция -> слева). Координаты не трогает — оборачивает
// каждый блок в <g transform="translate(±D,0)">, где D = расстояние между
// центрами столбцов (по x заголовков). Общие элементы (фон, разделители,
// центрированные подписи) остаются на месте.
const fs = require('fs');

const slug = process.argv[2];
if (!slug) { console.error('usage: node flip_diagram.js <slug>'); process.exit(1); }
const FILE = `src/scripts/duality/${slug}_md.txt`;
let text = fs.readFileSync(FILE, 'utf8');

const UNIT_RE = /<g\b[^>]*>[\s\S]*?<\/g>|<text\b[^>]*>[\s\S]*?<\/text>|<rect\b[^>]*\/>|<line\b[^>]*\/>|<polygon\b[^>]*\/>|<polyline\b[^>]*\/>|<circle\b[^>]*\/>|<path\b[^>]*\/>/g;

function xsOf(unit) {
  const xs = [];
  const push = re => { let m; while ((m = re.exec(unit))) xs.push(parseFloat(m[1])); };
  push(/\bx=["']([-\d.]+)/g);
  push(/\bx1=["']([-\d.]+)/g);
  push(/\bx2=["']([-\d.]+)/g);
  push(/\bcx=["']([-\d.]+)/g);
  // точки polygon/polyline: первая координата каждой пары
  let pm; const pr = /points=["']([^"']+)["']/g;
  while ((pm = pr.exec(unit))) for (const pair of pm[1].trim().split(/\s+/)) xs.push(parseFloat(pair.split(',')[0]));
  return xs;
}

let figIdx = 0;
text = text.replace(/<svg\b[^>]*>[\s\S]*?<\/svg>/g, (svg) => {
  figIdx++;
  const wm = svg.match(/viewBox=["'][\d.]+ [\d.]+ ([\d.]+)/) || svg.match(/width=["']([\d.]+)/);
  const W = parseFloat(wm[1]);
  const open = svg.match(/<svg\b[^>]*>/)[0];
  const close = '</svg>';
  let inner = svg.slice(open.length, svg.length - close.length);

  const units = inner.match(UNIT_RE) || [];
  // заголовки столбцов = два bold-текста с наименьшим y
  const titles = units
    .filter(u => /<text/.test(u) && /font-weight=["']700["']/.test(u))
    .map(u => ({ x: parseFloat((u.match(/\bx=["']([-\d.]+)/) || [])[1]), y: parseFloat((u.match(/\by=["']([-\d.]+)/) || [])[1]) }))
    .filter(t => !isNaN(t.x) && !isNaN(t.y))
    .sort((a, b) => a.y - b.y)
    .slice(0, 2)
    .sort((a, b) => a.x - b.x);
  if (titles.length < 2) { console.error(`фиг.${figIdx}: не нашёл два заголовка`); process.exit(1); }
  const leftC = titles[0].x, rightC = titles[1].x;
  const mid = (leftC + rightC) / 2;
  const D = rightC - leftC;

  const pre = [], left = [], right = [], post = [];
  let seenSide = false;
  for (const u of units) {
    const xs = xsOf(u);
    const minX = Math.min(...xs), maxX = Math.max(...xs), c = xs.reduce((a, b) => a + b, 0) / xs.length;
    const isBg = /<rect/.test(u) && /\bx=["']0["']/.test(u) && (maxX - minX) === 0 || (/<rect/.test(u) && parseFloat((u.match(/width=["']([\d.]+)/) || [0, 0])[1]) >= 0.8 * W);
    const straddle = minX < mid - 30 && maxX > mid + 30;
    const centered = Math.abs(c - mid) < 30;
    if (isBg || straddle || centered) { (seenSide ? post : pre).push(u); continue; }
    seenSide = true;
    if (c < mid) left.push(u); else right.push(u);
  }
  const g = (d, arr) => arr.length ? `<g transform="translate(${d} 0)">${arr.join('')}</g>` : '';
  const rebuilt = pre.join('') + g(D, left) + g(-D, right) + post.join('');
  console.log(`фиг.${figIdx}: W=${W} D=${D} | left=${left.length} right=${right.length} shared=${pre.length + post.length}`);
  return open + rebuilt + close;
});

fs.writeFileSync(FILE, text);
console.log(`${slug}: ${figIdx} фигур отзеркалено`);
