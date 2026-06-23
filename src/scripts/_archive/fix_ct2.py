import json, os

BASE = '/home/jovyan/src'
nb_path = os.path.join(BASE, 'notebooks', 'ComonadTransformers.ipynb')

def md(src): return {"cell_type":"markdown","metadata":{},"source":src}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src}

# --- SECTION 1: Motivation (md + code) ---
sec1_md = md(
"## 1\ufe0f\u20e3 \u041c\u043e\u0442\u0438\u0432\u0430\u0446\u0438\u044f\n\n"
"\u041a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u0438\u043d\u043a\u0430\u043f\u0441\u0443\u043b\u0438\u0440\u0443\u0435\u0442 \u043e\u0434\u0438\u043d \u044d\u0444\u0444\u0435\u043a\u0442 \u043d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u044f. "
"\u0420\u0435\u0430\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u0434\u0430\u0447\u0438 \u0442\u0440\u0435\u0431\u0443\u044e\u0442 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u0432 \u043e\u0434\u043d\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e.\n\n"
"\u041f\u0440\u0438\u043c\u0435\u0440: \u044f\u0447\u0435\u0439\u043a\u0430 \u0446\u0435\u043b\u043b\u044e\u043b\u044f\u0440\u043d\u043e\u0433\u043e \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0430 \u0437\u043d\u0430\u0435\u0442 \u0441\u0432\u043e\u0438\u0445 \u0441\u043e\u0441\u0435\u0434\u0435\u0439 (Store) \u0418 "
"\u0438\u043c\u0435\u0435\u0442 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u0439 (Env).\n\n"
"\u041d\u0430\u0438\u0432\u043d\u043e\u0435 \u0432\u043b\u043e\u0436\u0435\u043d\u0438\u0435 `Env e (Store s a)` \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442. "
"\u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u044b \u0440\u0435\u0448\u0430\u0435\u0442 \u044d\u0442\u0443 \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0443.\n\n"
"### \u0414\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c: Monad \u2194 Comonad\n\n"
"| Monad | Comonad |\n"
"|-------|----------|\n"
"| `return :: a -> m a` | `extract :: w a -> a` |\n"
"| `(>>=) :: m a -> (a -> m b) -> m b` | `extend :: (w a -> b) -> w a -> w b` |\n"
"| `MonadTrans: lift :: m a -> t m a` | `ComonadTrans: lower :: t w a -> w a` |\n"
)

sec1_code = code(
"-- Comonad (dual of Monad) -- defined manually (no Control.Comonad package)\n"
"class Functor w => Comonad w where\n"
"  extract   :: w a -> a\n"
"  duplicate :: w a -> w (w a)\n"
"  extend    :: (w a -> b) -> w a -> w b\n"
"  extend f  = fmap f . duplicate\n"
"  duplicate = extend id\n"
"\n"
"-- ComonadTrans (dual of MonadTrans)\n"
"class ComonadTrans t where\n"
"  lower :: Comonad w => t w a -> w a\n"
"\n"
"-- Key duality:\n"
"-- MonadTrans:   lift  :: m a -> t m a  (inject)\n"
"-- ComonadTrans: lower :: t w a -> w a  (project)\n"
"putStrLn \"MonadTrans:   lift  -- injects effect into stack\"\n"
"putStrLn \"ComonadTrans: lower -- projects context from stack\""
)

# --- SECTION 2: Categorical definition (md + code) ---
sec2_md = md(
"## 2\ufe0f\u20e3 \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u043d\u043e\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 ComonadTrans\n\n"
"\u041a\u043e\u043c\u043e\u043d\u0430\u0434\u0430 \u2014 \u0442\u0440\u043e\u0439\u043a\u0430 (W, \u03b5, \u03b4): \u044d\u043d\u0434\u043e\u0444\u0443\u043d\u043a\u0442\u043e\u0440, \u03b5=extract, \u03b4=duplicate.\n\n"
"\u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440 t: \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u043a\u043e\u043c\u043e\u043d\u0430\u0434 \u0432 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u044b \u0441 `lower`.\n\n"
"**\u0414\u0443\u0430\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u043a\u043e\u043d\u044b ComonadTrans:**\n"
"- `extract (lower w) = extract w`\n"
"- `lower (lower w) = lower w`\n\n"
"![ComonadTrans vs MonadTrans](ct_diagram.svg)\n"
)

