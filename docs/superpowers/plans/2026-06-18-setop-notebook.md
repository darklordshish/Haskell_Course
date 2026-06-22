# SetOp.ipynb Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Построить исполнимый ноутбук-этюд `src/notebooks/SetOp.ipynb` про категорию `Set^op` (ствол + 3 ветки: CABA, логика/ко-Гейтинг, пространства-vs-алгебры+CPS), всё в сравнении с `Set`.

**Architecture:** Повторяем пайплайн `Duality`: каждый раздел — файлы `src/scripts/setop/<slug>_md.txt` (проза + inline `<svg>`) и опционально `<slug>_hs.txt` (Haskell). Скрипт `fill_section.js` вписывает их в ячейки ноутбука и **выносит** каждый `<svg>` во внешний файл `src/diagrams/setop/<slug>_<n>.svg` (JupyterLab вырезает инлайновый SVG из markdown). Проверка раздела — прогон в контейнере `gibiansky/ihaskell`, 0 ошибок и ожидаемый вывод.

**Tech Stack:** IHaskell/GHC (контейнер `gibiansky/ihaskell`), Node.js (генераторы ячеек), рукописный SVG (палитра курса, ASCII-only внутри `<svg>`).

**Спека:** `docs/superpowers/specs/2026-06-18-setop-notebook-design.md`.

**Команда прогона** (Git Bash, Windows):
```
MSYS_NO_PATHCONV=1 docker run --rm -v "/c/Users/semion/Documents/AIDD/Haskell_Course_git/src/notebooks:/work" -w //work gibiansky/ihaskell:latest jupyter nbconvert --to notebook --execute --inplace SetOp.ipynb --ExecutePreprocessor.timeout=900
```
**Проверка ошибок:**
```
node -e "const fs=require('fs');const nb=JSON.parse(fs.readFileSync('src/notebooks/SetOp.ipynb','utf8'));let e=0;nb.cells.forEach(c=>(c.outputs||[]).forEach(o=>{if(o.output_type==='error')e++}));console.log('errors:',e)"
```

**Слаги разделов (порядок):** `intro`, `limits`, `notccc`, `caba`, `partitions`, `coheyting`, `dualities`, `cps`.

**Диаграммы (внешние, палитра курса, сравнение с Set как 2 столбца):** `setop_mirror` (intro), `setop_limits` (limits), `setop_powerset` + `setop_caba_cube` (caba), `setop_partition_lattice` (partitions), `setop_open_closed` + `setop_boundary` (coheyting), `setop_dualities` (dualities), `setop_cps` (cps).

**Конвенции диаграмм:** см. memory `diagram-conventions` — внутри `<svg>` только ASCII, матсимволы `&#NNNN;`, подстрочный индекс `<tspan dy=2 font-size=8>`; приглушённая светлая палитра (индиго `#5872c9`/`#3a4a96` = Set^op-сторона, шалфей `#3f9d77`/`#2f6f54` = Set-сторона, нейтраль `#475569`/`#8a93a3`/`#cbd5e1`); наконечники — inline `<polygon>` (для чат-превью); пунктир = единственный/универсальный морфизм.

---

## Task 1: Инструменты + каркас ноутбука

**Files:**
- Create: `src/scripts/setop/build_setop_scaffold.js`
- Create: `src/scripts/setop/fill_section.js`
- Create (генерируется): `src/notebooks/SetOp.ipynb`

- [ ] **Step 1: Создать `fill_section.js`** (адаптация duality-версии: пути setop, вынос SVG в `src/diagrams/setop/`).

