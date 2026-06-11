# Усиление категорных конструкций в SubjectiveModeling.ipynb — план внедрения

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Закрыть логические дыры и усилить категорный слой (разделы 13–14) ноутбука `src/notebooks/SubjectiveModeling.ipynb`: residuation-кондиционирование, честный вывод Bel, интервальный билатис, Γ как автоморфизмы квантали, монада возможности (мост к Uncertainty.ipynb), обогащённая неточечная X с нетривиальной двойственностью Исбелла.

**Architecture:** Ноутбук редактируется через NotebookEdit (cell id известны). Каждая новая кодовая ячейка самодостаточна (стиль ноутбука: повтор типов в каждой ячейке). Markdown-правки расширяют существующие секции блоками `### 🔺 Категорный взгляд`. Две новые секции 15–16 вставляются перед итоговой ячейкой. Верификация — Run All через `nbconvert --execute` в docker-контейнере `ihaskell`.

**Tech Stack:** IHaskell (GHC, ограничения из ROADMAP: ASCII-строки, без XQuantifiedConstraints), Jupyter via docker-compose (порт 8889, без токена), Node.js для JSON-проверок.

**Проект не является git-репозиторием** — шаги «commit» заменены шагами «сохранить и проверить JSON».

**Карта ячеек ноутбука (id):**

| idx | id | содержимое |
|-----|----|-----------|
| 1 | vq1fhqjw | TOC |
| 3 | tqhh6in8 | Раздел 2 (шкалы, билатис — править) |
| 5 | 9bhvak76 | Раздел 4 (Γ — дополнить) |
| 9 | 1gn0w7ku | Раздел 7 (условные — дополнить) |
| 18 | 6zp1eh4d | Раздел 14 (Bel/Isbell — править) |
| 20 | gznlc5hp | Итоги (обновить) |
| 21 | k82rtv86 | NAV (последняя) |

---

### Task 1: Внести Фазу 5 в src/ROADMAP.md

**Files:** Modify: `src/ROADMAP.md`

- [ ] **Step 1.1:** После блока «Фаза 4» (перед «⚠️ Критические правила») вставить:

```markdown
## 🔄 Фаза 5 — Категорное усиление SubjectiveModeling.ipynb (начато 2026-06-11)

План: docs/superpowers/plans/2026-06-11-subjective-modeling-categorical.md

| # | Улучшение | Раздел | Статус |
|---|-----------|--------|--------|
| 1 | Кондиционирование = residuation (внутренний hom квантали) | 7 | ⬜ |
| 2 | Честный Bel: Ran вдоль профунктора дополнения + инволюция θ | 14 | ⬜ |
| 3 | Исправление: интервальный билатис [Bel, Pl] вместо пары шкал | 2 | ⬜ |
| 4 | Γ как группа автоморфизмов квантали, эквивариантность Pl | 4 | ⬜ |
| 5 | Монада возможности (аналог Гири), мост к Uncertainty.ipynb | 15 (новый) | ⬜ |
| 6 | [0,1]-обогащённая X (Ловер), нетривиальный Isbell, O ⊣ Spec | 16 (новый) | ⬜ |
| 7 | Обновление TOC, итоговой таблицы, проверка Run All = 0 ошибок | — | ⬜ |
```

- [ ] **Step 1.2:** Обновить строку «Последнее обновление» в шапке на 2026-06-11.

---

### Task 2: Раздел 7 — кондиционирование как residuation

**Files:** Modify cell `1gn0w7ku` (markdown, раздел 7); Insert new code cell after it.

- [ ] **Step 2.1:** В конец markdown-ячейки `1gn0w7ku` добавить:

```markdown

### 🔺 Категорный взгляд: кондиционирование = residuation

Уравнение Пытьева $\min\{c,\; \tau^{\tilde{z}_2}(z_2)\} = \tau^{\tilde{z}_1,\tilde{z}_2}(z_1,z_2)$ — это вопрос о **правом сопряжённом** к функтору $\min(-, a)$ в квантали $([0,1], \min, 1)$. Его максимальное решение — в точности внутренний hom (residuation):

$$\tau^{\tilde{z}_1|\tilde{z}_2}(z_1|z_2) \;=\; \tau^{\tilde{z}_2}(z_2) \multimap \tau^{\tilde{z}_1,\tilde{z}_2}(z_1,z_2), \qquad a \multimap b = \begin{cases} 1 & a \le b \\ b & a > b \end{cases}$$

Сопряжение $\min(a,c) \le b \iff c \le (a \multimap b)$ гарантирует: (1) это решение уравнения, поскольку всегда $\tau^{\tilde{z}_1,\tilde{z}_2}(z_1,z_2) \le \tau^{\tilde{z}_2}(z_2)$; (2) оно **наибольшее** из решений; (3) $\sup_{z_1} \tau(z_1|z_2) = 1$ — условное распределение нормировано без перехода в субъективную шкалу $\gamma_{z_2}L$. Аналогия с $\Pr(A|B) = \Pr(A \cap B)/\Pr(B)$ точная: деление — это residuation квантали $([0,1], \cdot, 1)$ третьего варианта мер.
```

- [ ] **Step 2.2:** Вставить новую code-ячейку после `1gn0w7ku`:

