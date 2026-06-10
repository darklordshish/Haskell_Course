# Uncertainty.ipynb Expanded Rework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework `src/notebooks/Uncertainty.ipynb` from terse telegraphic style into a unified, verbose teaching format — full per-section skeleton, SVG diagrams for heavy sections, and a 3-channel (text/table/diagram) categorical-constructions summary.

**Architecture:** Two passes. Pass 1 (prose) rewrites every markdown cell by one author for a single voice, then one kernel run verifies code still executes. Pass 2 (visual) builds independent SVGs (parallelizable across agents) and assembles them, then a final kernel run. Notebook edits go through Python patch scripts executed inside the Docker container `haskell_course_git-ihaskell-1`.

**Tech Stack:** IHaskell/Jupyter kernel in Docker, Python (json patch scripts + `jupyter_client` executor), SVG (canonical course style).

---

## Conventions (read once)

**Patch-script workflow** (every cell edit):
1. Write a Python script locally under `src/_patch/<name>.py` that does `json.load` → mutate `cells` → `json.dump(..., ensure_ascii=False, indent=1)`.
2. Copy/run inside container:
   `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/<name>.py`
   (host `src/` is mounted; verify mount path with `docker exec haskell_course_git-ihaskell-1 ls /home/jovyan/work/notebooks/`).
3. Identify cells by their `id`, never by index (indices shift).

**Cell ids (current, section 1–8 markdown):**
- sec1 = id of "# 1. Неопределённость как Функтор" cell
- sec2, sec3, sec4, sec5, sec6, sec7, sec8 similarly (resolve by matching `# N.` heading prefix in the patch script).
- intro = "# ❓ Uncertainty & Randomness" cell; summary = "## Сводка" cell.
- Section 9 cells (sec9_intro, sec91..sec95, bridge) are the **style reference** — DO NOT rewrite their prose; only touch if the summary table needs alignment.

**Kernel execution harness** (`src/_patch/_run.py`, reuse from prior phases):
- Uses `jupyter_client` to start kernel, runs every code cell in order, collects `error` outputs, writes outputs back to JSON, prints `ERRORS: N`.
- Run: `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/_run.py Uncertainty.ipynb`
- Expected after each pass: `ERRORS: 0`.

**Hard rules:** math delimiters only `$...$` (never `\(...\)`); SVG = ASCII text only, white background `#ffffff`, `font-family="monospace,Arial,sans-serif"`, `<defs>` first, no cyrillic unicode entities; commit after each task.

**Per-section skeleton** (every content section ends with these 7 beats, as markdown sub-blocks within ONE expanded markdown cell, code cell unchanged unless noted):
1. **Мотивация** — what uncertainty, where it arises.
2. **Идея / конструкция** — structure + categorical meaning.
3. **Формализм** — definitions, formulas in `$...$`.
4. **Код + демо** — point to the existing code cell; add 2-4 sentences explaining what the demo shows and why.
5. **Пример из жизни** — one concrete applied case.
6. **Границы применимости** — when it works / breaks / how it differs from neighbours.
7. **Мостик** — one sentence linking to the next section.

---

## Task 0: Infrastructure

**Files:**
- Create: `src/_patch/` (scripts dir), `src/diagrams/uncertainty/` (svg dir)
- Reuse/create: `src/_patch/_run.py`

- [ ] **Step 1: Confirm mount path and container**

Run: `docker exec haskell_course_git-ihaskell-1 ls /home/jovyan/work/notebooks/Uncertainty.ipynb`
Expected: path prints (no error). If different, record actual mount root and substitute everywhere below.

- [ ] **Step 2: Create dirs**

```bash
mkdir -p src/_patch src/diagrams/uncertainty
```

- [ ] **Step 3: Place `_run.py` executor**

Recover the executor used in Phase 8 (jupyter_client-based). If absent, write `src/_patch/_run.py` that: takes a notebook filename arg, starts an IHaskell kernel via `KernelManager`, executes each `code` cell with `wait_for_ready`, captures `error` msgs, writes outputs back, prints `ERRORS: <count>`.

- [ ] **Step 4: Baseline run (sanity)**