```js
// fill_section.js <slug> — вписывает раздел в SetOp.ipynb, выносит inline <svg>
// в src/diagrams/setop/<slug>_<n>.svg и ставит ![..](../diagrams/setop/..). Идемпотентно.
const fs = require('fs'), path = require('path');
const slug = process.argv[2];
if (!slug) { console.error('usage: node fill_section.js <slug>'); process.exit(1); }
const NB = path.join(__dirname, '..', '..', 'notebooks', 'SetOp.ipynb');
const DIAGRAMS = path.join(__dirname, '..', '..', 'diagrams', 'setop');
const mdPath = path.join(__dirname, slug + '_md.txt');
const hsPath = path.join(__dirname, slug + '_hs.txt');
const nb = JSON.parse(fs.readFileSync(NB, 'utf8'));
const toLines = s => s.replace(/\n$/, '').split(/(?<=\n)/);
fs.mkdirSync(DIAGRAMS, { recursive: true });
let mdText = fs.readFileSync(mdPath, 'utf8');
let n = 0;
mdText = mdText.replace(/<svg[\s\S]*?<\/svg>/g, (svg) => {
  n++;
  const bad = (svg.replace(/&#\d+;/g, '').match(/[^\x00-\x7F]/g) || []);
  if (bad.length) { console.error('НЕ-ASCII в SVG #' + n + ' (' + slug + '): ' + [...new Set(bad)].join(' ')); process.exit(1); }
  const name = `${slug}_${n}.svg`;
  fs.writeFileSync(path.join(DIAGRAMS, name), svg + '\n');
  return `![${slug} fig.${n}](../diagrams/setop/${name})`;
});
const setLines = (id, text, isCode) => {
  const cell = nb.cells.find(c => c.id === id);
  if (!cell) throw new Error('нет ячейки ' + id);
  cell.source = toLines(text);
  if (isCode) { cell.outputs = []; cell.execution_count = null; }
};
setLines('setop_' + slug + '_md', mdText, false);
if (fs.existsSync(hsPath)) setLines('setop_' + slug + '_hs', fs.readFileSync(hsPath, 'utf8'), true);
fs.writeFileSync(NB, JSON.stringify(nb, null, 1) + '\n');
console.log(`раздел ${slug} вписан, ${n} SVG в diagrams/setop/`);
```

- [ ] **Step 2: Создать `build_setop_scaffold.js`** — строит каркас с setup-ячейкой, заголовком, TOC, стаб-ячейками разделов (для разделов с кодом — пара md+code, иначе только md), NAV.

```js
const fs = require('fs'), path = require('path');
const md = (id, src) => ({ cell_type: 'markdown', id, metadata: {}, source: src.replace(/\n$/, '').split(/(?<=\n)/) });
const code = (id, src) => ({ cell_type: 'code', id, metadata: {}, outputs: [], execution_count: null, source: src.replace(/\n$/, '').split(/(?<=\n)/) });
// разделы: [slug, заголовок, естьКод?]
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
// TOC
let toc = '## 📌 Содержание\n\n| # | Раздел | О чём |\n|---|--------|-------|\n';
const tocRows = [
  ['Ствол', 'переверни стрелки; (ко)пределы; не CCC/не топос', ''],
  ['A', 'Set^op &#8771; CABA: powerset, предикат-трансформеры', '#setop-caba'],
  ['B', 'логика: разбиения, ко-Гейтинг, граница, &#172;&#172;', '#setop-coheyting'],
  ['C', 'пространства vs алгебры; CPS-мост (Op, Cont)', '#setop-cps'],
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
```

- [ ] **Step 3: Собрать каркас и прогнать в контейнере.**

Run:
```
node src/scripts/setop/build_setop_scaffold.js
MSYS_NO_PATHCONV=1 docker run --rm -v "/c/Users/semion/Documents/AIDD/Haskell_Course_git/src/notebooks:/work" -w //work gibiansky/ihaskell:latest jupyter nbconvert --to notebook --execute --inplace SetOp.ipynb --ExecutePreprocessor.timeout=900
```
Expected: «SETUP OK», `node` проверка ошибок → `errors: 0`.

- [ ] **Step 4: Commit.**
```
git add src/scripts/setop src/notebooks/SetOp.ipynb
git commit -m "setop: каркас SetOp.ipynb + инструменты (scaffold, fill_section)"
```

---

## Task 2: Ствол — раздел `intro` (T0 парадокс + T1 определение)

