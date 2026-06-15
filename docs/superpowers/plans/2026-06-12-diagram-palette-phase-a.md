# План: Фаза A — унификация палитры диаграмм

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Спека: `docs/superpowers/specs/2026-06-12-diagram-palette-unification-design.md` (только Фаза A — палитра; Фаза B — стрелки — отдельным планом).

**Goal:** Привести все `src/diagrams/**/*.svg` к единой приглушённой светлой палитре «в тон карте курса».

**Architecture:** Детерминированный node-реколор `normalize_palette.js`: явная таблица для частых цветов + HSL-фолбэк (бакет по hue → семейство, снап по светлоте → узел/база/тинт), отчёт об остатке вне канона. 4 тёмно-коллажных файла — вручную. Нейтральная slate-шкала уже консистентна — её сохраняем, нормализуем в основном акценты (saturated→muted). `course_map.svg` не трогаем.

**Tech Stack:** Node.js; визуальная проверка — в Jupyter (контейнер поднят, bind-mount `src`).

**Канон (из спеки):** нейтрали `#0f172a/#475569/#8a93a3/#cbd5e1/#f7f8fa/#ffffff`; семейства узел/база/тинт: индиго `#3a4a96/#5872c9/#eef1fb`, шалфей `#2f6f54/#3f9d77/#e9f4ee`, лаванда `#5f4a86/#8b6db5/#efeaf6`, охра `#8a6418/#d9a441/#f4e7cf`, терракота `#8f3f3c/#c4625f/#f5e3e2`.

---

### Task 0: Ветка

- [ ] `git checkout master; git pull; git checkout -b diagram-palette`

### Task 1: Скрипт нормализации

**Files:** Create `src/scripts/coursemap/normalize_palette.js`

- [ ] Записать скрипт (UTF-8 без BOM):

