#!/usr/bin/env python3
"""Phase 12: expand T4 markdown with arrow-notation logic + insert Set code cell."""
import json, sys
PATH = "/home/jovyan/src/notebooks/Toposes.ipynb"

ARROW_BLOCK = r"""### Связки как классифицирующие стрелки (стрелочная нотация)

В элементарном топосе **все** логические связки — это морфизмы на $\Omega$, заданные через
классификатор подобъектов (характеристические стрелки определяющих подобъектов).

**Истина и ложь.** $\mathrm{true} : 1 \to \Omega$ — структура классификатора; ложь — это
характеристическая стрелка моно из инициального объекта:
$$\mathrm{false} = \chi_{(0 \hookrightarrow 1)} : 1 \to \Omega.$$

**Конъюнкция** $\wedge : \Omega\times\Omega \to \Omega$ — характеристическая стрелка точки
«обе истинны» $\langle\mathrm{true},\mathrm{true}\rangle : 1 \hookrightarrow \Omega\times\Omega$:
$$\begin{array}{ccc}
1 & \xrightarrow{\;!\;} & 1 \\
{\scriptstyle\langle\mathrm{true},\mathrm{true}\rangle}\downarrow & \square & \downarrow{\scriptstyle\mathrm{true}} \\
\Omega\times\Omega & \xrightarrow{\;\wedge\;} & \Omega
\end{array}$$

**Внутренний порядок и импликация.** Подобъект ${\leq}\hookrightarrow \Omega\times\Omega$ —
это эквалайзер пары $(\wedge,\ \pi_1)$, то есть $\{(x,y)\mid x\wedge y = x\}$. Импликация —
его характеристическая стрелка:
$$\Rightarrow\ =\ \chi_{(\leq)} : \Omega\times\Omega \to \Omega.$$

**Дизъюнкция** $\vee : \Omega\times\Omega \to \Omega$ — характеристическая стрелка **образа**
объединения двух «прямых истинности»
$[\langle \mathrm{true}\circ\,!,\ \mathrm{id}\rangle,\ \langle \mathrm{id},\ \mathrm{true}\circ\,!\rangle] : \Omega \sqcup \Omega \to \Omega\times\Omega$:
$$\vee\ =\ \chi_{\mathrm{im}[\dots]}.$$

**Отрицание** $\neg : \Omega \to \Omega$ — характеристическая стрелка лжи, равносильно
$\neg = (\Rightarrow)\circ\langle\mathrm{id},\ \mathrm{false}\circ\,!\rangle$:
$$\neg\ =\ \chi_{(\mathrm{false} : 1 \hookrightarrow \Omega)}.$$

**Гейтингова сопряжённость.** Эти стрелки делают $\Omega$ внутренней гейтинговой алгеброй:
$(-\wedge a)\dashv(a\Rightarrow -)$, то есть $x \leq (a\Rightarrow y) \iff (x\wedge a)\leq y$.

![Конъюнкция и отрицание как классифицирующие стрелки](../diagrams/topos/topos_conj_neg.svg)

![Импликация (эквалайзер) и дизъюнкция (образ)](../diagrams/topos/topos_impl_disj.svg)

> **Связь с реализацией ниже.** Открытые формулы в таблице ($\cap,\ \cup,\ \mathrm{Int}((X\setminus U)\cup V),\ \mathrm{Int}(X\setminus U)$) — это те же стрелки $\wedge,\vee,\Rightarrow,\neg$, реализованные в топосе пучков $\mathbf{Sh}(X)$. В $\mathbf{Set}$ ($\Omega=2$) из тех же pullback-квадратов выпадают классические таблицы истинности — это проверяет код далее.

"""

