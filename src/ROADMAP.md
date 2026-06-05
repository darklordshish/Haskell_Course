# 🗳️ ROADMAP: Haskell + Теория Категорий

> Документ разработки: хронология, технические решения, актуальный статус и планы на будущее.
> Путеводитель по содержанию ноутбуков — в README.ipynb.
> Последнее обновление: 2026-06-03

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

**Итого Фаза 1:** 603 ячейки, 31 SVG-файл, 0 ошибок. (+Toposes.ipynb: 23 ячейки, 10 SVG, diagrams/topos/)

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

## ✅ Фаза 4 — Обновление SVG на тёмную тему (2026-06-03)

Все 30 SVG-диаграмм приведены к единой тёмной палитре (#0f172a фон).

Обновлено за сессию: yo_yoneda.svg, dimap_square.svg, initial_alg.svg,
hylo_tree.svg, falgebra_diagram.svg, mp_th_stages.svg, mp_generics.svg,
kan/*.svg (6 файлов), dist_landscape.svg, gpu_landscape.svg,
conc_landscape.svg, hask_circle.svg.

FoldableTraversable.ipynb: исправлена запись — 2 SVG (ft_foldable.svg + ft_compare.svg).

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

## 🌑 Правила тёмных SVG-диаграмм (введено 2026-05-31)

### Палитра (обязательная, единая для всех SVG)

| Роль | HEX | Использование |
|------|-----|---------------|
| **Фон** | `#0f172a` | rect background (весь SVG) |
| **Фон карточки** | `#1e293b` | rect внутри (узлы, блоки) |
| **Граница карточки** | `#334155` | stroke вокруг блоков |
| **Текст основной** | `#e2e8f0` | все подписи |
| **Текст вторичный** | `#94a3b8` | метки стрелок, пояснения |
| **Акцент синий** | `#60a5fa` | ключевые узлы, заголовки |
| **Акцент зелёный** | `#34d399` | вторая категория / результат |
| **Акцент фиолет.** | `#a78bfa` | третья категория / специал. |
| **Акцент оранж.** | `#fb923c` | выделение / предупреждение |
| **Стрелки** | `#60a5fa` | основные морфизмы |
| **Стрелки пунктир** | `#475569` | вспомогательные связи |
| **Заголовок SVG** | `#f1f5f9` | title текст диаграммы |

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
  <rect width="800" height="400" fill="#0f172a" rx="8"/>

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
        font-size="16" font-weight="bold" fill="#f1f5f9">
    Название диаграммы
  </text>

  <!-- Node example -->
  <rect x="60" y="80" width="140" height="50"
        fill="#1e293b" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="130" y="110" text-anchor="middle"
        font-size="14" fill="#60a5fa">Узел A</text>

  <!-- Arrow example -->
  <line x1="200" y1="105" x2="340" y2="105"
        stroke="#60a5fa" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="270" y="98" text-anchor="middle"
        font-size="12" fill="#94a3b8">f</text>

</svg>
```

### Что нужно переделать (список SVG для обновления)

Все 29 существующих SVG-диаграмм нужно привести к тёмной палитре.
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
