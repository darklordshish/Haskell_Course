#!/usr/bin/env python3
"""Task 19: embed section diagrams into Uncertainty.ipynb markdown cells."""
import json, sys

PATH = "/home/jovyan/src/notebooks/Uncertainty.ipynb"

# section heading prefix -> (image markdown, anchor before which to insert)
IMG = {
    "# 3. ": "![Kleisli-композиция монады Гири](../diagrams/uncertainty/unc_giry_kleisli.svg)",
    "# 4. ": "![Решётка [0,1] и связки нечёткой логики](../diagrams/uncertainty/unc_fuzzy_lattice.svg)",
    "# 5. ": "![Фрейм Крипке (W, R)](../diagrams/uncertainty/unc_kripke_frame.svg)",
    "# 6. ": "![Байесовская сеть «поливалки»](../diagrams/uncertainty/unc_bayes_net.svg)",
    "# 7. ": "![Марковская цепь из трёх состояний](../diagrams/uncertainty/unc_markov_chain.svg)",
}
ANCHOR = "## Формализм"

# Section 9.1 special-case: insert dual-scales image after the dual-scales formula.
S91_PREFIX = "## 9.1"
S91_AFTER = r"$$L = ([0,1],\ \max,\ \min), \qquad \bar L = ([0,1],\ \min,\ \max).$$"
S91_IMG = "![Дуальные шкалы L и L^op](../diagrams/uncertainty/unc_dual_scales.svg)"


def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    inserted = 0
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        s = "".join(c["source"])
        for pref, img in IMG.items():
            if s.startswith(pref):
                if img in s:
                    break
                if ANCHOR not in s:
                    print(f"ERROR: anchor not found in {pref}", file=sys.stderr); sys.exit(1)
                s = s.replace(ANCHOR, f"{img}\n\n{ANCHOR}", 1)
                c["source"] = s.splitlines(keepends=True)
                inserted += 1
                break
        else:
            if s.startswith(S91_PREFIX) and S91_IMG not in s:
                if S91_AFTER not in s:
                    print("ERROR: 9.1 formula anchor not found", file=sys.stderr); sys.exit(1)
                s = s.replace(S91_AFTER, f"{S91_AFTER}\n\n{S91_IMG}", 1)
                c["source"] = s.splitlines(keepends=True)
                inserted += 1
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"inserted {inserted} images")


if __name__ == "__main__":
    main()
