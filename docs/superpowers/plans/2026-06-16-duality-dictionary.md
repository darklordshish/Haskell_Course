# План: ноутбук-словарь двойственности (Duality.ipynb)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Спека: `docs/superpowers/specs/2026-06-16-duality-dictionary-design.md`. Разделы независимы и **возобновляемы** — при упоре в лимит продолжить со следующего нетронутого раздела.

**Goal:** Справочник-ноутбук `Duality.ipynb`: парад двойственных конструкций, единая ось `C^op`, подача «примитивы → Кан-движок → всё через Кан».

**Architecture:** Каркас собирается node-скриптом `build_duality_scaffold.js` (титул, мотивация, сводная таблица, setup, NAV, и стаб-ячейки всех разделов с фиксированными id). Затем каждый раздел наполняется отдельным шагом — правкой своих ячеек по id (markdown + code + inline-SVG по канону Faza 6/Фазы B). Диаграммы — кит маркеров (`↣/↠/↔/⇒`), светлая палитра, ASCII-only, матсимволы `&#NNNN;`. Верификация — `nbconvert --execute` в контейнере.

**Tech Stack:** IHaskell/GHC (контейнер gibiansky/ihaskell), Node.js.

**Порядок разделов (спека):** 1 примитивы (mono/epi, вариантность функтора, algebra/coalgebra) → 2 Кан-движок (Lan/Ran) → 3 общие lim/colim через Кан → 4 формы `J` (terminal/initial, product/coproduct, equalizer/coequalizer, pullback/pushout) → 5 сопряжения (Ran_F Id / Lan_G Id) → 6 монады/комонады (Codensity=Ran f f, Density=Lan f f).

**Фиксированные id ячеек раздела `X`:** `dual_<X>_md` (теория+диаграмма) и `dual_<X>_hs` (Haskell). Слаги разделов: `monoepi`, `variance`, `algcoalg`, `kan`, `limcolim`, `termini`, `prodcoprod`, `equ`, `pbpo`, `adj`, `monadcomonad`.

---

### Task 0: Ветка

- [ ] `git checkout master; git pull; git checkout -b duality-notebook`

### Task 1: Каркас (build_duality_scaffold.js → Duality.ipynb)

**Files:** Create `src/scripts/duality/build_duality_scaffold.js`, `src/notebooks/Duality.ipynb`

- [ ] Скрипт пишет `src/notebooks/Duality.ipynb` (nbformat 4.5, kernel haskell, `JSON.stringify(nb,null,1)+'\n'`, UTF-8 без BOM). Состав ячеек по порядку, у каждой ASCII-id:
  1. `dual_setup` (code): `:set` расширений (RankNTypes, ScopedTypeVariables, TypeOperators, FlexibleInstances, FlexibleContexts, DeriveFunctor, GADTs), импорты `Data.Functor.Contravariant` (если есть) — иначе объявить локально, `putStrLn "\x2705 SETUP OK"`. (Без `:load` — словарь самодостаточен.)
  2. `dual_title` (md): `# 🔄 Словарь двойственности` + 1 абзац: одна ось `C^op`, подача примитивы→Кан→всё через Кан.
  3. `dual_motiv` (md): мотивация (см. скелет §0 ниже).
  4. `dual_toc` (md): сводная таблица (см. ниже) со ссылками на якоря `#dual-<slug>`.
  5. Для каждого slug по порядку: md-стаб `dual_<slug>_md` (`<a id="dual-<slug>"></a>` + `## <Заголовок>` + «*Раздел в наполнении — скелет по шаблону словаря.*») и code-стаб `dual_<slug>_hs` (комментарий `-- Haskell: <pair> — заполняется`).
  6. `dual_nav` (md): «Справочник-приложение, вне ствола 0–VI. ↩ [Путеводитель](README.ipynb)».