**Files:** Create `src/scripts/setop/intro_md.txt`. Diagram `setop_mirror`.

- [ ] **Step 1: Написать `intro_md.txt`** — проза T0+T1 (по спеке) + диаграмма `setop_mirror`.

Содержание прозы: парадокс «перевернул стрелки — что за объект?»; определение `C^op` (те же объекты, `Hom_op(A,B)=Hom(B,A)`); в Set стрелка `A→B` = функция `B→A`; обещание трёх веток.

Диаграмма `setop_mirror` (два столбца, ~520×180): СЛЕВА «in Set» (шалфей) — объекты `a,b` (чипы), стрелка `f : a &#8594; b`; СПРАВА «in Set^op» (индиго) — те же `a,b`, стрелка перевёрнута `f : b &#8594; a` (та же `f`, направление обратное), подпись «same objects, arrow reversed». Внизу: «Hom_op(a,b) = Hom(b,a)». ASCII-only, наконечники `<polygon>`.

- [ ] **Step 2: Вписать и прогнать.**
```
node src/scripts/setop/fill_section.js intro
MSYS_NO_PATHCONV=1 docker run --rm -v "/c/Users/semion/Documents/AIDD/Haskell_Course_git/src/notebooks:/work" -w //work gibiansky/ihaskell:latest jupyter nbconvert --to notebook --execute --inplace SetOp.ipynb --ExecutePreprocessor.timeout=900
```
Expected: `errors: 0`; файл `src/diagrams/setop/intro_1.svg` создан.

- [ ] **Step 3: Превью диаграммы** через `mcp__visualize__show_widget` (вставить содержимое `intro_1.svg`); проверить геометрию/зеркало; при правках — повторить Step 1–2.

- [ ] **Step 4: Commit.**
```
git add src/scripts/setop/intro_md.txt src/diagrams/setop/intro_1.svg src/notebooks/SetOp.ipynb
git commit -m "setop: раздел intro (определение Set^op, диаграмма-зеркало)"
```

---

## Task 3: Ствол — раздел `limits` (T2 (ко)пределы, mono/epi)

**Files:** Create `src/scripts/setop/limits_md.txt`. Diagram `setop_limits`.

- [ ] **Step 1: Написать `limits_md.txt`** — проза: инъекция↔сюръекция; терминал `Set^op` = `∅` (нач. Set), начальный = `{∗}`; произведение `Set^op` = `⊔` (копроизв. Set), копроизв. = `×`; `Set` (ко)полна ⇒ `Set^op` тоже. Краткая таблица свопов. Ссылка `[Duality.ipynb](Duality.ipynb)` (не дублируем общий словарь). + диаграмма `setop_limits`.

Диаграмма `setop_limits` (~560×190): таблица-парад свопов в 2 столбца «Set | Set^op»: терминал `{∗} | ∅`, начальный `∅ | {∗}`, произведение `&#215; | &#8852;`, копроизведение `&#8852; | &#215;`, mono `&#8611; инъекция | сюръекция-наоборот`, epi `&#8608; сюръекция | инъекция-наоборот`. ASCII-only.

- [ ] **Step 2: Вписать и прогнать** (как Task 2 Step 2, slug `limits`). Expected `errors: 0`.
- [ ] **Step 3: Превью `setop_limits`**, проверить.
- [ ] **Step 4: Commit.**
```
git add src/scripts/setop/limits_md.txt src/diagrams/setop/limits_1.svg src/notebooks/SetOp.ipynb
git commit -m "setop: раздел limits ((ко)пределы и mono/epi, свопы со ссылкой на Duality)"
```

---

## Task 4: Ствол — раздел `notccc` (T3 не CCC + T4 не топос)

**Files:** Create `src/scripts/setop/notccc_md.txt`. Без кода, без диаграммы (проза).

