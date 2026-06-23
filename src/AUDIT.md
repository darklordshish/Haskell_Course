# 🔍 Аудит ноутбуков курса

> Автоматический прогон + ручная проверка, 2026-06-23. Сканер: `node` по всем `.ipynb`.
> Проверялось: ошибки выполнения, битые ссылки на картинки, hlint-шум в сохранённых
> выводах, разнобой транслитерации «Ёнеда», пустые колонки в оглавлениях, наличие
> setup/Содержание/навигации.

## ✅ Статус (2026-06-23)

Работа ведётся в Фазе 20 ROADMAP. Закрыто: баг ComonadTransformers (перепрогон 0 ошибок),
транслитерация Ёнеда, оглавления (Profunctors переведён, Uncertainty добавлен, 5 ноутбуков
с пустой «Суть» заполнены), инфраструктура (архив скриптов, check_status, gitignore).
hlint-шум — **решено оставить** (подсказки линтера полезны для обучения). Ложные срабатывания сканера:
DesignShowcase (`filename.svg` в код-блоке), Adjunctions/Monads (Суть уже заполнена),
README (колонка «Уровень», не «Суть»).

---

## 🔴 Критичное (содержательные ошибки)

| Ноутбук | Проблема |
|---|---|
| **ComonadTransformers.ipynb** | Ячейка `navDemo` («Pattern 2: StateT over StoreT») **не компилируется**: `extract (runStateT navAction 0)` → *Ambiguous type variable `w0`* (GHC-39999). Нужна аннотация типа или переработка примера. Опровергает «0 ошибок» в ROADMAP. |
| **DesignShowcase.ipynb** | Битая ссылка на картинку `filename.svg` (плейсхолдер из шаблона, файла нет). Нет первой setup-ячейки. *(Возможно by-design — это витрина шаблона, но плейсхолдер стоит убрать.)* |

## 🟠 Сквозные огрехи (массовые)

### hlint-шум зашит в сохранённые выводы
Предупреждения линтера (`Functor law`, `Eta reduce`, `Redundant lambda`, `Use <$>`,
`Avoid lambda`) сохранены в выводах ячеек. Местами вредит педагогике (напр. в Yoneda
линтер советует ровно ту оптимизацию слияния `fmap`, что демонстрируется руками).

| Ноутбук | Ячеек с шумом |
|---|---|
| FoldableTraversable.ipynb | 34 |
| AlgebrasCoalgebras.ipynb | 7 |
| ComonadTransformers.ipynb | 5 |
| Monads.ipynb | 5 |
| Uncertainty.ipynb | 5 |
| YonedaLemma.ipynb | 5 |
| Optics.ipynb | 4 |
| SubjectiveModeling.ipynb | 4 |
| Arrows / BaseHaskell / DistributedHaskell | 3 каждый |
| Comonads / KanExtensions / Toposes | 2 каждый |
| Extensions / TypeAlgebra | 1 каждый |

**Рекомендация:** глушить hlint в учебных ячейках (`-- hlint: ignore`/`{-# ANN #-}`)
либо чистить вывод перед коммитом.

### Пустая колонка «Суть» в оглавлениях
Таблица TOC содержит колонку «Суть», но ячейки пустые:
Adjunctions, Concurrency, DistributedHaskell, FunctorHierarchy, GPUHaskell,
Monads, YonedaLemma, README.
**Рекомендация:** заполнить либо убрать колонку в генераторе TOC.

## 🟡 Точечное

| Ноутбук | Проблема |
|---|---|
| **YonedaLemma.ipynb** | Разнобой транслитерации: «Енед» — 5 вхождений (заголовок `# ∀ Лемма Енеды`, эпиграф), «Ёнед» — 5. Канон — **Ёнеда**. Также «Том Лайнстер» → обычно «Лейнстер». |

## ⚪ Проверить — возможно by-design

Справочные/служебные ноутбуки вне ствола; отсутствие навигации/TOC может быть намеренным,
но стоит подтвердить:

| Ноутбук | Что отсутствует |
|---|---|
| Duality.ipynb | нет «Содержание», нет навигации (справочник) |
| SetOp.ipynb | нет навигации (этюд-справочник) |
| Profunctors.ipynb | нет «Содержание» *(но это ствол — вероятно настоящий пропуск)* |
| Uncertainty.ipynb | нет «Содержание» (есть «карта» — другое слово) |
| README.ipynb | нет навигации (это индекс — ок) |

## ✅ Чисто

MetaProgramming.ipynb, MonadTransformers.ipynb.

---

## Инфраструктурное (вне ноутбуков)

- `src/scripts/` — кладбище одноразовых скриптов: `fix_algebras{,2,3}.py`,
  `inspect2/3.py`, `gen_ct2.py`, `build_ct{,_final}.py`, `make_ct.py`, `full_ct.py`,
  `ct_gen.py` и т.п. рядом с боевыми генераторами. Архивировать/удалить.
- `src/scripts/check_status.py` — хардкод-список из 17 ноутбуков, протух: нет Toposes,
  Arrows, Adjunctions, Duality, SetOp и модулей V/VI. Брать список из `course_order.js`.
- В рабочей копии сабмодуля `src/lib` — untracked артефакты сборки (`.o/.hi/.dyn_o/.dyn_hi`).
  Добавить в `.gitignore` сабмодуля.