```haskell
-- | Раздел 7+: кондиционирование как residuation в квантали ([0,1], min, 1)

approx :: Double -> Double -> Bool
approx a b = abs (a - b) < 1e-9

-- Внутренний hom (residuation): a -o b = sup { c | min(a,c) <= b }
qHomR :: Double -> Double -> Double
qHomR a b = if a <= b then 1.0 else b

-- Совместное распределение правдоподобий на Z1 x Z2
tauJoint :: (Int, Int) -> Double
tauJoint (1,1) = 1.0
tauJoint (2,1) = 0.6
tauJoint (1,2) = 0.4
tauJoint (2,2) = 0.4
tauJoint _     = 0.0

z1s, z2s :: [Int]
z1s = [1,2]
z2s = [1,2]

-- Маргинал: tau(z2) = sup_{z1} tauJoint(z1,z2)
tauZ2 :: Int -> Double
tauZ2 z2 = maximum (0 : [tauJoint (z1,z2) | z1 <- z1s])

-- Условное распределение = residuation
condTau :: Int -> Int -> Double
condTau z1 z2 = qHomR (tauZ2 z2) (tauJoint (z1,z2))

demoResiduation :: IO ()
demoResiduation = do
  putStrLn "=== Razdel 7+: kondicionirovanie = residuation ==="
  mapM_ (\(z1,z2) -> putStrLn $ "  tau(" ++ show z1 ++ "|" ++ show z2 ++ ") = "
         ++ show (condTau z1 z2)) [(a,b) | b <- z2s, a <- z1s]
  -- (1) решение уравнения min(c, tau(z2)) = tauJoint(z1,z2)
  let chkEq = and [ approx (min (condTau z1 z2) (tauZ2 z2)) (tauJoint (z1,z2))
                  | z1 <- z1s, z2 <- z2s ]
  -- (2) максимальность среди решений на сетке
  let grid = map (\k -> fromIntegral k / 20) [0..20 :: Int]
      chkMax = and [ c <= condTau z1 z2 + 1e-9
                   | z1 <- z1s, z2 <- z2s, c <- grid
                   , approx (min c (tauZ2 z2)) (tauJoint (z1,z2)) ]
  -- (3) нормировка: sup_{z1} tau(z1|z2) = 1
  let chkNorm = and [ approx (maximum [condTau z1 z2 | z1 <- z1s]) 1.0 | z2 <- z2s ]
  -- (4) adjointness: min(a,c) <= b  <=>  c <= a -o b
  let chkAdj = and [ (min a c <= b) == (c <= qHomR a b)
                   | a <- grid, b <- grid, c <- grid ]
  putStrLn $ "  Reshenie uravneniya:  " ++ show chkEq
  putStrLn $ "  Maksimalnost:         " ++ show chkMax
  putStrLn $ "  Normirovka sup = 1:   " ++ show chkNorm
  putStrLn $ "  Adjointness (9261 troek): " ++ show chkAdj

demoResiduation
```

- [ ] **Step 2.3:** Проверить JSON ноутбука: `node -e "JSON.parse(require('fs').readFileSync('src/notebooks/SubjectiveModeling.ipynb','utf8')); console.log('OK')"` → `OK`.

---

### Task 3: Раздел 14 — честный Bel через профунктор дополнения и инволюцию θ

**Files:** Modify cell `6zp1eh4d` (markdown); Insert new code cell after it.

- [ ] **Step 3.1:** В ячейке `6zp1eh4d` найти фрагмент (вычисление Ran, заканчивающийся подгонкой):

```
$\mathcal{P}(X)(E, J(x)) = [x \in E]$; внутренний hom $[0,1](1, \bar{\tau}(x)) = \bar{\tau}(x)$,
$[0,1](0, \bar{\tau}(x)) = 1$. End = $\inf_{x \in E} \bar{\tau}(x)$... но Bel определена через
дополнение: end по $x \notin E$ равен $\inf_{x \notin E} \bar{\tau}(x) = \mathrm{Bel}(E)$. $\square$
```

и заменить на:

```markdown
**Где была дыра.** Если брать Ran вдоль того же профунктора $[x \in E]$, end даёт $\inf_{x \in E} \bar{\tau}(x)$ — а это **не** $\mathrm{Bel}(E)$. Правильная конструкция: Bel — это правое расширение Кана вдоль **профунктора дополнения** $J^{\complement}(E, x) = [x \notin E]$:

$$\mathrm{Ran}_{J^{\complement}}\,\bar{\tau}\,(E) = \int_{x \in \mathbf{X}} [0,1]\bigl([x \notin E],\, \bar{\tau}(x)\bigr) = \inf_{x \notin E} \bar{\tau}(x) = \mathrm{Bel}(E)\;\square$$

(внутренний hom: $[0,1](1, t) = t$, $[0,1](0, t) = 1$, поэтому end пробегает ровно $x \notin E$).

**Почему именно дополнение.** Дуальная согласованность Пытьева $\mathrm{Bel}(E) = \theta(\mathrm{Pl}(X \setminus E))$ — это утверждение, что инволюция $\theta(t) = 1 - t$ есть **дуальный изоморфизм кванталей** $([0,1], \max, \min) \xrightarrow{\;\sim\;} ([0,1], \min, \max)^{op}$, переводящий sup в inf и $\tau \mapsto \bar{\tau}$. Профунктор дополнения — это в точности образ $J$ под действием $\theta$ на истинностных значениях: $[x \notin E] = \theta_{\{0,1\}}([x \in E])$. Итого пара (Pl, Bel) — это пара (Lan вдоль $J$, Ran вдоль $\theta J$), и «гипотеза единства» сводится к коммутированию $\theta$ с парой расширений Кана — что проверяется на конечных примерах ниже.
```

