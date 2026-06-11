# Спека: библиотека категорного ядра `src/lib/` + миграция ноутбуков

Дата: 2026-06-11. Статус: на ревью.

## Цель

Извлечь общую математику теорий неопределённости (Пытьев, возможность, вероятность) в мини-библиотеку Haskell-модулей, подключаемую в IHaskell-ноутбуки через `:load`. Полностью мигрировать кодовые ячейки `SubjectiveModeling.ipynb` и тематически пересекающиеся ячейки `Uncertainty.ipynb` на эту библиотеку. Ноутбуки становятся отладочной витриной библиотеки: все проверки законов — `True` на экране.

## Решения (зафиксированы с пользователем)

1. **Подключение:** модули `.hs` в `src/lib/`, один `:load` со всеми модулями в setup-ячейке каждого мигрируемого ноутбука (вариант A из обсуждения). Повторных `:load` в теле ноутбука нет (сбрасывает контекст REPL).
2. **Глубина миграции:** вариант B — полная миграция обоих ноутбуков. Дубли `SubjModel` (3 шт.) и локальные `approx*`/`qHom*` (5 шт.) из SubjectiveModeling удаляются; в Uncertainty мигрируют ячейки, пересекающиеся с ядром, ячейки про монаду Гири/стохастические матрицы без пересечения — не трогаются. Новый витринный ноутбук НЕ создаётся.
3. **Параметризация полукольцом:** ДА. Общая монада распределений `Dist r a` над `class Semiring r`; возможность и дискретная вероятность — её специализации.
4. **Гибридная абстракция (решение от 2026-06-11):** ядро (`Quantale`, `KanExtension`, `Distribution`) полиморфно по классам `Lattice`/`Quantale` с инстансами `UnitInterval` и `Bool` (Pl над Bool = ∃, Bel = ∀ — демонстрация в ноутбуке). `Bitopos` и `SubjectiveModel` остаются конкретными на `UnitInterval`: инволюция θ, энтропии и топологии Скотта содержательно привязаны к [0,1]. Сравнение с допуском — `class ApproxEq`.
5. **Комментарии-расширения:** в каждом модуле библиотеки оставлять блочные комментарии `-- ИДЕИ РАСШИРЕНИЯ:` с конкретными направлениями (Лукасевич/тропическое квантале, некоммутативные квантали, произвольная инволюция θ как параметр, непрерывные домены вместо списков, связь с Giry через подходящую монаду и т.п.).

## Структура библиотеки (5 модулей, зависимости только сверху вниз)

### 1. `src/lib/Quantale.hs`
Ядро без зависимостей. Полиморфное.
- `class ApproxEq q where (=~) :: q -> q -> Bool` — инстансы: `UnitInterval` (1e-9), `Bool` (==).
- `class (Ord q, ApproxEq q) => Lattice q where ljoin, lmeet :: q -> q -> q; lbot, ltop :: q` + `joins, meets :: Lattice q => [q] -> q` (свёртки, joins [] = lbot).
- `class Lattice q => Quantale q where qTensor :: q -> q -> q; qUnit :: q; qHom :: q -> q -> q` (residuation; для фреймов qTensor = lmeet).
- `newtype UnitInterval = UI Double deriving (Eq, Ord, Show)` — инстанс: join=max, meet=min=tensor, qHom a b = if a<=b then top else b. Конструктор `ui :: Double -> UnitInterval` (с clamp 0..1), `unUI`.
- Инстанс `Bool`: join=||, meet=&&=tensor, qHom a b = not a || b (импликация).
- Только для UnitInterval: инволюция `theta`; Γ: `isQuantaleAuto`, `gammaGrid`, `gammaSq`, `gammaSqrt`.
- Полиморфные проверки законов: `checkResiduationAdj`, `checkFrameDistributivity :: Quantale q => [q] -> Bool` (по переданной сетке).

