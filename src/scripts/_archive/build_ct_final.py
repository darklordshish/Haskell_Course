import json, os

BASE = '/home/jovyan/src'
nb_path = os.path.join(BASE, 'notebooks', 'ComonadTransformers.ipynb')

def md(src): return {"cell_type":"markdown","metadata":{},"source":src}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src}

cells = []

# =================== CELL 0: SETUP ===================
cells.append(code(
":set -XRankNTypes\n"
":set -XScopedTypeVariables\n"
":set -XFlexibleContexts\n"
":set -XFlexibleInstances\n"
":set -XMultiParamTypeClasses\n"
":set -XDeriveFunctor\n"
"putStrLn \"Setup done.\""
))

# =================== CELL 1: HEADER ===================
cells.append(md(
"# \u2b50 \u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u044b \u043a\u043e\u043c\u043e\u043d\u0430\u0434 \u0432 Haskell\n\n"
"\u0414\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430, \u043f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043f\u0430\u0442\u0442\u0435\u0440\u043d\u044b \u0438 \u043a\u043e\u043c\u0431\u0438\u043d\u0430\u0446\u0438\u044f \u0441 \u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u0430\u043c\u0438 \u043c\u043e\u043d\u0430\u0434\n\n"
"> \"\u041c\u043e\u043d\u0430\u0434\u044b \u043f\u0438\u0448\u0443\u0442 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b. \u041a\u043e\u043c\u043e\u043d\u0430\u0434\u044b \u043d\u0430\u0431\u043b\u044e\u0434\u0430\u044e\u0442 \u0437\u0430 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430\u043c\u0438. \u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u044b \u043a\u043e\u043c\u043e\u043d\u0430\u0434 \u2014 \u044d\u0442\u043e \u043b\u0438\u043d\u0437\u044b, \u0432\u0441\u0442\u0440\u043e\u0435\u043d\u043d\u044b\u0435 \u0432 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 \u0434\u0440\u0443\u0433 \u0434\u0440\u0443\u0433\u0430.\"\n"
))

# =================== CELL 2: TOC ===================
cells.append(md(
"\u2764 \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435\n\n"
"| # | \u0422\u0435\u043c\u0430 | \u0421\u0443\u0442\u044c |\n"
"|---|------|------|\n"
"| 1 | \u041c\u043e\u0442\u0438\u0432\u0430\u0446\u0438\u044f | \u041f\u0440\u043e\u0431\u043b\u0435\u043c\u0430 \u043a\u043e\u043c\u0431\u0438\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043a\u043e\u043c\u043e\u043d\u0430\u0434 |\n"
"| 2 | \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u043d\u043e\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 ComonadTrans | \u0414\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c MonadTrans |\n"
"| 3 | EnvT | \u0414\u0443\u0430\u043b ReaderT |\n"
"| 4 | StoreT | \u0414\u0443\u0430\u043b StateT, \u043e\u0441\u043d\u043e\u0432\u0430 Lens |\n"
"| 5 | TracedT | \u0414\u0443\u0430\u043b WriterT |\n"
"| 6 | \u0421\u0442\u0435\u043a\u0438 \u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u043e\u0432 | \u041d\u0430\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u0438 \u043e\u0440\u0434\u0435\u0440 |\n"
"| 7 | \u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043f\u0440\u0438\u043c\u0435\u0440\u044b | \u0426\u0435\u043b\u043b\u044e\u043b\u044f\u0440\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442, UI |\n"
"| 8 | \u041a\u043e\u043c\u0431\u0438\u043d\u0430\u0446\u0438\u044f ComonadT + MonadT | \u041f\u043e\u0440\u044f\u0434\u043e\u043a \u043a\u043e\u043c\u043f\u043e\u0437\u0438\u0446\u0438\u0438 |\n"
"| 9 | \u0421\u0432\u044f\u0437\u044c \u0441 Adjunctions, Lens | \u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043f\u043e\u0434\u043b\u043e\u0436\u043a\u0430 |\n"
))

