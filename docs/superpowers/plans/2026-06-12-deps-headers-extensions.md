# План: шапки зависимостей + Extensions.ipynb

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Спека: `docs/superpowers/specs/2026-06-12-deps-headers-extensions-notebook-design.md`.

**Goal:** Автогенерируемая шапка «📦 Зависимости» в каждом ноутбуке + нулевой ноутбук Extensions.ipynb (бриф по расширениям GHC).

**Architecture:** Словарь `src/scripts/deps/dictionary.json` (один источник правды) + идемпотентный генератор `gen_headers.js` (вставляет/обновляет markdown-ячейку `deps_header`). Extensions.ipynb собирается node-скриптом `build_extensions.js` из JSON-описания ячеек, исполняется в контейнере.

**Tech Stack:** Node.js, IHaskell/GHC (контейнер gibiansky/ihaskell).

**Факты (собраны 2026-06-12):** 24 ноутбука; объединение расширений — 26 штук:
DeriveFunctor, ScopedTypeVariables, RankNTypes, TupleSections, FlexibleInstances,
FlexibleContexts, MultiParamTypeClasses, FunctionalDependencies, TypeOperators,
InstanceSigs, LambdaCase, Arrows, TypeFamilies, DeriveFoldable, DeriveTraversable,
ExistentialQuantification, TemplateHaskell, QuasiQuotes, DeriveGeneric,
DefaultSignatures, TypeSynonymInstances, OverloadedStrings,
GeneralizedNewtypeDeriving, GADTs, DataKinds, PolyKinds.
Пакеты по префиксам: base (по умолчанию), containers (Data.Map, Data.Set),
array (Data.Array), time (Data.Time), template-haskell (Language.Haskell),
process (System.Process). Модули src/lib: Quantale, KanExtension, Bitopos,
Distribution, SubjectiveModel.

---

### Task 0: Ветка

- [ ] `git checkout master; git pull; git checkout -b deps-headers`

### Task 1: Словарь

**Files:** Create `src/scripts/deps/dictionary.json`

- [ ] Записать словарь. Структура:

```json
{
  "extensions": {
    "OverloadedStrings": { "blurb": "строковые литералы любого типа IsString", "anchor": "overloadedstrings" },
    "LambdaCase": { "blurb": "\\case вместо \\x -> case x of", "anchor": "lambdacase" },
    "TupleSections": { "blurb": "частичное применение конструктора кортежа: (,5)", "anchor": "tuplesections" },
    "ScopedTypeVariables": { "blurb": "переменные типа из сигнатуры видны в теле", "anchor": "scopedtypevariables" },
    "RankNTypes": { "blurb": "forall внутри аргументов функций", "anchor": "rankntypes" },
    "ExistentialQuantification": { "blurb": "скрытие типа за конструктором (forall в data)", "anchor": "existentialquantification" },
    "FlexibleInstances": { "blurb": "инстансы для конкретных типов-применений", "anchor": "flexibleinstances" },
    "FlexibleContexts": { "blurb": "произвольные ограничения в контекстах", "anchor": "flexiblecontexts" },
    "TypeSynonymInstances": { "blurb": "инстансы для синонимов типов", "anchor": "flexibleinstances" },
    "MultiParamTypeClasses": { "blurb": "классы с несколькими параметрами", "anchor": "multiparamtypeclasses" },
    "FunctionalDependencies": { "blurb": "зависимости параметров класса: | m -> s", "anchor": "multiparamtypeclasses" },
    "InstanceSigs": { "blurb": "сигнатуры методов прямо в instance", "anchor": "instancesigs" },
    "DefaultSignatures": { "blurb": "default-реализации с другой сигнатурой", "anchor": "instancesigs" },
    "DeriveFunctor": { "blurb": "deriving Functor", "anchor": "deriving" },
    "DeriveFoldable": { "blurb": "deriving Foldable", "anchor": "deriving" },
    "DeriveTraversable": { "blurb": "deriving Traversable", "anchor": "deriving" },
    "DeriveGeneric": { "blurb": "deriving Generic для GHC.Generics", "anchor": "deriving" },
    "GeneralizedNewtypeDeriving": { "blurb": "newtype наследует инстансы обёрнутого типа", "anchor": "deriving" },
    "TypeOperators": { "blurb": "операторы на уровне типов: f :+: g", "anchor": "typeoperators" },
    "TypeFamilies": { "blurb": "функции на уровне типов", "anchor": "typefamilies" },
    "GADTs": { "blurb": "конструкторы с уточнёнными типами результата", "anchor": "gadts" },
    "DataKinds": { "blurb": "типы поднимаются в сорта (kinds)", "anchor": "datakinds" },
    "PolyKinds": { "blurb": "полиморфизм по сортам", "anchor": "datakinds" },
    "Arrows": { "blurb": "proc-нотация для стрелок", "anchor": "arrows" },
    "TemplateHaskell": { "blurb": "метапрограммирование: генерация кода при компиляции", "anchor": "templatehaskell" },
    "QuasiQuotes": { "blurb": "встраиваемые DSL-литералы [q|...|]", "anchor": "templatehaskell" }
  },
  "packages": {
    "Data.Map": "containers", "Data.Set": "containers",
    "Data.Array": "array", "Data.Time": "time",
    "Language.Haskell": "template-haskell", "System.Process": "process",
    "_default": "base"
  },
  "libModules": ["Quantale", "KanExtension", "Bitopos", "Distribution", "SubjectiveModel"]
}
```

