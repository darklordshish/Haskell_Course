# Optics.ipynb Expansion + Rework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`).

**Goal:** Expand and restructure `src/notebooks/Optics.ipynb` to the verbose teaching format (Phases 9–10): clean 1–19 section order, 6 new executable sections (laws, review/re, AffineTraversal, Fold/Getter/Setter, indexed, container Ix/At/Each, Lens↔Store, practical example), full skeleton, fixed + new diagrams, 3-channel summary; fix structural bugs (code-in-markdown cell, numbering, duplicate summaries).

**Architecture:** Two passes. Pass 1 reorders/rewrites markdown inline (single voice) and adds new markdown+code cells, one kernel run verifies (ERRORS: 0). Pass 2 fixes existing optics SVGs and adds new ones (agents or manual fallback). Edits via Python patch scripts in container `haskell_course_git-ihaskell-1`.

**Tech Stack:** IHaskell/Jupyter in Docker; Python json patch scripts + `src/scripts/_run.py`, `_lint.py`; SVG canonical style.

---

## Conventions (reuse from Phases 9–10)

- Container mount: `/home/jovyan/src/`; notebooks at `/home/jovyan/src/notebooks/`.
- Patch scripts in `src/scripts/`; run `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/src/scripts/<n>.py`.
- `json.dump(..., ensure_ascii=False, indent=1)`; locate cells by heading prefix.
- Executor: `_run.py Optics.ipynb` → `ERRORS: 0`. Lint: `_lint.py Optics.ipynb`.
- **IHaskell constraints:** keep each new code cell self-contained — define its own `Identity`/`Const`/newtypes locally (the notebook already redefines per cell). No external `lens`/`optics` imports. ASCII in SVG only; markdown may use unicode math but formulas use `$...$`.
- Per-section skeleton: Мотивация → Идея/категорный смысл → Формализм → Код+демо → Пример из жизни → Границы → Мостик.

---

## Task 0: Branch + baseline
- [ ] `git checkout master && git checkout -b phase11-optics-rework`.
- [ ] Baseline `_run.py Optics.ipynb` → record current ERRORS (note: cell 19 code-in-markdown won't execute as code today; that's expected). Expect `ERRORS: 0` for actual code cells.

---

## PASS 1 — PROSE/CODE (Tasks 1–22)

**Restructure note:** the notebook will be rebuilt to the 1–19 order. Strategy: (a) rewrite existing section markdown cells to skeleton in place; (b) insert new markdown+code cells at the right positions; (c) remove duplicate summary cells and fold the code-in-markdown cell. Because reordering by patch script is error-prone, we insert new cells relative to existing anchors and do a final explicit order fix in Task 21.

### Existing-section reskeleton (prose only; keep their code cells)
- [ ] **Task 1:** Section "Линза через геттер/сеттер" → skeleton (motivation: nested update pain; idea: lens = getter+setter pair; laws teased; bridge to VL).
- [ ] **Task 2:** "Линза Ван Лааровена" → skeleton (idea: `forall f. Functor f => (a -> f b) -> s -> f t`; Identity=over, Const=view).
- [ ] **Task 3:** "Композиция линз" → skeleton (lenses compose as plain `(.)`; order reads outside-in).
- [ ] **Task 5 prose:** "Призма" → skeleton; mention preview/review duality (code added Task 12 below).
- [ ] **Task 6:** "Изо" → skeleton (s ≅ a; from/to; every iso is both lens and prism).
- [ ] **Task 8:** "Обход (Traversal)" → skeleton (`forall f. Applicative f => ...`; multiple foci).
- [ ] **Task 12prose:** "Унификация через профункторы" → skeleton (Strong→Lens, Choice→Prism).
- [ ] **Task 13:** "Grate" → skeleton (Closed profunctor; coexponential).
- [ ] **Task 14:** "Все оптики через профунктор-интерфейс" → skeleton.
- [ ] **Task 16:** "Оптики и Traversable" → skeleton.
- [ ] Each: patch script replaces the cell source; commit per small group.