- [ ] **Step 1: Написать `notccc_md.txt`** — проза: `Set^op` CCC ⟺ в `Set` есть ко-экспоненты — их нет (поэтому в `Set^op` нет объектов-функций); `Hask` — CCC (потому и программируем), `Hask^op` — нет; раз не CCC, то и не элементарный топос → завязка: «а какая структура там ЕСТЬ?» (переход к ветке B). Без диаграммы и кода.
- [ ] **Step 2: Вписать и прогнать** (slug `notccc`). Expected `errors: 0`.
- [ ] **Step 3: Commit.**
```
git add src/scripts/setop/notccc_md.txt src/notebooks/SetOp.ipynb
git commit -m "setop: раздел notccc (не CCC через ко-экспоненты, не топос)"
```

---

## Task 5: Ветка A — раздел `caba` (Set^op ≃ CABA) + код

**Files:** Create `src/scripts/setop/caba_md.txt`, `src/scripts/setop/caba_hs.txt`. Diagrams `setop_powerset`, `setop_caba_cube`.

- [ ] **Step 1: Написать `caba_hs.txt`** (этюд A).

```haskell
-- Контравариантный powerset: функция f : a -> b даёт прообраз f^{-1} : 2^b -> 2^a.
-- f^{-1} — гомоморфизм булевых алгебр (сохраняет пересечение/объединение/дополнение).
powerset :: [a] -> [[a]]
powerset = subsequences

preimage :: Eq b => (a -> b) -> [a] -> [b] -> [a]
preimage f dom s = [ x | x <- dom, f x `elem` s ]

setA = [0,1,2,3] :: [Int]
f x = even x                       -- f : A -> B = Bool

inter xs ys = [x | x <- xs, x `elem` ys]
union' xs ys = nub (xs ++ ys)

s1 = [True]; s2 = [False]
checkInter = sort (preimage f setA (inter s1 s2))
           == sort (inter (preimage f setA s1) (preimage f setA s2))
checkUnion = sort (preimage f setA (union' s1 s2))
           == sort (union' (preimage f setA s1) (preimage f setA s2))

-- стрелка Set^op как предикат-трансформер: предикат на b -> предикат на a
newtype Op r a = Op { runOp :: a -> r }
contramapOp :: (a -> b) -> Op r b -> Op r a
contramapOp f (Op g) = Op (g . f)

adult = Op (>= (18 :: Int)) :: Op Bool Int
byLen = contramapOp length adult :: Op Bool String   -- предикат на строках через length

(preimage f setA [True], checkInter, checkUnion, runOp adult 20, runOp byLen "hi")
```
Ожидаемый вывод: `([0,2],True,True,True,False)`.

- [ ] **Step 2: Прогнать этюд изолированно** (быстрый чек до сборки): создать временный `.hs` и `ghc -fno-code`, либо сразу Step 4. (Опционально.)

- [ ] **Step 3: Написать `caba_md.txt`** — проза A1–A3 (powerset контравариантен; теорема `Set^op &#8771; CABA`, атомы=элементы; стрелка=предикат-трансформер) + 2 диаграммы.

Диаграмма `setop_powerset` (~560×190): СЛЕВА Set — `f : a &#8594; b`; СПРАВА — `f^{-1} : 2^b &#8594; 2^a` (стрелка обратно), подпись «preimage = предикат-трансформер»; пунктир показывает соответствие. ASCII.

Диаграмма `setop_caba_cube` (~520×220): множество `X = {1,2,3}` (три точки) ↦ булев куб `2^X` (8 вершин, рёбра включения), атомы `{1},{2},{3}` отмечены; подпись «объект Set^op = его булева алгебра подмножеств; атомы = элементы». ASCII.

- [ ] **Step 4: Вписать и прогнать** (slug `caba`).
```
node src/scripts/setop/fill_section.js caba
MSYS_NO_PATHCONV=1 docker run ... --execute --inplace SetOp.ipynb ...
```
Expected: `errors: 0`; вывод ячейки `setop_caba_hs` = `([0,2],True,True,True,False)`.

- [ ] **Step 5: Превью `setop_powerset` и `setop_caba_cube`**; проверить.