Run: `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/_run.py Uncertainty.ipynb`
Expected: `ERRORS: 0` (current notebook already executes clean).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "chore: scaffold patch/exec infra and uncertainty diagram dir"
```

---

## PASS 1 — PROSE (Tasks 1–11)

Each section task: one patch script replaces the section's markdown cell `source` with the expanded 7-beat skeleton. Code cells are NOT changed (except adding a leading comment if the task says so). After writing prose for a section, DO NOT run the kernel per-section — batch verification is Task 11.

### Task 1: Section 1 — Uncertainty as Functor

**Files:** Modify `Uncertainty.ipynb` (cell id sec1) via `src/_patch/p1.py`

- [ ] **Step 1: Write expanded markdown.** Replace sec1 source with the 7 beats:
  - *Мотивация:* simplest uncertainty = "value may be absent / may be an error / may be many". Pure FP encodes this in the type, not in exceptions.
  - *Идея:* each is an **endofunctor on Hask**; `fmap` lifts pure computation over the uncertainty wrapper.
  - *Формализм:* `Maybe`=$1+a$, `Either e`=$e+a$, `[]`=free monoid, `Validation e` accumulates via `Semigroup e`. Functor laws `$fmap\;id = id$`, `$fmap (g\circ f)=fmap\,g\circ fmap\,f$`.
  - *Код+демо:* point to existing `demo_sec1`; explain `safeDiv`/`parseAge`/`Validation`/list-nondeterminism each illustrate a different functor.
  - *Пример из жизни:* form validation collecting ALL field errors at once (Validation) vs short-circuit (Either).
  - *Границы:* functors compose computation but give **no quantitative measure** of uncertainty — no probabilities/degrees; that motivates Section 2.
  - *Мостик:* "Чтобы взвесить исходы, нужна не структура-обёртка, а распределение — монада Dist."
  - Keep existing table; expand its abbreviations into a full sentence column.
- [ ] **Step 2: Run patch script** `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/p1.py`. Expected: `patched sec1`.
- [ ] **Step 3: Commit** `git add -A && git commit -m "docs(uncertainty): expand section 1 (functors)"`

### Task 2: Section 2 — Discrete Distribution Monad

**Files:** Modify cell sec2 via `src/_patch/p2.py`

- [ ] **Step 1:** Replace sec2 source, 7 beats:
  - *Мотивация:* weight the outcomes — finite probability distribution `Dist a`.
  - *Идея:* `Dist` is a **monad**; `Kleisli(Dist) ≅ FinStoch` (objects = types, morphisms `a -> Dist b` = stochastic maps). `return` = point mass, `>>=` = law of total probability.
  - *Формализм:* `$Dist\,a = \{(x_i,p_i)\mid p_i\ge0,\ \sum p_i=1\}$`; bind `$(m \gg\!= k)(y)=\sum_x m(x)\,k(x)(y)$`.
  - *Код+демо:* existing `Dist` Monad instance + demo; explain normalization and that `>>=` marginalizes.
  - *Пример из жизни:* dice/coin compositions, drawing without replacement.
  - *Границы:* finite support only; no continuous measures (→ Giry), no conditioning syntax yet (→ Section 6). Floating-point `Double` masses drift; exact would need rationals.
  - *Мостик:* "Бесконечные/непрерывные пространства требуют меры — монада Гири."
- [ ] **Step 2:** Run `p2.py`. **Step 3:** Commit `docs(uncertainty): expand section 2 (Dist monad)`

### Task 3: Section 3 — Giry Monad

**Files:** Modify cell sec3 via `src/_patch/p3.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивация:* probability on arbitrary (measurable) spaces, not just finite sets.
  - *Идея:* Giry monad `G` on **Meas**; Markov kernel = morphism `X -> G(Y)` in `Kleisli(G)`; `>>=` = **integration against the kernel** (Chapman–Kolmogorov).
  - *Формализм:* `$(\kappa_2\circ\kappa_1)(A\mid x)=\int_Y \kappa_2(A\mid y)\,\kappa_1(dy\mid x)$`. Note finite model `Kernel a b = a -> Dist b` is the discrete shadow.
  - *Код+демо:* existing `composeK`; explain it IS Kleisli composition / kernel integration on finite support.
  - *Пример из жизни:* sensor noise model `state -> G(reading)` chained with inference.
  - *Границы:* full Giry needs measure theory (σ-algebras, integrability); here we only realize the **finite/discrete** fragment. Composition cost grows with support size.
  - *Мостик:* "Иногда неопределённость не вероятностная, а градуированная истинность — нечёткая математика."