```js
// normalize_palette.js [--check] — реколор src/diagrams/**/*.svg к единой светлой палитре.
// course_map.svg исключён. ASCII-инвариант сохраняется. Идемпотентен.
const fs = require('fs'), path = require('path'), cp = require('child_process');
const ROOT = path.join(__dirname, '..', '..', '..');
const files = cp.execSync('git ls-files "src/diagrams/**/*.svg"', { cwd: ROOT, encoding: 'utf8' })
  .trim().split('\n').filter(Boolean);

// канон
const N = { text1: '#0f172a', text2: '#475569', arrow: '#8a93a3', border: '#cbd5e1', card: '#f7f8fa', bg: '#ffffff' };
const FAM = {
  indigo:     { node: '#3a4a96', base: '#5872c9', tint: '#eef1fb' },
  sage:       { node: '#2f6f54', base: '#3f9d77', tint: '#e9f4ee' },
  lavender:   { node: '#5f4a86', base: '#8b6db5', tint: '#efeaf6' },
  ochre:      { node: '#8a6418', base: '#d9a441', tint: '#f4e7cf' },
  terracotta: { node: '#8f3f3c', base: '#c4625f', tint: '#f5e3e2' },
};
const CANON = new Set([...Object.values(N), ...Object.values(FAM).flatMap(f => Object.values(f)), '#000000']);

// явная таблица частых цветов (из аудита) -> канон
const MAP = {
  // нейтрали
  '#f8fafc': N.bg, '#f1f5f9': N.card, '#f7f8fa': N.card, '#e2e8f0': N.border, '#cbd5e1': N.border,
  '#94a3b8': N.arrow, '#64748b': N.arrow, '#334155': N.text2, '#475569': N.text2, '#0f172a': N.text1,
  '#1e293b': N.text1, '#6b7280': N.arrow, '#9ca3af': N.arrow, '#e5e7eb': N.border, '#374151': N.text2,
  '#e0e0e0': N.border, '#b0b0b0': N.arrow, '#666666': N.arrow, '#f8f9fa': N.bg, '#c0c8d8': N.border,
  // индиго (синий saturated/navy -> muted)
  '#2563eb': FAM.indigo.base, '#3b82f6': FAM.indigo.base, '#4488dd': FAM.indigo.base, '#6699ee': FAM.indigo.base,
  '#60a5fa': FAM.indigo.base, '#93c5fd': FAM.indigo.base, '#58a6ff': FAM.indigo.base, '#4477bb': FAM.indigo.base,
  '#4477cc': FAM.indigo.base, '#556688': FAM.indigo.base, '#446688': FAM.indigo.base,
  '#1d4ed8': FAM.indigo.node, '#1e40af': FAM.indigo.node, '#1e3a8a': FAM.indigo.node, '#1e3a5f': FAM.indigo.node,
  '#2a50a0': FAM.indigo.node, '#1a4488': FAM.indigo.node, '#1a3a88': FAM.indigo.node, '#1a2a6a': FAM.indigo.node,
  '#2255cc': FAM.indigo.node, '#2255aa': FAM.indigo.node, '#334466': FAM.indigo.node, '#0c2340': FAM.indigo.node,
  '#1a2744': FAM.indigo.node, '#2c3e6e': FAM.indigo.node, '#2d4a6e': FAM.indigo.node, '#1a56b0': FAM.indigo.node,
  '#dbeafe': FAM.indigo.tint, '#bfdbfe': FAM.indigo.tint, '#eff6ff': FAM.indigo.tint, '#e0f2fe': FAM.indigo.tint,
  '#eef2ff': FAM.indigo.tint, '#eef4ff': FAM.indigo.tint, '#e0e8ff': FAM.indigo.tint, '#dbe8f8': FAM.indigo.tint,
  '#f0f4ff': FAM.indigo.tint, '#ccddee': FAM.indigo.tint, '#dde3ee': FAM.indigo.tint,
  // шалфей (зелёный)
  '#059669': FAM.sage.base, '#16a34a': FAM.sage.base, '#15803d': FAM.sage.base, '#34d399': FAM.sage.base,
  '#22c55e': FAM.sage.base, '#44aa66': FAM.sage.base, '#3fb950': FAM.sage.base, '#39d353': FAM.sage.base,
  '#44cc44': FAM.sage.base, '#66cc88': FAM.sage.base, '#228844': FAM.sage.base, '#226644': FAM.sage.base,
  '#065f46': FAM.sage.node, '#14532d': FAM.sage.node, '#166534': FAM.sage.node, '#144422': FAM.sage.node,
  '#226633': FAM.sage.node, '#116633': FAM.sage.node, '#1a7a2a': FAM.sage.node, '#1e6e3e': FAM.sage.node,
  '#145533': FAM.sage.node, '#0a4422': FAM.sage.node, '#115522': FAM.sage.node, '#0a3a1a': FAM.sage.node, '#1a3322': FAM.sage.node,
  '#dcfce7': FAM.sage.tint, '#d1fae5': FAM.sage.tint, '#bbf7d0': FAM.sage.tint, '#f0fdf4': FAM.sage.tint,
  '#a7e3bf': FAM.sage.tint, '#aaddcc': FAM.sage.tint, '#d4edda': FAM.sage.tint, '#f0faf0': FAM.sage.tint, '#f0fff4': FAM.sage.tint,
  // лаванда (фиолетовый)
  '#7c3aed': FAM.lavender.base, '#9333ea': FAM.lavender.base, '#8b5cf6': FAM.lavender.base, '#a855f7': FAM.lavender.base,
  '#a78bfa': FAM.lavender.base, '#c084fc': FAM.lavender.base, '#9966cc': FAM.lavender.base, '#aa44cc': FAM.lavender.base,
  '#9944dd': FAM.lavender.base, '#7733aa': FAM.lavender.base, '#7733bb': FAM.lavender.base, '#884499': FAM.lavender.base,
  '#5b21b6': FAM.lavender.node, '#6d28d9': FAM.lavender.node, '#4422aa': FAM.lavender.node, '#5533aa': FAM.lavender.node,
  '#2d1b4e': FAM.lavender.node, '#6622aa': FAM.lavender.node, '#6b21a8': FAM.lavender.node, '#1e1040': FAM.lavender.node,
  '#3d2b7a': FAM.lavender.node, '#5b3fa6': FAM.lavender.node, '#441166': FAM.lavender.node, '#662288': FAM.lavender.node,
  '#553388': FAM.lavender.node, '#664499': FAM.lavender.node, '#664488': FAM.lavender.node, '#4c4c99': FAM.lavender.node, '#2a1a2a': FAM.lavender.node,
  '#ede9fe': FAM.lavender.tint, '#e9d5ff': FAM.lavender.tint, '#ddd6fe': FAM.lavender.tint, '#f5f3ff': FAM.lavender.tint,
  '#f5f0ff': FAM.lavender.tint, '#fdf4ff': FAM.lavender.tint, '#e8e0f8': FAM.lavender.tint, '#cc99ff': FAM.lavender.tint,
  '#fdf0ff': FAM.lavender.tint, '#f0f4ff': FAM.lavender.tint, '#e9d5ff': FAM.lavender.tint,
  // охра (оранжевый + жёлтый/золото)
  '#ea580c': FAM.ochre.base, '#d97706': FAM.ochre.base, '#f59e0b': FAM.ochre.base, '#cc7700': FAM.ochre.base,
  '#cc6600': FAM.ochre.base, '#eab308': FAM.ochre.base, '#ca8a04': FAM.ochre.base, '#ccaa00': FAM.ochre.base,
  '#aa8800': FAM.ochre.base, '#886600': FAM.ochre.base, '#fb923c': FAM.ochre.base, '#f0883e': FAM.ochre.base,
  '#e3722c': FAM.ochre.base, '#aa6600': FAM.ochre.base, '#a16207': FAM.ochre.base, '#c2410c': FAM.ochre.base,
  '#9a3412': FAM.ochre.node, '#b45309': FAM.ochre.node, '#92400e': FAM.ochre.node, '#854d0e': FAM.ochre.node,
  '#664400': FAM.ochre.node, '#78350f': FAM.ochre.node, '#713f12': FAM.ochre.node, '#7a4a06': FAM.ochre.node,
  '#7a3a00': FAM.ochre.node, '#774400': FAM.ochre.node, '#995500': FAM.ochre.node, '#856404': FAM.ochre.node,
  '#664d03': FAM.ochre.node, '#884422': FAM.ochre.node, '#885533': FAM.ochre.node, '#774422': FAM.ochre.node, '#1c1306': FAM.ochre.node, '#c25a10': FAM.ochre.node,
  '#ffedd5': FAM.ochre.tint, '#fff7ed': FAM.ochre.tint, '#fef3c7': FAM.ochre.tint, '#fef9c3': FAM.ochre.tint,
  '#fde68a': FAM.ochre.tint, '#fde9d3': FAM.ochre.tint, '#fff3cd': FAM.ochre.tint, '#fffbe6': FAM.ochre.tint,
  '#fefce8': FAM.ochre.tint, '#fff8ee': FAM.ochre.tint, '#fff4ec': FAM.ochre.tint, '#fde9d3': FAM.ochre.tint,
  // терракота (красный)
  '#dc2626': FAM.terracotta.base, '#ef4444': FAM.terracotta.base, '#cc4444': FAM.terracotta.base, '#f43f5e': FAM.terracotta.base,
  '#be185d': FAM.terracotta.base, '#994444': FAM.terracotta.base, '#991b1b': FAM.terracotta.node, '#b91c1c': FAM.terracotta.node,
  '#7a1414': FAM.terracotta.node, '#882222': FAM.terracotta.node, '#991111': FAM.terracotta.node, '#9f1239': FAM.terracotta.node,
  '#fee2e2': FAM.terracotta.tint, '#fef2f2': FAM.terracotta.tint, '#fdeaea': FAM.terracotta.tint, '#fbcaca': FAM.terracotta.tint,
  '#fff0f0': FAM.terracotta.tint, '#e7b3b3': FAM.terracotta.tint, '#f7d6d6': FAM.terracotta.tint,
  // teal/cyan -> индиго (ближе к синему)
  '#0e7490': FAM.indigo.base, '#0891b2': FAM.indigo.base, '#155e75': FAM.indigo.node, '#cffafe': FAM.indigo.tint,
  '#555555': N.arrow, '#444444': N.text2, '#333333': N.text1, '#666666': N.arrow,
  '#888888': N.arrow, '#999999': N.arrow, '#aaaaaa': N.border, '#aa1111': FAM.terracotta.node,
};

function hexToHsl(hex) {
  let h = hex.replace('#', '');
  if (h.length === 3) h = h.split('').map(c => c + c).join('');
  const r = parseInt(h.slice(0,2),16)/255, g = parseInt(h.slice(2,4),16)/255, b = parseInt(h.slice(4,6),16)/255;
  const mx = Math.max(r,g,b), mn = Math.min(r,g,b), d = mx - mn;
  let H = 0; const L = (mx+mn)/2; const S = d === 0 ? 0 : d/(1-Math.abs(2*L-1));
  if (d !== 0) {
    if (mx === r) H = ((g-b)/d) % 6; else if (mx === g) H = (b-r)/d + 2; else H = (r-g)/d + 4;
    H *= 60; if (H < 0) H += 360;
  }
  return { h: H, s: S, l: L };
}
function famOfHue(h) {
  if (h >= 345 || h < 18) return 'terracotta';
  if (h < 70) return 'ochre';
  if (h < 175) return 'sage';
  if (h < 248) return 'indigo';
  return 'lavender';
}
function fallback(hex) {
  const { s, l } = hexToHsl(hex);
  if (s < 0.12) { // нейтраль по светлоте
    const scale = [[0.16, N.text1], [0.40, N.text2], [0.60, N.arrow], [0.82, N.border], [0.93, N.card], [1.01, N.bg]];
    return scale.find(([t]) => l <= t)[1];
  }
  const f = FAM[famOfHue(hexToHsl(hex).h)];
  if (l > 0.80) return f.tint;
  if (l < 0.38) return f.node;
  return f.base;
}

const leftover = {};
const checkOnly = process.argv.includes('--check');
let changed = 0;
for (const rel of files) {
  if (rel.endsWith('course_map.svg')) continue;
  const p = path.join(ROOT, rel);
  const orig = fs.readFileSync(p, 'utf8');
  // (?<!&) — не цеплять numeric-entity (&#937; и т.п.); 3-значные разворачиваем в 6
  const out = orig.replace(/(?<!&)#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b/g, (m) => {
    let lc = m.toLowerCase();
    if (lc.length === 4) lc = '#' + lc[1] + lc[1] + lc[2] + lc[2] + lc[3] + lc[3];
    if (CANON.has(lc)) return lc;
    if (MAP[lc]) return MAP[lc];
    const fb = fallback(lc);
    (leftover[lc] = leftover[lc] || 0); leftover[lc]++;
    return fb;
  });
  const na = t => (t.replace(/&#\d+;/g, '').match(/[^\x00-\x7F]/g) || []).length;
  if (na(out) > na(orig)) { console.error('ВНЕСён не-ASCII в ' + rel); process.exit(1); }
  if (out !== orig) { changed++; if (!checkOnly) fs.writeFileSync(p, out); }
}
console.log((checkOnly ? 'would change: ' : 'changed: ') + changed + ' / ' + files.length);
const tail = Object.entries(leftover).sort((a,b)=>b[1]-a[1]);
if (tail.length) {
  console.log('\nфолбэком (не в явной таблице) — проверить ' + tail.length + ' цветов:');
  console.log(tail.map(([c,n]) => n + '  ' + c).join('\n'));
}
```

