'use strict';
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------
const ROOT = path.resolve(__dirname, '../../..');
const DICT_PATH = path.join(__dirname, 'dictionary.json');
const OUT_PATH = path.join(ROOT, 'src', 'notebooks', 'Extensions.ipynb');

// ---------------------------------------------------------------------------
// Load dictionary & reverse index
// ---------------------------------------------------------------------------
const dict = JSON.parse(fs.readFileSync(DICT_PATH, 'utf8'));
const indexJson = cp.execSync(
  'node ' + path.join(__dirname, 'gen_headers.js') + ' --index',
  { encoding: 'utf8' }
);
const reverseIndex = JSON.parse(indexJson); // { ExtName: ["Foo.ipynb", ...] }

// Helper: notebook names without .ipynb, comma-separated; "—" if none
// Extensions.ipynb is filtered out to avoid self-reference.
function notebookList(extName) {
  const nbs = (reverseIndex[extName] || []).filter(n => n !== 'Extensions.ipynb');
  if (nbs.length === 0) return '—';
  return nbs.map(n => n.replace(/\.ipynb$/, '')).join(', ');
}

// ---------------------------------------------------------------------------
// Cell helpers
// ---------------------------------------------------------------------------
function mdCell(id, text) {
  const source = text.split('\n').map((l, i, arr) =>
    i < arr.length - 1 ? l + '\n' : l
  );
  return { cell_type: 'markdown', id, metadata: {}, source };
}

function codeCell(id, text) {
  const source = text.split('\n').map((l, i, arr) =>
    i < arr.length - 1 ? l + '\n' : l
  );
  return {
    cell_type: 'code',
    id,
    metadata: {},
    execution_count: null,
    outputs: [],
    source
  };
}

// ---------------------------------------------------------------------------
// Cell definitions
// ---------------------------------------------------------------------------
const cells = [];

// ── 1. Титул ────────────────────────────────────────────────────────────────
cells.push(mdCell('ext_title', `\
# 0️⃣ Расширения GHC: бриф

**Language extensions** — это управляемые расширения стандарта Haskell, которые включаются прагмой \`{-# LANGUAGE ... #-}\` или командой \`:set -X...\` в REPL/IHaskell.

Стандарт Haskell 2010 намеренно консервативен; расширения дают доступ к более выразительным возможностям системы типов и синтаксиса, которые либо ещё не вошли в стандарт, либо принципиально выходят за его рамки.

## О чём этот ноутбук

Каждый ноутбук курса включает только те расширения, которые действительно нужны для его кода.
Здесь — краткий справочник: **что, зачем, в чём соль** для каждого из ${Object.keys(dict.extensions).length} расширений курса.

## Правило курса

Расширения включаются в **setup-ячейке** каждого ноутбука через \`:set -X...\`, например:

\`\`\`
:set -XOverloadedStrings -XLambdaCase -XScopedTypeVariables
\`\`\``));

// ── 2. SETUP ─────────────────────────────────────────────────────────────────
// All extensions demonstrated by code below (exclude Arrows, TemplateHaskell, QuasiQuotes)
cells.push(codeCell('ext_setup', `\
:set -XOverloadedStrings
:set -XLambdaCase
:set -XTupleSections
:set -XScopedTypeVariables
:set -XRankNTypes
:set -XExistentialQuantification
:set -XFlexibleInstances
:set -XTypeSynonymInstances
:set -XFlexibleContexts
:set -XMultiParamTypeClasses
:set -XFunctionalDependencies
:set -XInstanceSigs
:set -XDefaultSignatures
:set -XDeriveFunctor
:set -XDeriveFoldable
:set -XDeriveTraversable
:set -XDeriveGeneric
:set -XGeneralizedNewtypeDeriving
:set -XTypeOperators
:set -XTypeFamilies
:set -XGADTs
:set -XDataKinds
:set -XPolyKinds
putStrLn "\x2705 SETUP OK"`));