# =================== CELLS 3-4: Section 1 - Motivation ===================
cells.append(md(
"## 1\ufe0f\u20e3 \u041c\u043e\u0442\u0438\u0432\u0430\u0446\u0438\u044f\n\n"
"\u041a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u0438\u043d\u043a\u0430\u043f\u0441\u0443\u043b\u0438\u0440\u0443\u0435\u0442 \u043e\u0434\u0438\u043d \u044d\u0444\u0444\u0435\u043a\u0442 \u043d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u044f. "
"\u0420\u0435\u0430\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u0434\u0430\u0447\u0438 \u0442\u0440\u0435\u0431\u0443\u044e\u0442 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u0432 \u043e\u0434\u043d\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e.\n\n"
"\u041f\u0440\u0438\u043c\u0435\u0440: \u044f\u0447\u0435\u0439\u043a\u0430 \u0446\u0435\u043b\u043b\u044e\u043b\u044f\u0440\u043d\u043e\u0433\u043e \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0430 \u0437\u043d\u0430\u0435\u0442 \u0441\u0432\u043e\u0438\u0445 \u0441\u043e\u0441\u0435\u0434\u0435\u0439 (Store) "
"\u0418 \u0438\u043c\u0435\u0435\u0442 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u0439 (Env).\n\n"
"### \u0414\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c: Monad \u2194 Comonad\n\n"
"| Monad | Comonad |\n"
"|-------|----------|\n"
"| `return :: a -> m a` | `extract :: w a -> a` |\n"
"| `(>>=) :: m a -> (a -> m b) -> m b` | `extend :: (w a -> b) -> w a -> w b` |\n"
"| `MonadTrans: lift :: m a -> t m a` | `ComonadTrans: lower :: t w a -> w a` |\n"
))

cells.append(code(
"-- Comonad: dual of Monad (defined manually, no comonad package needed)\n"
"class Functor w => Comonad w where\n"
"  extract   :: w a -> a\n"
"  duplicate :: w a -> w (w a)\n"
"  extend    :: (w a -> b) -> w a -> w b\n"
"  extend f  = fmap f . duplicate\n"
"  duplicate = extend id\n"
"\n"
"-- ComonadTrans: dual of MonadTrans\n"
"class ComonadTrans t where\n"
"  lower :: Comonad w => t w a -> w a\n"
"\n"
"putStrLn \"MonadTrans:   lift  -- injects effect into stack\"\n"
"putStrLn \"ComonadTrans: lower -- projects context from stack\""
))

print(f"cells 0-4 done: {len(cells)}")

# =================== CELLS 5-6: Section 2 - Categorical definition ===================
cells.append(md(
"## 2\ufe0f\u20e3 \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u043d\u043e\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 ComonadTrans\n\n"
"\u041a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u2014 \u0442\u0440\u043e\u0439\u043a\u0430 (W, \u03b5, \u03b4): \u044d\u043d\u0434\u043e\u0444\u0443\u043d\u043a\u0442\u043e\u0440, \u03b5=extract, \u03b4=duplicate.\n\n"
"\u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440 t: \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u043a\u043e\u043c\u043e\u043d\u0430\u0434 \u0432 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u044b \u0441 `lower`.\n\n"
"**\u0414\u0443\u0430\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u043a\u043e\u043d\u044b ComonadTrans:**\n"
"- `extract . lower = extract`\n"
"- `lower . duplicate = duplicate . lower` (\u043d\u0430\u0442\u0443\u0440\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c)\n\n"
"![ComonadTrans vs MonadTrans](ct_diagram.svg)\n"
))

cells.append(code(
"-- Simple Identity-like comonad for testing\n"
"newtype Id a = Id { runId :: a } deriving (Functor, Show)\n"
"\n"
"instance Comonad Id where\n"
"  extract (Id a) = a\n"
"  duplicate w@(Id _) = Id w\n"
"\n"
"-- EnvT laws test (using Id as base comonad)\n"
"-- EnvT e w a = (e, w a)\n"
"newtype EnvT e w a = EnvT (e, w a) deriving (Functor)\n"
"\n"
"instance Comonad w => Comonad (EnvT e w) where\n"
"  extract (EnvT (_, wa)) = extract wa\n"
"  duplicate w@(EnvT (e, wa)) = EnvT (e, extend (\\wa' -> EnvT (e, wa')) wa)\n"
"\n"
"instance ComonadTrans (EnvT e) where\n"
"  lower (EnvT (_, wa)) = wa\n"
"\n"
"askEnv :: EnvT e w a -> e\n"
"askEnv (EnvT (e, _)) = e\n"
"\n"
"-- Law 1: extract . lower = extract\n"
"let w1 = EnvT (\"cfg\", Id 42) :: EnvT String Id Int\n"
"let lhs1 = (extract . lower) w1\n"
"let rhs1 = extract w1\n"
"putStrLn $ \"Law 1 (extract.lower = extract): \" ++ show (lhs1 == rhs1)\n"
"putStrLn $ \"extract = \" ++ show lhs1"
))

