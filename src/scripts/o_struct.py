#!/usr/bin/env python3
"""Phase 11 structural pass for Optics.ipynb:
- reorder cells to target 1-19 order
- fix code-in-markdown cell (id 20baa427 -> code)
- drop duplicate summaries / diagram heading / lone image
- insert 6 new fully-populated executable sections + new 3-channel summary
Existing-section markdown is left as-is here (reskeleton done in a later step).
"""
import json, sys
PATH = "/home/jovyan/src/notebooks/Optics.ipynb"

def md(idv, text):
    return {"cell_type": "markdown", "id": idv, "metadata": {},
            "source": text.splitlines(keepends=True)}

def code(idv, text):
    return {"cell_type": "code", "id": idv, "metadata": {},
            "execution_count": None, "outputs": [],
            "source": text.splitlines(keepends=True)}

# ---------- NEW SECTION CONTENT ----------

S4_MD = r"""## 4️⃣ Законы линз

Корректная («lawful») линза подчиняется трём законам, связывающим `get` и `set`:

- **get-put:** `set s (get s) = s` — записать то, что прочитали, ничего не меняет;
- **put-get:** `get (set s a) = a` — прочитать записанное даёт записанное;
- **put-put:** `set (set s a) b = set s b` — последняя запись побеждает.

Линза, нарушающая хоть один закон (например, сеттер с нормализацией или побочным
эффектом), формально линзой не является — она «well-behaved» только при всех трёх.
"""

S4_CODE = r"""-- S4: lens laws (concrete getter/setter)
:set -XScopedTypeVariables
data CLens s a = CLens { cget :: s -> a, cset :: s -> a -> s }

data P = P { px :: Int, py :: Int } deriving (Eq, Show)
lx :: CLens P Int
lx = CLens px (\p v -> p { px = v })

lawGetPut :: Eq s => CLens s a -> s -> Bool
lawGetPut l s = cset l s (cget l s) == s
lawPutGet :: Eq a => CLens s a -> s -> a -> Bool
lawPutGet l s a = cget l (cset l s a) == a
lawPutPut :: Eq s => CLens s a -> s -> a -> a -> Bool
lawPutPut l s a b = cset l (cset l s a) b == cset l s b

demoLaws :: IO ()
demoLaws = do
  let s = P 3 4
  putStrLn ("get-put: " ++ show (lawGetPut lx s))
  putStrLn ("put-get: " ++ show (lawPutGet lx s 9))
  putStrLn ("put-put: " ++ show (lawPutPut lx s 9 12))
demoLaws"""

S5_REV_CODE = r"""-- S5b: prism review/re (build, not only preview)
data CPrism s a = CPrism { previewP :: s -> Maybe a, reviewP :: a -> s }

_JustP :: CPrism (Maybe a) a
_JustP = CPrism id Just

_LeftP :: CPrism (Either e a) e
_LeftP = CPrism (\x -> case x of { Left e -> Just e; Right _ -> Nothing }) Left

demoPrism :: IO ()
demoPrism = do
  print (previewP _JustP (Just (5::Int)))             -- Just 5
  print (previewP _JustP (Nothing :: Maybe Int))      -- Nothing
  print (reviewP _JustP (7::Int))                     -- Just 7   (build)
  print (previewP _LeftP (Left "e" :: Either String Int))   -- Just "e"
  print (reviewP _LeftP "boom" :: Either String Int)        -- Left "boom"
  -- prism law: preview . review = Just
  print (previewP _JustP (reviewP _JustP (1::Int)))   -- Just 1
demoPrism"""

S7_MD = r"""## 7️⃣ AffineTraversal (Optional): фокус 0-или-1

**AffineTraversal** (она же `Optional`) фокусируется ровно на **нуле или одном**
элементе. Это недостающее звено решётки: она слабее линзы (фокус может отсутствовать)
и слабее призмы (структура может быть составной), но сильнее обхода (не более одной цели).
Линза = всегда 1 цель; призма = 0/1 цель в сумме; AffineTraversal = 0/1 в любом `s`.
"""