- [ ] **Step 6: Commit.**
```
git add src/scripts/setop/caba_md.txt src/scripts/setop/caba_hs.txt src/diagrams/setop/caba_1.svg src/diagrams/setop/caba_2.svg src/notebooks/SetOp.ipynb
git commit -m "setop: ветка A (Set^op =~ CABA, powerset/предикат-трансформер), 0 ошибок"
```

---

## Task 6: Ветка B1 — раздел `partitions` (субобъекты=разбиения) + код

**Files:** Create `src/scripts/setop/partitions_md.txt`, `src/scripts/setop/partitions_hs.txt`. Diagram `setop_partition_lattice`.

- [ ] **Step 1: Написать `partitions_hs.txt`** (этюд B1: решётка разбиений + контрпример дистрибутивности).

```haskell
-- Субобъект в Set^op = сюръекция/разбиение в Set. Решётка разбиений недистрибутивна.
type Partition = [[Int]]

norm :: Partition -> Partition
norm = sort . map sort

partitions :: [Int] -> [Partition]
partitions [] = [[]]
partitions (x:xs) = concatMap ins (partitions xs)
  where ins p = ([x]:p) : [ (x:b):rest | (b,rest) <- picks p ]
        picks [] = []
        picks (b:bs) = (b,bs) : [ (b', b:bs') | (b',bs') <- picks bs ]

meetP :: Partition -> Partition -> Partition         -- общее измельчение (пересечения блоков)
meetP a b = norm [ i | ba <- a, bb <- b, let i = [x | x <- ba, x `elem` bb], not (null i) ]

joinP :: Partition -> Partition -> Partition          -- огрубление (слияние пересекающихся блоков)
joinP a b = norm (merge (a ++ b))
  where merge bs = case [ (x,y) | x <- bs, y <- bs, x < y, any (`elem` y) x ] of
                     []        -> bs
                     ((x,y):_) -> merge (nub (x ++ y) : filter (\z -> z /= x && z /= y) bs)

-- разбиения {1,2,3}: три «средних» атома, верх и низ
pa = [[1,2],[3]]; pb = [[1,3],[2]]; pc = [[2,3],[1]]
lhs = meetP pa (joinP pb pc)                  -- a /\ (b \/ c)
rhs = joinP (meetP pa pb) (meetP pa pc)        -- (a/\b) \/ (a/\c)

(length (partitions [1,2,3]), norm lhs, norm rhs, norm lhs == norm rhs)
```
Ожидаемый вывод: `(5,[[1,2],[3]],[[1],[2],[3]],False)` — 5 разбиений (`Π(3)=M₃`), и `a∧(b∨c) ≠ (a∧b)∨(a∧c)` (недистрибутивность).

- [ ] **Step 2: Написать `partitions_md.txt`** — проза B1 (субобъект=разбиение; `Π(X)` недистрибутивна; `Π(3)=M₃`, `Π(4)` немодулярна; наивная надежда на co-логику проваливается) + диаграмма.

Диаграмма `setop_partition_lattice` (~560×240): СЛЕВА булев куб `2³` (дистрибутивная решётка подмножеств `{1,2,3}`); СПРАВА `M₃` — решётка разбиений `Π(3)`: низ `{1|2|3}`, три средних атома `{12|3},{13|2},{23|1}`, верх `{123}`; подпись «недистрибутивна: a&#8743;(b&#8744;c)=a, (a&#8743;b)&#8744;(a&#8743;c)=&#8869;». ASCII.

- [ ] **Step 3: Вписать и прогнать** (slug `partitions`). Expected: `errors: 0`; вывод = `(5,[[1,2],[3]],[[1],[2],[3]],False)`.
- [ ] **Step 4: Превью `setop_partition_lattice`**.
- [ ] **Step 5: Commit.**
```
git add src/scripts/setop/partitions_md.txt src/scripts/setop/partitions_hs.txt src/diagrams/setop/partitions_1.svg src/notebooks/SetOp.ipynb
git commit -m "setop: ветка B1 (субобъекты=разбиения, M3 недистрибутивна), 0 ошибок"
```

---

## Task 7: Ветка B2-3 — раздел `coheyting` (ко-Гейтинг, граница, ¬¬) + код