### 2. `src/lib/KanExtension.hs`
Импортирует Quantale. Всё на конечных списках. Полностью полиморфен по `Quantale q`.
- Тип профунктора: `type Prof q a e = e -> a -> q`.
- `lanAlong :: Quantale q => Prof q a e -> [a] -> (a -> q) -> e -> q` — coend: `joins [qTensor (prof e x) (tau x)]`.
- `ranAlong :: Quantale q => Prof q a e -> [a] -> (a -> q) -> e -> q` — end: `meets [qHom (prof e x) (tauBar x)]`.
- Частные случаи: `memberProf` (x∈E → qUnit | lbot), `complementProf`; `plMeasure = lanAlong memberProf`, `belMeasure = ranAlong complementProf`. Над Bool: Pl = ∃, Bel = ∀ (демо в ноутбуке).
- Обогащённый hom: `type EnrichedHom q a = a -> a -> q`; `isTransitive` (tensor-транзитивность), `isPresheaf`, `yonedaHat` (Lan вдоль Йонеды).
- Isbell: `isbellO`, `isbellSpec :: Quantale q => EnrichedHom q a -> [a] -> (a -> q) -> a -> q`; `checkIsbellUnit`, `checkIsbellTriangle`.

### 3. `src/lib/Bitopos.hs`
Импортирует Quantale.
- Топологии Скотта на [0,1]: `scottUpOpen t x = x > t`, `scottDownOpen t x = x < t`.
- Индуцированная битопология на X: `scottUpOnX`, `scottDownOnX :: (a -> Double) -> Double -> [a] -> [a]`.
- Интервальный билатис: `data IV = IV { ivBel, ivPl :: Double }`; `leqT`, `leqK`; `joinT/meetT/joinK/meetK`; константы `bTrue/bFalse/bUnknown/bContra`; проверки `checkLatticeT`, `checkLatticeK`, `checkInterlacing` (по сетке-выборке).

### 4. `src/lib/Distribution.hs`
Импортирует Quantale. Параметризация полукольцом.
- `class Semiring r where szero, sone :: r; splus, stimes :: r -> r -> r`.
- Общий инстанс-мост: любое квантале — идемпотентное полукольцо. Из-за запрета на сложные расширения — без `instance Quantale q => Semiring q` (overlap); вместо этого конкретные инстансы: `Semiring UnitInterval` (max/min — возможность), `newtype ProbW = ProbW Double` (+, × — вероятность), `Semiring Bool` (||/&& — достижимость).
- `newtype Dist r a = Dist { runDist :: Map a r }`.
- `diracD :: (Semiring r, Ord a) => a -> Dist r a`; `bindD :: (Semiring r, Ord b) => Dist r a -> (a -> Dist r b) -> Dist r b` (свёртка через splus/stimes, агрегация `fromListWith splus`).
- `type Poss a = Dist UnitInterval a`; удобства `possOf`, `eqPoss` (сравнение через ApproxEq, нули отфильтрованы); `kleisliD` (композиция ядер); `nStepsD`.
- Проверки законов монады на конкретных данных: `checkMonadLaws :: ... -> Bool` (left/right id, assoc) — работает для любого r с Eq-сравнением через переданный предикат.

### 5. `src/lib/SubjectiveModel.hs`
Импортирует Quantale, KanExtension. Слой Пытьева.
- `data SubjModel a = SubjModel { smDomain :: [a], smTau, smTauBar :: a -> Double }` — единственное определение на проект.
- Конструкторы: `absoluteIgnorance`, `exactKnowledge`, `dualConsistent` (tauBar = theta . tau).
- Меры: `smPl`, `smBel` (через plMeasure/belMeasure из KanExtension); образ `imageModel`; `applyGamma`.
- Интегралы: `plIntegral` (sup-min), `belIntegral` (inf-max).
- Независимость: `plJointDist` (min), `belJointDist` (max).
- Кондиционирование = residuation: `condTau :: Ord b => [(a,b)] -> ((a,b) -> Double) -> b -> a -> Double` через `qHom` маргинала.
- Энтропии: `subjInformativity`, `subjUncertainty`, `dualEntropy`, `thirdVariantEntropy`.
- Идентификация: `optimalDecision` (минимакс по матрице потерь).
- Комбинирование: `compMatrix`, `matrixDist`, `combineDistributions` (матрицы парных сравнений, п. 2.2).

