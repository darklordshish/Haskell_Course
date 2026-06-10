#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 6 (Yoneda as Ran Id)."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 6️⃣ Лемма Ёнеды как частный случай Ran

## Мотивация

Лемму Ёнеды часто подают как отдельное «волшебство». На самом деле это **простейший частный
случай** правого расширения Кана: расширение вдоль тождественного функтора.

## Идея и категорный смысл

При `g = Id` расширение схлопывается: `Ran Id h ≅ h`. Разворачивая end-формулу, получаем
ровно лемму Ёнеды:
$$\mathrm{Nat}(\mathrm{Hom}(a,-),\,h) \;\cong\; h(a).$$

```haskell
newtype Yoneda f a = Yoneda { runYoneda :: forall b. (a -> b) -> f b }
```

### Диаграмма

![Yoneda как частный случай Ran Id](../diagrams/kan/kan_yoneda.svg)

## Формализм

$\mathrm{Ran}_{\mathrm{Id}} h \cong h$, потому что $\int_b h(b)^{(a\to b)} \cong h(a)$
(подстановка $b := a$, $\mathrm{id}_a$ — универсальный элемент). Тип `Yoneda f a` изоморфен
`f a` через `liftYoneda`/`lowerYoneda`.

## Код и демонстрация

В ячейке — `newtype Yoneda` и round-trip `liftYoneda`/`lowerYoneda`. Главное наблюдение:
`fmap g . fmap f` внутри `Yoneda` склеивается в одно применение — это **fmap-fusion**.

## Пример из жизни

Слияние `fmap` (fmap fusion): длинная цепочка `fmap`-ов над структурой сливается в один проход,
устраняя промежуточные аллокации. `Yoneda` делает это бесплатно за счёт отложенной композиции.

## Границы применимости

Изоморфизм параметрический; выигрыш — в *слиянии*, а не в выразительности (`Yoneda f a` и `f a`
содержат одно и то же). Польза проявляется при многократном `fmap`.

## Мостик

Расширения Кана восстанавливают и **сопряжённые** функторы — сопряжения через Ran.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 6️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec6")

if __name__ == "__main__": main()