- [ ] Проверка синтаксиса: `node -e "require('./src/scripts/coursemap/normalize_palette.js')"` упадёт на записи — поэтому только просмотр в Task 2.

### Task 2: Прогон и сходимость

- [ ] `node src/scripts/coursemap/normalize_palette.js --check` → печатает число к изменению + список «фолбэком». Изучить список: цвета, попавшие во фолбэк, но с риском неверного тона — добавить в `MAP` явными строками. Повторять `--check` пока список фолбэка не станет коротким/безопасным.
- [ ] Боевой прогон: `node src/scripts/coursemap/normalize_palette.js` → `changed: N`.
- [ ] Идемпотентность: повторный прогон → `changed: 0`.
- [ ] Палитра сошлась: `node` — собрать все hex по `src/diagrams/**` кроме course_map, убедиться, что вне канона (нейтрали+15 акцентов+#fff/#000) осталось ≈0; распечатать остаток.
- [ ] **Спот-чек в Jupyter**: открыть `/files/diagrams/<...>.svg` для 6–8 файлов из разных папок (monads, kan, topos, optics, uncertainty, algebras) — глазами подтвердить читаемость (текст на тинтах тёмный, на узлах белый, фон белый).
- [ ] Commit: `git add src/scripts/coursemap/normalize_palette.js src/diagrams; git commit -m "diagrams: единая светлая палитра (normalize_palette.js)"`

### Task 3: Ручные тёмно-коллажные файлы

**Files:** Modify `src/diagrams/haskell/{gpu_landscape,conc_landscape,dist_landscape}.svg`, `src/diagrams/topos/topos_libraries.svg`

- [ ] Для каждого: открыть, найти тёмные карточки (`fill="#1a2744"`/`#222233`/`#2c3e6e`/`#3d2b7a` и пр.) и светлый текст на них. Перекрасить: карточка → тинт семейства по смыслу (или `#f7f8fa`), обводка → база семейства, текст внутри → тёмный (`#0f172a`/тон семейства). Фон → `#ffffff`. Стрелки → `#8a93a3`.
- [ ] После правки каждого: `node -e "JSON... "` не нужен (это SVG) — проверить well-formed: файл содержит `</svg>`, только ASCII (кроме `&#NNNN;`).
- [ ] Спот-чек этих 4 в Jupyter.
- [ ] Commit: `git add src/diagrams/haskell src/diagrams/topos/topos_libraries.svg; git commit -m "diagrams: ручная переделка тёмных коллажей под канон"`

### Task 4: Документация

**Files:** Modify `src/notebooks/DesignShowcase.ipynb`, `src/ROADMAP.md`

- [ ] `DesignShowcase.ipynb`: ячейку «🌑 Тёмная тема SVG — палитра» заменить на светлый канон (таблица нейтралей + 5 семейств узел/база/тинт); ячейку с «✅ решение: тёмные SVG» — на «светлая, в тон карте курса». Добавить markdown-ячейку «Кит маркеров стрелок» с блоком `<defs>` и таблицей применения (mono/epi/iso/nat) из спеки. Правка — node-скриптом по id ячеек или через поиск подстроки; `JSON.stringify(nb,null,1)+'\n'`, ensure_ascii не требуется (Jupyter), но проверить JSON-валидность.
- [ ] `ROADMAP.md`: в «Критические правила → SVG/палитра» заменить тёмную палитру на светлый канон; смягчить правило про `&#NNNN;` (numeric-entity для матсимволов разрешены — ASCII-безопасны и рендерятся); удалить/закрыть устаревший блок «Faza 6 — Ispravleniye SVG-diagramm» (кириллицы 0, тёмного фона 0). Добавить: «палитра диаграмм нормализуется `src/scripts/coursemap/normalize_palette.js`; новые диаграммы — по киту маркеров из DesignShowcase».
- [ ] Commit: `git add src/notebooks/DesignShowcase.ipynb src/ROADMAP.md; git commit -m "docs: светлый канон палитры + кит стрелок, закрыт устаревший SVG-аудит"`

### Task 5: Верификация и финиш

- [ ] Повторный `node src/scripts/coursemap/normalize_palette.js` → `changed: 0` (идемпотентность).
- [ ] ASCII-инвариант: ни одного non-ASCII (кроме `&#NNNN;`) во всех diagrams SVG.
- [ ] `git status` чист (кроме `? src/lib`).
- [ ] superpowers:finishing-a-development-branch — merge в master по выбору пользователя.
