#!/usr/bin/env python3
"""Phase 12: fix pre-existing breakage in the Van Laarhoven lens cell (missing
Applicative instances + stray <$> in traverse identity law)."""
import json, sys
PATH = "/home/jovyan/src/notebooks/Toposes.ipynb"

NEW = r"""-- Van Laarhoven lens: форма зависимого типа Mitchell-Benabou
-- Lens s a = forall f. Functor f => (a -> f a) -> s -> f s
-- "forall f" работает благодаря RankNTypes (включён в SETUP)
-- Это "внутренний hom" в категории функторов над топосом Set

type LensT s a = forall f. Functor f => (a -> f a) -> s -> f s

-- Const функтор = "просто прочитать" (заморозить значение)
newtype ConstL r a = ConstL { getConstL :: r } deriving (Show)
instance Functor (ConstL r) where fmap _ (ConstL r) = ConstL r
-- как Applicative (нужно для traverse): накапливаем r в моноиде
instance Monoid r => Applicative (ConstL r) where
  pure _ = ConstL mempty
  ConstL a <*> ConstL b = ConstL (a <> b)

-- Identity функтор = "просто изменить"
newtype IdentityL a = IdentityL { runIdentityL :: a } deriving (Show)
instance Functor IdentityL where fmap f (IdentityL a) = IdentityL (f a)
instance Applicative IdentityL where
  pure = IdentityL
  IdentityL f <*> IdentityL a = IdentityL (f a)

-- view и over через единый тип LensT
viewL :: LensT s a -> s -> a
viewL l s = getConstL (l ConstL s)

overL :: LensT s a -> (a -> a) -> s -> s
overL l f s = runIdentityL (l (IdentityL . f) s)

setL :: LensT s a -> a -> s -> s
setL l x = overL l (const x)

-- Пример: фокус на первом элементе пары
_fstL :: LensT (a, b) a
_fstL f (a, b) = fmap (\a' -> (a', b)) (f a)

-- Пример: фокус на втором элементе
_sndL :: LensT (a, b) b
_sndL f (a, b) = fmap (\b' -> (a, b')) (f b)

-- Traversal = морфизм пучков: traverse сохраняет структуру, меняет значения
-- traverse :: (Traversable t, Applicative f) => (a -> f b) -> t a -> f (t b)
-- Закон: traverse (Identity . id) = Identity (сохранение идентичности)
-- Const-обход = foldMap (сбор значений в моноид)
checkTraverseLaws :: IO ()
checkTraverseLaws = do
  let xs = [1,2,3,4,5] :: [Int]
  -- Закон 1: traverse (Identity . id) = Identity  =>  runIdentityL (...) == xs
  let law1 = runIdentityL (traverse (IdentityL . id) xs) == xs
  -- Const-обход собирает элементы в список (моноид), затем суммируем
  let collected      = getConstL (traverse (\x -> ConstL [x]) xs) :: [Int]
      sumViaTraverse = sum collected
      sumDirect      = sum xs
  putStrLn $ "\x2705 T9 (new): Lens как внутренний язык"
  putStrLn $ "  view _fst (10, 20)    = " ++ show (viewL _fstL (10::Int, 20::Int))
  putStrLn $ "  over _fst (*2) (3,4)  = " ++ show (overL _fstL (*2) (3::Int, 4::Int))
  putStrLn $ "  set  _snd 99  (1,2)   = " ++ show (setL  _sndL 99 (1::Int, 2::Int))
  putStrLn $ "  Traversal law (traverse (Id.id) = id on lists): " ++ show law1
  putStrLn $ "  Const-traverse collects [1..5] => sum = " ++ show sumViaTraverse ++ " == " ++ show sumDirect
  putStrLn   "  Lens = forall f. Functor f => (a->fa)->s->fs"
  putStrLn   "       = внутренний hom в Cat(Functor) = Mitchell-Benabou зависимый тип"

checkTraverseLaws"""

def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "code" and "".join(c["source"]).startswith("-- Van Laarhoven lens"):
            c["source"] = NEW.splitlines(keepends=True)
            c["outputs"] = []
            c["execution_count"] = None
            n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("fixed Van Laarhoven cell")

if __name__ == "__main__":
    main()