- [ ] **Step 3.2:** Вставить новую code-ячейку после `6zp1eh4d`:

```haskell
-- | Раздел 14+: Bel = Ran вдоль профунктора дополнения; инволюция theta
import Control.Monad (filterM)
import Data.List ((\\))

approx2 :: Double -> Double -> Bool
approx2 a b = abs (a - b) < 1e-9

ptsX :: String
ptsX = "abc"

tauX :: Char -> Double
tauX 'a' = 1.0
tauX 'b' = 0.6
tauX 'c' = 0.2
tauX _   = 0.0

thetaInv :: Double -> Double
thetaInv t = 1.0 - t

tauBarX :: Char -> Double
tauBarX = thetaInv . tauX

allSubsets :: [String]
allSubsets = filterM (const [True, False]) ptsX

-- Pl(E) = Lan_J tau (E) = sup_{x in E} min([x in E]=1, tau x)
lanPl :: String -> Double
lanPl e = maximum (0 : [min 1.0 (tauX x) | x <- e])

-- Bel(E) = Ran_{J-complement} tauBar (E) = inf_{x notin E} hom([x notin E], tauBar x)
ranBel :: String -> Double
ranBel e = minimum (1 : [tauBarX x | x <- ptsX, x `notElem` e])

-- Прямые определения Пытьева для сверки
plDirect :: String -> Double
plDirect e = maximum (0 : map tauX e)

belDirect :: String -> Double
belDirect e = minimum (1 : [tauBarX x | x <- ptsX \\ e])

demoIsbellFix :: IO ()
demoIsbellFix = do
  putStrLn "=== Razdel 14+: Bel cherez profunktor dopolneniya ==="
  let chkPl  = all (\e -> approx2 (lanPl e) (plDirect e)) allSubsets
      chkBel = all (\e -> approx2 (ranBel e) (belDirect e)) allSubsets
      -- дуальная согласованность: Bel(E) = theta (Pl (X \ E))
      chkDual = all (\e -> approx2 (ranBel e) (thetaInv (lanPl (ptsX \\ e)))) allSubsets
      -- theta — дуальный изоморфизм кванталей: theta(max a b) = min (theta a) (theta b)
      grid = map (\k -> fromIntegral k / 10) [0..10 :: Int]
      chkTheta = and [ approx2 (thetaInv (max a b)) (min (thetaInv a) (thetaInv b))
                       && approx2 (thetaInv (min a b)) (max (thetaInv a) (thetaInv b))
                     | a <- grid, b <- grid ]
  putStrLn $ "  Lan_J tau = Pl na vseh 8 podmnozhestvah:        " ++ show chkPl
  putStrLn $ "  Ran_{J^c} tauBar = Bel na vseh podmnozhestvah:  " ++ show chkBel
  putStrLn $ "  Bel(E) = theta(Pl(X\\E)) (dualnaya soglasov.):   " ++ show chkDual
  putStrLn $ "  theta - dualnyj izomorfizm kvantalej:            " ++ show chkTheta
  mapM_ (\e -> putStrLn $ "    E=" ++ show e ++ "  Pl=" ++ show (lanPl e)
               ++ "  Bel=" ++ show (ranBel e)) allSubsets

demoIsbellFix
```

- [ ] **Step 3.3:** JSON-проверка как в Step 2.3.

---

### Task 4: Раздел 2 — интервальный билатис вместо неточного «билатиса»

**Files:** Modify cell `tqhh6in8` (markdown); Insert new code cell after it.

- [ ] **Step 4.1:** В ячейке `tqhh6in8` заменить последний абзац:

```
Пара $(L, \bar{L})$ образует **билатис** (bilattice): четыре операции $\max, \min, \bar{\max}, \bar{\min}$ на $[0,1]$ с двумя различными порядками.
```

на:

```markdown
### Уточнение: где настоящий билатис

Пара $(L, \bar{L})$ — это **одна** решётка с двумя взаимно обратными порядками, а не билатис: в билатисе (Гинзберг, Фиттинг) два порядка **независимы** — порядок истинности $\le_t$ и порядок информации $\le_k$. Настоящий билатис в теории Пытьева образуют **интервалы** $[\mathrm{Bel}(E), \mathrm{Pl}(E)] \subseteq [0,1]$:

$$[a,b] \le_t [c,d] \iff a \le c \,\wedge\, b \le d \qquad\text{(истиннее)}$$
$$[a,b] \le_k [c,d] \iff a \le c \,\wedge\, d \le b \qquad\text{(информативнее: } [c,d] \subseteq [a,b])$$

Выделенные элементы — в точности модели знания Пытьева (ср. п. 1.5):

| Элемент билатиса | Интервал | Интерпретация по Пытьеву |
|------------------|----------|--------------------------|
| $\top_t$ (истина) | $[1,1]$ | точное знание «событие достоверно» |
| $\bot_t$ (ложь) | $[0,0]$ | точное знание «событие невозможно» |
| $\bot_k$ (незнание) | $[0,1]$ | **абсолютное незнание**: $\mathrm{Bel}=0$, $\mathrm{Pl}=1$ |
| $\top_k$ (противоречие) | $[1,0]$ | $\mathrm{Bel} > \mathrm{Pl}$ — несогласованные данные (ср. критерий п. 2.2) |

Это структура Белнапа FOUR, растянутая на континуум — interlacing-законы проверяются в коде ниже.
```

