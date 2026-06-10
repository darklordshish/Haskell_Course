# KanExtensions.ipynb Expanded Rework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Rework `src/notebooks/KanExtensions.ipynb` into the verbose teaching format established for Uncertainty (Phase 9): full per-section skeleton, more illustrative examples, fixed + new SVG diagrams, and a 3-channel summary.

**Architecture:** Two passes. Pass 1 (prose) rewrites all markdown inline (single voice) + adds a summary section, one kernel run verifies. Pass 2 (visual) fixes the 7 existing kan SVGs and adds 3 new ones (parallel agents), assembles refs, final run. Edits via Python patch scripts in container `haskell_course_git-ihaskell-1`.

**Tech Stack:** IHaskell/Jupyter in Docker; Python json patch scripts + `src/scripts/_run.py` executor (already exists); SVG canonical style.

---

## Conventions (reuse from Phase 9)

- Mount root in container: `/home/jovyan/src/` (notebooks at `/home/jovyan/src/notebooks/`).
- Patch scripts under `src/scripts/`; run via `MSYS_NO_PATHCONV=1 docker exec haskell_course_git-ihaskell-1 python3 /home/jovyan/src/scripts/<name>.py`.
- `json.load`/`json.dump(..., ensure_ascii=False, indent=1)`; locate cells by heading prefix, not index.
- Executor: `python3 /home/jovyan/src/scripts/_run.py KanExtensions.ipynb` → expect `ERRORS: 0`.
- Lint: `_lint.py` (adapt PATH to KanExtensions) — no `\(...\)`, balanced `$`.
- SVG rules: `<defs>` first; `viewBox="0 0 W H"` matching width/height; white bg `#ffffff`; ASCII text only; `font-family="monospace,Arial,sans-serif"`; light palette (#2255cc/#7733aa/#16a34a/#334466); valid XML.

**Per-section skeleton:** Мотивация → Идея/категорный смысл → Формализм (`$...$`) → Код+демо → Пример из жизни → Границы применимости → Мостик. Keep existing code cells; existing diagram refs stay (fix paths in Pass 2).

---

## Task 0: Branch + infra check

- [ ] **Step 1:** `git checkout master && git pull` then `git checkout -b phase10-kan-rework`.
- [ ] **Step 2:** Baseline run: `_run.py KanExtensions.ipynb` → expect `ERRORS: 0`.
- [ ] **Step 3:** Commit (none yet) — proceed.

---

## PASS 1 — PROSE (Tasks 1–12)

Each task: patch script replaces the section markdown cell `source` with the expanded skeleton. Existing `### Диаграмма` + image refs are PRESERVED inside the cell (the *Идея* beat references the diagram). Do not run kernel per-section; batch verify in Task 12.

### Task 1: Section 1 — Ran (right Kan extension)
- [ ] Expand cell `## 1️⃣`:
  - *Мотивация:* we have `h : C -> E` but want a functor on `D`; Ran is the **best (universal) approximation** to "extending h along g" from the right.
  - *Идея:* `Ran g h` is the right Kan extension; universal property = terminal among cones; in Haskell `forall b. (a -> g b) -> h b` (end formula). Keep the `### Диаграмма` ref `../diagrams/kan/ran_diagram.svg`.
  - *Формализм:* $\mathrm{Ran}_g h\,(d) = \int_{c} h(c)^{D(d,\,g c)}$ (end); Haskell newtype shown.
  - *Код+демо:* point to the `Ran` newtype + any demo; explain the `forall b` quantifier encodes the end.
  - *Пример из жизни:* "continuation-like" — given any way to map `a` into `g b`, produce `h b`; precursor to Codensity (CPS).
  - *Границы:* needs RankNTypes; Ran exists only when the relevant (co)limits exist; in Hask we work with the end encoding, not arbitrary categories.
  - *Мостик:* dual construction from the left — Lan.
- [ ] Run script; commit `docs(kan): expand section 1 (Ran)`.

### Task 2: Section 2 — Lan (left Kan extension)
- [ ] Expand `## 2️⃣`:
  - *Мотивация:* the left/initial dual — best approximation from the **left**.
  - *Идея:* `Lan g h` = left Kan extension; coend formula; Haskell existential `data Lan g h a = forall b. Lan (g b -> a) (h b)`. Keep `lan_diagram.svg` ref.
  - *Формализм:* $\mathrm{Lan}_g h\,(d) = \int^{c} D(g c,\,d) \times h(c)$ (coend); existential = the coend's "there exists b".
  - *Код+демо:* the existential encoding; explain pair `(g b -> a, h b)`.
  - *Пример из жизни:* `Lan (:[]) Id ≅ []` — list as left Kan; "free" feel.
  - *Границы:* existential hides `b` — you can only use it parametrically; needs ExistentialQuantification.
  - *Мостик:* concrete functors via Kan — Maybe/[]/Either.
- [ ] Run; commit `docs(kan): expand section 2 (Lan)`.

### Task 3: Section 3 — Concrete examples (Maybe/[]/Either)
- [ ] Expand `## 3️⃣`. **Fix the broken diagram ref here**: change `![...](kan_examples.svg)` → `![Конкретные примеры Ran/Lan](../diagrams/kan/kan_examples.svg)`.
  - *Мотивация:* abstract Kan becomes concrete — recover familiar functors via universal properties.
  - *Идея:* `Ran Just Id ≅ Maybe`, `Lan (:[]) Id ≅ []`, `Ran Left Id ≅ Either e`.
  - *Формализм:* show the round-trip isos as type equalities.
  - *Код+демо:* the `fromRanMaybe`/`LanList` cells; explain the round-trip recovers the functor.
  - *Пример из жизни:* "every functor is a Kan extension" — practical lens: derive `Maybe` from `Just`.
  - *Границы:* the iso holds up to the end/coend encoding; performance not the point here.
  - *Мостик:* a functor extended along itself gives a monad — Codensity.
- [ ] Run; commit `docs(kan): expand section 3 + fix kan_examples ref`.

### Task 4: Section 4 — Codensity monad
- [ ] Expand `## 4️⃣` (keep `kan_codensity.svg` ref):
  - *Мотивация:* any functor `f` yields a monad `Ran f f`, even non-monadic ones.
  - *Идея:* Codensity = `Ran f f`; CPS structure; right-associates `>>=`.
  - *Формализм:* `newtype Codensity f a = Codensity { runCodensity :: forall b. (a -> f b) -> f b }`; monad instance.
  - *Код+демо:* the Codensity newtype + monad; explain `>>=` composition.
  - *Пример из жизни:* speeding up free monads / `>>=`-heavy code; bridges to section 9 (DList).
  - *Границы:* benefit only when right-association matters; extra wrapping overhead otherwise.
  - *Мостик:* dual gives a comonad — Density.
- [ ] Run; commit `docs(kan): expand section 4 (Codensity)`.

### Task 5: Section 5 — Density comonad
- [ ] Expand `## 5️⃣` (keep `kan_density.svg` ref):
  - *Мотивация:* the comonadic dual of Codensity.
  - *Идея:* Density = `Lan f f`; symmetry table Codensity(monad) vs Density(comonad).
  - *Формализм:* `data Density f a = forall b. Density (f b -> a) (f b)`; comonad instance (`extract`, `duplicate`).
  - *Код+демо:* the Density type + comonad.
  - *Пример из жизни:* context-carrying computations; relation to Store-like comonads.
  - *Границы:* existential; less commonly used than Codensity in practice.
  - *Мостик:* the most famous special case of Ran — Yoneda.
- [ ] Run; commit `docs(kan): expand section 5 (Density)`.

### Task 6: Section 6 — Yoneda as Ran Id
- [ ] Expand `## 6️⃣` (keep `kan_yoneda.svg` ref):
  - *Мотивация:* the Yoneda lemma is not separate magic — it's `Ran Id h ≅ h`.
  - *Идея:* set `g = Id`; the end collapses; `Nat(Hom(a,-), h) ≅ h a`.
  - *Формализм:* `newtype Yoneda f a = Yoneda { runYoneda :: forall b. (a -> b) -> f b }`; iso to `f a`.
  - *Код+демо:* Yoneda type + `liftYoneda`/`lowerYoneda` round-trip; fmap-fusion note.
  - *Пример из жизни:* fmap fusion — collapse a chain of `fmap` into one.
  - *Границы:* iso is parametric; benefit is fusion, not expressiveness.
  - *Мостик:* Kan also recovers adjoints — adjunctions via Ran.
- [ ] Run; commit `docs(kan): expand section 6 (Yoneda)`.

### Task 7: Section 7 — Adjunctions via Ran
- [ ] Expand `## 7️⃣` (keep `kan_adjunction.svg` ref):
  - *Мотивация:* even adjunctions are Kan extensions of the identity.
  - *Идея:* if `f ⊣ g` then `Ran f Id ≅ g` and `Lan g Id ≅ f`.
  - *Формализм:* state the isos; right adjoint = Ran of Id along f.
  - *Код+демо:* the `adjUnit`/`adjCounit` cell; explain unit/counit.
  - *Пример из жизни:* `(e,) ⊣ (e->)` (currying) recovered as Kan.
  - *Границы:* needs an actual adjunction to exist; not every functor has an adjoint.
  - *Мостик:* an adjunction always yields a monad.
- [ ] Run; commit `docs(kan): expand section 7 (adjunctions via Ran)`.

### Task 8: Section 8 — Monad from adjunction
- [ ] Expand `## 8️⃣`. Add NEW diagram ref `![Монада из сопряжения](../diagrams/kan/kan_monad_adj.svg)` after the *Идея* beat.
  - *Мотивация:* where do monads come from? Every adjunction makes one.
  - *Идея:* `f ⊣ g ⇒ T = g∘f` is a monad; `return = η`, `join = g·ε·f`.
  - *Формализм:* the composite + unit/counit derivation.
  - *Код+демо:* the `StateM` cell; explain `(e,) ⊣ (e->)` gives `State`.
  - *Пример из жизни:* State/Maybe/[] all arise this way (give the 3 adjunction→monad pairs).
  - *Границы:* the converse (every monad from an adjunction) needs Eilenberg–Moore/Kleisli — mention briefly.
  - *Мостик:* Codensity as a practical optimization.
- [ ] Run; commit `docs(kan): expand section 8 (monad from adjunction)`.

### Task 9: Section 9 — Codensity optimization
- [ ] Expand `## 9️⃣`. Switch its diagram ref to a NEW dedicated one `![DList: O(n^2) -> O(n)](../diagrams/kan/kan_dlist.svg)` (currently it reuses kan_codensity.svg).
  - *Мотивация:* left-nested `++`/`>>=` is O(n²); Codensity fixes it.
  - *Идея:* `DList = Codensity []`; difference lists right-associate appends.
  - *Формализм:* `newtype DList a = DList { runDList :: [a] -> [a] }`; `O(n²)→O(n)`.
  - *Код+демо:* the `DList` cell; explain the function-composition trick.
  - *Пример из жизни:* logging/building big lists, `ShowS`, free monad reflection.
  - *Границы:* constant-factor overhead; helps only for left-nested association.
  - *Мостик:* (final section before summary) — wrap up in the summary.
- [ ] Run; commit `docs(kan): expand section 9 (Codensity optimization)`.

### Task 10: Intro cell
- [ ] Expand `# 🔭` intro: keep MacLane quote; add a framing paragraph (Ran/Lan as the two universal extensions; everything else — Yoneda, adjoints, density monads — are special cases). Expand the Содержание into a one-line-each annotated list. Add a "как читать" note (the 7-beat skeleton).
- [ ] Run; commit `docs(kan): expand intro framing`.

### Task 11: Summary section (NEW cell, 3 channels)
- [ ] Insert a new markdown cell before the nav-footer cell (id `nav-footer`), titled `## 🔟 Сводка: карта расширений Кана`:
  - **SVG poster** ref `![Карта расширений Кана](../diagrams/kan/kan_summary_poster.svg)` (built in Pass 2).
  - **Table:** rows = {Ran, Lan, Codensity, Density, Yoneda, Adjunction-as-Kan, Monad-from-adj}, columns = Определение / Haskell-тип / Частный случай или связь / Польза.
  - **Narration paragraph:** Ran/Lan are the two universal extensions; Yoneda = `Ran Id`, adjoints = Kan of Id, density (co)monads = Kan of f along itself; the practical payoff is fusion (Yoneda) and right-association (Codensity/DList).
  - Insert via patch script that adds a cell with a fresh id right before the cell whose source starts with `---\n\n**← Предыдущий:`.
- [ ] Run; commit `docs(kan): add 3-channel summary section`.

### Task 12: Pass-1 verification
- [ ] **Step 1:** `_run.py KanExtensions.ipynb` → `ERRORS: 0`.
- [ ] **Step 2:** `_lint.py` (PATH=KanExtensions) → no `\(...\)`, balanced `$`. Note: existing prose uses unicode `≅ ⊣ · η ε` in markdown — that is allowed in markdown (only SVG must be ASCII). Lint only checks delimiters/`$` balance.
- [ ] **Step 3:** commit `test(kan): pass-1 prose executes clean, delimiters linted`.

---

## PASS 2 — VISUAL (Tasks 13–17)

### Task 13: Fix the 7 existing kan SVGs (parallel-safe, one agent or split)
Files: `src/diagrams/kan/{ran_diagram,lan_diagram,kan_codensity,kan_density,kan_yoneda,kan_adjunction,kan_examples}.svg`
- [ ] For EACH file: add `viewBox="0 0 W H"` matching its `width`/`height`; ensure a `<rect ... fill="#ffffff"/>` background exists (add if missing); ensure `<defs>` is first; verify all elements fit inside the viewBox (fix obvious overflow/misalignment); keep content meaning unchanged.
- [ ] **`kan_examples.svg` specifically:** replace all 9 non-ASCII chars with ASCII/translit (e.g. Cyrillic labels → Latin), keep the Maybe/[]/Either example content.
- [ ] Validate each: PowerShell `[xml]` parse OK, non-ASCII count = 0.
- [ ] Commit `fix(diagram): add viewBox + white bg + ASCII to 7 kan SVGs`.

### Task 14: New SVG — monad from adjunction
- [ ] Create `src/diagrams/kan/kan_monad_adj.svg` (~600x260): `f ⊣ g` (written "f -| g") → composite `T = g . f`, with `unit = eta`, `join = g . eps . f`, and a row of examples `(e,) -| (e->) => State`, `Maybe -| Id => Maybe`. ASCII only, viewBox, white bg, valid XML. Validate.
- [ ] Commit `feat(diagram): kan monad-from-adjunction`.

### Task 15: New SVG — DList optimization
- [ ] Create `src/diagrams/kan/kan_dlist.svg` (~620x260): left-nested `((a++b)++c)++d` O(n^2) vs right-associated via `DList = Codensity []` O(n); show function-composition of `[a]->[a]`. ASCII only, viewBox, white bg, valid XML. Validate.
- [ ] Commit `feat(diagram): kan DList O(n^2)->O(n)`.

### Task 16: New SVG — summary poster
- [ ] Create `src/diagrams/kan/kan_summary_poster.svg` (~900x460): grid titled "Map of Kan extensions". Rows {Ran, Lan, Codensity=Ran f f, Density=Lan f f, Yoneda=Ran Id, Adjoint=Ran/Lan of Id, Monad=g.f}, columns {Definition, Haskell type, Special case / link, Payoff}. Color families. ASCII only, viewBox, white bg, valid XML. Validate.
- [ ] Commit `feat(diagram): kan summary poster`.

### Task 17: Final verification + sync
- [ ] **Step 1:** Confirm every image ref in the notebook resolves to an existing file (grep refs → check files). No broken `![]`.
- [ ] **Step 2:** Final kernel run `_run.py KanExtensions.ipynb` → `ERRORS: 0`.
- [ ] **Step 3:** Update README counters: KanExtensions diagrams `6 SVG` → `9 SVG` (card + summary-table row 13) and totals `76` → `79 SVG`; cell count `24` → new count (after adding 1 summary cell ⇒ 25). Update both card and table row and totals line.
- [ ] **Step 4:** ROADMAP: add Phase 10 section marked complete.
- [ ] **Step 5:** Cleanup one-off patch scripts (keep `_run.py`, `_lint.py`).
- [ ] **Step 6:** Commit; merge to master on user approval.

---

## Self-Review notes
- Skeleton covers all 9 sections + intro + new summary (Tasks 1–11). ✓
- Broken `kan_examples.svg` ref fixed (Task 3) and its non-ASCII fixed (Task 13). ✓
- viewBox added to all 7 (Task 13) — addresses "crooked" rendering. ✓
- Section 9 gets its own diagram (was sharing kan_codensity) — Tasks 9 + 15. ✓
- 3-channel summary = poster (Task 16) + table + narration (Task 11). ✓
- Cell count changes by +1 (summary) → README must say 25; SVG 6→9. Captured in Task 17. ✓
