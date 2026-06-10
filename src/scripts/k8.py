#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 8 (monad from adjunction) + new diagram ref."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 8️⃣ Монада из сопряжения

## Мотивация

Откуда вообще берутся монады? Один из главных источников: **каждое сопряжение порождает
монаду**. Это объясняет, почему State, Maybe, список — монады «не случайно».

## Идея и категорный смысл

Если `f ⊣ g`, то композиция `T = g ∘ f` — монада, причём её структура читается из
единицы/коединицы сопряжения:

$$\mathrm{return} = \eta, \qquad \mathrm{join} = g\,\varepsilon\,f.$$

### Диаграмма

![Монада из сопряжения: T = g . f](../diagrams/kan/kan_monad_adj.svg)

## Формализм

`return = η : Id → g f = T` — единица сопряжения. `join = g ε f : T T = g f g f → g f = T`
применяет коединицу $\varepsilon : f g → \mathrm{Id}$ «в середине». Законы монады следуют из
треугольных тождеств сопряжения.

## Код и демонстрация

В ячейке — `StateM s` как монада. Она возникает из сопряжения `(s,) ⊣ (s->)`: композиция
`g ∘ f = (s ->) ∘ (s, -)` даёт `s -> (a, s)` — в точности `State`.

## Пример из жизни

Три классические пары «сопряжение → монада»:

| Сопряжение | Монада |
|---|---|
| `(e,) ⊣ (e->)` | `State` (через `s -> (a,s)`) |
| `Free ⊣ Forget` | `[]` / свободная монада |
| `Maybe-структура ⊣ Id` | `Maybe` |

## Границы применимости

Прямое направление всегда даёт монаду. **Обратное** — что *всякая* монада возникает из
сопряжения — верно, но требует конструкций Эйленберга–Мура или Клейсли (отдельная теория).

## Мостик

Codensity — это не только теория, но и практический приём ускорения; о нём — финальный раздел.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 8️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec8")

if __name__ == "__main__": main()