### NEW Section 4 — Lens laws
- [ ] Insert markdown (skeleton) + code cell after Composition section. Code (self-contained):
```haskell
:set -XScopedTypeVariables
data CLens s a = CLens { cget :: s -> a, cset :: s -> a -> s }

data P = P { px :: Int, py :: Int } deriving (Eq, Show)
lx :: CLens P Int
lx = CLens px (\p v -> p { px = v })

lawGetPut :: (Eq s) => CLens s a -> s -> Bool
lawGetPut l s = cset l s (cget l s) == s
lawPutGet :: (Eq a) => CLens s a -> s -> a -> Bool
lawPutGet l s a = cget l (cset l s a) == a
lawPutPut :: (Eq s) => CLens s a -> s -> a -> a -> Bool
lawPutPut l s a b = cset l (cset l s a) b == cset l s b

demoLaws :: IO ()
demoLaws = do
  let s = P 3 4
  putStrLn ("get-put: " ++ show (lawGetPut lx s))
  putStrLn ("put-get: " ++ show (lawPutGet lx s 9))
  putStrLn ("put-put: " ++ show (lawPutPut lx s 9 12))
demoLaws
```
Skeleton boundaries: a getter/setter that violates a law is NOT a lawful lens (e.g. setter with side effects / normalization). Commit.

### NEW Section 5 code — Prism review/re
- [ ] Add code cell after the existing Prism section code:
```haskell
data CPrism s a = CPrism { previewP :: s -> Maybe a, reviewP :: a -> s }

_Just :: CPrism (Maybe a) a
_Just = CPrism id Just

_Left :: CPrism (Either e a) e
_Left = CPrism (either Just (const Nothing)) Left

demoPrism :: IO ()
demoPrism = do
  print (previewP _Just (Just 5))           -- Just 5
  print (previewP _Just (Nothing :: Maybe Int)) -- Nothing
  print (reviewP _Just 7)                    -- Just 7  (build)
  print (previewP _Left (Left "e" :: Either String Int)) -- Just "e"
  print (reviewP _Left "boom" :: Either String Int)      -- Left "boom"
demoPrism
```
Skeleton: prism law `preview . review = Just`; review = smart constructor / parser inverse. Commit.

### NEW Section 7 — AffineTraversal / Optional
- [ ] markdown skeleton + code:
```haskell
data Optional s a = Optional { matchO :: s -> Maybe a, setO :: s -> a -> s }

-- focus on the head of a list: 0-or-1
headO :: Optional [a] a
headO = Optional (\xs -> case xs of { (x:_) -> Just x; [] -> Nothing })
                 (\xs v -> case xs of { (_:t) -> v:t; [] -> [] })

overO :: Optional s a -> (a -> a) -> s -> s
overO o f s = case matchO o s of { Just a -> setO o s (f a); Nothing -> s }

demoOpt :: IO ()
demoOpt = do
  print (matchO headO [10,20,30])      -- Just 10
  print (matchO headO ([] :: [Int]))   -- Nothing
  print (overO headO (*100) [1,2,3])   -- [100,2,3]
  print (overO headO (*100) ([] :: [Int])) -- []
demoOpt
```
Skeleton: AffineTraversal = Lens ∧ Prism in the lattice; exactly 0 or 1 focus; sits below both. Commit.

### NEW Section 9 — Fold / Getter / Setter
- [ ] markdown skeleton + code:
```haskell
type Getter s a   = s -> a
type Fold s a     = s -> [a]
type Setter s t a b = (a -> b) -> s -> t

toView :: Getter s a -> s -> a
toView g = g

foldOf :: Fold s a -> s -> [a]
foldOf f = f

over' :: Setter s t a b -> (a -> b) -> s -> t
over' s = s

demoFGS :: IO ()
demoFGS = do
  let g = fst :: Getter (Int,Char) Int
      fld = (\(a,b) -> [a,b]) :: Fold (Int,Int) Int
      st  = map :: Setter [Int] [Int] Int Int
  print (toView g (7,'z'))         -- 7
  print (foldOf fld (3,4))          -- [3,4]
  print (over' st (+1) [1,2,3])     -- [2,3,4]
demoFGS
```
Skeleton: read-only (Getter/Fold) vs write-only (Setter); where they sit in the hierarchy (most restricted). Commit.