- [ ] **Step 2:** Run `p3.py`. **Step 3:** Commit `docs(uncertainty): expand section 3 (Giry)`

### Task 4: Section 4 — Fuzzy Mathematics

**Files:** Modify cell sec4 via `src/_patch/p4.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивация:* vagueness of predicates ("tall", "young") — membership is a degree in `[0,1]`, not a bit.
  - *Идея:* fuzzy set = morphism `X -> [0,1]`; logic lives in the lattice/quantale `([0,1], min, max)`; `[0,1]` is a **complete closed subcategory** structure (enrichment) — connectives = t-norms (AND) / t-conorms (OR).
  - *Формализм:* t-norm `$\top(a,b)$` (min, product, Łukasiewicz `$\max(0,a+b-1)$`), t-conorm `$\bot$` (max), negation `$1-x$`, implication `$\min(1,1-a+b)$`. Defuzzification = centroid `$\frac{\sum x\mu(x)}{\sum\mu(x)}$`.
  - *Код+демо:* existing `tall/young/tMin/tProd/tLuka/defuzzCentroid`; explain choice of t-norm changes the AND semantics.
  - *Пример из жизни:* fuzzy thermostat / control: "if warm AND humid then …".
  - *Границы:* **not** probability — degrees need not sum to 1, no normalization, no frequency law. Choice of t-norm is modelling, not derived. Distinct from possibility theory (Section 9), though both use `[0,1]` lattice.
  - *Мостик:* "Необходимость/возможность как операторы — модальные логики."
- [ ] **Step 2:** Run `p4.py`. **Step 3:** Commit `docs(uncertainty): expand section 4 (fuzzy)`

### Task 5: Section 5 — Modal Logics

**Files:** Modify cell sec5 via `src/_patch/p5.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивація:* reason about necessity/possibility across "possible worlds".
  - *Идея:* Kripke frame `(W, R)`; `$\Box p$` = true in all `R`-reachable worlds, `$\Diamond p$` = in some. `$\Box$` is a **right adjoint** (preserves limits/∧), `$\Diamond$` a left adjoint.
  - *Формализм:* `$w\models\Box p \iff \forall v.\,wRv\Rightarrow v\models p$`; axioms S4 (`$\Box p\to\Box\Box p$`, R transitive), S5 (`$\Diamond p\to\Box\Diamond p$`, R equivalence). Keep S4/S5 table, expand.
  - *Код+демо:* existing `KripkeFrame`/`access`; explain how `Box`/`Diamond` are computed over reachable worlds.
  - *Пример из жизни:* knowledge/epistemic logic ("agent knows p"), temporal "always/eventually".
  - *Границы:* qualitative (no degrees); different frame conditions = different logics — must pick axioms to match domain. No quantitative combination of evidence.
  - *Мостик:* "Чтобы программировать вероятностные модели декларативно — стохастический DSL."
- [ ] **Step 2:** Run `p5.py`. **Step 3:** Commit `docs(uncertainty): expand section 5 (modal)`

### Task 6: Section 6 — Stochastic DSL / Bayesian