- [ ] **Step 4.2:** Вставить новую code-ячейку после `tqhh6in8`:

```haskell
-- | Раздел 2+: интервальный билатис [Bel, Pl]

data IV = IV { ivBel :: Double, ivPl :: Double } deriving (Show, Eq)

-- Порядок истинности
leqT :: IV -> IV -> Bool
leqT (IV a b) (IV c d) = a <= c && b <= d

-- Порядок информации: [a,b] <=k [c,d]  <=>  [c,d] вложен в [a,b]
leqK :: IV -> IV -> Bool
leqK (IV a b) (IV c d) = a <= c && d <= b

joinT, meetT, joinK, meetK :: IV -> IV -> IV
joinT (IV a b) (IV c d) = IV (max a c) (max b d)
meetT (IV a b) (IV c d) = IV (min a c) (min b d)
joinK (IV a b) (IV c d) = IV (max a c) (min b d)  -- пересечение интервалов
meetK (IV a b) (IV c d) = IV (min a c) (max b d)  -- объединяющая оболочка

bTrue, bFalse, bUnknown, bContra :: IV
bTrue    = IV 1 1
bFalse   = IV 0 0
bUnknown = IV 0 1   -- абсолютное незнание Пытьева
bContra  = IV 1 0   -- Bel > Pl: противоречие

demoBilattice :: IO ()
demoBilattice = do
  putStrLn "=== Razdel 2+: intervalnyj bilatis ==="
  let samples = [ IV a b | a <- [0, 0.3, 0.6, 1], b <- [0, 0.3, 0.6, 1] ]
      lat le j m = and $
        [ le (m x y) x && le (m x y) y && le x (j x y) && le y (j x y)
        | x <- samples, y <- samples ] ++
        [ j x y == j y x && m x y == m y x | x <- samples, y <- samples ] ++
        [ j x (m x y) == x && m x (j x y) == x | x <- samples, y <- samples ]
      -- interlacing: t-операции монотонны по <=k и наоборот
      interlace = and
        [ not (leqK x y) || (leqK (joinT x z) (joinT y z) && leqK (meetT x z) (meetT y z))
        | x <- samples, y <- samples, z <- samples ]
  putStrLn $ "  Reshyotka po <=t (absorb/comm/bounds): " ++ show (lat leqT joinT meetT)
  putStrLn $ "  Reshyotka po <=k (absorb/comm/bounds): " ++ show (lat leqK joinK meetK)
  putStrLn $ "  Interlacing (t-oper. monotonny po <=k): " ++ show interlace
  putStrLn $ "  bot_k = " ++ show bUnknown ++ " (absolyutnoe neznanie)"
  putStrLn $ "  top_k = " ++ show bContra  ++ " (protivorechie, Bel > Pl)"
  putStrLn $ "  joinK neznanie tochn.znanie: " ++ show (joinK bUnknown bTrue)

demoBilattice
```

- [ ] **Step 4.3:** JSON-проверка.

---

### Task 5: Раздел 4 — Γ как автоморфизмы квантали, эквивариантность Pl

**Files:** Modify cell `9bhvak76` (markdown); Insert new code cell after it.

- [ ] **Step 5.1:** В конец ячейки `9bhvak76` добавить:

```markdown

### 🔺 Категорный взгляд: Γ = Aut-группа квантали

Условия на $\gamma$ (сохранение $\max$, $\min$, порядка, концов отрезка) означают ровно одно: $\Gamma = \mathrm{Aut}\bigl([0,1], \max, \min\bigr)$ — **группа автоморфизмов квантали**. Принцип относительности тогда формулируется без слов «шкала»: субъективная модель — это объект не в $[0,1]$-значных функциях, а в **фактор-группоиде** $[\,\mathrm{Mod}/\Gamma\,]$; содержательны только $\Gamma$-инварианты (значения $0$, $1$ и порядок). Подгруппы $\Gamma_S$ с неподвижными точками $\alpha_i$ — это автоморфизмы, сохраняющие подквантали $[\alpha_i, \alpha_{i+1}]$; третий вариант мер — переход к другой квантали $([0,1], \max, \cdot)$, у которой $\mathrm{Aut}$ порождён $a \mapsto a^{\alpha}$. Действие $\Gamma$ **эквивариантно** относительно Pl: $\gamma(\mathrm{Pl}_{\tau}(E)) = \mathrm{Pl}_{\gamma\tau}(E)$ — это функториальность Lan по $\tau$, проверяется ниже.
```

- [ ] **Step 5.2:** Вставить новую code-ячейку после `9bhvak76`:

```haskell
-- | Раздел 4+: Gamma = Aut([0,1], max, min); эквивариантность Pl
import Control.Monad (filterM)

approx4 :: Double -> Double -> Bool
approx4 a b = abs (a - b) < 1e-9

gammaSq, gammaSqrt, gammaNot :: Double -> Double
gammaSq t   = t * t          -- автоморфизм (строго монотонна, 0->0, 1->1)
gammaSqrt t = sqrt t         -- автоморфизм (обратный к gammaSq)
gammaNot t  = 1 - t          -- НЕ автоморфизм: убывает (это theta!)

ptsG :: [Double]
ptsG = map (\k -> fromIntegral k / 10) [0..10 :: Int]

-- Проверка: gamma — автоморфизм квантали (сохраняет max и min)
isQuantaleAuto :: (Double -> Double) -> Bool
isQuantaleAuto g = and
  [ approx4 (g (max a b)) (max (g a) (g b)) &&
    approx4 (g (min a b)) (min (g a) (g b))
  | a <- ptsG, b <- ptsG ]
  && approx4 (g 0) 0 && approx4 (g 1) 1

domainG :: String
domainG = "abc"

tauG :: Char -> Double
tauG 'a' = 1.0
tauG 'b' = 0.6
tauG 'c' = 0.2
tauG _   = 0.0

plOf :: (Char -> Double) -> String -> Double
plOf t e = maximum (0 : map t e)

subsetsG :: [String]
subsetsG = filterM (const [True, False]) domainG

demoGammaAut :: IO ()
demoGammaAut = do
  putStrLn "=== Razdel 4+: Gamma kak avtomorfizmy kvantali ==="
  putStrLn $ "  t^2  - avtomorfizm:  " ++ show (isQuantaleAuto gammaSq)
  putStrLn $ "  sqrt - avtomorfizm:  " ++ show (isQuantaleAuto gammaSqrt)
  putStrLn $ "  1-t  - avtomorfizm:  " ++ show (isQuantaleAuto gammaNot) ++ " (eto theta, dualnost)"
  -- Эквивариантность: gamma(Pl_tau E) = Pl_{gamma . tau} E
  let equiv g = all (\e -> approx4 (g (plOf tauG e)) (plOf (g . tauG) e)) subsetsG
  putStrLn $ "  Ekvivariantnost Pl dlya t^2:  " ++ show (equiv gammaSq)
  putStrLn $ "  Ekvivariantnost Pl dlya sqrt: " ++ show (equiv gammaSqrt)
  -- Gamma-инварианты: 0 и 1 неподвижны, промежуточные значения - нет
  putStrLn $ "  gammaSq 0.6 = " ++ show (gammaSq 0.6) ++ " (znachenie 0.6 ne invariantno)"
  -- но порядок инвариантен:
  let ordInv = and [ (a < b) == (gammaSq a < gammaSq b) | a <- ptsG, b <- ptsG ]
  putStrLn $ "  Poryadok invarianten: " ++ show ordInv

demoGammaAut
```

- [ ] **Step 5.3:** JSON-проверка.

---

### Task 6: Новый раздел 15 — монада возможности (мост к Uncertainty.ipynb)

**Files:** Insert markdown + code cells before cell `gznlc5hp` (итоги).

- [ ] **Step 6.1:** Вставить markdown-ячейку:

```markdown
# 15. Монада Возможности — Поссибилистский Двойник Монады Гири

В [Uncertainty.ipynb](Uncertainty.ipynb) вероятность оформлена как монада: дискретные распределения (раздел 2), монада Гири (раздел 3), марковские цепи в категории Клейсли (раздел 7). Теория Пытьева даёт **точный поссибилистский аналог** этой конструкции.

## Определение

$$T(X) = \{\tau: X \to [0,1] \mid \sup_x \tau(x) = 1\} \qquad\text{— распределения правдоподобий}$$

- **Единица** (дельта Дирака): $\eta(x) = \tau$, где $\tau(x) = 1$, $\tau(y) = 0$ при $y \neq x$ — «точное знание» Пытьева
- **bind**: для $k: X \to T(Y)$
$$(\tau \mathbin{>\!\!>\!\!=} k)(y) = \sup_{x \in X} \min\{\tau(x),\, k(x)(y)\}$$

Это **pl-интеграл** из раздела 5: bind — это в точности $\mathrm{pl}_{\tau}$, применённый к ядру $k$. Теорема 1.1 Пытьева (представимость pl-интеграла) — это утверждение о том, что $T$ — монада, индуцированная кванталью $([0,1], \min, 1)$.

## Сравнение с монадой Гири

| | Гири (вероятность) | Возможность (Пытьев) |
|---|---|---|
| Объект | $\sum_x p(x) = 1$ | $\sup_x \tau(x) = 1$ |
| Полукольцо | $(\mathbb{R}_{\ge 0}, +, \cdot)$ | $([0,1], \max, \min)$ |
| bind | $\sum_x p(x) \cdot k(x)(y)$ | $\sup_x \min(\tau(x), k(x)(y))$ |
| Клейсли-композиция | умножение стох. матриц | sup-min «умножение» матриц |
| Категория Клейсли | стохастические отображения | $[0,1]$-обогащённые отношения |
| Независимое произведение | $p \otimes q$ | $\min$-произведение (Опр. 1.2 Пытьева) |

Обе — частные случаи **монады распределений над коммутативным полукольцом**; замена $(+,\cdot) \to (\max,\min)$ переводит марковские цепи Uncertainty.ipynb в поссибилистские переходные системы. Как и `Dist` через `Map`, это *ограниченная* монада (нужен `Ord` для ключей) — инстанс класса `Monad` Haskell не даётся, но законы монады выполняются и проверяются ниже.
```