### NEW Section 10 — Indexed optics
- [ ] markdown skeleton + code:
```haskell
itraverseList :: Applicative f => (Int -> a -> f b) -> [a] -> f [b]
itraverseList f = go 0
  where go _ []     = pure []
        go i (x:xs) = (:) <$> f i x <*> go (i+1) xs

-- collect with index using Const-like accumulation via lists
ifoldList :: (Int -> a -> b) -> [a] -> [b]
ifoldList f xs = zipWith f [0..] xs

demoIdx :: IO ()
demoIdx = do
  print (ifoldList (\i x -> (i,x)) "abc")     -- [(0,'a'),(1,'b'),(2,'c')]
  r <- itraverseList (\i x -> do { putStrLn (show i ++ ":" ++ show x); return (x*10) }) [4,5,6]
  print r                                      -- [40,50,60]
demoIdx
```
Skeleton: index carries position/key through the traversal; basis of `itraversed`. Commit.

### NEW Section 11 — Container optics Ix / At / Each
- [ ] markdown skeleton + code:
```haskell
-- Ix: modify element at an index (partial; no-op if absent)
ixList :: Int -> (a -> a) -> [a] -> [a]
ixList i f xs = [ if j == i then f x else x | (j,x) <- zip [0..] xs ]

-- At: insert/delete/lookup by key in an assoc list (Maybe v focus)
atKey :: Eq k => k -> [(k,v)] -> Maybe v
atKey k = lookup k
setAt :: Eq k => k -> Maybe v -> [(k,v)] -> [(k,v)]
setAt k Nothing  m = filter ((/= k) . fst) m
setAt k (Just v) m = (k,v) : filter ((/= k) . fst) m

-- Each: apply to every element
eachList :: (a -> b) -> [a] -> [b]
eachList = map

demoCont :: IO ()
demoCont = do
  print (ixList 1 (*100) [1,2,3])                  -- [1,200,3]
  print (atKey "b" [("a",1),("b",2)])              -- Just 2
  print (setAt "c" (Just 9) [("a",1)])             -- [("c",9),("a",1)]
  print (setAt "a" Nothing  [("a",1),("b",2)])     -- [("b",2)]
  print (eachList (+1) [10,20])                    -- [11,21]
demoCont
```
Skeleton: Ix=partial index, At=Maybe-valued (insert/delete), Each=Traversal over all. Commit.

### NEW Section 15 — Lens ↔ Store comonad
- [ ] markdown skeleton + code:
```haskell
data Store s a = Store (s -> a) s
posS :: Store s a -> s
posS (Store _ s) = s
peekS :: Store s a -> s -> a
peekS (Store f _) = f

data CLens2 s a = CLens2 { lget :: s -> a, lset :: s -> a -> s }

-- a lens IS a coalgebra s -> Store a s
lensToStore :: CLens2 s a -> s -> Store a s
lensToStore l s = Store (lset l s) (lget l s)

-- recover get/set from the Store coalgebra
demoStore :: IO ()
demoStore = do
  let l = CLens2 fst (\(_,b) a -> (a,b)) :: CLens2 (Int,Char) Int
      st = lensToStore l (1,'x')
  print (posS st)            -- 1   (= get)
  print (peekS st 99)        -- (99,'x')  (= set 99)
demoStore
```
Skeleton: lens = Store-coalgebra; comonad laws ⇔ lens laws; `Store ⊣ State` (cross-link to Comonads.ipynb). Commit.