S7_CODE = r"""-- S7: AffineTraversal / Optional (0-or-1 focus)
data Optional s a = Optional { matchO :: s -> Maybe a, setO :: s -> a -> s }

headO :: Optional [a] a
headO = Optional (\xs -> case xs of { (x:_) -> Just x; [] -> Nothing })
                 (\xs v -> case xs of { (_:t) -> v:t; [] -> [] })

overO :: Optional s a -> (a -> a) -> s -> s
overO o f s = case matchO o s of { Just a -> setO o s (f a); Nothing -> s }

demoOpt :: IO ()
demoOpt = do
  print (matchO headO [10,20,30::Int])     -- Just 10
  print (matchO headO ([] :: [Int]))       -- Nothing
  print (overO headO (*100) [1,2,3::Int])  -- [100,2,3]
  print (overO headO (*100) ([] :: [Int])) -- []
demoOpt"""

S9_MD = r"""## 9️⃣ Fold, Getter, Setter

Не все оптики «двунаправленные». Три ограниченные оптики лежат в основании решётки:

- **Getter** `s -> a` — только чтение одного значения;
- **Fold** `s -> [a]` — только чтение нескольких значений;
- **Setter** `(a -> b) -> s -> t` — только запись (модификация).

Lens и Traversal сильнее: из них выводятся и чтение, и запись. Getter/Fold/Setter —
это «половинки», полезные, когда направление одно.
"""

S9_CODE = r"""-- S9: Fold / Getter / Setter
type Getter s a     = s -> a
type Fold s a       = s -> [a]
type Setter s t a b = (a -> b) -> s -> t

toView :: Getter s a -> s -> a
toView g = g
foldOf :: Fold s a -> s -> [a]
foldOf f = f
overS :: Setter s t a b -> (a -> b) -> s -> t
overS s = s

demoFGS :: IO ()
demoFGS = do
  let g   = fst :: Getter (Int,Char) Int
      fld = (\(a,b) -> [a,b]) :: Fold (Int,Int) Int
      st  = map :: Setter [Int] [Int] Int Int
  print (toView g (7,'z'))       -- 7
  print (foldOf fld (3,4))        -- [3,4]
  print (overS st (+1) [1,2,3])   -- [2,3,4]
demoFGS"""

S10_MD = r"""## 1️⃣0️⃣ Индексированные оптики

**Индексированная** оптика проносит сквозь обход позицию/ключ элемента. Это позволяет
действиям зависеть от индекса (как `itraverse`, `imap`): не просто «обойти все», а
«обойти все, зная, где находишься».
"""

S10_CODE = r"""-- S10: indexed optics (traversal carrying an index)
itraverseList :: Applicative f => (Int -> a -> f b) -> [a] -> f [b]
itraverseList f = go 0
  where go _ []     = pure []
        go i (x:xs) = (:) <$> f i x <*> go (i+1) xs

ifoldList :: (Int -> a -> b) -> [a] -> [b]
ifoldList f xs = zipWith f [0..] xs

demoIdx :: IO ()
demoIdx = do
  print (ifoldList (\i x -> (i,x)) "abc")   -- [(0,'a'),(1,'b'),(2,'c')]
  r <- itraverseList (\i x -> do
                        putStrLn (show i ++ " -> " ++ show x)
                        return (x*10)) [4,5,6::Int]
  print r                                    -- [40,50,60]
demoIdx"""

S11_MD = r"""## 1️⃣1️⃣ Контейнерные оптики: Ix, At, Each

Самые «рабочие лошадки» на практике:

- **Ix** — частичный доступ по индексу/ключу (модификация на месте, no-op если нет);
- **At** — фокус на `Maybe v`: позволяет **вставлять и удалять** по ключу;
- **Each** — обход всех элементов контейнера (частный Traversal).
"""

S11_CODE = r"""-- S11: container optics Ix / At / Each (local impls)
ixList :: Int -> (a -> a) -> [a] -> [a]
ixList i f xs = [ if j == i then f x else x | (j,x) <- zip [0..] xs ]

atKey :: Eq k => k -> [(k,v)] -> Maybe v
atKey k = lookup k
setAt :: Eq k => k -> Maybe v -> [(k,v)] -> [(k,v)]
setAt k Nothing  m = filter ((/= k) . fst) m
setAt k (Just v) m = (k,v) : filter ((/= k) . fst) m

eachList :: (a -> b) -> [a] -> [b]
eachList = map

demoCont :: IO ()
demoCont = do
  print (ixList 1 (*100) [1,2,3::Int])                       -- [1,200,3]
  print (atKey "b" [("a",1),("b",2::Int)])                   -- Just 2
  print (setAt "c" (Just 9) [("a",1::Int)])                  -- [("c",9),("a",1)]
  print (setAt "a" Nothing  [("a",1),("b",2::Int)])          -- [("b",2)]
  print (eachList (+1) [10,20::Int])                         -- [11,21]
demoCont"""

