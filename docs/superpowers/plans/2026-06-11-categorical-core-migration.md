# План: библиотека src/lib + миграция ноутбуков (Фаза 6)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Спека: `docs/superpowers/specs/2026-06-11-categorical-core-library-design.md`.

**Goal:** Перевести SubjectiveModeling.ipynb и Uncertainty.ipynb на общую библиотеку `src/lib/` (5 модулей, гибридная абстракция Lattice/Quantale + Semiring).

**Architecture:** Модули уже написаны и компилируются (`ghc -fno-code` в контейнере — 0 ошибок). Миграция ячеек — node-скриптом `src/scripts/phase6/apply6.js` по образцу Фазы 5; источники новых ячеек — `src/scripts/phase6/*.hs|*.txt`. Верификация — `nbconvert --execute` в одноразовом контейнере.

**Tech Stack:** IHaskell/GHC (контейнер gibiansky/ihaskell), Node.js.

**Важно про `:load`:** в GHCi/IHaskell `:load` сбрасывает контекст импортов, поэтому в setup-ячейках порядок строго: `:set` → `:load` (все 5 модулей одной командой) → все импорты (библиотечные и стандартные) → прочее.

---

### Task 1: Библиотека (выполнено)
- [x] `src/lib/{Quantale,KanExtension,Bitopos,Distribution,SubjectiveModel}.hs` написаны, в каждом блок `-- ИДЕИ РАСШИРЕНИЯ`.
- [x] Компиляция: `docker run --rm -v <root>:/home/jovyan/pwd -w /home/jovyan/pwd/src/lib gibiansky/ihaskell ghc -fno-code Quantale.hs KanExtension.hs Bitopos.hs Distribution.hs SubjectiveModel.hs` → 5/5 OK.

### Task 2: Миграция SubjectiveModeling.ipynb
Файлы-источники в `src/scripts/phase6/`: `sm_setup.txt`, `sm_s15.hs`, `sm_s610.hs`, `sm_s1112.hs`, `sm_s1314.hs`, `sm_resd.hs`, `sm_bel.hs`, `sm_bil.hs`, `sm_gam.hs`, `sm_mon.hs`, `sm_isb.hs`.
- [x] apply6.js заменяет source ячеек: `5jry916m`→sm_setup, `htb0p13s`→sm_s15, `y5w0bn87`→sm_s610, `yirca393`→sm_s1112, `bu2gr960`→sm_s1314, `ph5resd1`→sm_resd, `ph5bel02`→sm_bel, `ph5bil03`→sm_bil, `ph5gam04`→sm_gam, `ph5mon06`→sm_mon, `ph5isb08`→sm_isb. Outputs ячеек обнуляются.
- [x] JSON-проверка обоих ноутбуков node-ом.

### Task 3: Миграция Uncertainty.ipynb
Источники: `un_setup.txt`, `un_s4_append.hs`, `un_s7_append.hs`, `un_s9.hs`.
- [x] `82e4316c`→un_setup (с `:load` и `import qualified Distribution as D` — локальный `newtype Dist` ноутбука не конфликтует); `ef70654e` += un_s4_append; `2ec203a5` += un_s7_append; `89b78813`→un_s9 (старые локальные SubjModel/Dist-дубли удаляются).
- [x] JSON-проверка.

### Task 4: Верификация
- [x] `docker run --rm -v <root>:/home/jovyan/pwd gibiansky/ihaskell jupyter nbconvert --to notebook --execute --inplace /home/jovyan/pwd/src/notebooks/SubjectiveModeling.ipynb --ExecutePreprocessor.timeout=900`
- [x] То же для Uncertainty.ipynb.
- [x] Проверка node-ом: `output_type === 'error'` отсутствует в обоих → `errors: 0`. (Закрывает и висящий Run All Фазы 5.)

### Task 5: ROADMAP
- [x] Добавить «Фаза 6 — Библиотека категорного ядра src/lib» с таблицей статусов; в Фазе 5 пункт 7 отметить ✅ «закрыт прогоном Фазы 6».
- [x] В «Критические правила» добавить: «`:load` — только в setup-ячейке, один раз, все модули сразу; после `:load` повторить все импорты».