# =================== CELLS 7-8: Section 3 - EnvT ===================
cells.append(md(
"## 3\ufe0f\u20e3 EnvT \u2014 \u0441\u0440\u0435\u0434\u0430 \u0441 \u0444\u043e\u043a\u0443\u0441\u043e\u043c\n\n"
"`EnvT e w a ~ (e, w a)` \u2014 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442 \u043d\u0435\u0438\u0437\u043c\u0435\u043d\u044f\u044e\u0449\u0443\u044e\u0441\u044f \u0441\u0440\u0435\u0434\u0443 \u043b\u044e\u0431\u043e\u0439 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0435.\n\n"
"**\u0414\u0443\u0430\u043b\u044c**: ReaderT\n\n"
"| \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f | EnvT | ReaderT |\n"
"|-----------|---------|----------|\n"
"| \u0427\u0442\u0435\u043d\u0438\u0435 \u0441\u0440\u0435\u0434\u044b | `askEnv` | `ask` |\n"
"| \u0427\u0442\u0435\u043d\u0438\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f | `extract` | `runReader r` |\n"
"| \u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f | `lower` | `lift` |\n\n"
"**\u041f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435**: \u0442\u0435\u043c\u044b UI, \u0433\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f\n"
))

cells.append(code(
"-- EnvT adds an immutable environment e on top of comonad w\n"
"-- (already defined in cell 2, reuse here)\n"
"\n"
"-- Example: UI components with a global theme\n"
"type Theme = String\n"
"type UIComp a = EnvT Theme Id a\n"
"\n"
"uiButton :: UIComp String\n"
"uiButton = EnvT (\"dark\", Id \"<button>\")\n"
"\n"
"uiInput :: UIComp String\n"
"uiInput = EnvT (\"dark\", Id \"<input>\")\n"
"\n"
"-- extend: apply function that uses both theme and value\n"
"renderWithTheme :: UIComp String -> String\n"
"renderWithTheme w = \"[\" ++ askEnv w ++ \"] \" ++ extract (lower w)\n"
"\n"
"demoEnvT :: IO ()\n"
"demoEnvT = do\n"
"  putStrLn $ \"Theme: \" ++ askEnv uiButton\n"
"  putStrLn $ \"Rendered button: \" ++ renderWithTheme uiButton\n"
"  putStrLn $ \"Rendered input:  \" ++ renderWithTheme uiInput\n"
"  -- switch theme: create new EnvT with different env\n"
"  let lightButton = EnvT (\"light\", lower uiButton) :: UIComp String\n"
"  putStrLn $ \"Light theme: \" ++ renderWithTheme lightButton\n"
"demoEnvT"
))

print(f"cells 5-8 added: {len(cells)}")

# =================== CELLS 9-10: Section 4 - StoreT ===================
cells.append(md(
"## 4\ufe0f\u20e3 StoreT \u2014 \u0445\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435 \u0441 \u0444\u043e\u043a\u0443\u0441\u043e\u043c\n\n"
"`StoreT s w a ~ w (s -> a), s` \u2014 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u0441 \u0444\u0443\u043d\u043a\u0446\u0438\u0435\u0439 \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430 \u0438 \u0442\u0435\u043a\u0443\u0449\u0435\u0439 \u043f\u043e\u0437\u0438\u0446\u0438\u0435\u0439.\n\n"
"**\u0414\u0443\u0430\u043b\u044c**: StateT\n\n"
"| \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f | StoreT | StateT |\n"
"|-----------|---------|--------|\n"
"| `pos` | \u0442\u0435\u043a\u0443\u0449\u0430\u044f \u043f\u043e\u0437\u0438\u0446\u0438\u044f | \u0442\u0435\u043a\u0443\u0449\u0435\u0435 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 |\n"
"| `peek s` | \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u044e s | `get` |\n"
"| `seek s` | \u0434\u0432\u0438\u0436\u0435\u043d\u0438\u0435 \u0444\u043e\u043a\u0443\u0441\u0430 | `put s` |\n\n"
"**\u041e\u0441\u043d\u043e\u0432\u0430 Lens**: Store - \u044d\u0442\u043e \u043f\u0440\u043e\u0441\u0442\u0435\u0439\u0448\u0430\u044f \u043c\u043e\u0434\u0435\u043b\u044c \u043b\u0438\u043d\u0437\u044b \u0432 Haskell.\n"
))