- [ ] Проверка: `node -e "JSON.parse(require('fs').readFileSync('src/scripts/deps/dictionary.json','utf8')); console.log('OK')"` → OK
- [ ] Commit: `git add src/scripts/deps/dictionary.json; git commit -m "deps: словарь расширений и пакетов"`

### Task 2: Генератор шапок

**Files:** Create `src/scripts/deps/gen_headers.js`

- [ ] Написать генератор:

```js
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
else console.log((checkOnly ? 'would change: ' : 'updated: ') + changed);
```

- [ ] Прогон `node src/scripts/deps/gen_headers.js --check` → число ноутбуков без ошибок словаря.
- [ ] Прогон без `--check` → `updated: N`; повторный прогон → `updated: 0` (идемпотентность).
- [ ] JSON-валидность всех ноутбуков: цикл `JSON.parse` по `src/notebooks/*.ipynb` → OK.
- [ ] Визуально проверить шапку в 2 ноутбуках (git diff): ячейка после титульной, формат как в спеке.
- [ ] Commit: `git add -A src/scripts/deps src/notebooks; git commit -m "deps: генератор шапок + шапки во всех ноутбуках"`

### Task 3: Extensions.ipynb — сборка

**Files:** Create `src/scripts/deps/build_extensions.js`, `src/notebooks/Extensions.ipynb`