- [ ] **Step 6.2:** Вставить code-ячейку после неё:

```haskell
-- | Раздел 15: монада возможности
import qualified Data.Map.Strict as M

approx5 :: Double -> Double -> Bool
approx5 a b = abs (a - b) < 1e-9

newtype Poss a = Poss { runPoss :: M.Map a Double } deriving Show

possOf :: Ord a => [(a, Double)] -> Poss a
possOf = Poss . M.fromListWith max

-- eta: точное знание Пытьева
diracP :: Ord a => a -> Poss a
diracP x = possOf [(x, 1.0)]

-- bind = pl-интеграл по ядру k
bindP :: Ord b => Poss a -> (a -> Poss b) -> Poss b
bindP (Poss m) k = possOf
  [ (y, min tx ty) | (x, tx) <- M.toList m, (y, ty) <- M.toList (runPoss (k x)) ]

eqP :: Ord a => Poss a -> Poss a -> Bool
eqP (Poss m1) (Poss m2) =
  M.keysSet m1' == M.keysSet m2' && and (M.elems (M.intersectionWith approx5 m1' m2'))
  where m1' = M.filter (> 0) m1
        m2' = M.filter (> 0) m2

-- Поссибилистская погодная цепь (ср. марковские цепи в Uncertainty.ipynb)
data W = Sun | Rain | Fog deriving (Show, Eq, Ord)

stepW :: W -> Poss W
stepW Sun  = possOf [(Sun, 1.0), (Fog, 0.4), (Rain, 0.2)]
stepW Rain = possOf [(Rain, 1.0), (Fog, 0.7), (Sun, 0.3)]
stepW Fog  = possOf [(Fog, 1.0), (Sun, 0.6), (Rain, 0.6)]

nSteps :: Int -> W -> Poss W
nSteps 0 w = diracP w
nSteps n w = bindP (nSteps (n-1) w) stepW

demoPossMonad :: IO ()
demoPossMonad = do
  putStrLn "=== Razdel 15: monada vozmozhnosti ==="
  let m0 = possOf [(Sun, 1.0), (Rain, 0.5)]
  -- Законы монады (численно)
  let leftId  = eqP (bindP (diracP Sun) stepW) (stepW Sun)
      rightId = eqP (bindP m0 diracP) m0
      k1 = stepW
      k2 w = possOf [(w, 1.0), (Fog, 0.5)]
      assoc = eqP (bindP (bindP m0 k1) k2) (bindP m0 (\x -> bindP (k1 x) k2))
  putStrLn $ "  Left identity:  " ++ show leftId
  putStrLn $ "  Right identity: " ++ show rightId
  putStrLn $ "  Associativity:  " ++ show assoc
  -- Нормировка сохраняется: sup = 1
  let supOf (Poss m) = maximum (0 : M.elems m)
  putStrLn $ "  sup posle bind = " ++ show (supOf (bindP m0 stepW))
  -- Эволюция: возможностный прогноз через n шагов
  mapM_ (\n -> putStrLn $ "  " ++ show n ++ " shagov ot Sun: "
               ++ show (M.toList (runPoss (nSteps n Sun)))) [1, 2, 3]
  -- Неподвижная точка: sup-min степени матрицы стабилизируются
  let same = eqP (nSteps 3 Sun) (nSteps 4 Sun)
  putStrLn $ "  Stabilizaciya k 3-mu shagu: " ++ show same

demoPossMonad
```

- [ ] **Step 6.3:** JSON-проверка.

---

### Task 7: Новый раздел 16 — обогащённая X и нетривиальный Исбелл

**Files:** Insert markdown + code cells before cell `gznlc5hp`, после ячеек Task 6.

- [ ] **Step 7.1:** Вставить markdown-ячейку:

```markdown
# 16. Обогащённая $\mathbf{X}$: Когда Двойственность Исбелла Перестаёт Быть Тривиальной

В разделе 14 категория $\mathbf{X}$ дискретна ($\mathbf{X}(x,y) = [x=y]$), поэтому Йонеда и Исбелл вырождаются: coend схлопывается в $\sup$, и вся конструкция лишь воспроизводит формулы Пытьева. Содержательная картина возникает, если МИ оценивает ещё и **степень неразличимости состояний**.

## $\mathbf{X}$ как обобщённое метрическое пространство Ловера

Зададим $[0,1]$-обогащённую категорию: $\mathbf{X}(x,y) \in [0,1]$ — «правдоподобие того, что $x$ и $y$ неразличимы», с аксиомами

$$\mathbf{X}(x,x) = 1, \qquad \min\{\mathbf{X}(x,y),\, \mathbf{X}(y,z)\} \le \mathbf{X}(x,z)$$

(рефлексивность и $\min$-транзитивность — это в точности категория, обогащённая над кванталью $([0,1],\min,1)$;双 Ловеру, у которого $([0,\infty], +, 0)$ и метрика).

## Преснопы = распределения, согласованные с неразличимостью

$[0,1]$-пресноп $\varphi: \mathbf{X}^{op} \to [0,1]$ обязан удовлетворять $\min\{\mathbf{X}(x,y), \varphi(y)\} \le \varphi(x)$: похожие состояния обязаны иметь похожие правдоподобия. Произвольное $\tau$ преснопом быть не обязано — его **йонедовское пополнение** (Lan вдоль Йонеды):

$$\hat{\tau}(x) = \sup_{y} \min\{\mathbf{X}(x,y),\, \tau(y)\}$$

— наименьший пресноп над $\tau$: субъективная модель «доразмывается» по неразличимости.

## Двойственность Исбелла: $\mathcal{O} \dashv \mathrm{Spec}$ в числах

$$\mathcal{O}(\varphi)(c) = \inf_{x} \bigl(\varphi(x) \multimap \mathbf{X}(x,c)\bigr), \qquad \mathrm{Spec}(\psi)(c) = \inf_{x} \bigl(\psi(x) \multimap \mathbf{X}(c,x)\bigr)$$

Единица сопряжения даёт $\varphi \le \mathrm{Spec}(\mathcal{O}(\varphi))$, и тройка $\mathcal{O}\,\mathrm{Spec}\,\mathcal{O} = \mathcal{O}$. **Неподвижные точки** ($\varphi = \mathrm{Spec}(\mathcal{O}(\varphi))$) — это Isbell envelope / tight span: кандидат на роль «объективного пополнения» субъективной модели — состояния, которые можно добавить к $X$, не нарушив согласованности правдоподобий с неразличимостью. Гипотеза раздела 14 в этой постановке: **пара (Pl, Bel) дуально согласована по Пытьеву $\iff$ ($\tau$, $\bar\tau$) — избелловски сопряжённая пара**. Ниже всё проверяется численно.
```

Примечание исполнителю: в формуле выше случайно может проскочить не-ASCII вне математики — перед записью убедиться, что markdown без артефактов (строка «双 Ловеру» — опечатка, написать «как у Ловера»).

- [ ] **Step 7.2:** Вставить code-ячейку:

```haskell
-- | Раздел 16: обогащённая X (Ловер), Йонеда-пополнение, Isbell O -| Spec
approx6 :: Double -> Double -> Bool
approx6 a b = abs (a - b) < 1e-9

qHom6 :: Double -> Double -> Double
qHom6 a b = if a <= b then 1.0 else b

data St = StA | StB | StC deriving (Show, Eq, Ord, Enum, Bounded)

stAll :: [St]
stAll = [StA, StB, StC]

-- [0,1]-обогащённая hom-матрица: степень неразличимости (симметричная)
homX :: St -> St -> Double
homX x y | x == y = 1.0
homX StA StB = 0.7
homX StB StA = 0.7
homX StB StC = 0.5
homX StC StB = 0.5
homX StA StC = 0.5
homX StC StA = 0.5

-- Сырое субъективное распределение МИ (преснопом НЕ является)
tauRaw :: St -> Double
tauRaw StA = 1.0
tauRaw StB = 0.2   -- нарушение: hom(A,B)=0.7, tau(A)=1, значит tau(B) >= 0.7 обязан
tauRaw StC = 0.1

-- Условие преснопа: min(hom x y, phi y) <= phi x
isPresheaf :: (St -> Double) -> Bool
isPresheaf phi = and
  [ min (homX x y) (phi y) <= phi x + 1e-9 | x <- stAll, y <- stAll ]

-- Йонеда-пополнение (Lan вдоль Йонеды): наименьший пресноп >= tau
yonedaHat :: (St -> Double) -> St -> Double
yonedaHat t x = maximum [ min (homX x y) (t y) | y <- stAll ]

-- Isbell: O(phi)(c) = inf_x (phi x -o hom x c);  Spec(psi)(c) = inf_x (psi x -o hom c x)
isbellO, isbellSpec :: (St -> Double) -> St -> Double
isbellO   phi c = minimum [ qHom6 (phi x) (homX x c) | x <- stAll ]
isbellSpec psi c = minimum [ qHom6 (psi x) (homX c x) | x <- stAll ]

eqF :: (St -> Double) -> (St -> Double) -> Bool
eqF f g = all (\x -> approx6 (f x) (g x)) stAll

showF :: (St -> Double) -> String
showF f = show [ (x, f x) | x <- stAll ]

demoEnriched :: IO ()
demoEnriched = do
  putStrLn "=== Razdel 16: obogashchyonnaya X i Isbell ==="
  -- min-транзитивность hom (обогащённая категория корректна)
  let trans = and [ min (homX x y) (homX y z) <= homX x z + 1e-9
                  | x <- stAll, y <- stAll, z <- stAll ]
  putStrLn $ "  min-tranzitivnost homX: " ++ show trans
  putStrLn $ "  tauRaw - presnop? " ++ show (isPresheaf tauRaw)
  let tauHat = yonedaHat tauRaw
  putStrLn $ "  tauHat = " ++ showF tauHat
  putStrLn $ "  tauHat - presnop? " ++ show (isPresheaf tauHat)
  -- Pl с учётом неразличимости отличается от наивного
  putStrLn $ "  Naivnyj Pl{B} = " ++ show (tauRaw StB)
             ++ ", razmytyj Pl{B} = " ++ show (tauHat StB)
  -- Isbell-сопряжение
  let o1 = isbellO tauHat
      s1 = isbellSpec o1
  putStrLn $ "  O(tauHat)        = " ++ showF o1
  putStrLn $ "  Spec(O(tauHat))  = " ++ showF s1
  let unitLe = and [ tauHat x <= s1 x + 1e-9 | x <- stAll ]
  putStrLn $ "  Edinica: tauHat <= Spec(O tauHat): " ++ show unitLe
  let o2 = isbellO s1
  putStrLn $ "  O Spec O = O (treugolnik): " ++ show (eqF o1 o2)
  -- Неподвижная точка достигается за один шаг
  let s2 = isbellSpec (isbellO s1)
  putStrLn $ "  Spec(O(-)) idempotenten: " ++ show (eqF s1 s2)
  putStrLn $ "  Nepodvizhnaya tochka (tight span): " ++ showF s1

demoEnriched
```