cells.append(code(
"-- StoreT s w a = w (s -> a), s\n"
"-- Dual to StateT\n"
"data StoreT s w a = StoreT (w (s -> a)) s\n"
"\n"
"instance Functor w => Functor (StoreT s w) where\n"
"  fmap f (StoreT wf s) = StoreT (fmap (f .) wf) s\n"
"\n"
"instance Comonad w => Comonad (StoreT s w) where\n"
"  extract (StoreT wf s) = extract wf s\n"
"  duplicate (StoreT wf s) = StoreT (extend (\\wf' -> \\s' -> StoreT wf' s') wf) s\n"
"\n"
"instance ComonadTrans (StoreT s) where\n"
"  lower (StoreT wf _) = fmap ($ undefined) wf  -- simplified\n"
"\n"
"-- Core operations\n"
"pos :: StoreT s w a -> s\n"
"pos (StoreT _ s) = s\n"
"\n"
"peek :: Comonad w => s -> StoreT s w a -> a\n"
"peek s (StoreT wf _) = extract wf s\n"
"\n"
"seek :: s -> StoreT s w a -> StoreT s w a\n"
"seek s (StoreT wf _) = StoreT wf s\n"
"\n"
"-- Simple Store (base case: Store s a = s -> a, s)\n"
"type Store s a = StoreT s Id a\n"
"\n"
"mkStore :: (s -> a) -> s -> Store s a\n"
"mkStore f s = StoreT (Id f) s\n"
"\n"
"-- 1D cellular automaton\n"
"type Grid1D = Store Int Bool\n"
"\n"
"rule30 :: Int -> Bool\n"
"rule30 n = n `mod` 3 == 0  -- simplified rule\n"
"\n"
"initialGrid :: Grid1D\n"
"initialGrid = mkStore rule30 5\n"
"\n"
"demoStore :: IO ()\n"
"demoStore = do\n"
"  putStrLn $ \"Pos: \" ++ show (pos initialGrid)\n"
"  putStrLn $ \"Cell at 5: \" ++ show (peek 5 initialGrid)\n"
"  putStrLn $ \"Cell at 3: \" ++ show (peek 3 initialGrid)\n"
"  putStrLn $ \"Cell at 6: \" ++ show (peek 6 initialGrid)\n"
"demoStore"
))

# =================== CELLS 11-12: Section 5 - TracedT ===================
cells.append(md(
"## 5\ufe0f\u20e3 TracedT \u2014 \u0430\u043a\u043a\u0443\u043c\u0443\u043b\u044f\u0446\u0438\u044f \u0441 \u0444\u043e\u043a\u0443\u0441\u043e\u043c\n\n"
"`TracedT m w a ~ w (m -> a)` \u2014 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u0441 \u0441\u0438\u043d\u0442\u0435\u0437\u043e\u043c \u043f\u043e \u043c\u043e\u043d\u043e\u0438\u0434\u0443.\n\n"
"**\u0414\u0443\u0430\u043b\u044c**: WriterT\n\n"
"| \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f | TracedT | WriterT |\n"
"|-----------|---------|----------|\n"
"| \u0432\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435/\u0447\u0442\u0435\u043d\u0438\u0435 | `trace` | `tell`/`listen` |\n"
"| \u043f\u0440\u043e\u0435\u043a\u0446\u0438\u044f | `lower` | `lift` |\n\n"
"**\u041f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435**: \u0430\u043d\u0438\u043c\u0430\u0446\u0438\u044f, \u043f\u043e\u0442\u043e\u043a\u0438 \u0432\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438\n"
))

cells.append(code(
"-- TracedT m w a = w (m -> a)  (m must be Monoid)\n"
"-- Dual to WriterT\n"
"newtype TracedT m w a = TracedT { runTracedT :: w (m -> a) }\n"
"\n"
"instance Functor w => Functor (TracedT m w) where\n"
"  fmap f (TracedT w) = TracedT (fmap (f .) w)\n"
"\n"
"instance (Comonad w, Monoid m) => Comonad (TracedT m w) where\n"
"  extract (TracedT w) = extract w mempty\n"
"  duplicate (TracedT w) = TracedT $ extend (\\w' -> \\m -> TracedT $ fmap (. (m <>)) w') w\n"
"\n"
"instance Monoid m => ComonadTrans (TracedT m) where\n"
"  lower (TracedT w) = fmap ($ mempty) w\n"
"\n"
"-- trace: read value at a specific monoidal position\n"
"traceAt :: Comonad w => m -> TracedT m w a -> a\n"
"traceAt m (TracedT w) = extract w m\n"
"\n"
"-- Example: Fibonacci as a Traced comonad\n"
"type Traced' m a = TracedT m Id a\n"
"\n"
"fibs :: Traced' (Sum Int) Int\n"
"fibs = TracedT $ Id $ \\(Sum n) ->\n"
"  let go 0 = 0\n"
"      go 1 = 1\n"
"      go k = go (k-1) + go (k-2)\n"
"  in go n\n"
"\n"
"newtype Sum a = Sum { getSum :: a } deriving (Show)\n"
"instance Num a => Semigroup (Sum a) where Sum a <> Sum b = Sum (a + b)\n"
"instance Num a => Monoid (Sum a) where mempty = Sum 0\n"
"\n"
"demoTraced :: IO ()\n"
"demoTraced = do\n"
"  putStrLn $ \"fib(0..9): \" ++ show [traceAt (Sum i) fibs | i <- [0..9]]\n"
"  -- derivative: consecutive differences\n"
"  let diff = extend (\\w -> traceAt (Sum 1) w - extract w) fibs\n"
"  putStrLn $ \"diff(1..9): \" ++ show [traceAt (Sum i) diff | i <- [1..9]]\n"
"demoTraced"
))

