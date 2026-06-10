# 🗳️ ROADMAP: Haskell + Теория Категорий

> Документ разработки: хронология, технические решения, актуальный статус и планы на будущее.
> Путеводитель по содержанию ноутбуков — в README.ipynb.
> Последнее обновление: 2026-06-10 (Фаза 9: развёрнутая переработка Uncertainty выполнена)

---

## ✅ Пройденный путь

### Фаза 1 — Базовые ноутбуки
Создано 13 ноутбуков, покрывающих Haskell от основ до экспертных тем.
Все ноутбуки содержат **0 ошибок** и SVG-диаграммы для ключевых концепций.

| Ноутбук | Ячеек | SVG | Примечание |
|---------|-------|-----|------------|
| BaseHaskell.ipynb | 74 | — | Основы языка |
| TypeAlgebra.ipynb | 19 | 3 | ta_product_coproduct.svg, ta_semiring.svg, ta_zipper.svg |
| FunctorHierarchy.ipynb | 20 | 1 | fh_hierarchy.svg |
| Monads.ipynb | 137 | — | |
| MonadTransformers.ipynb | 71 | 2 | mt_stack.svg, mt_diagram.svg |
| Comonads.ipynb | 86 | 1 | cm_comonad.svg |
| ComonadTransformers.ipynb | 23 | 2 | ../diagrams/comonads/ct_diagram.svg, ../diagrams/comonads/ct_stack.svg |
| Uncertainty.ipynb | 22 | 1 | uncertainty_overview.svg |
| FoldableTraversable.ipynb | 56 | 2 | ft_foldable.svg, ft_compare.svg |
| AlgebrasCoalgebras.ipynb | 49 | 3 | initial_alg.svg, hylo_tree.svg, falgebra_diagram.svg |
| Profunctors.ipynb | 19 | 1 | dimap_square.svg |
| Optics.ipynb | 22 | 1 | op_optics.svg |
| YonedaLemma.ipynb | 19 | 1 | yo_yoneda.svg |
| KanExtensions.ipynb | 23 | 2 | ran_diagram.svg, lan_diagram.svg |
| Toposes.ipynb | 23 | 10 | three_faces.svg ... bitopos_zoo.svg |
| Adjunctions.ipynb | 32 | 1 | adj_adjunction.svg |
| MetaProgramming.ipynb | 27 | 2 | mp_th_stages.svg, mp_generics.svg |

**Итого Фаза 1:** 626 ячеек, 33 SVG-файла, 0 ошибок. (+ComonadTransformers.ipynb: 23 ячейки, 2 SVG) (+Toposes.ipynb: 23 ячейки, 10 SVG, diagrams/topos/)

---

### Фаза 2 — Распределённые вычисления

| Ноутбук | Ячеек | SVG | Статус |
|---------|-------|-----|--------|
| Concurrency.ipynb | 22 | 1 | ✅ готов (0 ошибок) |
| DistributedHaskell.ipynb | 13 | 1 | ✅ готов (0 ошибок) |
| GPUHaskell.ipynb | 11 | 1 | ✅ готов (0 ошибок) |

**Итого Фаза 2:** 46 ячеек, 3 SVG-файла, 0 ошибок.

---

**Общий итог:** 651 ячейка, 27 SVG-файлов, 0 ошибок, 17 ноутбуков готово. Унификация структуры (setup+TOC+nav) завершена для всех 18 ноутбуков.

---

## ✅ Фаза 3 — Синтез (выполнено 2026-06-02)

### 17. Arrows.ipynb — выполнено
- ✅ 21 ячейка, 8 секций: Category, Arrow, ArrowChoice, ArrowLoop, ArrowApply, Kleisli
- ✅ 3 SVG: `arr_hierarchy.svg`, `arr_dataflow.svg`, `arr_kleisli.svg`
- ✅ Практические примеры: конвейер обработки данных, Kleisli для Maybe и []
- ✅ Категорный взгляд: моноидальная категория, traced monoidal, связь с профункторами
- ✅ GPUHaskell.ipynb nav обновлён: → Arrows

