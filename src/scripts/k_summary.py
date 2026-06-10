#!/usr/bin/env python3
"""Pass-1 prose: insert new 3-channel summary section before nav footer."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 🔟 Сводка: карта расширений Кана

Девять разделов складываются в одну картину: всё держится на двух универсальных операциях —
правом `Ran` и левом `Lan` расширениях. Остальное — их частные случаи и приложения.

![Карта расширений Кана](../diagrams/kan/kan_summary_poster.svg)

| Конструкция | Определение | Haskell-тип | Частный случай / связь | Польза |
|---|---|---|---|---|
| **Ran g h** | правое расширение, *end* | `forall b. (a->g b)->h b` | база | универсальное приближение справа |
| **Lan g h** | левое расширение, *coend* | `exists b. (g b->a, h b)` | база | универсальное приближение слева |
| **Codensity f** | `Ran f f` | `forall b. (a->f b)->f b` | монада из любого `f` | правоассоц. `>>=` |
| **Density f** | `Lan f f` | `exists b. (f b->a, f b)` | комонада из любого `f` | контекстные вычисления |
| **Yoneda** | `Ran Id h ≅ h` | `forall b. (a->b)->f b` | `g = Id` | fmap-fusion |
| **Сопряжение** | `g ≅ Ran f Id` | — | расширение `Id` вдоль `f` | восстановление сопряжённых |
| **Монада из ⊣** | `T = g∘f` | напр. `s->(a,s)` | `f ⊣ g ⇒ монада` | происхождение State/Maybe/[] |

### Единая картина

`Ran` и `Lan` — две универсальные операции продолжения функтора. Лемма Ёнеды — это `Ran` вдоль
тождества; сопряжённые функторы — расширения `Id`; монада и комонада плотности — расширение
функтора вдоль самого себя; а композиция сопряжённых даёт монаду. Практический выигрыш везде
один и тот же по духу: **отложить и склеить** — слить цепочку `fmap` (Yoneda) или
правоассоциировать `>>=`/`++` (Codensity, DList). Поэтому «все концепции — расширения Кана»:
это не лозунг, а буквальный способ вывести знакомые конструкции из одного универсального свойства.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    # find nav footer cell index
    idx = None
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("---") \
           and "Предыдущий" in "".join(c["source"]):
            idx = i; break
    if idx is None:
        print("ERROR: nav footer not found", file=sys.stderr); sys.exit(1)
    # idempotency: skip if summary already present
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 🔟 Сводка"):
            print("summary already present"); return
    new_cell = {
        "cell_type": "markdown",
        "id": "kan-summary",
        "metadata": {},
        "source": MD.splitlines(keepends=True),
    }
    nb["cells"].insert(idx, new_cell)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"inserted summary before cell {idx}")

if __name__ == "__main__": main()