**Files:** Create `src/scripts/setop/coheyting_md.txt`, `src/scripts/setop/coheyting_hs.txt`. Diagrams `setop_open_closed`, `setop_boundary`.

- [ ] **Step 1: Написать `coheyting_hs.txt`** (этюд B2: конечная топология; Гейтинг на открытых, ко-Гейтинг+граница на замкнутых).

```haskell
-- Топология = up-sets цепи 1<2<3 (Alexandrov). Открытые -> Гейтинг; замкнутые -> ко-Гейтинг.
universe = [1,2,3] :: [Int]
opens = [ [], [3], [2,3], [1,2,3] ] :: [[Int]]

subset xs ys   = all (`elem` ys) xs
complement s   = [x | x <- universe, x `notElem` s]
interior s     = sort (nub (concat [o | o <- opens, o `subset` s]))   -- наибольший открытый <= s
closure s      = complement (interior (complement s))                  -- двойственно
hImpl a b      = interior (nub (complement a ++ b))                    -- Гейтинг a -> b (на открытых)
hNot a         = hImpl a []                                            -- not a
cSub a b       = closure [x | x <- a, x `notElem` b]                   -- ко-Гейтинг a \ b (на замкнутых)
cNot a         = cSub universe a                                       -- ~a = T \ a
boundary a     = [x | x <- a, x `elem` cNot a]                          -- d a = a /\ ~a

oa = [3]      -- открытое:  Гейтинг
ca = [1,2]    -- замкнутое: ко-Гейтинг
( hNot oa, [x | x <- oa, x `elem` hNot oa]   -- not a и a /\ not a  (= [])
, cNot ca, boundary ca )                      -- ~a и d a  (граница != [])
```
Ожидаемый вывод: `([],[],[1,2,3],[1,2])` — Гейтинг `a∧¬a=∅`, но ко-Гейтинг `∂a=[1,2]≠∅` (паранепротиворечивая граница).

- [ ] **Step 2: Написать `coheyting_md.txt`** — проза B2 (ко-Гейтинг: вычитание `&#8722;` слева от `&#8744;`, ко-отрицание `~a`, граница `&#8706;a=a&#8743;~a&#8800;&#8869;`; пример: открытые=Гейтинг, замкнутые=ко-Гейтинг, `∂a`=топологическая граница) + B3 (мост `&#172;&#172;`: в Set всё булево; нуклеус `¬¬`→буализация→CABA (ветка A); вычислительная тень `¬¬` = `Cont` при `r=2` (ветка C); живая паранепротиворечивость требует не-булева топоса) + где живёт (Голдблатт/Toposes, Lawvere–Reyes, Mortensen) + 2 диаграммы.

Диаграмма `setop_open_closed` (~560×210): СЛЕВА «opens = Heyting (intuitionistic)» — решётка открытых цепи, `a&#8594;b`, `&#172;a`, `a&#8743;&#172;a=&#8869;`; СПРАВА «closeds = co-Heyting (paraconsistent)» — решётка замкнутых, `a&#8722;b`, `~a`, `&#8706;a&#8800;&#8869;`. ASCII.

Диаграмма `setop_boundary` (~520×200): топологическое пространство (интервал/множество), множество `a` залито, его **граница** `&#8706;a` выделена; подпись «`&#8706;a = a &#8743; ~a` — то, что и `a`, и `~a` держат вместе; в Гейтинге было бы `&#8869;`». ASCII.

- [ ] **Step 3: Вписать и прогнать** (slug `coheyting`). Expected: `errors: 0`; вывод = `([],[],[1,2,3],[1,2])`.
- [ ] **Step 4: Превью `setop_open_closed`, `setop_boundary`**.
- [ ] **Step 5: Commit.**
```
git add src/scripts/setop/coheyting_md.txt src/scripts/setop/coheyting_hs.txt src/diagrams/setop/coheyting_1.svg src/diagrams/setop/coheyting_2.svg src/notebooks/SetOp.ipynb
git commit -m "setop: ветка B2-3 (ко-Гейтинг, граница, мост двойного отрицания), 0 ошибок"
```