print(f"cells 9-12 added: {len(cells)}")

# =================== CELLS 13-14: Section 6 - Stacks ===================
cells.append(md(
"## 6\ufe0f\u20e3 \u0421\u0442\u0435\u043a\u0438 \u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u043e\u0432 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\n\n"
"\u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u044b \u043c\u043e\u0436\u043d\u043e \u0441\u043a\u043b\u0430\u0434\u044b\u0432\u0430\u0442\u044c \u0434\u0440\u0443\u0433 \u043d\u0430 \u0434\u0440\u0443\u0433\u0430:\n\n"
"```\n"
"EnvT Scenario (Store Pos) Bool\n"
"-- Outer (global): Env provides Scenario\n"
"-- Inner (local):  Store provides Pos focus\n"
"```\n\n"
"**\u041f\u0440\u0430\u0432\u0438\u043b\u043e**: `lower` = \u043f\u0440\u043e\u0435\u043a\u0446\u0438\u044f, \u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0432\u043b\u0438\u044f\u0435\u0442 \u043d\u0430 \u0441\u0435\u043c\u0430\u043d\u0442\u0438\u043a\u0443.\n\n"
"![Stacks of comonad transformers](ct_stack.svg)\n"
))

cells.append(code(
"-- Stack: EnvT Scenario (Store Pos) Bool\n"
"-- Outer (global): environment/scenario\n"
"-- Inner (local):  position/focus\n"
"type Scenario = String\n"
"type Pos = Int\n"
"type CAWithScenario = EnvT Scenario (StoreT Pos Id) Bool\n"
"\n"
"-- Create a cellular automaton with a scenario\n"
"makeCellAuto :: Scenario -> [Bool] -> Pos -> CAWithScenario\n"
"makeCellAuto scenario cells p =\n"
"  let lookup i = if i >= 0 && i < length cells\n"
"                 then cells !! i\n"
"                 else False\n"
"  in EnvT (scenario, StoreT (Id lookup) p)\n"
"\n"
"demoStack :: IO ()\n"
"demoStack = do\n"
"  let ca = makeCellAuto \"rule-30\" [True,False,True,True,False] 2\n"
"  putStrLn $ \"Scenario: \" ++ askEnv ca\n"
"  putStrLn $ \"Cell at focus: \" ++ show (extract ca)\n"
"  -- lower gives us Store Pos Bool (without scenario)\n"
"  let innerStore = lower ca\n"
"  putStrLn $ \"Inner store pos: \" ++ show (pos innerStore)\n"
"  putStrLn $ \"Cell at 0: \" ++ show (peek 0 innerStore)\n"
"  putStrLn $ \"Cell at 1: \" ++ show (peek 1 innerStore)\n"
"demoStack"
))

# =================== CELLS 15-16: Section 7 - Game of Life ===================
cells.append(md(
"## 7\ufe0f\u20e3 \u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043f\u0440\u0438\u043c\u0435\u0440\u044b\n\n"
"\u0426\u0435\u043b\u043b\u044e\u043b\u044f\u0440\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442 \u0447\u0435\u0440\u0435\u0437 Store:\n\n"
"- `Store (Int,Int) Bool` \u2014 \u0431\u0435\u0441\u043a\u043e\u043d\u0435\u0447\u043d\u0430\u044f \u0441\u0435\u0442\u043a\u0430\n"
"- `extend rule grid` \u2014 \u043e\u0434\u0438\u043d \u0448\u0430\u0433 \u044d\u0432\u043e\u043b\u044e\u0446\u0438\u0438\n"
"- `extract` \u2014 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0432 \u0444\u043e\u043a\u0443\u0441\u0435\n\n"
"**\u041a\u043b\u044e\u0447\u0435\u0432\u043e\u0439 \u0438\u043d\u0441\u0430\u0439\u0442**: `extend f` = \u043f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c `f` \u043a\u043e \u0432\u0441\u0435\u043c\u0443 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u0443 \u043e\u0434\u043d\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e.\n"
))