S15_MD = r"""## 1️⃣5️⃣ Связь: Lens и комонада Store

Линза — это в точности **коалгебра комонады `Store`**: отображение `s -> Store a s`,
где `Store a s = (a -> s, a)` несёт «текущий фокус» и «способ перезаписать». Законы
комонады `Store` соответствуют законам линзы один-в-один. А сама `Store` возникает из
сопряжения `Store ⊣ State` (см. [Comonads.ipynb](Comonads.ipynb)) — поэтому линзы,
комонады и сопряжения — три грани одной конструкции.
"""

S15_CODE = r"""-- S15: lens as a Store-comonad coalgebra
data Store s a = Store (s -> a) s
posS :: Store s a -> s
posS (Store _ s) = s
peekS :: Store s a -> s -> a
peekS (Store f _) = f

data CLens2 s a = CLens2 { lget :: s -> a, lset :: s -> a -> s }

-- a lens IS a coalgebra  s -> Store a s
lensToStore :: CLens2 s a -> s -> Store a s
lensToStore l s = Store (lset l s) (lget l s)

demoStore :: IO ()
demoStore = do
  let l  = CLens2 fst (\(_,b) a -> (a,b)) :: CLens2 (Int,Char) Int
      st = lensToStore l (1,'x')
  print (posS st)        -- 1          (= get)
  print (peekS st 99)    -- (99,'x')   (= set 99)
demoStore"""

S18_MD = r"""## 1️⃣8️⃣ Практический пример: глубокий апдейт вложенной записи

Классическая боль Haskell — обновить поле глубоко внутри вложенных записей: руками это
гнездо `r { a = (a r) { b = ... } }`. Композиция линз превращает это в **одну строку**:
`over (deptL . headL . salaryL) (+15000) company`.
"""

S18_CODE = r"""-- S18: nested record update via composed VL lenses
:set -XRankNTypes
newtype Id3 a = Id3 { runId3 :: a }
instance Functor Id3 where fmap f (Id3 a) = Id3 (f a)
newtype Const3 r a = Const3 { getConst3 :: r }
instance Functor (Const3 r) where fmap _ (Const3 r) = Const3 r

type Lens3 s a = forall f. Functor f => (a -> f a) -> s -> f s
view3 :: Lens3 s a -> s -> a
view3 l s = getConst3 (l Const3 s)
over3 :: Lens3 s a -> (a -> a) -> s -> s
over3 l f s = runId3 (l (Id3 . f) s)

data Employee = Employee { _salary :: Int }   deriving Show
data Dept     = Dept     { _head   :: Employee } deriving Show
data Company  = Company  { _dept   :: Dept }   deriving Show

salaryL :: Lens3 Employee Int
salaryL f (Employee s) = fmap Employee (f s)
headL :: Lens3 Dept Employee
headL f (Dept h) = fmap Dept (f h)
deptL :: Lens3 Company Dept
deptL f (Company d) = fmap Company (f d)

demoNested :: IO ()
demoNested = do
  let c    = Company (Dept (Employee 100000))
      path = deptL . headL . salaryL
  print (view3 path c)            -- 100000
  print (over3 path (+15000) c)   -- salary raised, structure preserved
demoNested"""

SUMMARY_MD = r"""## 1️⃣9️⃣ Сводка: иерархия оптик

Оптики образуют **решётку по мощности**: чем выше, тем больше можно (читать и писать,
произвольное число целей), чем ниже — тем специализированнее.

![Иерархия оптик](../diagrams/optics/op_hierarchy_poster.svg)

| Оптика | Фокус | Чтение | Запись | Целей | Кодировка (VL/проф.) |
|---|---|---|---|---|---|
| **Iso** | `s` &#8596; `a` | да | да | 1 (обратимо) | `Exchange` / profunctor |
| **Lens** | поле произведения | да | да | ровно 1 | `Strong` |
| **Prism** | ветвь суммы | preview | review | 0 или 1 | `Choice` |
| **AffineTraversal** | 0-или-1 в любом `s` | да (Maybe) | да | 0 или 1 | `Strong`+`Choice` |
| **Traversal** | много значений | да | да | 0..n | `Applicative` |
| **Fold** | много (read-only) | да | нет | 0..n | `Const` |
| **Getter** | одно (read-only) | да | нет | 1 | `Const` |
| **Setter** | модификация | нет | да | 0..n | `Identity` |
| **Grate** | коэкспоненциал | da | да | n | `Closed` |

### Единая картина

Все оптики — это **естественные преобразования** `forall p. C p => p a b -> p s t`,
где класс `C` (Strong, Choice, Applicative, Closed, ...) задаёт *вид* оптики. Поэтому
они компонуются обычной `(.)`, а профункторное представление объединяет их все под одной
сигнатурой. Решётка мощности и профункторная унификация — два взгляда на одно и то же.
"""