// ── 3. TOC ──────────────────────────────────────────────────────────────────
cells.push(mdCell('ext_toc', `\
## Содержание

1. [Синтаксис и литералы](#overloadedstrings): OverloadedStrings, LambdaCase, TupleSections
2. [Forall-полиморфизм](#scopedtypevariables): ScopedTypeVariables, RankNTypes, ExistentialQuantification
3. [Классы типов](#flexibleinstances): FlexibleInstances/TypeSynonymInstances, FlexibleContexts, MultiParamTypeClasses/FunctionalDependencies, InstanceSigs/DefaultSignatures
4. [Deriving](#deriving): DeriveFunctor/Foldable/Traversable/Generic, GeneralizedNewtypeDeriving
5. [Уровень типов](#typeoperators): TypeOperators, TypeFamilies, GADTs, DataKinds/PolyKinds
6. [Стрелки (Arrows)](#arrows): proc-нотация
7. [Метапрограммирование](#templatehaskell): TemplateHaskell, QuasiQuotes
8. [За пределами курса](#beyond)
9. [Итоговая таблица](#table)`));

// ── 4. Синтаксис и литералы ─────────────────────────────────────────────────
cells.push(mdCell('ext_syntax_md', `\
<a id="overloadedstrings"></a>
## Синтаксис и литералы

### OverloadedStrings
**В чём соль:** строковый литерал \`"hello"\` перегружается — его тип становится \`IsString a => a\`, а не фиксированным \`String\`. Позволяет писать \`"key"\` там, где ожидается \`Text\`, \`ByteString\` и т.д., без явных конверсий.
Ноутбуки-потребители: ${notebookList('OverloadedStrings')}

<a id="lambdacase"></a>
### LambdaCase
**В чём соль:** синтаксический сахар \`\\case\` эквивалентен \`\\x -> case x of\`. Убирает лишнее имя-пустышку и делает point-free стиль доступным там, где нужен pattern-matching.
Ноутбуки-потребители: ${notebookList('LambdaCase')}

<a id="tuplesections"></a>
### TupleSections
**В чём соль:** \`(,True)\` — частично применённый конструктор пары; \`(,True) 5\` даёт \`(5,True)\`. Удобно в комбинации с \`map\`, \`fmap\` и стрелками.
Ноутбуки-потребители: ${notebookList('TupleSections')}`));

cells.push(codeCell('ext_syntax_code', `\
import Data.String (IsString(..))

-- OverloadedStrings: кастомный тип, реализующий IsString
newtype MyStr = MyStr String deriving (Show)

instance IsString MyStr where
  fromString s = MyStr s

greet :: MyStr
greet = "Привет, мир"

-- LambdaCase: сопоставление без имени переменной
describeInt :: Maybe Int -> Int
describeInt = (\\case { Just x -> x; Nothing -> 0 })

-- TupleSections: частичное применение конструктора пары
pairs :: [(Int, Bool)]
pairs = map (,True) [1, 2, 3]

putStrLn ("OverloadedStrings: " ++ show greet)
putStrLn ("LambdaCase: " ++ show (describeInt (Just 42)) ++ ", " ++ show (describeInt Nothing))
putStrLn ("TupleSections: " ++ show pairs)`));

// ── 5. Forall ────────────────────────────────────────────────────────────────
cells.push(mdCell('ext_forall_md', `\
<a id="scopedtypevariables"></a>
## Forall-полиморфизм

### ScopedTypeVariables
**В чём соль:** переменные типа из сигнатуры функции (введённые явным \`forall\`) становятся видны в теле, в том числе в \`where\`-клаузулах и вложенных аннотациях. Без этого расширения вложенные аннотации типов создают независимые переменные.
Ноутбуки-потребители: ${notebookList('ScopedTypeVariables')}

<a id="rankntypes"></a>
### RankNTypes
**В чём соль:** аргумент функции сам может быть полиморфным — т.е. иметь тип \`forall a. ...\`. Стандарт допускает только ранг-1 (polym. только на верхнем уровне). Нужен для \`runST\`, линз, CPS и других паттернов.
Ноутбуки-потребители: ${notebookList('RankNTypes')}

<a id="existentialquantification"></a>
### ExistentialQuantification
**В чём соль:** тип-параметр конструктора данных скрывается снаружи — \`forall a. Show a => Box a\` позволяет класть в один список значения разных типов, объединённых только ограничением.
Ноутбуки-потребители: ${notebookList('ExistentialQuantification')}`));