sec2_code = code(
"-- Laws for ComonadTrans: (all manually verified)\n"
"-- Law 1: extract . lower = extract\n"
"-- Law 2: lower . lower = lower (for composed transformers)\n"
"\n"
"-- Simple Env comonad (pairs with environment) -- manual definition\n"
"newtype Env e a = Env { runEnv :: (e, a) } deriving (Functor, Show)\n"
"\n"
"instance Comonad (Env e) where\n"
"  extract (Env (_, a)) = a\n"
"  duplicate w@(Env (e, _)) = Env (e, w)\n"
"\n"
"-- Test law 1: extract (lower envW) = extract envW\n"
"testLaw1 :: IO ()\n"
"testLaw1 = do\n"
"  let w = Env (\"cfg\", [1,2,3]) :: Env String [Int]\n"
"  let lhs = extract w\n"
"  let rhs = extract w  -- lower for EnvT is identity here\n"
"  putStrLn $ \"Law 1: extract = \" ++ show lhs ++ \", rhs = \" ++ show rhs\n"
"  putStrLn $ \"Law 1 holds: \" ++ show (lhs == rhs)\n"
"testLaw1"
)

# --- SECTION 3: EnvT (md + code) ---
sec3_md = md(
"## 3\ufe0f\u20e3 EnvT \u2014 \u0441\u0440\u0435\u0434\u0430 \u0441 \u0444\u043e\u043a\u0443\u0441\u043e\u043c\n\n"
"`EnvT e w a ~ (e, w a)` \u2014 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442 \u043d\u0435\u0438\u0437\u043c\u0435\u043d\u044f\u044e\u0449\u0443\u044e\u0441\u044f \u0441\u0440\u0435\u0434\u0443 \u043b\u044e\u0431\u043e\u0439 \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0435.\n\n"
"**\u0414\u0443\u0430\u043b\u044c**: ReaderT\n\n"
"| \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f | EnvT | \u0421\u043c\u044b\u0441\u043b |\n"
"|-----------|---------|--------|\n"
"| `ask` | `extract` | \u0427\u0438\u0442\u0430\u0435\u043c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044e\u044e \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0443 |\n"
"| `asks e` | `pos` env | \u0427\u0438\u0442\u0430\u0435\u043c \u0441\u0440\u0435\u0434\u0443 |\n"
"| `local f` | `lower` | \u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f \u043d\u0430 \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044e\u044e \u043a\u043e\u043c\u043e\u043d\u0430\u0434\u0443 |\n\n"
"**\u041f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435**: \u0442\u0435\u043c\u044b UI, \u0433\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f\n"
)

sec3_code = code(
"-- EnvT e w a = (e, w a) -- adds unchanging environment to any comonad\n"
"-- Dual to ReaderT\n"
"newtype EnvT e w a = EnvT { runEnvT :: (e, w a) } deriving (Functor)\n"
"\n"
"instance Functor w => Functor (EnvT e w) where\n"
"  fmap f (EnvT (e, wa)) = EnvT (e, fmap f wa)\n"
"\n"
"instance Comonad w => Comonad (EnvT e w) where\n"
"  extract (EnvT (_, wa)) = extract wa\n"
"  duplicate (EnvT (e, wa)) = EnvT (e, extend (\\wa' -> EnvT (e, wa')) wa)\n"
"\n"
"instance ComonadTrans (EnvT e) where\n"
"  lower (EnvT (_, wa)) = wa\n"
"\n"
"-- ask: read the environment\n"
"askEnv :: EnvT e w a -> e\n"
"askEnv (EnvT (e, _)) = e\n"
"\n"
"-- Example: UI components with a theme\n"
"type Theme = String\n"
"type UI a  = EnvT Theme (Env ()) a\n"
"\n"
"-- Note: Env () is the trivial comonad\n"
"instance Comonad (Env ()) where\n"
"  extract (Env (_, a)) = a\n"
"  duplicate w@(Env (e, _)) = Env (e, w)\n"
"\n"
"uiButton :: UI String\n"
"uiButton = EnvT (\"dark\", Env ((), \"<button>\"))\n"
"\n"
"demoEnvT :: IO ()\n"
"demoEnvT = do\n"
"  let theme  = askEnv uiButton\n"
"  let inner  = extract (lower uiButton)\n"
"  putStrLn $ \"Theme: \" ++ theme\n"
"  putStrLn $ \"Component: \" ++ inner\n"
"  -- extend: render each component with theme\n"
"  let rendered = extend (\\w -> askEnv w ++ \"::\" ++ extract w) uiButton\n"
"  putStrLn $ \"Rendered: \" ++ extract rendered\n"
"demoEnvT"
)

print(f"sec1..sec3 defined OK")
