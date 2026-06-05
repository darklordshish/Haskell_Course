import json, os

def md(src):
    return {"cell_type":"markdown","metadata":{},"source":src}

def code(src):
    return {"cell_type":"code","metadata":{},"outputs":[],"execution_count":None,"source":src}

cells = []

# 0: SETUP
cells.append(code(
""":set -XArrows
:set -XTupleSections
:set -XFlexibleInstances
:set -XFlexibleContexts
:set -XInstanceSigs
import Control.Arrow
import Control.Category
import Prelude hiding (id, (.))
putStrLn "Setup done.""""))

# 1: HEADER
cells.append(md(
"""# Arrows in Haskell

**Arrows** (strelki) -- obobshchenie funktsij, monad i profunktorov v odnom interfeise.
Strelka `arr a b` -- eto vychislenie, preobrazuyushchee `a` v `b`, no bolee moshchnoe
chem prostaya funktsiya: so sostoyaniem, vetvleniem, obratnoy svyaz\'yu.

> Hughes (2000): *"Generalising Monads to Arrows"* -- strelki pozvolyayut abstragirovat'
> bol\'she vychislitel\'nykh patternov, chem monady."""))

# 2: TOC
cells.append(md(
"""## Contents

| # | Section | Key idea |
|---|---------|----------|
| 1 | Category: the base | id and (.) for any morphisms |
| 2 | Arrow: lifting and parallelism | arr, first, (***), (\&\&\&) |
| 3 | ArrowChoice: branching | left, right, (+++), (|||) |
| 4 | ArrowLoop: feedback | loop -- traced monoidal |
| 5 | ArrowApply: first class | app -- equivalent to Monad |
| 6 | Kleisli: Monad => Arrow | Monad m => Arrow (Kleisli m) |
| 7 | Practical examples | parser, validation, pipeline |
| 8 | Categorical view | monoidal categories, traced |"""))

# 3: Section 1
cells.append(md(
"""---

## 1. Category: the foundation

### Definition

```haskell
class Category arr where
  id  :: arr a a
  (.) :: arr b c -> arr a b -> arr a c
```

Laws (same as for functions):
- **left identity:** `id . f = f`
- **right identity:** `f . id = f`
- **associativity:** `(f . g) . h = f . (g . h)`

### Instances

| Type | What a morphism is |
|------|--------------------|
| `(->)` | ordinary functions |
| `Kleisli m` | monadic functions `a -> m b` |
| `Star f` | `a -> f b` (from profunctors) |

### Categorical view

`Category` is literally a mathematical category in Haskell:
objects = types, morphisms = arrows `arr a b`, composition = `(.)`."""))

# 4: Code - Category
cells.append(code(
"""-- Category instance for (->) is built-in
-- Verify the laws

f :: Int -> Int
f x = x + 1

g :: Int -> Int
g x = x * 2

-- Left identity: id . f = f
test1 :: Bool
test1 = (id . f) 5 == f 5

-- Right identity: f . id = f
test2 :: Bool
test2 = (f . id) 5 == f 5

-- Associativity
h :: Int -> String
h x = show x

test3 :: Bool
test3 = ((h . f) . g) 3 == (h . (f . g)) 3

print (test1, test2, test3)  -- (True, True, True)"""))

# 5: Section 2 - Arrow
cells.append(md(
"""---

## 2. Arrow: lifting and parallelism

### Definition

```haskell
class Category arr => Arrow arr where
  arr   :: (a -> b) -> arr a b           -- lift a pure function
  first :: arr a b  -> arr (a,c) (b,c)   -- apply to left of pair
```

Derived combinators (defined via `first`):

```haskell
second :: Arrow arr => arr a b -> arr (c,a) (c,b)
second f = arr swap >>> first f >>> arr swap

(***) :: Arrow arr => arr a b -> arr c d -> arr (a,c) (b,d)
f *** g = first f >>> second g

(&&&) :: Arrow arr => arr a b -> arr a c -> arr a (b,c)
f &&& g = arr (\\x -> (x,x)) >>> (f *** g)
```

### Categorical view

`(***)` is the tensor product of a monoidal category.
The pair `(Arrow, (***))` forms a **monoidal category** with unit `()`.

![Arrow dataflow combinators](../diagrams/arrows/arr_dataflow.svg)"""))

# 6: Code - Arrow
cells.append(code(
"""-- arr lifts pure functions into arrows ((->) instance)
double :: Int -> Int
double = (*2)

addOne :: Int -> Int
addOne = (+1)

-- (>>>) sequential composition
pipeline :: Int -> Int
pipeline = arr double >>> arr addOne

-- (***) parallel on pairs: double fst, addOne snd
bothOps :: (Int, Int) -> (Int, Int)
bothOps = arr double *** arr addOne

-- (&&&) fan-out: apply both to same input
forkOps :: Int -> (Int, Int)
forkOps = arr double &&& arr addOne

print (pipeline 5)        -- 11
print (bothOps (3, 7))    -- (6, 8)
print (forkOps 10)        -- (20, 11)"""))

# 7: Section 3 - ArrowChoice
cells.append(md(
"""---

## 3. ArrowChoice: branching via Either

### Definition

```haskell
class Arrow arr => ArrowChoice arr where
  left  :: arr a b -> arr (Either a c) (Either b c)
  right :: arr a b -> arr (Either c a) (Either c b)

  (+++) :: arr a b -> arr c d -> arr (Either a c) (Either b d)
  (|||) :: arr a c -> arr b c -> arr (Either a b) c
```

### Comparison with `(***)`

| Combinator | Structure | Semantics |
|-----------|-----------|-----------|
| `(***)` | pair `(a,b)` | parallel, both inputs always |
| `(+++)` | `Either a b` | choice, only one path taken |
| `(&&&)` | duplicate input | fanout, split once |
| `(|||)` | `Either a b -> c` | merge, one output |

### Categorical view

`ArrowChoice` + `Arrow` = **bicartesian monoidal category**:
products via `(***)`, coproducts via `(+++)`."""))

# 8: Code - ArrowChoice
cells.append(code(
"""routeEvenOdd :: Int -> Either Int Int
routeEvenOdd n = if even n then Left n else Right n

processEven :: Int -> String
processEven n = "even: " ++ show (n `div` d)
  where d = 2

processOdd :: Int -> String
processOdd n  = "odd:  " ++ show (n * 3 + 1)

-- (+++) applies different arrows to each side
processChoice :: Either Int Int -> Either String String
processChoice = arr processEven +++ arr processOdd

-- (|||) merges both branches
processAny :: Either Int Int -> String
processAny = arr processEven ||| arr processOdd

classifyAndProcess :: Int -> String
classifyAndProcess = arr routeEvenOdd >>> processAny

mapM_ (putStrLn . classifyAndProcess) [1..6]"""))

# 9: Section 4 - ArrowLoop
cells.append(md(
"""---

## 4. ArrowLoop: feedback (traced monoidal)

### Definition

```haskell
class Arrow arr => ArrowLoop arr where
  loop :: arr (a, c) (b, c) -> arr a b
```

`c` is internal state fed back from output to input.
Requirement: `c` must be produced lazily.

### Categorical view

`ArrowLoop` corresponds to a **traced monoidal category**:
operation `trace :: (A x C -> B x C) -> (A -> B)` "loops" cable C back.
Formal basis for cycles, counters, recursive circuits."""))

# 10: Code - ArrowLoop
cells.append(code(
"""import Data.List (unfoldr)

-- Running sum via loop state
runningSum :: [Int] -> [Int]
runningSum xs = scanl1 (+) xs

-- Fibonacci via unfoldr (loop pattern)
fibList :: [Integer]
fibList = unfoldr (\(a,b) -> Just (a, (b, a+b))) (0, 1)

-- loop on (->) instance: stateful counter
-- loop :: ((a,c) -> (b,c)) -> a -> b
counterFrom :: Int -> [Int]
counterFrom n = loop go n
  where
    go :: (Int, [Int]) -> ([Int], [Int])
    go (start, _) = let xs = [start..start+4] in (xs, xs)

print (runningSum [1,2,3,4,5])   -- [1,3,6,10,15]
print (take 10 fibList)           -- [0,1,1,2,3,5,8,13,21,34]
print (counterFrom 3)             -- [3,4,5,6,7]"""))

# 11: Section 5 - ArrowApply
cells.append(md(
"""---

## 5. ArrowApply: first-class arrows

### Definition

```haskell
class Arrow arr => ArrowApply arr where
  app :: arr (arr a b, a) b
```

`app` takes an arrow as data and applies it -- arrows become first-class values.

### Key theorem

```
ArrowApply  <=>  Monad
```

- Every `Monad` gives `ArrowApply` via `Kleisli`
- Every `ArrowApply` is equivalent to a monad

### Why this matters

Plain `Arrow` is stricter than `Monad`: arrows cannot dynamically choose
the next arrow based on intermediate values.
`ArrowApply` removes this restriction, but loses static analysis guarantees."""))

# 12: Code - ArrowApply
cells.append(code(
"""-- ArrowApply for (->) is uncurry ($)
-- Demonstrating Monad <=> ArrowApply equivalence

monadStyle :: Maybe Int
monadStyle = do
  x <- Just 5
  y <- Just (x * 2)
  return (x + y)

-- Kleisli arrow style (same computation, structural)
arrowStyle :: Maybe Int
arrowStyle = runKleisli pipeline3 5
  where
    pipeline3 =
      Kleisli (\x -> Just (x, x * 2)) >>>
      arr (\(a,b) -> a + b) >>>
      Kleisli Just

print monadStyle  -- Just 15
print arrowStyle  -- Just 15"""))

# 13: Section 6 - Kleisli
cells.append(md(
"""---

## 6. Kleisli: every Monad gives an Arrow

### The construction

For any monad `m`, there is a canonical `Arrow` instance:

```haskell
newtype Kleisli m a b = Kleisli { runKleisli :: a -> m b }

instance Monad m => Category (Kleisli m) where
  id              = Kleisli return
  Kleisli f . Kleisli g = Kleisli (g >=> f)

instance Monad m => Arrow (Kleisli m) where
  arr f               = Kleisli (return . f)
  first (Kleisli f)   = Kleisli (\\(a,c) -> f a >>= \\b -> return (b,c))
```

### Correspondence table

| Monad operation | Arrow operation |
|----------------|----------------|
| `return` | `arr id` |
| `>>=` | `>>>` (essentially) |
| `>=>` | `.` (Kleisli composition) |
| `liftM` | `arr` |
| `join` | `app` (for ArrowApply) |

### Categorical view

The Kleisli category `Kl(m)`: objects = Haskell types,
morphisms `a -> b` in `Kl(m)` = `a -> m b` in Hask.
The monad's `unit` and `join` become `id` and `(.)`.

![Kleisli construction: Monad gives Arrow](../diagrams/arrows/arr_kleisli.svg)"""))

# 14: Code - Kleisli
cells.append(code(
"""-- Kleisli arrows for Maybe monad
safeDiv :: Int -> Kleisli Maybe Int Int
safeDiv d = Kleisli (\n -> if d == 0 then Nothing else Just (n `div` d))

safeSqrt :: Kleisli Maybe Int Double
safeSqrt = Kleisli (\n -> if n < 0 then Nothing else Just (sqrt (fromIntegral n)))

-- Compose with >>>
pipeline2 :: Kleisli Maybe Int Double
pipeline2 = safeDiv 2 >>> safeSqrt

test :: [Maybe Double]
test = map (runKleisli pipeline2) [100, 0, -4, 49]

-- Kleisli for [] (nondeterminism)
expand :: Kleisli [] Int Int
expand = Kleisli (\n -> [n-1, n, n+1])

expand2 :: Kleisli [] Int Int
expand2 = expand >>> expand

listResult :: [Int]
listResult = runKleisli expand2 0

print test        -- [Just 7.07..., Nothing, Nothing, Just 3.5]
print listResult  -- [-2,-1,0,-1,0,1,0,1,2]"""))

# 15: Section 7 - Practical
cells.append(md(
"""---

## 7. Practical examples: pipeline, validation

### Classical vs arrow style

```haskell
-- Classical (chained functions)
process :: String -> Either String Int
process s = parseNum s >>= validatePositive >>= (Right . transform)

-- Arrow style (structural, statically inspectable)
processA :: String -> Either String Int
processA = runKleisli $
  Kleisli parseNum >>>
  Kleisli validatePositive >>>
  arr transform
```

The arrow pipeline can be traversed, visualized, optimized -- without running it.
The monad version only reveals its structure at runtime."""))

# 16: Code - practical
cells.append(code(
"""parseNum :: String -> Either String Int
parseNum s = case reads s of
  [(n,"")] -> Right n
  _        -> Left ("parse error: " ++ s)

validatePositive :: Int -> Either String Int
validatePositive n
  | n > 0     = Right n
  | otherwise = Left ("must be positive, got: " ++ show n)

doubleIt :: Int -> Int
doubleIt = (*2)

processKleisli :: Kleisli (Either String) String Int
processKleisli =
  Kleisli parseNum >>>
  Kleisli validatePositive >>>
  arr doubleIt

inputs :: [String]
inputs = ["42", "abc", "-5", "7"]

mapM_ (print . runKleisli processKleisli) inputs
-- Right 84
-- Left "parse error: abc"
-- Left "must be positive, got: -5"
-- Right 14"""))

# 17: Section 8 - Categorical
cells.append(md(
"""---

## 8. Categorical view

### Arrow hierarchy

```
           Category
               |
            Arrow              -- monoidal category
           /   |    \\
  ArrowChoice  |   ArrowLoop   -- bicartesian + traced
              \\|/
           ArrowApply           -- equivalent to Monad
```

### Arrow as monoidal category

`Arrow` with `(***)` forms a **strict monoidal category**:
- Tensor product: `(***)` on morphisms, `(,)` on objects
- Unit: `()`
- Tensor laws: `first (f >>> g) = first f >>> first g`

### ArrowLoop = Traced monoidal category

`ArrowLoop` adds the trace operation:
```
trace_C (f : A x C -> B x C) : A -> B
```
Enables modeling of cyclic circuits, counters, recursive feedback.

### Connection to profunctors

An `Arrow arr` is a `Strong` profunctor with extra structure:
- `arr f` lifts pure morphisms (like `rmap`)
- `first` = applying to left of pair (Strong)
- `ArrowApply` adds closedness (similar to `Closed` profunctor)

![Arrow class hierarchy](../diagrams/arrows/arr_hierarchy.svg)"""))

# 18: Code - laws
cells.append(code(
"""-- Verify arrow laws

-- law: arr (f . g) = arr f . arr g
law1_left :: Int -> String
law1_left = arr (show . (+1))

law1_right :: Int -> String
law1_right = arr (+1) >>> arr show

test_law1 :: Bool
test_law1 = map law1_left [1..5] == map law1_right [1..5]

-- law: first (arr f) = arr (first f)  (where first for (->) is (***id))
law2_left :: (Int, String) -> (Int, String)
law2_left = first (arr (+1))

law2_right :: (Int, String) -> (Int, String)
law2_right = arr (\(a,b) -> (a+1, b))

test_law2 :: Bool
test_law2 = map law2_left [(1,"a"),(2,"b")] == map law2_right [(1,"a"),(2,"b")]

print (test_law1, test_law2)  -- (True, True)"""))

# 19: Summary
cells.append(md(
"""---

## Summary

### Arrow hierarchy

| Class | Key operations | Categorical meaning |
|-------|---------------|---------------------|
| `Category` | `id`, `(.)` | Category |
| `Arrow` | `arr`, `first`, `(***)`, `(&&&)` | Monoidal category |
| `ArrowChoice` | `left`, `(+++)`, `(|||)` | Bicartesian monoidal |
| `ArrowLoop` | `loop` | Traced monoidal category |
| `ArrowApply` | `app` | Equivalent to Monad |

### When to use arrows

- **Arrows over monads**: when computation structure should be statically analyzable
- **Monads over arrows**: when dynamic data-dependent branching is needed
- **Kleisli**: universal bridge -- every monad automatically gives an arrow

### Connections

- [Monads](Monads.ipynb) -- every monad gives a Kleisli arrow
- [Profunctors](Profunctors.ipynb) -- Arrow is a Strong profunctor with extra structure
- [Adjunctions](Adjunctions.ipynb) -- Kleisli category and adjunction algebra
- [FunctorHierarchy](FunctorHierarchy.ipynb) -- arrows as alternative effect organization"""))

# 20: NAV
cells.append(md(
"""
---
**<- Previous:** [GPUHaskell](GPUHaskell.ipynb)  |  **Next ->** *(in development)*"""))

nb = {
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "kernelspec": {"display_name": "Haskell", "language": "haskell", "name": "haskell"},
    "language_info": {"name": "haskell"}
  },
  "cells": cells
}

path = "/home/jovyan/src/notebooks/Arrows.ipynb"
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("DONE cells=" + str(len(cells)) + " size=" + str(os.path.getsize(path)))