cells.push(codeCell('ext_forall_code', `\
-- ScopedTypeVariables: явный forall, чтобы использовать 'a' в where
reverseGeneric :: forall a. [a] -> [a]
reverseGeneric xs = go xs []
  where
    go :: [a] -> [a] -> [a]
    go []     acc = acc
    go (h:t)  acc = go t (h:acc)

-- RankNTypes: аргумент сам полиморфен
applyBoth :: (forall a. a -> a) -> (Int, Bool) -> (Int, Bool)
applyBoth f (x, y) = (f x, f y)

-- ExistentialQuantification: гетерогенный контейнер
data Showable = forall a. Show a => MkShowable a

showIt :: Showable -> String
showIt (MkShowable x) = show x

things :: [Showable]
things = [MkShowable (42 :: Int), MkShowable True, MkShowable "hello"]

putStrLn ("ScopedTypeVariables: " ++ show (reverseGeneric [1,2,3::Int]))
putStrLn ("RankNTypes: " ++ show (applyBoth id (7, False)))
putStrLn ("ExistentialQuantification: " ++ unwords (map showIt things))`));

// ── 6. Классы типов ──────────────────────────────────────────────────────────
cells.push(mdCell('ext_classes_md', `\
<a id="flexibleinstances"></a>
## Классы типов

### FlexibleInstances + TypeSynonymInstances
**В чём соль:** Haskell 2010 разрешает инстансы только вида \`C T\` или \`C (T a b)\` с переменными-аргументами. FlexibleInstances снимает это ограничение — можно писать \`instance C [Int]\` или \`instance C (Maybe String)\`. TypeSynonymInstances разрешает использовать синонимы типов (\`String\`) как голову инстанса.
Ноутбуки-потребители: ${notebookList('FlexibleInstances')}

<a id="flexiblecontexts"></a>
### FlexibleContexts
**В чём соль:** контекст ограничений может содержать произвольные применения классов, не только \`C a\` с голой переменной. Например, \`(Show (f a)) =>\` становится легальным.
Ноутбуки-потребители: ${notebookList('FlexibleContexts')}

<a id="multiparamtypeclasses"></a>
### MultiParamTypeClasses + FunctionalDependencies
**В чём соль:** класс типов может принимать несколько параметров: \`class Convertible a b\`. FunctionalDependencies (\`| a -> b\`) задают функциональные зависимости между параметрами, помогая type-checker'у выводить типы однозначно.
Ноутбуки-потребители: ${notebookList('MultiParamTypeClasses')}

<a id="instancesigs"></a>
### InstanceSigs + DefaultSignatures
**В чём соль:** InstanceSigs позволяет явно писать сигнатуры методов внутри \`instance\`-блока — удобно для документирования и специализации. DefaultSignatures позволяют объявить реализацию метода по умолчанию с более конкретной сигнатурой (например, с дополнительным ограничением).
Ноутбуки-потребители: ${notebookList('InstanceSigs')}`));

cells.push(codeCell('ext_classes_code', `\
-- MultiParamTypeClasses + FunctionalDependencies
class Container c e | c -> e where
  empty  :: c
  insert :: e -> c -> c
  toList :: c -> [e]

instance Container [Int] Int where
  empty      = []
  insert x c = x : c
  toList     = id

-- FlexibleInstances: инстанс для конкретного типа [Char]
class Describable a where
  describe :: a -> String

instance Describable [Char] where
  describe s = "строка: " ++ s

instance Describable Int where
  describe n = "число: " ++ show n

-- InstanceSigs: явная сигнатура в инстансе
class Wrap a where
  wrap   :: a -> [a]
  wrap x = [x]           -- default

instance Wrap Int where
  wrap :: Int -> [Int]
  wrap x = [x, x]        -- переопределяем

let c0 = empty :: [Int]
    c1 = insert 3 (insert 1 (insert 2 c0))
putStrLn ("Container: " ++ show (toList c1))
putStrLn (describe ("мир" :: String))
putStrLn (describe (99 :: Int))
putStrLn ("InstanceSigs wrap: " ++ show (wrap (5 :: Int)))`));

// ── 7. Deriving ──────────────────────────────────────────────────────────────
cells.push(mdCell('ext_deriving_md', `\
<a id="deriving"></a>
## Deriving

### DeriveFunctor / DeriveFoldable / DeriveTraversable
**В чём соль:** компилятор автоматически генерирует экземпляры \`Functor\`, \`Foldable\`, \`Traversable\` для пользовательских типов данных, следуя структуре конструкторов. Исключает boilerplate для деревьев, потоков, rose-trees и т.п.
Ноутбуки-потребители: ${notebookList('DeriveFunctor')} (Functor), ${notebookList('DeriveFoldable')} (Foldable), ${notebookList('DeriveTraversable')} (Traversable)

### DeriveGeneric
**В чём соль:** генерирует инстанс \`GHC.Generics.Generic\`, открывая доступ к структуре типа на уровне типов. Основа для библиотек \`aeson\`, \`binary\`, \`lens\` (deriving-through-Generic).
Ноутбуки-потребители: ${notebookList('DeriveGeneric')}

### GeneralizedNewtypeDeriving
**В чём соль:** \`newtype\` автоматически наследует инстансы обёрнутого типа — не только стандартные классы, но и любой класс, для которого реализация корректна через coerce. Устраняет необходимость писать делегирующие инстансы вручную.
Ноутбуки-потребители: ${notebookList('GeneralizedNewtypeDeriving')}`));