---

## Task 8: Ветка C1 — раздел `dualities` (пространства против алгебр)

**Files:** Create `src/scripts/setop/dualities_md.txt`. Diagram `setop_dualities`. Без кода.

- [ ] **Step 1: Написать `dualities_md.txt`** — проза C1: узор «пространство ↔ алгебра функций, стрелки наоборот»: `Ring^op`=аффинные схемы (Spec), `Bool^op`=Stone, `CRing/C*`=Gelfand, `Frame^op`=Locale; `Set^op&#8771;CABA` — дискретная игрушка. + диаграмма.

Диаграмма `setop_dualities` (~600×230): таблица-парад в 2 столбца «Пространства (геометрия) | Алгебры (op)»: строки `Set | CABA`, `Stone-пр. | Bool`, `компакт. хаусдорф. | C*-алгебры (Gelfand)`, `аффинные схемы | Ring (Spec)`, `локали | фреймы`; стрелка `&#8594;` помечена «functions / op». Подпись «Set^op — дискретный край этой лестницы». ASCII.

- [ ] **Step 2: Вписать и прогнать** (slug `dualities`). Expected `errors: 0`.
- [ ] **Step 3: Превью `setop_dualities`**.
- [ ] **Step 4: Commit.**
```
git add src/scripts/setop/dualities_md.txt src/diagrams/setop/dualities_1.svg src/notebooks/SetOp.ipynb
git commit -m "setop: ветка C1 (пространства против алгебр, парад двойственностей)"
```

---

## Task 9: Ветка C2-3 — раздел `cps` (CPS-мост) + код

**Files:** Create `src/scripts/setop/cps_md.txt`, `src/scripts/setop/cps_hs.txt`. Diagram `setop_cps`.

- [ ] **Step 1: Написать `cps_hs.txt`** (этюд C: Op, Cont, единица двойного отрицания).

```haskell
-- Haskell-зеркало Set^op = CPS. Op r a = a -> r (контравариант);
-- Cont r a = (a -> r) -> r — двойное отрицание; единица a -> Cont r a.
newtype Op r a = Op { runOp :: a -> r }
contramapOp :: (a -> b) -> Op r b -> Op r a
contramapOp f (Op g) = Op (g . f)

newtype Cont r a = Cont { runCont :: (a -> r) -> r }
instance Functor (Cont r) where
  fmap f (Cont c) = Cont (\k -> c (k . f))
instance Applicative (Cont r) where
  pure a = Cont (\k -> k a)
  Cont f <*> Cont x = Cont (\k -> f (\g -> x (k . g)))
instance Monad (Cont r) where
  Cont c >>= f = Cont (\k -> c (\a -> runCont (f a) k))

unit :: a -> Cont r a              -- единица двойного отрицания (return)
unit = pure

demo = runCont (do { x <- unit 7; unit (x + 1) }) id :: Int   -- 8
adult = Op (>= (18 :: Int)) :: Op Bool Int
byLen = contramapOp length adult :: Op Bool String

(demo, runOp adult 20, runOp byLen "hello, world")
```
Ожидаемый вывод: `(8,True,False)`.

- [ ] **Step 2: Написать `cps_md.txt`** — проза C2 (CPS-зеркало: `Op` контравариантен; `Cont r=(a→r)→r` двойное отрицание, при `r=2` двойной powerset; «программы наоборот») + C3 (применения: CPS-компиляция, delimited continuations, Stone в CS, Spec, базы Спивака; подводные камни: полнота+атомарность для `Set^op&#8771;CABA`, чистые BA→Stone-пространства, роль `r`, `Set^op&#8800;Set` — нет функц. пространств) + диаграмма.

Диаграмма `setop_cps` (~560×200): СЛЕВА Set/Hask — значение `a`, прямая стрелка; СПРАВА — `(a&#8594;r)&#8594;r` (двойное отрицание), стрелки «наоборот»; подпись «`r=2`: двойной powerset; `Cont` — вычислительная тень `&#172;&#172;`». ASCII.