## Ограничения среды (из ROADMAP, обязательны)

- Строковые литералы в Haskell — ASCII; `\xNNNN`, не `\uNNNN`. Комментарии в модулях — можно по-русски (файлы UTF-8), но вывод `putStrLn` — ASCII-транслит, как в существующих ячейках.
- Без `XQuantifiedConstraints`; `data` с функциональными полями не полиморфны по контексту (SubjModel уже такой — ок).
- `:load` в IHaskell: один раз, в setup-ячейке, все модули перечислены в одной команде; пути относительные от `src/notebooks/`: `:load ../lib/Quantale.hs ../lib/KanExtension.hs ../lib/Bitopos.hs ../lib/Distribution.hs ../lib/SubjectiveModel.hs`. После `:load` — явные `import` модулей.
- Контейнер: одноразовый `docker run --rm -v <root>:/home/jovyan/pwd gibiansky/ihaskell jupyter nbconvert --execute --inplace ...` (порт 8889 занят соседним проектом — не трогать).

## Миграция SubjectiveModeling.ipynb

- Setup-ячейка (`5jry916m`): добавить `:load` и импорты модулей; существующие импорты сохранить.
- 8 кодовых ячеек переписываются: остаются демо-данные, вызовы библиотеки, проверки законов и `putStrLn`-вывод. Удаляются: 3 определения `SubjModel`, локальные `plMeasure/belMeasure/plIntegral/belIntegral`, 5 копий `approx*`, `qHom*`-дубли, локальные `compMatrix` и пр. — всё это теперь из библиотеки.
- Демо-данные едины: τ на `{a,b,c}` = (1.0, 0.6, 0.2); hom-матрица неразличимости (1/0.7/0.5); погодная цепь Sun/Rain/Fog.
- Markdown-ячейки не меняются, кроме упоминаний «определим заново» там, где код теперь библиотечный (точечные правки по факту).

## Миграция Uncertainty.ipynb

- Setup-ячейка: тот же `:load`.
- Мигрируют: раздел 2 (дискретные распределения → `Dist ProbW`), раздел 7 (марковские цепи → `kleisliD`/`nStepsD` над ProbW), раздел 4 (нечёткая математика — операции min/max → Quantale), раздел 9 (живой код: та же погодная цепь над MaxMin и над ProbW рядом — «одна математика, две теории»).
- НЕ мигрируют: монада Гири (раздел 3, непрерывный случай), стохастические матрицы/теория меры (раздел 8), модальные логики (раздел 5), DSL (раздел 6).

## Верификация

1. Каждый модуль компилируется автономно: `docker run ... ghc -fno-code /home/jovyan/pwd/src/lib/<M>.hs` (или `runghc` со смоук-main — по факту окружения).
2. Run All обоих ноутбуков в одноразовом контейнере → 0 ошибок (`output_type == 'error'` отсутствует).
3. Числа в демо совпадают с дофазовыми выводами там, где данные не менялись.
4. Незакрытая верификация Фазы 5 закрывается этим же прогоном.

## ROADMAP

Новая «Фаза 6 — Библиотека категорного ядра src/lib» с таблицей: 5 модулей, миграция 2 ноутбуков, верификация. Внутри отметка, что Run All Фазы 5 закрыт прогоном Фазы 6. Правило в «Критические правила»: «`:load` — только в setup-ячейке, один раз, все модули сразу».

## Вне скоупа

- Cabal-пакет, собственный Docker-образ.
- Новый витринный ноутбук.
- Миграция остальных 16 ноутбуков.
- SVG-диаграммы для библиотеки (по желанию позже).
