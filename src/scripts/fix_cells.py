import json

nb_path = '/home/jovyan/src/notebooks/ComonadTransformers.ipynb'
nb = json.load(open(nb_path))

# Fix cell 18: StoreWithState - can't partially apply Store (it's a type synonym)
# Replace problematic type synonym with a newtype wrapper
new_cell18 = (
"-- Pattern 1: ComonadT over a Monad\n"
"-- EnvT Config IO: IO inside, EnvT outside\n"
"-- We have a fixed Config AND can do IO effects\n"
"type Config = String\n"
"\n"
"explainCombo :: IO ()\n"
"explainCombo = do\n"
'  putStrLn "EnvT Config IO a:"\n'
'  putStrLn "  extract: get IO action (runs effects)"\n'
'  putStrLn "  askEnv:  read config (comonadic)"\n'
'  putStrLn ""\n'
'  putStrLn "StateT s (Store s) a:"\n'
'  putStrLn "  Store provides READ context (observe surroundings)"\n'
'  putStrLn "  State provides WRITE effects (update state, do IO)"\n'
'  putStrLn ""\n'
'  putStrLn "Order: outer = global, inner = local"\n'
"explainCombo\n"
"\n"
"-- Pattern 2: MonadT over a Comonad (conceptual demo)\n"
"import Control.Monad.Trans.State (StateT, runStateT, get, put)\n"
"\n"
"-- Store-based grid with stateful navigation\n"
"-- StateT Int (StoreT Int Id) Bool\n"
"-- Store provides: read cell value at any position\n"
"-- State provides: track/update current position\n"
"\n"
"-- Demo: navigate a 1D grid using State for position tracking\n"
"navDemo :: IO ()\n"
"navDemo = do\n"
'  putStrLn "Pattern 2: StateT over StoreT"\n'
"  let grid = StoreT (Id (\\p -> p `elem` [1,3,5])) (0 :: Int)  -- odd positions live\n"
"  -- Run a stateful navigation on the grid\n"
"  let navAction = do\n"
"        put (3 :: Int)   -- navigate to position 3\n"
"        s <- get\n"
"        return s\n"
"  let (finalPos, _) = extract (runStateT navAction 0)\n"
"  putStrLn $ \"Navigated to: \" ++ show finalPos\n"
"  putStrLn $ \"Cell alive: \" ++ show (peek finalPos grid)\n"
"navDemo"
)

# Fix cell 20: Lens - view function conflicts with Prelude
# The problem is 'extract (ln s)' where ln :: Lens s a = s -> Store a s
# Store a s means 'a' is the value type, but StoreT s w a has value type 'a'
# Our Store s a = StoreT s Id a, so Store Int Bool means focus=Int, value=Bool
# Lens s a = s -> Store a s  means: given s, get Store focused on 'a' in 's'
# So fstLens :: Lens (a,b) a = (a,b) -> Store a (a,b) = StoreT a Id (a,b)
# That means StoreT (Id f) x where f :: a -> (a,b) and x :: a

new_cell20 = (
"-- Store s a = (s -> a, s): this IS the definition of a Lens!\n"
"-- Lens: s -> Store a s  (focus on 'a' inside 's')\n"
"-- Store a s = StoreT a Id s: position=a, value=s\n"
"\n"
"-- Simple lens type using Store\n"
"type Lens' s a = s -> StoreT a Id s\n"
"\n"
"-- Lens for first element of a pair\n"
"fstLens :: Lens' (a, b) a\n"
"fstLens (x, y) = StoreT (Id (\\x' -> (x', y))) x\n"
"\n"
"-- view: get the focused value\n"
"viewLens :: Lens' s a -> s -> a\n"
"viewLens ln s = pos (ln s)\n"
"\n"
"-- set: set the focused value  \n"
"setLens :: Lens' s a -> a -> s -> s\n"
"setLens ln a s = peek a (ln s)\n"
"\n"
"-- over: modify the focused value\n"
"overLens :: Lens' s a -> (a -> a) -> s -> s\n"
"overLens ln f s = setLens ln (f (viewLens ln s)) s\n"
"\n"
"demonstrateLens :: IO ()\n"
"demonstrateLens = do\n"
"  let pair = (42 :: Int, \"hello\")\n"
"  putStrLn $ \"Focus (fst): \" ++ show (viewLens fstLens pair)\n"
"  putStrLn $ \"Set to 100: \" ++ show (setLens fstLens 100 pair)\n"
"  putStrLn $ \"Add 1: \" ++ show (overLens fstLens (+1) pair)\n"
"  -- extend: apply to all positions comonadically\n"
"  let store = fstLens pair  -- StoreT focused on 42\n"
"  let store' = extend (\\w -> peek (pos w + 1) w) store\n"
"  putStrLn $ \"After +1 (fst): \" ++ show (pos store')\n"
"demonstrateLens"
)

nb['cells'][18]['source'] = new_cell18
nb['cells'][20]['source'] = new_cell20

with open(nb_path, 'w', encoding='utf-8') as f:
  json.dump(nb, f, ensure_ascii=True, indent=1)

print(f"Fixed cells 18 and 20. Total cells: {len(nb['cells'])}")
