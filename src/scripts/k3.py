#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 3 (concrete examples) + fix broken diagram ref."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 3️⃣ Конкретные примеры: Ran/Lan для Maybe, [], Either

## Мотивация

Абстрактные `Ran`/`Lan` становятся осязаемыми, когда из них **восстанавливаются знакомые
функторы**. Лозунг «всякий функтор — это расширение Кана» здесь обретает конкретику.

## Идея и категорный смысл

Беря тождественный `h = Id` и подходящую вкладку `g`, получаем привычные типы:

- **`Ran Just Id ≅ Maybe`** — правый сопряжённый к `Just`;
- **`Lan (:[]) Id ≅ []`** — левый сопряжённый к `singleton`;
- **`Ran Left Id ≅ Either e`** — правый сопряжённый к `Left`.

### Диаграмма

![Конкретные примеры Ran/Lan для Maybe, [], Either](../diagrams/kan/kan_examples.svg)

## Формализм

Изоморфизмы означают **round-trip без потерь**: `Maybe a ≅ Ran Just Id a` через пару
функций `toRan`/`fromRan`, и аналогично для остальных. Тип-уровневое равенство восстанавливает
исходный функтор из его универсального свойства.

## Код и демонстрация

В ячейках — `fromRanMaybe` (восстановление `Maybe` из `Ran`) и `LanList` (список как `Lan`).
Демонстрация показывает, что round-trip возвращает исходное значение: универсальное свойство
не теряет информации.

## Пример из жизни

Практический взгляд: «`Maybe` — это `Just`, продолженный по Кану». Так любой функтор можно
*вывести* из более примитивной операции, а не постулировать.

## Границы применимости

Изоморфизм держится в рамках end/coend-кодировки; это утверждение о **выразимости**, а не об
эффективности — round-trip через `Ran`/`Lan` обычно дороже прямого функтора.

## Мостик

Если расширять функтор **вдоль самого себя** (`Ran f f`), получится монада — Codensity.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 3️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec3 (+fixed kan_examples ref)")

if __name__ == "__main__": main()