- [ ] Сводная таблица (md, вручную) — строки по всем разделам, колонки: `Пара | Двойственная | Идея | Через Кан? | Где в курсе | →`. Значения «Через Кан?»: mono/epi — нет (примитив), variance — нет, algebra/coalgebra — нет, остальные — да. «Где в курсе»: mono/epi→Toposes, variance→FunctorHierarchy, algebra/coalgebra→AlgebrasCoalgebras, kan→KanExtensions, limcolim/формы→KanExtensions+Toposes, adj→Adjunctions, monad/comonad→Monads/Comonads.
- [ ] Запуск: `node src/scripts/duality/build_duality_scaffold.js`; JSON-валидность.
- [ ] Якоря: каждый `#dual-<slug>` из таблицы присутствует ровно один раз (`<a id=...>`).
- [ ] Контейнер: `docker run --rm -v "<root>:/home/jovyan/pwd" gibiansky/ihaskell jupyter nbconvert --to notebook --execute --inplace /home/jovyan/pwd/src/notebooks/Duality.ipynb --ExecutePreprocessor.timeout=900` → 0 ошибок (исполняется только setup + пустые стабы).
- [ ] Commit: `git add src/scripts/duality src/notebooks/Duality.ipynb; git commit -m "duality: каркас Duality.ipynb (таблица + стабы разделов)"`

### Шаблон наполнения раздела (для Tasks 2+)

Каждый раздел (правка `dual_<slug>_md` + `dual_<slug>_hs`) состоит из:
1. **Идея** (1–2 строки): в чём пара, как один получается обращением стрелок / зеркалом `C^op`.
2. **Мат-определение** обоих членов + **универсальное свойство**.
3. **Парная диаграмма** (inline `<svg>` в md): левый/правый член бок о бок, видно обращение стрелок; для §4 — форма `J` в центре. Канон: светлая палитра, кит маркеров (`↣/↠/↔/⇒`), ASCII-only, матсимволы `&#NNNN;`.
4. **Haskell** обоих (исполняемый код в `dual_<slug>_hs`).
5. **«В чём двойственность»** — одна строка.
6. **«Где в курсе»** — ссылки на ноутбуки.
После каждого раздела: контейнер-прогон (0 ошибок), commit `duality: раздел <slug>`.

### Task 2 (v1-образец): Примитив mono/epi (slug `monoepi`)

- [ ] **Идея:** `mono` = лево-сократим (инъекция), `epi` = право-сократим (сюръекция); `mono в C = epi в C^op`. Примитив: чистое обращение стрелок, Каном не порождается.
- [ ] **Мат:** определения через сократимость + универсальная картинка (моно как `↣`, эпи как `↠`); напомнить (из ревью): iso = mono+epi только в сбалансированных (Set, топосы); `⤖` = биморфизм.
- [ ] **Диаграмма:** слева `A ↣ B` (хвостик), справа `A ↠ B` (двойная голова), подпись «обращение стрелок: `C ⇄ C^op`». Кит маркеров (хвостик/двойная голова как в Фазе B).
- [ ] **Haskell:** иллюстративно — `newtype Mono a b` / инъективность на примере `data`-конструктора; `epi`/сюръекция как покрытие. Минимальный исполняемый пример (например проверка инъективности функции на конечном типе).
- [ ] **Двойственность/курс:** строка + ссылка `[Toposes](Toposes.ipynb)` (классификатор подобъектов, `S ↣ Ω`).
- [ ] Контейнер-прогон, commit `duality: раздел monoepi`.

### Task 3 (v1-образец): Кан-движок Lan/Ran (slug `kan`)

- [ ] **Идея:** `Lan` (левое) ↔ `Ran` (правое) — зеркальная пара `C^op` (`(Lan_K F)^op ≅ Ran_{K^op}(F^op)`) и универсальный движок словаря.
- [ ] **Мат:** универсальные свойства `Nat(Lan_g h, f) ≅ Nat(h, f∘g)` и `Nat(f, Ran_g h) ≅ Nat(f∘g, h)`.
- [ ] **Диаграмма:** переиспользовать стиль `kan/lan_diagram.svg`/`ran_diagram.svg` (уже в каноне) — обе бок о бок, видно зеркало.
- [ ] **Haskell:** `data Lan g h a = forall b. Lan (g b -> a) (h b)`; `newtype Ran g h a = Ran { runRan :: forall b. (a -> g b) -> h b }`. Мини-демо.
- [ ] **Двойственность/курс:** строка + `[KanExtensions](KanExtensions.ipynb)`.
- [ ] Контейнер-прогон, commit `duality: раздел kan`.