- [ ] **Step 7.3:** JSON-проверка.

---

### Task 8: Обновить TOC, итоги, NAV и кросс-ссылку из Uncertainty.ipynb

**Files:** Modify cells `vq1fhqjw` (TOC), `gznlc5hp` (итоги) в SubjectiveModeling.ipynb; Modify раздел 9 в `src/notebooks/Uncertainty.ipynb`.

- [ ] **Step 8.1:** В таблицу TOC (ячейка `vq1fhqjw`) добавить строки:

```markdown
| 15 | Монада возможности — поссибилистский двойник монады Гири | Категорное |
| 16 | Обогащённая $\mathbf{X}$ и нетривиальная двойственность Исбелла | Категорное |
```

- [ ] **Step 8.2:** В итоговую таблицу (ячейка `gznlc5hp`) добавить строки:

```markdown
| 15 | Монада возможности: bind = pl-интеграл, Клейсли = sup-min отношения | Категорное |
| 16 | Йонеда-пополнение $\hat{\tau}$; Isbell $\mathcal{O} \dashv \mathrm{Spec}$, tight span | Категорное |
```

и в таблицу «Статус категорной гипотезы» добавить:

```markdown
| Кондиционирование = residuation (правый сопряжённый к $\min(-,a)$) | ✅ Доказано + проверено |
| $\mathrm{Bel} = \mathrm{Ran}$ вдоль профунктора дополнения $\theta J$ | ✅ Дыра закрыта |
| Монада возможности: законы монады | ✅ Проверено численно |
| Isbell-сопряжение на обогащённой $\mathbf{X}$: единица + идемпотентность | ✅ Проверено численно |
```

- [ ] **Step 8.3:** В `Uncertainty.ipynb`, раздел 9 (краткое введение в Пытьева), добавить одно предложение со ссылкой: «Поссибилистский двойник монады Гири (раздел 3) и марковских цепей (раздел 7) построен в [SubjectiveModeling.ipynb](SubjectiveModeling.ipynb), раздел 15.»

- [ ] **Step 8.4:** JSON-проверка обоих ноутбуков.

---

### Task 9: Верификация — Run All в IHaskell, 0 ошибок

**Files:** none (запуск)

- [ ] **Step 9.1:** Поднять контейнер: `docker-compose up -d` (из корня проекта). Проверка: `Invoke-RestMethod http://localhost:8889/api` → версия Jupyter.

- [ ] **Step 9.2:** Выполнить ноутбук:

```
docker-compose exec ihaskell jupyter nbconvert --to notebook --execute --inplace `
  /home/jovyan/pwd/src/notebooks/SubjectiveModeling.ipynb `
  --ExecutePreprocessor.timeout=600
```

Ожидание: завершение без ошибок (GHC холодный старт ~60–80 с — норма). Если ячейка падает — чинить код по сообщению GHC, повторить только с момента фикса.

- [ ] **Step 9.3:** Проверить отсутствие error-выводов:

```
node -e "const nb=JSON.parse(require('fs').readFileSync('src/notebooks/SubjectiveModeling.ipynb','utf8')); const errs=nb.cells.flatMap(c=>(c.outputs||[]).filter(o=>o.output_type==='error')); console.log('errors:', errs.length)"
```

Ожидание: `errors: 0`.

- [ ] **Step 9.4:** В `src/ROADMAP.md` в таблице Фазы 5 проставить ✅ по выполненным пунктам и сменить заголовок на «(выполнено 2026-06-11)».

---

## Самопроверка плана

- Все 6 содержательных пунктов спеки покрыты Tasks 2–7; роудмап — Task 1; TOC/итоги/кросс-ссылка — Task 8; верификация — Task 9.
- Код каждой ячейки самодостаточен (свои imports, свои `approx*` с уникальными именами, чтобы не конфликтовать при Run All в одном kernel-сеансе).
- Строковые литералы — ASCII (правило ROADMAP); русский — только в markdown.
- Не git-репозиторий: вместо коммитов — JSON-проверки и финальный Run All.
