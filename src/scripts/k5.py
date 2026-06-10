#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 5 (Density)."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 5️⃣ Комонада плотности (Density)

## Мотивация

По принципу двойственности у Codensity есть зеркальный близнец: если `Ran f f` — монада, то
`Lan f f` — **комонада**. Это завершает симметричную картину «расширение функтора вдоль себя».

## Идея и категорный смысл

Комонада плотности (density comonad) — это `Density f = Lan f f`. Симметрия:

| Конструкция | Что это | Операции |
|---|---|---|
| `Codensity f = Ran f f` | монада | `return`, `>>=` |
| `Density f = Lan f f` | комонада | `extract`, `duplicate` |

```haskell
data Density f a = forall b. Density (f b -> a) (f b)
```

### Диаграмма

![Density comonad: Lan f f](../diagrams/kan/kan_density.svg)

## Формализм

$$\mathrm{Density}\,f \;=\; \mathrm{Lan}_f f \;=\; \int^{b}\, (f b \to a)\,\times\,f(b).$$
Инстанс `Comonad (Density f)` существует для любого `f`: `extract` применяет упакованную
функцию `f b -> a` к упакованному `f b`, `duplicate` раздваивает контекст.

## Код и демонстрация

В ячейке — `data Density` с экзистенциалом и инстансы `Functor`/`Comonad`. Значение несёт
«контекст» `f b` вместе со способом извлечь из него `a`.

## Пример из жизни

Вычисления, несущие контекст (по духу близко к комонаде `Store`): значение + способ его
интерпретировать. На практике встречается реже, чем Codensity.

## Границы применимости

Экзистенциал прячет `b` (только параметрическое использование). Density полезна в специфических
сценариях «контекстно-зависимых» вычислений и редка в обычном коде.

## Мостик

Самый знаменитый частный случай `Ran` — лемма Ёнеды (при `g = Id`).
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 5️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec5")

if __name__ == "__main__": main()