T4B_CODE = r"""-- T4b: связки как классифицирующие стрелки (Set-топос, Omega = Bool)
-- Каждая связка = характеристическая стрелка своего определяющего подобъекта.

type Om = Bool
omElems :: [Om]
omElems = [False, True]

trueArr :: () -> Om
trueArr () = True
falseArr :: () -> Om
falseArr () = False

-- chi_S : A -> Omega ; chi_S a = (a принадлежит S), подобъект S задан списком элементов
chiOf :: Eq a => [a] -> a -> Om
chiOf s a = a `elem` s

prod2 :: [(Om, Om)]
prod2 = [(x,y) | x <- omElems, y <- omElems]

-- AND = chi <true,true> : 1 |-> Omega x Omega
andArr :: (Om, Om) -> Om
andArr = chiOf [(True, True)]

-- внутренний порядок (<=) = эквалайзер (AND, pi1) = {(x,y) | x/\y = x}
leqSub :: [(Om, Om)]
leqSub = [p | p <- prod2, andArr p == fst p]

-- IMP = chi (<=)
impArr :: (Om, Om) -> Om
impArr = chiOf leqSub

-- OR = chi образа объединения двух прямых истинности = {(x,y) | x=T или y=T}
orSub :: [(Om, Om)]
orSub = [p | p <- prod2, fst p || snd p]
orArr :: (Om, Om) -> Om
orArr = chiOf orSub

-- NOT = chi false : 1 |-> Omega ; равносильно imp . <id, false>
notArr :: Om -> Om
notArr = chiOf [False]
notViaImp :: Om -> Om
notViaImp x = impArr (x, falseArr ())

leqB :: Om -> Om -> Bool
leqB p q = (p && q) == p

pad :: Om -> String
pad b = let s = show b in s ++ replicate (5 - length s) ' '

demoArrowLogic :: IO ()
demoArrowLogic = do
  putStrLn "x     y     | and   or    imp   | classic &&/||/->"
  mapM_ (\(x,y) -> putStrLn $
            pad x ++ " " ++ pad y ++ " | "
            ++ pad (andArr (x,y)) ++ " " ++ pad (orArr (x,y)) ++ " " ++ pad (impArr (x,y))
            ++ " | " ++ show (x && y) ++ " " ++ show (x || y) ++ " " ++ show (not x || y)) prod2
  putStrLn $ "neg via chi(false): " ++ show (map notArr omElems)
  putStrLn $ "neg via (=> false): " ++ show (map notViaImp omElems)
  putStrLn $ "two negations agree: " ++ show (map notArr omElems == map notViaImp omElems)
  let adj a = and [ leqB x (impArr (a,y)) == leqB (andArr (x,a)) y
                  | x <- omElems, y <- omElems ]
  putStrLn $ "\x2705 Heyting adjunction (-/\\a -| a=>-) holds for all a: " ++ show (all adj omElems)

demoArrowLogic"""

def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    cells = nb["cells"]
    # 1) expand T4 markdown: insert ARROW_BLOCK before "### Почему логика интуиционистская?"
    t4_idx = None
    for i, c in enumerate(cells):
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("---\n\n## 4️⃣ T4"):
            t4_idx = i; break
    if t4_idx is None:
        print("ERROR: T4 markdown not found", file=sys.stderr); sys.exit(1)
    s = "".join(cells[t4_idx]["source"])
    anchor = "### Почему логика интуиционистская?"
    if "Связки как классифицирующие стрелки" not in s:
        if anchor not in s:
            print("ERROR: anchor not found in T4", file=sys.stderr); sys.exit(1)
        s = s.replace(anchor, ARROW_BLOCK + anchor, 1)
        cells[t4_idx]["source"] = s.splitlines(keepends=True)
    # 2) insert T4b code cell right after the existing T4 code cell
    t4code_idx = None
    for i, c in enumerate(cells):
        if c["cell_type"] == "code" and "".join(c["source"]).startswith("-- T4: Гейтингова алгебра"):
            t4code_idx = i; break
    if t4code_idx is None:
        print("ERROR: T4 code not found", file=sys.stderr); sys.exit(1)
    already = any(c["cell_type"] == "code" and "".join(c["source"]).startswith("-- T4b:")
                  for c in cells)
    if not already:
        newc = {"cell_type": "code", "id": "topos-t4b-arrows", "metadata": {},
                "execution_count": None, "outputs": [],
                "source": T4B_CODE.splitlines(keepends=True)}
        cells.insert(t4code_idx + 1, newc)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("T4 expanded + T4b code inserted")

if __name__ == "__main__":
    main()