**Files:** Modify cell sec6 via `src/_patch/p6.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивация:* express generative probabilistic models as readable programs; infer posteriors.
  - *Идея:* a stochastic program = morphism in `Kleisli(Dist)`; Bayesian update = **disintegration** of a joint distribution; `Prior × Likelihood ∝ Posterior`.
  - *Формализм:* `$P(H\mid E)=\dfrac{P(E\mid H)\,P(H)}{\sum_{H'}P(E\mid H')P(H')}$`. Sprinkler net: `Cloudy → {Sprinkler,Rain} → WetGrass`.
  - *Код+демо:* existing sprinkler Bayesian network; explain `do`-notation = sampling the joint, filtering = conditioning.
  - *Пример из жизни:* medical diagnosis (symptom → disease posterior); spam filtering.
  - *Границы:* exact inference is exponential in network width (enumerates joint); fine for small discrete nets, needs sampling/variational methods at scale. Requires explicit CPTs.
  - *Мостик:* "Динамика во времени — марковские цепи."
- [ ] **Step 2:** Run `p6.py`. **Step 3:** Commit `docs(uncertainty): expand section 6 (Bayesian DSL)`

### Task 7: Section 7 — Markov Chains

**Files:** Modify cell sec7 via `src/_patch/p7.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивация:* uncertainty evolving over discrete time, memoryless.
  - *Идея:* Markov chain = endo-kernel `S -> Dist S` in `Kleisli(Dist)`; n-step = Kleisli power; stationary distribution = **fixed point** of the transition functor.
  - *Формализм:* `$\pi P=\pi$`, `$\sum\pi=1$`; n-step `$P^n$` via `runChain`. (Note: present as fixed point; "initial algebra" phrasing kept only if accurate — prefer "стационарное распределение = неподвижная точка отображения переноса".)
  - *Код+демо:* existing `runChain`/`TransKernel`; explain iteration converges to stationary for ergodic chains.
  - *Пример из жизни:* PageRank, weather day-to-day, queue states.
  - *Границы:* memoryless assumption (order-1); convergence needs ergodicity (irreducible+aperiodic); periodic/reducible chains don't converge to unique π.
  - *Мостик:* "Обобщим в категорную картину мер и матриц."
- [ ] **Step 2:** Run `p7.py`. **Step 3:** Commit `docs(uncertainty): expand section 7 (Markov)`

### Task 8: Section 8 — Stochastic Matrices & Measure

**Files:** Modify cell sec8 via `src/_patch/p8.py`

- [ ] **Step 1:** 7 beats:
  - *Мотивация:* unify the previous sections under one categorical/measure-theoretic lens.
  - *Идея:* three categories `Hask` (pure fns) → `Kleisli(Dist)` (`a->Dist b`) → `FinStoch` (stochastic matrices); the monad `(Dist, return, join)`; `join` = marginalizing a distribution of distributions.
  - *Формализм:* keep/expand the categories table; `$join(\mathit{Dist}\,(\mathit{Dist}\,a))$` mixes; entropy `$H=-\sum p\log p$`, KL `$D(p\Vert q)=\sum p\log\frac{p}{q}$` as natural invariants.
  - *Код+демо:* existing `joinDist`; explain it's the monad multiplication = mixture collapse.
  - *Пример из жизни:* channel capacity / information loss measured by entropy.
  - *Границы:* finite stochastic matrices only; entropy/KL assume a fixed reference; KL undefined when support mismatches.
  - *Мостик:* "А если само вероятностное пространство нестабильно — теория возможностей."
- [ ] **Step 2:** Run `p8.py`. **Step 3:** Commit `docs(uncertainty): expand section 8 (measure)`

### Task 9: Intro cell

**Files:** Modify intro cell via `src/_patch/p_intro.py`

- [ ] **Step 1:** Expand the blockquote into 3-4 sentences framing the notebook's arc: from qualitative wrappers → quantitative probability → graded/possibilistic, and the recurring theme "uncertainty = a functor/monad/enrichment in the right category". Keep the 9-row contents table; expand row 9 label to "Теория возможностей Пытьева" (drop the bare arrow). Add a one-line "как читать" note pointing at the per-section skeleton.
- [ ] **Step 2:** Run `p_intro.py`. **Step 3:** Commit `docs(uncertainty): expand intro framing`

### Task 10: Summary cell + 3-channel markdown table

**Files:** Modify summary cell via `src/_patch/p_summary.py`

- [ ] **Step 1:** Rewrite "## Сводка":
  - Keep the prose recap, lightly expand.
  - Replace the 9-row idea table with the **categorical-constructions markdown table** (the text+table channels of the 3-channel summary):

  | Вид неопределённости | Категория / контекст | Эндофунктор / обогащение | Композиция | Измерение |
  |---|---|---|---|---|
  | Maybe / Either / [] / Validation | Hask | эндофунктор | `fmap` | — (нет меры) |
  | Dist (дискретн.) | Kleisli(Dist) ≅ FinStoch | монада Dist | `>>=` (тотальная вероятность) | `$\sum p=1$` |
  | Giry | Kleisli(G) на Meas | монада G | интеграл по ядру | мера `$\mu$` |
  | Fuzzy | обогащение над `[0,1]` | `X→[0,1]` | t-норма / t-конорма | степень `$\mu$` |
  | Modal | Kripke `(W,R)` | `$\Box$` (прав. сопр.) / `$\Diamond$` | по достижимости `R` | качественно |
  | Markov | эндо-Kleisli(Dist) | `S→Dist S` | Kleisli-степень | стац. `$\pi P=\pi$` |
  | Possibility (Пытьев) | решётка `L=([0,1],max,min)` | `τ:X→[0,1]`, `$\sup τ=1$` | `max`/`min` | `$\Pi=\sup τ$`, `$N=\inf \barτ$` |

  - Add a paragraph (the **text channel**) narrating the single picture: each row is "the same idea — lift computation over uncertainty — instantiated in a different category, with a different notion of composition and measurement."
  - Add an image reference placeholder for the poster (filled in Pass 2): `![Категорные конструкции неопределённости](../diagrams/uncertainty/unc_summary_poster.svg)` — verify the relative path the notebook uses for other images first and match it.
- [ ] **Step 2:** Run `p_summary.py`. **Step 3:** Commit `docs(uncertainty): rewrite summary with categorical-constructions table`

### Task 11: Pass-1 kernel verification

- [ ] **Step 1: Run executor**

Run: `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/_run.py Uncertainty.ipynb`
Expected: `ERRORS: 0`.

- [ ] **Step 2: Delimiter lint.** Grep the notebook JSON for `\(` / `\)` in markdown — expected: none. Fix any to `$...$`.
- [ ] **Step 3: `$` balance check.** Script counts `$` per markdown cell; expected: even in every cell. Fix unbalanced.
- [ ] **Step 4: Commit** `git add -A && git commit -m "test(uncertainty): pass-1 prose executes clean, delimiters linted"`

---

## PASS 2 — VISUAL (Tasks 12–20)

Diagrams are independent → Tasks 12–18 can be dispatched to parallel agents. Each agent gets: the canonical SVG rules, the target file path, the panel spec below. Each SVG must parse via `DOMParser` (validate with a quick node/python xml parse) and use ASCII-only text.

**Canonical SVG rules (give to every agent):** `<svg xmlns=... font-family="monospace,Arial,sans-serif">`; `<defs>` (markers) first; background `<rect ... fill="#ffffff"/>` (or light `#f8fafc` panel) with light stroke; ASCII text only (no cyrillic — use translit/Latin/math ASCII); arrowheads via `<marker>`; keep all elements inside the viewBox; light palette (blues `#2255cc`, purples `#7733aa`, greens `#16a34a`, slate `#334466`).

### Task 12: `unc_giry_kleisli.svg` (Section 3)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_giry_kleisli.svg`, ~640×260. Three objects X, Y, Z as boxes; two kernels `k1: X -> G(Y)`, `k2: Y -> G(Z)`; composite `k2 . k1` as a curved arrow underneath labeled `integrate over Y` with formula text `(k2.k1)(A|x) = SUM_y k2(A|y) k1(y|x)`. Caption: "Kleisli(G): composition = integration against the kernel".
- [ ] **Step 2:** Validate XML parse. **Step 3:** Commit `feat(diagram): giry kleisli composition`

### Task 13: `unc_fuzzy_lattice.svg` (Section 4)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_fuzzy_lattice.svg`, ~680×320. Left: the `[0,1]` interval as a vertical lattice (0 bottom, 1 top) with `min`=meet, `max`=join labels. Right: a small table of connectives — `T-norm min: min(a,b)`, `T-norm prod: a*b`, `Luka: max(0,a+b-1)`, `T-conorm: max(a,b)`, `neg: 1-x`. Bottom: example `tall(175)=0.5 AND young(30)=0.67 -> min=0.5`. Caption: "Fuzzy logic in the lattice ([0,1], min, max)".
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): fuzzy [0,1] lattice`

### Task 14: `unc_kripke_frame.svg` (Section 5)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_kripke_frame.svg`, ~620×300. 4 worlds w1..w4 as circles with accessibility arrows R (show a transitive cluster). Annotate one world with `p=true`. Side legend: `Box p @ w  iff  all R-reachable |= p`; `Dia p @ w iff some R-reachable |= p`. Caption: "Kripke frame (W,R)".
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): kripke frame`

### Task 15: `unc_bayes_net.svg` (Section 6)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_bayes_net.svg`, ~560×300. Sprinkler DAG: `Cloudy -> Sprinkler`, `Cloudy -> Rain`, `Sprinkler -> WetGrass`, `Rain -> WetGrass`. Show small CPT hint boxes. Caption: "Bayesian network = morphism in Kleisli(Dist); update = disintegration".
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): sprinkler bayes net`

### Task 16: `unc_markov_chain.svg` (Section 7)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_markov_chain.svg`, ~600×280. 3-state chain (e.g. Sunny/Cloudy/Rainy) with labeled transition probabilities on arrows (including self-loops). Side note: `stationary: pi P = pi, sum pi = 1`. Caption: "Markov chain = endo-kernel S -> Dist S".
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): markov chain`

### Task 17: `unc_dual_scales.svg` (Section 9, optional support)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_dual_scales.svg`, ~620×260. Two parallel `[0,1]` scales: `L=([0,1],max,min)` and `Lbar=([0,1],min,max)`, with `theta(t)=1-t` mapping arrow between them, and `Pi=sup tau`, `N=inf tauBar`, `L ~ L^op`. Caption: "Dual scales of possibility theory (Pyt'ev)". (Only insert into notebook if it strengthens 9.1 without disrupting reference prose.)
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): possibility dual scales`

### Task 18: `unc_summary_poster.svg` (Summary, the visual channel)

- [ ] **Step 1:** Create `src/diagrams/uncertainty/unc_summary_poster.svg`, ~900×460. A grid/poster mirroring the Task 10 table: rows = {Functor, Dist, Giry, Fuzzy, Modal, Markov, Possibility}; columns = {Category, Endofunctor/Enrichment, Composition, Measure}. Each cell short ASCII text. Color rows by family (wrappers/probabilistic/graded). Title: "Categorical constructions of uncertainty".
- [ ] **Step 2:** Validate. **Step 3:** Commit `feat(diagram): uncertainty summary poster`

### Task 19: Assemble diagrams into notebook

**Files:** Modify section markdown cells via `src/_patch/p_imgs.py`

- [ ] **Step 1:** Verify the image-reference convention other notebooks use (relative path from notebook to `diagrams/...`). Match it exactly.
- [ ] **Step 2:** Insert `![alt](path)` references into the corresponding section cells: sec3→giry, sec4→fuzzy, sec5→kripke, sec6→bayes, sec7→markov, summary→poster, (sec9.1→dual_scales only if Task 17 produced an insert-worthy diagram). Place each image right after the *Идея/конструкция* beat.
- [ ] **Step 3:** Run `p_imgs.py`. Expected: `inserted N images`.
- [ ] **Step 4:** Commit `docs(uncertainty): embed section diagrams`

### Task 20: Final verification + sync

- [ ] **Step 1: Final kernel run.** `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/work/notebooks/_patch/_run.py Uncertainty.ipynb` → Expected `ERRORS: 0`.
- [ ] **Step 2: Image-load check.** Confirm each referenced SVG file exists at the resolved path; no broken `![]`.
- [ ] **Step 3: Update counters.** New cell count and SVG count → update `src/README.ipynb` summary table and `src/ROADMAP.md` Phase 9 checkboxes (mark done). Do NOT restructure README otherwise.
- [ ] **Step 4: Cleanup.** Remove `src/_patch/` scratch scripts (keep `_run.py` if useful), ensure no stray temp files committed.
- [ ] **Step 5: Commit + push.** `git add -A && git commit -m "docs(uncertainty): Phase 9 complete — expanded format, diagrams, summary" && git push`

---

## Self-Review notes
- Spec coverage: skeleton (Tasks 1–8), intro/summary (9–10), 3-channel summary = table (Task 10) + poster (Task 18) + narration paragraph (Task 10); diagrams per heavy section (12–17); applicability boundaries present in every section task. ✓
- Delimiters `$...$` enforced in Task 11 lint. ✓
- SVG rules repeated in Pass 2 header for cold parallel agents. ✓
- Code logic unchanged — only prose/comments + image refs, preserving `ERRORS: 0` invariant. ✓
