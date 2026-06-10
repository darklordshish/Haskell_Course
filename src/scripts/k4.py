#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 4 (Codensity)."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 4️⃣ Монада плотности (Codensity)

## Мотивация

Удивительный факт: **любой** функтор `f` — даже не являющийся монадой — порождает монаду
`Ran f f`. Это даёт универсальный способ «омонадить» функтор и попутно ускорить вычисления.

## Идея и категорный смысл

Монада плотности (codensity monad) — это `Codensity f = Ran f f`. Её структура — это CPS
(continuation-passing style): вычисление параметризовано «продолжением» `a -> f b`. Именно CPS
организует `>>=` **правоассоциативно**.

```haskell
newtype Codensity f a = Codensity { runCodensity :: forall b. (a -> f b) -> f b }
```

### Диаграмма

![Codensity: CPS-преобразование и оптимизация](../diagrams/kan/kan_codensity.svg)

## Формализм

$$\mathrm{Codensity}\,f \;=\; \mathrm{Ran}_f f \;=\; \int_b\, f(b)^{\,(a \to f b)}.$$
Инстанс `Monad (Codensity f)` определён для **любого** `f` без всяких ограничений: `return`
кладёт значение в продолжение, `>>=` компонует продолжения.

## Код и демонстрация

В ячейке — `newtype Codensity` и его `Monad`-инстанс. Ключевой момент: `>>=` не строит
промежуточных структур, а **сцепляет продолжения**, поэтому глубоко вложенные `>>=` не
деградируют по скорости.

## Пример из жизни

Ускорение свободных монад и `>>=`-тяжёлого кода: оборачивание в `Codensity` превращает
лево-вложенные связывания в правоассоциативные. Прямой мост к разделу 9 (DList).

## Границы применимости

Выигрыш есть только там, где важна правоассоциативность; иначе остаётся накладной расход на
обёртку `forall b. (a -> f b) -> f b`. Семантика `f` при этом сохраняется.

## Мостик

Двойственная конструкция `Lan f f` даёт не монаду, а комонаду — Density.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 4️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec4")

if __name__ == "__main__": main()