### NEW Section 18 — Practical example (nested update)
- [ ] markdown skeleton + code (uses VL lenses, self-contained):
```haskell
:set -XRankNTypes
newtype I a = I { unI :: a }
instance Functor I where fmap f (I a) = I (f a)
type Lens s a = forall f. Functor f => (a -> f a) -> s -> f s
viewL :: Lens s a -> s -> a
viewL l s = getC (l C s) where { newtype' = () }
```
(Note: during execution, implement `view`/`over` with the notebook's existing Const/Identity pattern; the final code defines `Company/Dept/Employee`, three lenses, and shows `over (deptL . headL . salaryL) (+1000)` and `view` of the nested field. Keep it self-contained and executable; verify in Task 20.)
Skeleton: motivation realized — deep update without optics is nested record-syntax hell; with composed lenses it is one line. Commit.

### Task 19: Intro + Contents
- [ ] Rewrite intro framing (optics = composable accessors; the power lattice Iso ⊃ Lens/Prism ⊃ AffineTraversal ⊃ Traversal ⊃ Fold/Setter; profunctor unification). Rebuild the Contents table to the 1–19 order. Add "как читать" note.

### Task 20: Cleanup structure
- [ ] Fix the code-in-markdown cell (former cell 19): split into markdown + a real code cell (or merge into the adjacent profunctor code cell).
- [ ] Remove the duplicate "Итоги" cell and duplicate hierarchy-diagram cell (keep only the final summary built in Task 21).
- [ ] Ensure all section headings use clean sequential numbers 1–19.

### Task 21: Summary section (3 channels)
- [ ] Replace remaining summary with one `## 1️⃣9️⃣ Сводка: иерархия оптик`:
  - poster ref `../diagrams/optics/op_hierarchy_poster.svg` (Pass 2),
  - table: rows = {Iso, Lens, Prism, AffineTraversal, Traversal, Fold, Getter, Setter, Grate}, columns = Фокус / Может читать? / Может писать? / Сколько целей / Кодировка,
  - narration paragraph (the power lattice + profunctor unification).

### Task 22: Pass-1 verification
- [ ] `_run.py Optics.ipynb` → `ERRORS: 0`.
- [ ] `_lint.py Optics.ipynb` → no `\(...\)`, balanced `$`.
- [ ] Verify section numbering 1–19 unique; no duplicate summaries.
- [ ] commit `test(optics): pass-1 executes clean, structure fixed`.

---

## PASS 2 — VISUAL (Tasks 23–27)

### Task 23: Fix existing optics SVGs
- [ ] `op_optics.svg`, `op_optics_full.svg`: ensure `viewBox`, white bg, no text overflow (reflow long lines as in Phase 10). Validate `[xml]` + non-ASCII=0. Commit.

### Task 24: New SVG — lens laws (commutative squares)
- [ ] `src/diagrams/optics/op_lens_laws.svg` (~660x300): three small commuting squares for get-put, put-get, put-put. ASCII, viewBox, white bg, valid XML. Commit.

### Task 25: New SVG — power lattice with AffineTraversal
- [ ] `src/diagrams/optics/op_lattice.svg` (~640x340): Hasse-style lattice Iso at top → Lens, Prism → AffineTraversal → Traversal → Fold/Getter/Setter at bottom, annotated read/write/#foci. ASCII, viewBox, white bg. Commit.

### Task 26: New SVG — Lens ↔ Store + summary poster
- [ ] `src/diagrams/optics/op_lens_store.svg` (~600x260): `lens : s -> Store a s`, `Store ⊣ State`, laws correspondence.
- [ ] `src/diagrams/optics/op_hierarchy_poster.svg` (~900x460): table poster mirroring the Task 21 table. ASCII, viewBox, white bg. Commit.
- [ ] (If agents unavailable due to API 529, author manually — as in Phase 10.)

### Task 27: Embed new diagrams + final verification + sync
- [ ] Insert image refs into sections 4 (laws), 7 (lattice — or section 19), 15 (store), 19 (poster) after the *Идея* beat.
- [ ] Verify every image ref resolves; no broken `![]`.
- [ ] Final `_run.py Optics.ipynb` → `ERRORS: 0`.
- [ ] README: Optics cells (29 → new count) and SVG (2 → new referenced count); totals (80 → new); ROADMAP Phase 11 section (complete).
- [ ] Cleanup one-off scripts (keep `_run.py`, `_lint.py`). Commit; merge on approval.

---

## Self-Review notes
- 6 new executable sections all carry concrete self-contained Haskell (laws, review/re, Optional, Fold/Getter/Setter, indexed, container, Lens↔Store, practical) — note Section 18 code is finalized during execution against the notebook's Const/Identity pattern and must be verified to run. ✓
- Structural bugs (code-in-markdown, numbering, duplicate summaries) handled in Tasks 20–21. ✓
- Diagrams: fix existing (23) + 4 new (24–26); embed + verify (27). ✓
- Invariant ERRORS: 0 verified at Task 22 and Task 27. ✓
- Cell count grows substantially; README/ROADMAP sync in Task 27 with actual counts. ✓
