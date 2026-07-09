// build_map.js — генерирует src/notebooks/course_map.svg (схема метро курса).
// Правки карты — только здесь. ASCII-only внутри SVG (правило курса).
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', '..', 'notebooks', 'course_map.svg');

const C = { base: '#8a93a3', yellow: '#d9a441', yellowName: '#b8862e',
  blue: '#5872c9', blueDark: '#3d4f8f', red: '#c4625f',
  ref: '#8b80bf', refName: '#6f63a8',
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
  { n: 'SubjectiveModeling', y: 968, mix: C.yellow },
  { n: 'SubjApplied', y: 1024, terminus: true }, // прикладное продолжение — на стволе
];
// справочники вне ствола — тупики (sidings) на пунктирном отводе от станции-якоря
const refs = [
  { n: 'Duality',  x: 500, y: 850, px: 350, py: 736 }, // <- KanExtensions
  { n: 'SetOp',    x: 540, y: 905, px: 350, py: 858 }, // <- Toposes
  { n: 'PytevIso', x: 470, y: 990, px: 350, py: 968 }, // <- SubjectiveModeling (сноска-доказательство)
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
// пунктирный отвод от станции-якоря к тупику-справочнику (со сдвигом от контуров)
function refStub(px, py, x, y) {
  const dx = x - px, dy = y - py, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
  const x1 = (px + 10 * ux).toFixed(1), y1 = (py + 10 * uy).toFixed(1);
  const x2 = (x - 9 * ux).toFixed(1), y2 = (y - 9 * uy).toFixed(1);
  return `<path class="lnref" d="M${x1} ${y1} L${x2} ${y2}"/>`;
}
// станция-тупик: полый квадрат (отличается от кружков ствола)
function refStation(r) {
  return `<rect x="${r.x - 6}" y="${r.y - 6}" width="12" height="12" rx="3" fill="${C.bg}" stroke="${C.ref}" stroke-width="3"/>` +
    `<text x="${r.x + 14}" y="${r.y + 5}" text-anchor="start" class="stref">${esc(r.n)}</text>`;
}

const body = `
<path class="ln" stroke="${C.base}" d="M${TX} 96 V500"/>
<path class="ln" stroke="${C.yellow}" d="M${TX} 500 C${TX} 560 ${YX} 540 ${YX} 600 V940 C${YX} 1006 254 1014 341 976"/>
<path class="ln" stroke="${C.blue}" d="M${TX} 500 V1024"/>
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
${refs.map(r => refStub(r.px, r.py, r.x, r.y)).join('\n')}
${refs.map(refStation).join('\n')}
<g transform="translate(656 96)">
<rect x="-18" y="-24" width="222" height="250" rx="12" fill="none" stroke="#e2e8f0"/>
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
<rect x="9" y="160" width="12" height="12" rx="3" fill="none" stroke="${C.ref}" stroke-width="2.5"/>
<text x="42" y="170" class="sub">reference (off-trunk siding)</text>
<text x="0" y="198" class="sub">further along the line = harder</text>
</g></g>`;

const svg = `<svg viewBox="0 0 880 1080" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Segoe UI', system-ui, sans-serif">
<title>Course map</title>
<desc>Metro-style map: gray base line, yellow structures, blue category theory, red practice. Interchange stations mix topics.</desc>
<style>
.st { font-size: 14px; font-weight: 450; fill: ${C.text}; }
.stb { font-size: 14px; font-weight: 650; fill: ${C.text}; }
.line-name { font-size: 11.5px; font-weight: 700; letter-spacing: .12em; }
.sub { font-size: 11px; fill: ${C.sub}; }
.ln { fill: none; stroke-linecap: round; stroke-width: 7; }
.stn { fill: ${C.bg}; stroke-width: 3.5; }
.stref { font-size: 13px; font-weight: 600; fill: ${C.text}; }
.lnref { fill: none; stroke: ${C.ref}; stroke-width: 2.5; stroke-dasharray: 2 6; stroke-linecap: round; }
</style>
${body}
</svg>
`;

if (/[^\x00-\x7F]/.test(svg)) { console.error('NOT ASCII-ONLY'); process.exit(1); }
fs.writeFileSync(OUT, svg);
console.log('course_map.svg written, bytes: ' + svg.length);