- [ ] Получить обратный индекс: `node src/scripts/deps/gen_headers.js --index` → JSON «расширение → ноутбуки» (использовать в ячейках разделов и итоговой таблице).
- [ ] Написать `build_extensions.js`, который пишет `src/notebooks/Extensions.ipynb` (nbformat 4.5, kernel haskell, у каждой ячейки уникальный ASCII id). Состав ячеек:
  1. **Титул** (md): `# 0️⃣ Расширения GHC: бриф` + аннотация «о чём, зачем, в чём соль» + правило курса: расширения включаются `:set -X...` в setup-ячейке.
  2. **SETUP** (code): `:set` всех расширений, которые демонстрируются кодом (без Arrows/TemplateHaskell — для них отдельные локальные пометки в тексте), `putStrLn "\x2705 SETUP OK"`.
  3. **TOC** (md): список разделов с якорями.
  4. Разделы — по группам, каждый: md-заголовок с `<a id="...">` (якоря из dictionary.json), мини-пример «без/с», список ноутбуков из индекса. Группы и примеры:
     - `overloadedstrings`, `lambdacase`, `tuplesections` — синтаксис и литералы. Пример: `(\case Just x -> x; Nothing -> 0) (Just 5)` и `map (,True) [1,2]`.
     - `scopedtypevariables`, `rankntypes`, `existentialquantification` — forall. Пример RankNTypes: `applyBoth :: (forall a. a -> a) -> (Int, Bool) -> (Int, Bool); applyBoth f (x, y) = (f x, f y)`.
     - `flexibleinstances` (+TypeSynonymInstances), `flexiblecontexts`, `multiparamtypeclasses` (+FunctionalDependencies), `instancesigs` (+DefaultSignatures) — классы типов. Пример MPTC+fundeps: `class Container c e | c -> e where empty :: c; insert :: e -> c -> c`.
     - `deriving` (DeriveFunctor/Foldable/Traversable/Generic, GeneralizedNewtypeDeriving). Пример: `data Tree a = Leaf | Node (Tree a) a (Tree a) deriving (Functor, Foldable, Show)` + `newtype Age = Age Int deriving (Show, Num)`.
     - `typeoperators`, `typefamilies`, `gadts`, `datakinds` (+PolyKinds) — уровень типов. Пример GADT: `data Expr a where { IntE :: Int -> Expr Int; BoolE :: Bool -> Expr Bool; If :: Expr Bool -> Expr a -> Expr a -> Expr a }` с total `eval`.
     - `arrows` — proc-нотация (md-описание + ссылка на Arrows.ipynb, код не исполнять: `:set -XArrows` ломает последующие лямбды в некоторых сборках IHaskell — проверить; если работает, добавить пример).
     - `templatehaskell` (+QuasiQuotes) — метапрограммирование (md + ссылка на MetaProgramming.ipynb).
  5. **За пределами курса** (md, без кода): TypeApplications, BangPatterns/StrictData, OverloadedRecordDot, PatternSynonyms, LinearTypes — по абзацу «в чём соль».
  6. **Итоговая таблица** (md): `| Расширение | Зачем | Ноутбуки |` — все 26 строк из словаря + индекса.
  7. **NAV** (md): ссылка на BaseHaskell.ipynb как следующий шаг.
- [ ] Запустить: `node src/scripts/deps/build_extensions.js`; JSON-валидность Extensions.ipynb.
- [ ] Commit: `git add src/scripts/deps/build_extensions.js src/notebooks/Extensions.ipynb; git commit -m "deps: Extensions.ipynb — бриф по расширениям"`

### Task 4: Верификация в контейнере

- [ ] `docker run --rm -v "<root>:/home/jovyan/pwd" gibiansky/ihaskell jupyter nbconvert --to notebook --execute --inplace /home/jovyan/pwd/src/notebooks/Extensions.ipynb --ExecutePreprocessor.timeout=900`
- [ ] Проверка node-ом: нет `output_type === 'error'` → errors: 0. Если ошибки — чинить пример в build_extensions.js, пересобрать, перепрогнать (не править ipynb руками).
- [ ] Commit: `git add src/notebooks/Extensions.ipynb; git commit -m "deps: Extensions.ipynb прогнан, 0 ошибок"`

### Task 5: ROADMAP + README

**Files:** Modify `src/ROADMAP.md`, `README.md`

- [ ] ROADMAP: новая фаза «Фаза 16 — Шапки зависимостей + Extensions.ipynb» с таблицей статусов (словарь / генератор / 23 шапки / Extensions.ipynb / прогон 0 ошибок). В «Критические правила → IHaskell/GHC» добавить: «ячейка `deps_header` генерируется `src/scripts/deps/gen_headers.js` — руками не править; после изменения setup/импортов перегенерировать».
- [ ] README: в описание курса добавить Extensions.ipynb как нулевой/входной ноутбук; команду `node src/scripts/deps/gen_headers.js` в раздел про скрипты/workflow.
- [ ] Commit: `git add src/ROADMAP.md README.md; git commit -m "deps: ROADMAP Фаза 16 + README"`

### Task 6: Финиш

- [ ] Повторный `node src/scripts/deps/gen_headers.js` → `updated: 0`; `git status` чист.
- [ ] superpowers:finishing-a-development-branch (merge в master по выбору пользователя).