cells.push(codeCell('ext_deriving_code', `\
-- DeriveFunctor, DeriveFoldable, DeriveTraversable
data Tree a = Leaf | Node (Tree a) a (Tree a)
  deriving (Functor, Foldable, Show)

-- GeneralizedNewtypeDeriving: Age наследует Num у Int
newtype Age = Age Int
  deriving (Show, Eq, Num)

let t = Node (Node Leaf 1 Leaf) 2 (Node Leaf 3 Leaf)
putStrLn ("fmap (*10) tree: " ++ show (fmap (*10) t))
putStrLn ("sum tree: " ++ show (sum t))

let a1 = Age 30
    a2 = Age 5
putStrLn ("Age: " ++ show a1 ++ " + " ++ show a2 ++ " = " ++ show (a1 + a2))`));

// ── 8. Уровень типов ─────────────────────────────────────────────────────────
cells.push(mdCell('ext_types_md', `\
<a id="typeoperators"></a>
## Уровень типов

### TypeOperators
**В чём соль:** операторы (символьные идентификаторы) могут использоваться как конструкторы типов: \`data f :+: g = ...\`. Используется в GHC.Generics, optics-библиотеках.
Ноутбуки-потребители: ${notebookList('TypeOperators')}

<a id="typefamilies"></a>
### TypeFamilies
**В чём соль:** функции на уровне типов — \`type family Elem c where Elem [a] = a\`. Позволяют выражать вычисления над типами в стиле функциональной зависимости, но более мощно и удобно, чем FunctionalDependencies.
Ноутбуки-потребители: ${notebookList('TypeFamilies')}

<a id="gadts"></a>
### GADTs
**В чём соль:** каждый конструктор может специализировать возвращаемый тип — \`IntE :: Int -> Expr Int\`. Это делает невозможным «неправильное» построение значений и позволяет писать тотальные функции-интерпретаторы без \`undefined\`.
Ноутбуки-потребители: ${notebookList('GADTs')}

<a id="datakinds"></a>
### DataKinds + PolyKinds
**В чём соль:** DataKinds «поднимает» типы данных на уровень сортов (kinds) — конструкторы \`True\`, \`False\` становятся типами сорта \`Bool\`. PolyKinds добавляет полиморфизм по сортам. Основа для type-level natural numbers, гетерогенных списков, phantom-типов.
Ноутбуки-потребители: ${notebookList('DataKinds')}`));

cells.push(codeCell('ext_types_code', `\
-- TypeFamilies: ассоциированное семейство типов
class Collection c where
  type Elem c
  fromList :: [Elem c] -> c
  size     :: c -> Int

instance Collection [a] where
  type Elem [a] = a
  fromList = id
  size     = length

-- GADTs: типобезопасное выражение
data Expr a where
  IntE  :: Int  -> Expr Int
  BoolE :: Bool -> Expr Bool
  If    :: Expr Bool -> Expr a -> Expr a -> Expr a

eval :: Expr a -> a
eval (IntE  n)    = n
eval (BoolE b)    = b
eval (If c t e)   = if eval c then eval t else eval e

-- TypeOperators: оператор-тип
data a :+: b = Inl a | Inr b deriving (Show)

let e1 = If (BoolE True) (IntE 42) (IntE 0)
    e2 = If (BoolE False) (IntE 1) (IntE 2)
putStrLn ("GADT eval: " ++ show (eval e1) ++ ", " ++ show (eval e2))
putStrLn ("TypeFamilies size: " ++ show (size (fromList [1,2,3] :: [Int])))
let v = Inl (42::Int) :: Int :+: Bool
putStrLn ("TypeOperators :+: " ++ show v)`));