cells.append(code(
"-- 2D cellular automaton with StoreT\n"
"type Grid = StoreT (Int,Int) Id Bool\n"
"\n"
"-- Create a grid from a list of lists\n"
"makeGrid :: [[Bool]] -> (Int,Int) -> Grid\n"
"makeGrid cells focus =\n"
"  let r = length cells\n"
"      c = if r > 0 then length (cells !! 0) else 0\n"
"      lookup (row,col) =\n"
"        if row >= 0 && row < r && col >= 0 && col < c\n"
"        then (cells !! row) !! col\n"
"        else False\n"
"  in StoreT (Id lookup) focus\n"
"\n"
"-- Count live neighbors\n"
"countNeighbors :: Grid -> Int\n"
"countNeighbors g = length $ filter id\n"
"  [ peek (row+dr, col+dc) g\n"
"  | dr <- [-1,0,1], dc <- [-1,0,1]\n"
"  , not (dr == 0 && dc == 0)\n"
"  ]\n"
"  where (row,col) = pos g\n"
"\n"
"-- Conway's Game of Life rule\n"
"golStep :: Grid -> Bool\n"
"golStep g =\n"
"  let alive = extract g\n"
"      n     = countNeighbors g\n"
"  in case (alive, n) of\n"
"       (True,  2) -> True\n"
"       (True,  3) -> True\n"
"       (False, 3) -> True\n"
"       _          -> False\n"
"\n"
"-- Glider pattern\n"
"glider :: [[Bool]]\n"
"glider = [ [False,True,False]\n"
"         , [False,False,True]\n"
"         , [True, True, True] ]\n"
"\n"
"demoGol :: IO ()\n"
"demoGol = do\n"
"  let g  = makeGrid glider (1,1)\n"
"  putStrLn $ \"Cell (1,1): \" ++ show (extract g)\n"
"  putStrLn $ \"Neighbors of (1,1): \" ++ show (countNeighbors g)\n"
"  let g2 = extend golStep g\n"
"  putStrLn $ \"After 1 step (1,1): \" ++ show (extract g2)\n"
"demoGol"
))

print(f"cells 13-16 added: {len(cells)}")

# =================== CELLS 17-18: Section 8 - ComonadT + MonadT ===================
cells.append(md(
"## 8\ufe0f\u20e3 \u041a\u043e\u043c\u0431\u0438\u043d\u0430\u0446\u0438\u044f ComonadT + MonadT\n\n"
"\u041a\u043e\u043c\u043e\u043d\u0430\u0434\u044b \u0438 \u043c\u043e\u043d\u0430\u0434\u044b \u043c\u043e\u0436\u043d\u043e \u043a\u043e\u043c\u0431\u0438\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0432\u0443\u043c\u044f \u0441\u043f\u043e\u0441\u043e\u0431\u0430\u043c\u0438.\n\n"
"### \u041f\u0430\u0442\u0442\u0435\u0440\u043d 1: ComonadT \u043f\u043e\u0432\u0435\u0440\u0445 Monad (`EnvT Config IO`)\n\n"
"```\n"
"EnvT Config IO a\n"
"-- IO \u0432\u043d\u0443\u0442\u0440\u0438, EnvT \u0441\u043d\u0430\u0440\u0443\u0436\u0438\n"
"-- extract :: IO \u043d\u0435\u0432\u043e\u0437\u043c\u043e\u0436\u0435\u043d (IO \u043d\u0435 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0430)!\n"
"-- \u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0447\u0435\u0440\u0435\u0437 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\n"
"```\n\n"
"### \u041f\u0430\u0442\u0442\u0435\u0440\u043d 2: MonadT \u043f\u043e\u0432\u0435\u0440\u0445 Comonad (`StateT s (Store s)`)\n\n"
"```\n"
"StateT s (Store s) a\n"
"-- Store \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u0432\u043d\u0443\u0442\u0440\u0438\n"
"-- StateT \u043c\u043e\u043d\u0430\u0434\u0430 \u0441\u043d\u0430\u0440\u0443\u0436\u0438\n"
"-- \u041a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0438\u0432\u0430\u0435\u0442 READ (observe surroundings)\n"
"-- \u041c\u043e\u043d\u0430\u0434\u0430 \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0438\u0432\u0430\u0435\u0442 WRITE (update state)\n"
"```\n\n"
"### \u041f\u043e\u0440\u044f\u0434\u043e\u043a \u043a\u043e\u043c\u043f\u043e\u0437\u0438\u0446\u0438\u0438\n\n"
"| \u041f\u043e\u0440\u044f\u0434\u043e\u043a | \u0422\u0438\u043f | \u0421\u0435\u043c\u0430\u043d\u0442\u0438\u043a\u0430 |\n"
"|--------|-----|----------|\n"
"| `ComonadT (MonadT m) w` | \u0433\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 + \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u044d\u0444\u0444\u0435\u043a\u0442\u044b | `EnvT Config (StateT s Identity)` |\n"
"| `MonadT m (ComonadT t w)` | \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u044d\u0444\u0444\u0435\u043a\u0442\u044b + \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u043d\u043e\u0435 \u043d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u0435 | `StateT s (Store s)` |\n\n"
"**\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e**: \u0432\u043d\u0435\u0448\u043d\u0438\u0439 = \u0433\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0439, \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 = \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439.\n"
))