# ---------- TARGET ORDER ----------
# tuples: ("keep", id) | ("code", id) | ("ins", cell_dict)
ORDER = [
    ("keep", "b7f3076c"),     # setup code
    ("keep", "d1452bd1"),     # intro (reskeleton later)
    ("keep", "cmp16c0daf1"),  # contents (rebuild later)
    ("keep", "ee4848b0"), ("keep", "73613c1a"),   # 1 Lens get/set
    ("keep", "eac66bac"), ("keep", "622db001"),   # 2 VL
    ("keep", "4fd0b3c1"), ("keep", "fbdca35c"),   # 3 composition
    ("ins", md("opt-s4-md", S4_MD)), ("ins", code("opt-s4-code", S4_CODE)),  # 4 laws
    ("keep", "8453f15d"), ("keep", "46066c05"),   # 5 prism
    ("ins", code("opt-s5rev-code", S5_REV_CODE)), # 5b review/re
    ("keep", "74aa2e15"), ("keep", "e40f0953"),   # 6 iso
    ("ins", md("opt-s7-md", S7_MD)), ("ins", code("opt-s7-code", S7_CODE)),  # 7 affine
    ("keep", "51067c07"), ("keep", "c681bb07"),   # 8 traversal
    ("ins", md("opt-s9-md", S9_MD)), ("ins", code("opt-s9-code", S9_CODE)),  # 9 FGS
    ("ins", md("opt-s10-md", S10_MD)), ("ins", code("opt-s10-code", S10_CODE)),  # 10 indexed
    ("ins", md("opt-s11-md", S11_MD)), ("ins", code("opt-s11-code", S11_CODE)),  # 11 container
    ("keep", "b5e30e1a"),                          # 12 profunctor unification md
    ("fixcode", "20baa427"),                       # was md-with-code -> code
    ("keep", "2093464f"),                          # profunctor optics code
    ("keep", "5fa12c01"), ("keep", "a02158fe"),    # 13 Grate md+code
    ("keep", "4e5812c4"),                          # 14 all optics md
    ("keep", "6f10152c"),                          # hierarchy-via-Applicative code (moved here)
    ("ins", md("opt-s15-md", S15_MD)), ("ins", code("opt-s15-code", S15_CODE)),  # 15 store
    ("keep", "b6e0bcce"),                          # 16 Traversable md
    ("keep", "4b621ada"),                          # 17 libraries md
    ("ins", md("opt-s18-md", S18_MD)), ("ins", code("opt-s18-code", S18_CODE)),  # 18 practical
    ("ins", md("opt-summary", SUMMARY_MD)),        # 19 summary
    ("keep", "nav-footer"),
]
# dropped ids: 65cb0f5e (mid итоги), b4741acb (final итоги), e1ca7e7d (diagram heading), b7481b73 (lone image)

def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    by_id = {c.get("id"): c for c in nb["cells"]}
    new_cells = []
    used = set()
    for kind, *rest in ORDER:
        if kind == "ins":
            new_cells.append(rest[0])
        else:
            cid = rest[0]
            c = by_id.get(cid)
            if c is None:
                print(f"ERROR: missing id {cid}", file=sys.stderr); sys.exit(1)
            if kind == "fixcode" and c["cell_type"] != "code":
                c["cell_type"] = "code"
                c.setdefault("outputs", [])
                c["execution_count"] = None
                c.pop("attachments", None)
            used.add(cid)
            new_cells.append(c)
    nb["cells"] = new_cells
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"rebuilt: {len(new_cells)} cells")

if __name__ == "__main__":
    main()