// ── 9. Arrows ────────────────────────────────────────────────────────────────
cells.push(mdCell('ext_arrows_md', `\
<a id="arrows"></a>
## Стрелки (Arrows)

### Arrows
**В чём соль:** расширение включает \`proc\`-нотацию — синтаксический сахар для комбинаторов класса \`Arrow\`. Стрелки обобщают монады: \`proc x -> do ...\` выглядит как do-нотация, но работает для любого \`Arrow\`, включая \`Function\`, \`Kleisli\`, парсер-комбинаторы.

\`\`\`haskell
addA :: Arrow a => a (b, c) b -> a (b, c) c -> a (b, c) (b, c)
addA f g = proc x -> do
  y <- f -< x
  z <- g -< x
  returnA -< (y, z)
\`\`\`

Ноутбуки-потребители: ${notebookList('Arrows')}

> Полный разбор с примерами: **[Arrows.ipynb](Arrows.ipynb)**`));

// ── 10. TemplateHaskell ───────────────────────────────────────────────────────
cells.push(mdCell('ext_th_md', `\
<a id="templatehaskell"></a>
## Метапрограммирование

### TemplateHaskell + QuasiQuotes
**В чём соль:** TemplateHaskell — метапрограммирование времени компиляции: сплайсы \`$(expr)\` вставляют сгенерированный AST прямо в код. QuasiQuotes (\`[myDSL| ... |]\`) — встраиваемые DSL-литералы, разбираемые кастомным парсером.

Примеры применений: автогенерация \`Lens\`-полей (\`makeLenses\`), персистентные схемы Persistent, генерация FFI-биндингов, compile-time парсинг регулярных выражений.

Ноутбуки-потребители: ${notebookList('TemplateHaskell')}

> Полный разбор с примерами: **[MetaProgramming.ipynb](MetaProgramming.ipynb)**`));

// ── 11. За пределами курса ────────────────────────────────────────────────────
cells.push(mdCell('ext_beyond_md', `\
<a id="beyond"></a>
## За пределами курса

Ниже — расширения, часто встречающиеся в реальных проектах, но не используемые в ноутбуках курса.

**TypeApplications** (\`-XTypeApplications\`): явное применение типов к полиморфным функциям — \`read @Int "42"\`. Убирает необходимость в вспомогательных аннотациях типов во многих местах.

**BangPatterns / StrictData** (\`-XBangPatterns\`, \`-XStrictData\`): управление строгостью на уровне паттернов (\`!x\`) или всего модуля. Используется для оптимизации пространственного потребления и устранения пространственных утечек.

**OverloadedRecordDot** (\`-XOverloadedRecordDot\`): синтаксис \`record.field\` для доступа к полям записей — как в большинстве других языков. Доступен начиная с GHC 9.2.

**PatternSynonyms** (\`-XPatternSynonyms\`): именованные алиасы для паттернов. Позволяют создавать стабильный публичный API поверх изменяемой внутренней структуры данных.

**LinearTypes** (\`-XLinearTypes\`): типы с линейными ограничениями — функция \`a %1 -> b\` обязана использовать аргумент ровно один раз. Открывает путь к safe manual memory management и resource tracking на уровне типов. Доступен с GHC 9.0.`));

// ── 12. Итоговая таблица ─────────────────────────────────────────────────────
// Build table programmatically from dictionary
const tableRows = Object.entries(dict.extensions).map(([extName, info]) => {
  const nbs = notebookList(extName);
  const blurb = info.blurb.replace(/\|/g, '\\|');
  return `| \`${extName}\` | ${blurb} | ${nbs} |`;
}).join('\n');

cells.push(mdCell('ext_table_md', `\
<a id="table"></a>
## Итоговая таблица расширений курса

| Расширение | Зачем | Ноутбуки |
|---|---|---|
${tableRows}`));

// ── 13. NAV ───────────────────────────────────────────────────────────────────
cells.push(mdCell('ext_nav_md', `\
---
**Следующий шаг:** [BaseHaskell.ipynb](BaseHaskell.ipynb)`));

// ---------------------------------------------------------------------------
// Assemble notebook
// ---------------------------------------------------------------------------
const notebook = {
  nbformat: 4,
  nbformat_minor: 5,
  metadata: {
    kernelspec: {
      display_name: 'Haskell',
      language: 'haskell',
      name: 'haskell'
    },
    language_info: { name: 'haskell' }
  },
  cells
};

fs.writeFileSync(OUT_PATH, JSON.stringify(notebook, null, 1) + '\n', { encoding: 'utf8' });
console.log('Written: ' + OUT_PATH);
console.log('Cell count: ' + cells.length);