### 18. Profunctors.ipynb — расширение выполнено
Добавлены 4 ячейки, 2 SVG:
- ✅ **Ends и Coends:** `newtype End p = End { getEnd :: forall x. p x x }`, wedge condition, композиция через coend; SVG: `prof_end_wedge.svg`
- ✅ **Тамбара-модули:** `class (Strong p) => Tambara p where alpha :: p a b -> p (f a) (f b)`, связь с оптиками; SVG: `prof_tambara.svg`
- **Итог:** Profunctors.ipynb — 23 ячейки, 3 SVG

### 19. Optics.ipynb — расширение выполнено
Добавлены 5 ячеек, 1 SVG:
- ✅ **Wander (Profunctor Traversal):** `class Wander p where wander :: (forall f. Applicative f => ...)`, инстанс `(->)`, пример `both`
- ✅ **Grate (coexponential optic):** `class Closed p where closed :: p a b -> p (x -> a) (x -> b)`, пример с Reader
- ✅ **Сводная таблица 9 оптик** через `forall p. Constraint p => p a b -> p s t`; SVG: `op_optics_full.svg`
- **Итог:** Optics.ipynb — 29 ячеек, 2 SVG

---

---

## ✅ Фаза 4 — Обновление SVG на светлую тему (2026-06-05)