cells.append(code(
"-- Pattern 1: ComonadT over a Monad\n"
"-- EnvT Config IO: IO inside, EnvT outside\n"
"-- We have a fixed Config AND can do IO effects\n"
"type Config = String\n"
"\n"
"-- Helper to run an EnvT over IO action\n"
"runWithConfig :: Config -> (Config -> IO a) -> IO a\n"
"runWithConfig cfg action = action cfg\n"
"\n"
"-- extract gives Config IO action, IO gives results\n"
"explainCombo :: IO ()\n"
"explainCombo = do\n"
"  putStrLn \"EnvT Config IO a:\"\n"
"  putStrLn \"  extract: get IO action (runs effects)\"\n"
"  putStrLn \"  askEnv:  read config (comonadic)\"\n"
"  putStrLn \"\"\n"
"  putStrLn \"StateT s (Store s) a:\"\n"
"  putStrLn \"  Store provides READ context (observe surroundings)\"\n"
"  putStrLn \"  State provides WRITE effects (update state, do IO)\"\n"
"  putStrLn \"\"\n"
"  putStrLn \"Order: outer = global, inner = local\"\n"
"explainCombo\n"
"\n"
"-- Pattern 2: MonadT over a Comonad\n"
"-- StateT over Store: adds mutable state to comonadic focus\n"
"import Control.Monad.Trans.State (StateT, runStateT, get, put, modify)\n"
"import Control.Monad.Trans.Class (lift)\n"
"\n"
"-- Store as base, StateT on top\n"
"-- Type: StateT s (Store s) a\n"
"-- Store provides:  read value at any position\n"
"-- State provides:  read/write current focus\n"
"type StoreWithState s a = StateT s (Store s) a\n"
"\n"
"-- Navigation: move focus and read value\n"
"navigateTo :: Int -> StoreWithState Int Bool\n"
"navigateTo newPos = do\n"
"  put newPos\n"
"  s <- get\n"
"  lift $ StoreT (Id (\\p -> p == s)) s  -- dummy: always True at s\n"
"\n"
"demoCombo :: IO ()\n"
"demoCombo = do\n"
"  putStrLn \"Pattern 2: StateT over Store\"\n"
"  let base = StoreT (Id (\\p -> p `elem` [1,3,5])) 0 :: Store Int Bool\n"
"  let (result, finalPos) = extract (runStateT (do { put 3; get }) 0 `asTypeOf` runStateT (return 0) 0 $ base)\n"
"  putStrLn $ \"Final state: \" ++ show (snd (extract (runStateT (put 3 >> get) 0) base))\n"
"demoCombo"
))

print(f"cells 17-18 added: {len(cells)}")

# =================== CELLS 19-20: Section 9 - Adjunctions ===================
cells.append(md(
"## 9\ufe0f\u20e3 \u0421\u0432\u044f\u0437\u044c \u0441 Adjunctions, Lens\n\n"
"### \u0421\u043e\u043f\u0440\u044f\u0436\u0435\u043d\u0438\u044f (-|) \u0438 \u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u044b\n\n"
"\u0415\u0441\u043b\u0438 `F -| G` (\u0444\u0443\u043d\u043a\u0442\u043e\u0440 `F` \u043b\u0435\u0432\u044b\u0439 \u0441\u043c\u0435\u0436\u043d\u044b\u0439 \u0441 `G`):\n\n"
"- `F` \u043f\u043e\u0440\u043e\u0436\u0434\u0430\u0435\u0442 \u043c\u043e\u043d\u0430\u0434\u0443: `return = unit`, `(>>=) = counit`\n"
"- `G` \u043f\u043e\u0440\u043e\u0436\u0434\u0430\u0435\u0442 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0443: `extract = counit`, `duplicate = unit`\n\n"
"### Store \u0438 Lens\n\n"
"Store s a \u2261 (s -> a, s) \u2014 \u044d\u0442\u043e \u0438\u043c\u0435\u043d\u043d\u043e \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 Lens \u0432 van Laarhoven!\n\n"
"```\n"
"type Lens s a = s -> Store a s\n"
"-- \u044d\u043a\u0432\u0438\u0432\u0430\u043b\u0435\u043d\u0442\u043d\u043e:\n"
"type Lens s a = forall f. Functor f => (a -> f a) -> s -> f s\n"
"```\n\n"
"**Store \u2194 State**: \u0441\u043e\u043f\u0440\u044f\u0436\u0435\u043d\u0438\u0435 `State s -| Store s`.\n"
))

