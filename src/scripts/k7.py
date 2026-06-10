#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 7 (adjunctions via Ran)."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 7️⃣ Сопряжения через Ran

## Мотивация

Сопряжения — центральное понятие теории категорий — тоже оказываются расширениями Кана
тождественного функтора. Это сводит ещё одну «фундаментальную» конструкцию к Ran/Lan.

## Идея и категорный смысл

Если `f ⊣ g` (f слева сопряжён g), то:

- **правый сопряжённый** `g ≅ Ran f Id` — правое расширение `Id` вдоль `f`;
- **левый сопряжённый** `f ≅ Lan g Id` — левое расширение `Id` вдоль `g`.

### Диаграмма

![Сопряжения через расширения Кана](../diagrams/kan/kan_adjunction.svg)

## Формализм

Сопряжение задаётся изоморфизмом $\mathrm{Hom}(f\,a, b) \cong \mathrm{Hom}(a, g\,b)$,
естественным по `a`, `b`. Единица $\eta : \mathrm{Id} \to g f$ и коединица
$\varepsilon : f g \to \mathrm{Id}$ удовлетворяют треугольным тождествам. Формула
$g \cong \mathrm{Ran}_f \mathrm{Id}$ выражает правый сопряжённый как расширение Кана.

## Код и демонстрация

В ячейке — `adjUnit`/`adjCounit` для канонического сопряжения. Они реализуют $\eta$ и
$\varepsilon$; на них держатся треугольные тождества.

## Пример из жизни

Каррирование `(e,) ⊣ (e->)`: `adjUnit a e = (e, a)` и `adjCounit (e, f) = f e` — это
$\eta$ и $\varepsilon$ сопряжения «произведение слева, экспонента справа», восстановленного
как расширение Кана.

## Границы применимости

Формулы работают, **только когда сопряжение существует**: не у всякого функтора есть
сопряжённый. Тогда `Ran f Id` либо не существует, либо не является функтором-сопряжённым.

## Мостик

Любое сопряжение автоматически порождает монаду — это следующий раздел.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 7️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec7")

if __name__ == "__main__": main()