Все 30 SVG-диаграмм приведены к единой светлой палитре (#ffffff фон).

Обновлено за сессию: yo_yoneda.svg, dimap_square.svg, initial_alg.svg,
hylo_tree.svg, falgebra_diagram.svg, mp_th_stages.svg, mp_generics.svg,
kan/*.svg (6 файлов), dist_landscape.svg, gpu_landscape.svg,
conc_landscape.svg, hask_circle.svg.

FoldableTraversable.ipynb: исправлена запись — 2 SVG (ft_foldable.svg + ft_compare.svg).



### ComonadTransformers.ipynb — выполнено (2026-06-05)
- ✅ 23 ячейки, 9 секций: Мотивация, ComonadTrans, EnvT, StoreT, TracedT, Стеки, Практика, ComonadT+MonadT, Связь
- ✅ 2 SVG: `ct_diagram.svg` (MonadTrans vs ComonadTrans duality), `ct_stack.svg` (стеки и порядок)
- ✅ Дуальность: lift ↔ lower, return ↔ extract, join ↔ duplicate
- ✅ Три основных трансформера: EnvT (dual ReaderT), StoreT (dual StateT, основа Lens), TracedT (dual WriterT)
- ✅ Секция 8: Комбинация ComonadT+MonadT, порядок композиции и эффекты
- ✅ Секция 9: Связь с Adjunctions, Lens, Corecursion

---

## 🔄 Фаза 5 — Углублённый синтез SubjectiveModeling (выполнено, 2026-06-05)



---

## Faza 6 -- Ispravleniye SVG-diagramm (v plane)

> Audit pokazal: bolshinstvo SVG sozdany v starom stile (bez #0f172a, s temnym fonom)
> i narushayut pravilo ASCII-only (kirillica pryamo v SVG XML).
> Nuzhno peresozdanie ~50 SVG v 9 papkakh.

### 6.1 topos/ -- vse 11 SVG (kiriллица + staryy stil)
- Status: PLAN
- bitopos_classifier, bitopos_zoo, geom_morph, logic_lattice, mitchell_benabou,
  omega_pullback, project_map, sheaf_gluing, test_omega, three_faces, topos_axioms

### 6.2 kan/ -- vse 7 SVG (staryy stil, net svetloy palitry)
- Status: PLAN
- kan_adjunction, kan_codensity, kan_density, kan_examples, kan_yoneda,
  lan_diagram, ran_diagram

### 6.3 monads/ + functors/ + haskell/ + algebras/ (20+ SVG)
- Status: PLAN  
- monads: 6/6 bad, functors: 3/3 bad, haskell: 5/5 bad, algebras: 6/8 bad

### 6.4 comonads/ + misc/ + optics/ + yoneda/ + subj/ (chastichnoe)
- Status: PLAN
- comonads: 3/5, misc: 2/3, optics: 2/6, yoneda: 4/5, subj: 6/6

---

## Faza 7 -- Kontent: svyazi i biblioteki (v plane)

### 7.1 Uncertainty.ipynb -- Razdel 9: svyaz s SubjectiveModeling
- Status: PLAN
- Dobavit kratkiy razdel o teorii Pityeva kak most mezhdu neopredelyonnostyu i
  subektivnym modelirovanием
- 1 SVG: uncertainty_to_subj.svg (skhema perekhoda)

### 7.2 SubjectiveModeling.ipynb -- opyaniye na KanExtensions i Toposes
- Status: PLAN  
- Dobavit Razdel 0 (Vvedeniye): yavnyye ssylki na KanExtensions.ipynb i Toposes.ipynb
- Dobavit cross-reference tablitsu: ponyatiye -> otkuda
- 1 SVG: subj_deps.svg (skhema zavisimostey)

### 7.3 Toposes.ipynb -- Razdel T9: Haskell-biblioteki po toposam
- Status: PLAN
- Issledovat Hackage: heyting (HeytingAlgebra typeclass), subhask,
  categories package, lens/optics kak toposnyye struktury
- Pokazat chto dostupno v IHaskell srede
- 1 SVG: topos_libraries.svg


### 19. SubjectiveModeling.ipynb — Раздел 15: три сравнительных примера

**Цель:** показать единство подходов Пытьева, битопологического и Кана на трёх примерах с разной градацией сложности.

| Пример | Сложность | Суть |
|--------|-----------|------|
| Пример 1 | Простой | X = {low, medium, high}, монотонная τ. Оба подхода совпадают тривиально — точка отсчёта |
| Пример 2 | Средний | X → Y через φ: X→Y. Битопос требует проталкивания топологии; Кан даёт `Lan_φ τ(y) = sup τ` естественно |
| Пример 3 | Сложный | X — poset, [0,1]-обогащённая категория (не дискретная). Обогащённый Кан vs Scott-топология на poset |

**SVG:** `subj_example1.svg`, `subj_example2.svg`, `subj_example3.svg` (`diagrams/subjective/`)

**Статус:** ✅ выполнено (2026-06-06)

**Результаты:**
- Пример 1: Pl(битопос) == Lan_J tau на дискретном X — точка отсчёта ✅
- Пример 2: tau_Y(y) = sup_{phi(x)=y} tau(x) (формула раздела 3 Пытьева) = Lan_phi tau — автоматически ✅
- Пример 3: poset X с тремя вариантами обогащения — Lan(poset{0,1}) == Pl(flat), Lan(непрерыв) — потенциально расходится ✅
- 3 новых SVG: subj_example1.svg, subj_example2.svg, subj_example3.svg
- SubjectiveModeling.ipynb: 16 → 30 ячеек

---

## ✅ Фаза 8 — Реорганизация: теория возможностей (2026-06-07)

> Из теорий Пытьева в Uncertainty.ipynb оставлена **только теория возможностей**.
> Субъективное моделирование полностью вынесено в SubjectiveModeling.ipynb.
> Ключевая правка интерпретации: аппарат возможности/необходимости и
> правдоподобия/доверия — **одна и та же** математическая конструкция; различается
> только интерпретация (частотно-объективная vs выражение интуиции эксперта).
> НЕ «τ̄ ограничена через θ vs τ̄ независима» — это было неверно.

### 8.1 Uncertainty.ipynb — раздел 9 переписан
- ✅ Заголовок: «9. Теория возможностей Пытьева» (вместо субъективного моделирования)
- ✅ 9.1 Дуальные шкалы `L=([0,1],max,min)`, `L̄=([0,1],min,max)`, меры Π и N; θ — координатное выражение `L≅L^op`, необязательное
- ✅ 9.2 Частотное построение возможностной модели (НОВОЕ): `τ(x)=ν(x)/max ν`
- ✅ 9.3 Построение по вероятностям: класс Γ(Pr), хвостовые суммы, интервалы Δ_k, порог тривиальности
- ✅ 9.4 Пример `w_n=1/pⁿ` — одни веса, две теории (sum-norm vs sup-norm)
- ✅ 9.5 Что значит «A возможнее B»: пороговый переход q=1, частотный смысл
- ✅ Удалены: ошибочное противопоставление τ̄, `distToSubjModel`, блок диагностики двигателя
- ✅ Краткий «мост» к SubjectiveModeling с корректной интерпретацией
- ✅ Выполнение: 0 ошибок

### 8.2 SubjectiveModeling.ipynb
- ✅ Раздел 0: добавлена заметка «Связь с теорией возможностей» — одна конструкция, разная интерпретация (корректный фрейминг)
- ✅ Раздел 16: перенесён и адаптирован пример диагностики двигателя (3 эксперта) под API разделов 1-5 (combineExperts, conditionModel, интегралы риска, принцип относительности, условная модель)
- ✅ Выполнение: 0 ошибок

### 8.3 Инфраструктура
- ✅ Workflow выполнения ноутбуков: собственный исполнитель через `jupyter_client` (nbconvert несовместим с холодным стартом IHaskell-ядра)

---

## ✅ Фаза 9 — Uncertainty.ipynb: развёрнутый учебный формат (2026-06-10)

> Спека: `docs/superpowers/specs/2026-06-10-uncertainty-rework-design.md`
> Проблема: телеграфный стиль markdown-обвязки (криптичные сокращения,
> непрозрачные таблицы, нет мотивации). Код развит, но «почему/откуда» не
> объяснено. Эталон объёма — секция 9 (Фаза 8).
> Цель: весь ноутбук (введение + 9 секций + сводка) к единому развёрнутому
> стилю; три канала восприятия (текст / таблица / визуал); явные границы
> применимости.

### 9.1 Единый скелет каждой секции
- ✅ Мотивация → Идея/конструкция (категорный смысл) → Формализм →
  Код+развёрнутая демо → Пример из жизни → Границы применимости → Мостик
- ✅ Код сохраняется исполнимым (0 ошибок), делимитеры только `$...$`

### 9.2 Визуал (новый каталог `src/diagrams/uncertainty/`)
- ✅ Kleisli-композиция ядер (Гири, сек. 3)
- ✅ Решётка `[0,1]` + t-нормы/t-конормы (Fuzzy, сек. 4)
- ✅ Kripke-фрейм + достижимость (модальные, сек. 5)
- ✅ Bayesian network (сек. 6), граф марковской цепи (сек. 7)
- ✅ Дуальные шкалы `L`/`L̄` (возможности, сек. 9 — при необходимости)
- Правила: ASCII-текст, белый фон `#ffffff`, monospace, defs наверху

### 9.3 Обзорная сводка категорных конструкций (3 канала)
- ✅ SVG-постер: строки = виды неопределённости, столбцы = категория /
  эндофунктор-или-обогащение / композиция (Kleisli/решётка) / измерение
- ✅ markdown-таблица с тем же содержанием
- ✅ текстовый абзац единой картины

### 9.4 Стратегия исполнения
- Проход 1 (проза): весь markdown за один проход + сводки-таблицы; 1 прогон ядра
- Проход 2 (визуал): SVG параллельно агентами; сборка; финальный прогон
- ✅ Синхронизировать навигацию + счётчики в README.ipynb (если изменился объём)

---

## ⚠️ Критические правила (не нарушать никогда)

### IHaskell / GHC
- `ensure_ascii=True` всегда в `json.dump`
- `\xNNNN` в Haskell-строках — никогда `\uNNNN`
- `XQuantifiedConstraints` — не использовать
- `data` с функциональными полями — не делать полиморфными
- `newtype` с `forall` в поле — OK
- `IHaskell.Display` — не импортировать
- GHC холодный старт ~60–80с — норма
- `reify` из TH не работает в интерактивном REPL
- **`forkIO + takeMVar` зависает** в IHaskell
- **`Control.Concurrent.Async`** — не установлен
- **`Control.Parallel.Strategies`** — не установлен

### JupyterLab API
- Все операции с файлами — через XHR API, не терминал
- `X-XSRFToken` из cookie `_xsrf` — обязателен для PUT/DELETE
- Перед записью ноутбука — `DELETE /api/sessions/{id}`
- После записи — « File > Reload Notebook from Disk »
- Кэш — `?_=${Date.now()}`
- SVG по адресу `/files/filename.svg`, в markdown — `![alt](filename.svg)`
- Ctrl+S после каждого этапа
- SVG: нельзя использовать unicode entities с кириллицей
- Унификация структуры завершена 2026-05-31: все 17 ноутбуков имеют SETUP + TOC + NAV. При записи ensure_ascii=False. (`&#NNNN;`) — разрывают XML-парсер; использовать только ASCII-текст в SVG

### SVG
- `&nbsp;` — невалидный XML, использовать `&#160;`
- Проверка: `DOMParser().parseFromString(content, 'image/svg+xml')` + parsererror

---

## 🎨 Правила унификации дизайна (введено 2026-05-31)

> Выбранный стиль: **B — Интерактивный**. Весёлый, живой, с визуальными якорями.
> Диаграммы: **тёмная тема** (dark mode, единая палитра).

### Язык написания

Все ноутбуки пишутся **на русском языке**:
- Заголовки секций, описания, пояснения — по-русски
- Имена полей таблиц (Section → Раздел, Key idea → Ключевая идея, и т.д.)
- Итоговые таблицы, блоки Summary — по-русски
- Комментарии в коде могут быть на английском (техническая необходимость)
- Строковые литералы в примерах кода — на английском (для ASCII-совместимости IHaskell)
- Термины без устоявшегося перевода пишутся латиницей: Arrow, Kleisli, profunctor и т.д.
- Английский в тексте — только технические термины, имена типов/классов/функций

### Структура каждого ноутбука

```
[SETUP-ЯЧЕЙКА]          ← code cell, ВСЕГДА ПЕРВАЯ
  :set -XExtensions...
  import ...
  putStrLn "Setup done."

[HEADER]                ← markdown cell
  # 🗺️ Тема в Haskell
  Одно-два предложения — суть ноутбука.

[TOC]                   ← markdown cell
  📌 Содержание
  | # | Тема | Суть |
  |---|------|------|
  | 1 | ... | ... |

---

[SECTION]               ← markdown cell
  ## 1️⃣ Раздел первый
  Теория + определение.

  | Закон | Формула |
  |-------|---------|
  | ...   | ...     |

  ### 🔺 Категорный взгляд
  Категорная интерпретация.

  ![описание](filename.svg)

[CODE]                  ← code cell (комментарии внутри)
---
[SECTION N]
...

[SUMMARY]               ← markdown cell
  ## 📊 Итог / Сравнение
  [таблица или краткое резюме]

[NAV]                   ← markdown cell (последняя)
  ---
  **← Предыдущий:** [X.ipynb](X.ipynb) | **→ Следующий:** [Y.ipynb](Y.ipynb)
```

### Правила заголовков

| Уровень | Формат | Пример |ls /home/jovyan/src/*.ipynb 2>/dev/null | head -30

|---------|--------|--------|
| H1 (название) | `# [эмодзи] [Тема] в Haskell` | `# 🗺️ Монады в Haskell` |
| H2 (секция) | `## N️⃣ Название` | `## 1️⃣ Functor` |
| H3 (подсекция) | `### 🔺 Категорный взгляд` | только для категорной интерпретации |
| H3 (реализация) | `### 📐 Реализация` | для разбора кода |
| H3 (примеры) | `### 💡 Примеры` | для практических примеров |

**Эмодзи-маркеры секций (H2):** 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟

### Оглавление (📌 Содержание)

- Всегда таблица с колонками: **#**, **Тема**, **Суть**
- Идёт сразу после intro-абзаца, до первой секции

### Разделители

- `---` между каждой H2-секцией — **обязательно**
- Также `---` перед навигационной строкой в конце

### Категорный блок

- Всегда `### 🔺 Категорный взгляд` — отдельная H3 после теории
- Присутствует в **каждой** содержательной секции (не только там где удобно)

### SVG-диаграммы

- `![описание](filename.svg)` — после категорного блока или теории секции
- Одна диаграмма на ключевую концепцию ноутбука

### Навигация (последняя ячейка)

```markdown
---
**← Предыдущий:** [Название](file.ipynb) | **→ Следующий:** [Название](file.ipynb)
```

---

## 🌑 Правила светлых SVG-диаграмм (введено 2026-05-31)

### Палитра (обязательная, единая для всех SVG)

| Роль | HEX | Использование |
|------|-----|---------------|
| **Фон** | `#ffffff` | rect background (весь SVG) |
| **Фон карточки** | `#f1f5f9` | rect внутри (узлы, блоки) |
| **Граница карточки** | `#cbd5e1` | stroke вокруг блоков |
| **Текст основной** | `#0f172a` | все подписи |
| **Текст вторичный** | `#64748b` | метки стрелок, пояснения |
| **Акцент синий** | `#2563eb` | ключевые узлы, заголовки |
| **Акцент зелёный** | `#34d399` | вторая категория / результат |
| **Акцент фиолет.** | `#a78bfa` | третья категория / специал. |
| **Акцент оранж.** | `#fb923c` | выделение / предупреждение |
| **Стрелки** | `#2563eb` | основные морфизмы |
| **Стрелки пунктир** | `#475569` | вспомогательные связи |
| **Заголовок SVG** | `#0f172a` | title текст диаграммы |

### Типографика SVG

```
font-family="monospace, 'JetBrains Mono', 'Cascadia Code', Arial, sans-serif"
```

| Роль | font-size | font-weight |
|------|-----------|-------------|
| Заголовок диаграммы | 16 | bold |
| Метка узла | 14 | normal |
| Метка стрелки / пояснение | 12 | normal |
| Мелкий текст | 11 | normal |

### Геометрия

- Узлы: `rect` с `rx="6"` (скруглённые углы)
- Стрелки: `marker` с `fill` = цвет стрелки
- Размер SVG: ширина 800–1000, высота по содержанию
- Отступы: минимум 20px от края

### Шаблон SVG (заготовка)

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"
     viewBox="0 0 800 400"
     font-family="monospace,Arial,sans-serif">

  <!-- Background -->
  <rect width="800" height="400" fill="#ffffff" rx="8"/>

  <!-- Arrow markers -->
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#60a5fa"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#34d399"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="400" y="30" text-anchor="middle"
        font-size="16" font-weight="bold" fill="#0f172a">
    Название диаграммы
  </text>

  <!-- Node example -->
  <rect x="60" y="80" width="140" height="50"
        fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" rx="6"/>
  <text x="130" y="110" text-anchor="middle"
        font-size="14" fill="#2563eb">Узел A</text>

  <!-- Arrow example -->
  <line x1="200" y1="105" x2="340" y2="105"
        stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="270" y="98" text-anchor="middle"
        font-size="12" fill="#94a3b8">f</text>

</svg>
```

### Что нужно переделать (список SVG для обновления)

Все 29 существующих SVG-диаграмм нужно привести к светлой палитре.
Приоритет переделки — при следующем редактировании соответствующего ноутбука.

| SVG-файл | Текущий фон | Статус |
|----------|-------------|--------|
| fh_hierarchy.svg | #0f172a (тёмный) | ✅ готов |
| mt_stack.svg | #0f172a (тёмный) | ✅ готов |
| mt_diagram.svg | #0f172a (тёмный) | ✅ готов |
| op_optics.svg | #0f172a (тёмный) | ✅ готов |
| ta_semiring.svg | #0f172a (тёмный) | ✅ готов |
| ta_product_coproduct.svg | #0f172a (тёмный) | ✅ готов |
| ta_zipper.svg | #0f172a (тёмный) | ✅ готов |
| ft_foldable.svg | #0f172a (тёмный) | ✅ готов |
| cm_comonad.svg | #0f172a (тёмный) | ✅ готов |
| falgebra_diagram.svg | #0f172a (тёмный) | ✅ готов |
| initial_alg.svg | #0f172a (тёмный) | ✅ готов |
| hylo_tree.svg | #0f172a (тёмный) | ✅ готов |
| dimap_square.svg | #0f172a (тёмный) | ✅ готов |
| yo_yoneda.svg | #0f172a (тёмный) | ✅ готов |
| ran_diagram.svg | #0f172a (тёмный) | ✅ готов |
| lan_diagram.svg | #0f172a (тёмный) | ✅ готов |
| kan_density.svg | #0f172a (тёмный) | ✅ готов |
| kan_adjunction.svg | #0f172a (тёмный) | ✅ готов |
| kan_yoneda.svg | #0f172a (тёмный) | ✅ готов |
| kan_examples.svg | #0f172a (тёмный) | ✅ готов |
| adj_adjunction.svg | #0f172a (тёмный) | ✅ соответствует |
| mp_th_stages.svg | #0f172a (тёмный) | ✅ готов |
| mp_generics.svg | #0f172a (тёмный) | ✅ готов |
| conc_landscape.svg | #0f172a (тёмный) | ✅ готов |
| dist_landscape.svg | #0f172a (тёмный) | ✅ готов |
| gpu_landscape.svg | #0f172a (тёмный) | ✅ готов |
| hask_circle.svg | #0f172a (тёмный) | ✅ готов |
| diagram.svg | — | ✅ шаблон |


---

## 📋 Шаблон: как добавляется новый ноутбук

```
1. Создать SVG-диаграммы и выгрузить через PUT /api/contents/name.svg
2. Сделать DELETE /api/sessions/{id} для ноутбука (если открыт)
3. Создать/обновить ноутбук через PUT /api/contents/name.ipynb
4. File > Reload Notebook from Disk в JupyterLab
5. Run All (»») → дождаться 0 ошибок
6. Ctrl+S
7. Обновить README.ipynb + ROADMAP.md
```

---

*Фаза 1 завершена 2026-05-30. Фаза 2 завершена 2026-05-30. Фаза 3 в планах (Arrows.ipynb). Правила унификации дизайна введены 2026-05-31.*

### Adjunctions.ipynb — выполнено (2026-06-01)
- ✅ ASCII-диаграмма треугольных тождеств заменена на SVG (`adj_triangle.svg`)
- ✅ Мусорная ячейка с `import json` удалена
- ✅ 3 пустые ячейки в начале удалены
- ✅ Структура разделов исправлена: 14 разделов вместо путаницы 9+6.5+7+8+9+10
- ✅ TOC обновлён: таблица из 14 строк
- ✅ Ячейки "Диаграмма" и SVG объединены
- ✅ Все ячейки выполнены без ошибок, Haskell | Idle