cells.append(code(
"-- Store s a = (s -> a, s): this IS the definition of a Lens!\n"
"-- Lens: s -> Store a s  (focus on 'a' inside 's')\n"
"\n"
"-- Simple lens type using Store\n"
"type Lens s a = s -> Store a s\n"
"\n"
"-- Lens for first element of a pair\n"
"fstLens :: Lens (a, b) a\n"
"fstLens (x, y) = StoreT (Id (\\x' -> (x', y))) x\n"
"\n"
"-- view: get the focused value\n"
"view :: Lens s a -> s -> a\n"
"view ln s = extract (ln s)\n"
"\n"
"-- set: set the focused value\n"
"set :: Lens s a -> a -> s -> s\n"
"set ln a s = peek a (ln s)\n"
"\n"
"-- over: modify the focused value\n"
"over :: Lens s a -> (a -> a) -> s -> s\n"
"over ln f s = set ln (f (view ln s)) s\n"
"\n"
"demonstrateLens :: IO ()\n"
"demonstrateLens = do\n"
"  let pair = (42 :: Int, \"hello\")\n"
"  putStrLn $ \"Focus (fst): \" ++ show (view fstLens pair)\n"
"  putStrLn $ \"Set to 100: \" ++ show (set fstLens 100 pair)\n"
"  putStrLn $ \"Add 1: \" ++ show (over fstLens (+1) pair)\n"
"  -- extend to modify: like over but comonadic\n"
"  let s' = extend (\\w -> peek (pos w + 1) w) (fstLens pair)\n"
"  putStrLn $ \"After +1: \" ++ show (extract s')\n"
"demonstrateLens"
))

# =================== CELL 21: SUMMARY ===================
cells.append(md(
"## \ud83d\udcca \u0418\u0442\u043e\u0433\n\n"
"| \u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440 | \u0422\u0438\u043f | \u0414\u0443\u0430\u043b\u044c | \u041f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 |\n"
"|-----------|------|-------|------------|\n"
"| EnvT e w a | `(e, w a)` | ReaderT | \u0422\u0435\u043c\u044b, \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f |\n"
"| StoreT s w a | `w(s->a), s` | StateT | Lens, \u0426\u0410 |\n"
"| TracedT m w a | `w(m->a)` | WriterT | \u0410\u043d\u0438\u043c\u0430\u0446\u0438\u044f, \u043f\u043e\u0442\u043e\u043a\u0438 |\n"
"| ComonadT+MonadT | \u0441\u043c\u0435\u0448\u0430\u043d\u043d\u044b\u0439 | \u2014 | UI, gameplay |\n\n"
"**\u041a\u043b\u044e\u0447\u0435\u0432\u043e\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e**: `lower` = \u043f\u0440\u043e\u0435\u043a\u0446\u0438\u044f, `lift` = \u0432\u044a\u0435\u043c. "
"\u0412\u043d\u0435\u0448\u043d\u0438\u0439 = \u0433\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0439, \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 = \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439.\n"
))

# =================== CELL 22: NAV ===================
cells.append(md(
"\u2190 **\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0439:** [Comonads.ipynb](Comonads.ipynb) | "
"\u2192 **\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439:** [MonadTransformers.ipynb](MonadTransformers.ipynb)\n"
))

# =================== WRITE NOTEBOOK ===================
nb = {
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "kernelspec": {"display_name": "Haskell", "language": "haskell", "name": "haskell"},
    "language_info": {"name": "haskell", "version": "9.6.7"}
  },
  "cells": cells
}

with open(nb_path, 'w', encoding='utf-8') as f:
  json.dump(nb, f, ensure_ascii=True, indent=1)

print(f"DONE! Written {len(cells)} cells to {nb_path}")