- [ ] **Step 3: Вписать и прогнать** (slug `cps`). Expected: `errors: 0`; вывод = `(8,True,False)`.
- [ ] **Step 4: Превью `setop_cps`**.
- [ ] **Step 5: Commit.**
```
git add src/scripts/setop/cps_md.txt src/scripts/setop/cps_hs.txt src/diagrams/setop/cps_1.svg src/notebooks/SetOp.ipynb
git commit -m "setop: ветка C2-3 (CPS-мост Op/Cont, применения, подводные камни), 0 ошибок"
```

---

## Task 10: Интеграция (шапка, NAV, README/ROADMAP) + слияние

**Files:** Modify `src/notebooks/SetOp.ipynb` (deps header, NAV), `README.md`, `src/README.ipynb`, `src/ROADMAP.md`.

- [ ] **Step 1: Шапка зависимостей.** Прогнать генератор шапок (если поддерживает новый ноутбук) или добавить ячейку `deps_header` вручную по образцу. Run:
```
node src/scripts/deps/gen_headers.js
```
Если SetOp не подхватывается — добавить его в конфиг генератора или вставить ячейку вручную (пакеты: base; расширения: ScopedTypeVariables, RankNTypes; модули src/lib — нет). Прогнать ноутбук, `errors: 0`.

- [ ] **Step 2: README.md** — в блок «Справочник (вне ствола)» добавить строку про `SetOp.ipynb` (категория Set^op: что это, логика, пространства/CPS, в сравнении с Set).

- [ ] **Step 3: README.ipynb** — добавить карточку `## 🪞 Этюд: Категория Set^op` после карточки Duality (файл, уровень ⚫, пререквизиты Duality/Toposes/KanExtensions, таблица трёх веток), строку в Содержание и Сводную (ячеек/SVG), через node-скрипт (как делалось для Duality).

- [ ] **Step 4: ROADMAP.md** — новая фаза «Этюд SetOp.ipynb» с таблицей разделов и пометкой «0 ошибок».

- [ ] **Step 5: Финальный полный прогон** в контейнере, `errors: 0`. Проверить, что все 9 SVG лежат в `src/diagrams/setop/` и в ноутбуке только `![](...)` (инлайнового `<svg>` нет):
```
node -e "const fs=require('fs');const nb=JSON.parse(fs.readFileSync('src/notebooks/SetOp.ipynb','utf8'));const all=nb.cells.map(c=>c.source.join('')).join('');console.log('inline svg:',(all.match(/<svg/g)||[]).length,'| refs:',(all.match(/diagrams\/setop\//g)||[]).length)"
```
Expected: `inline svg: 0 | refs: 9`.

- [ ] **Step 6: Commit + слияние в master.**
```
git add -A
git commit -m "setop: интеграция (шапка, NAV, README/ROADMAP), финальный прогон 0 ошибок"
git checkout master && git merge --no-ff <branch> -m "Merge: этюд SetOp.ipynb (категория Set^op)"
git push origin master
```

---

## Self-Review (выполнено при написании плана)

- **Покрытие спеки:** ствол T0–T4 → Tasks 2–4; ветка A → Task 5; B1 → Task 6; B2-3 → Task 7; C1 → Task 8; C2-3 → Task 9; механика/диаграммы/README → Tasks 1, 10. Все разделы спеки покрыты.
- **Плейсхолдеры:** Haskell-этюды даны полностью с ожидаемым выводом; диаграммы — точной спецификацией содержания (полный SVG авторится и превьюрится итеративно — особенность домена). Прозовые блоки кратко описаны со ссылкой на спеку (не дословный текст — допустимо для нарратива).
- **Согласованность типов/имён:** `Op`/`contramapOp`/`Cont`/`unit` согласованы между Task 5 и Task 9 (в обоих определяется `Op` локально в своей ячейке — это нормально, ячейки независимы); слаги совпадают со scaffold `SECTIONS`.