### Task 4 (v1-образец): Форма `J` — product/coproduct (slug `prodcoprod`)

- [ ] **Идея:** `J` = дискретная пара; предел = произведение (конус справа), копредел = копроизведение (коконус слева); как Кан вдоль `J→1`.
- [ ] **Мат:** универсальные свойства `A×B` (проекции, `⟨f,g⟩`) и `A+B` (инъекции, `[f,g]`); обращение стрелок между ними.
- [ ] **Диаграмма:** центральный приём — `J` (две точки) в центре, слева коконус `A+B`, справа конус `A×B`. Кит стрелок; уникальные медиаторы пунктиром.
- [ ] **Haskell:** `(a,b)` с `fst/snd/(&&&)`; `Either a b` с `Left/Right/either`. Мини-демо двойственности (`(&&&)` vs `either`).
- [ ] **Двойственность/курс:** строка + `[TypeAlgebra](TypeAlgebra.ipynb)`, `[KanExtensions](KanExtensions.ipynb)`.
- [ ] Контейнер-прогон, commit `duality: раздел prodcoprod`.

### Каталог отложенных разделов (стабы из Task 1; наполняются позже, каждый — свой шаг по Шаблону)

Скелеты (математическое наполнение для будущих шагов; диаграмма+Haskell по шаблону):
- [ ] `variance` — ковариантный (`Functor`, `fmap`) vs контравариантный (`Contravariant`, `contramap`); контравариантный `C→D` = ковариантный `C^op→D`. Курс: FunctorHierarchy.
- [ ] `algcoalg` — F-алгебра `F a -> a` (cata, начальная) vs F-коалгебра `a -> F a` (ana, финальная); неподвижные точки, обращение стрелки структуры. Вне Кана. Курс: AlgebrasCoalgebras.
- [ ] `limcolim` — общий `lim = Ran` вдоль `J→1`, `colim = Lan` вдоль `J→1`; конус/коконус. Курс: KanExtensions.
- [ ] `termini` — `J=∅`: терминальный (`()`, пустой конус) vs начальный (`Void`, пустой коконус). Курс: TypeAlgebra.
- [ ] `equ` — `J`=параллельная пара: уравнитель (подобъект, где `f=g`) vs коуравнитель (фактор по `f=g`); `↣`/`↠`. Курс: AlgebrasCoalgebras/Toposes.
- [ ] `pbpo` — `J`=коспан/спан: pullback (`A→C←B`) vs pushout (`A←C→B`). Курс: Toposes.
- [ ] `adj` — `F⊣G`; через Кан `G=Ran_F Id`, `F=Lan_G Id`; единица/коединица `⇒`. Курс: Adjunctions.
- [ ] `monadcomonad` — монада (`η,μ`) vs комонада (`ε,δ`); через Кан `Codensity f=Ran f f`, `Density f=Lan f f`; монада из сопряжения. Курс: Monads/Comonads.

### Task 5: README + ROADMAP

**Files:** Modify `README.md`, `src/ROADMAP.md`, опц. `src/README.ipynb`

- [ ] README.md / src/README.ipynb: упомянуть `Duality.ipynb` как справочник-приложение (вне ствола 0–VI).
- [ ] ROADMAP: запись «Словарь двойственности (Duality.ipynb)» со статусом (каркас + образцы mono/epi, Kan, prodcoprod; остальные разделы — стабы).
- [ ] Commit: `git add README.md src/ROADMAP.md src/README.ipynb; git commit -m "duality: README/ROADMAP — справочник-приложение"`

### Task 6: Финиш

- [ ] Полный контейнер-прогон `Duality.ipynb` → 0 ошибок; JSON-валидность; якоря таблицы целы; ссылки «где в курсе» ведут на существующие файлы.
- [ ] `node src/scripts/coursemap/normalize_palette.js` не трогает inline-SVG ноутбука (он вне `src/diagrams/`) — диаграммы соответствуют канону вручную; ASCII-only проверить скриптом.
- [ ] superpowers:finishing-a-development-branch — merge в master по выбору пользователя.
