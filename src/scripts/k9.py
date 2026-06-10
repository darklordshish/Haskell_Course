#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions Section 9 (Codensity optimization) + dedicated diagram."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""## 9️⃣ Оптимизация через Codensity

## Мотивация

Лево-вложенная конкатенация `((a ++ b) ++ c) ++ d` пересобирает левый список снова и снова —
это $O(n^2)$. Codensity (через difference lists) превращает её в $O(n)$. Чистая теория Кана
даёт измеримое ускорение.

## Идея и категорный смысл

`DList = Codensity []`. Список представляется **функцией** `[a] -> [a]` (отложенный «хвост»),
а конкатенация становится композицией функций — она правоассоциативна по построению.

```haskell
newtype DList a = DList { runDList :: [a] -> [a] }
```

### Диаграмма

![DList: O(n^2) против O(n)](../diagrams/kan/kan_dlist.svg)

## Формализм

`++` для `DList` — это `(.)`: `append (DList f) (DList g) = DList (f . g)`. Композиция
ассоциативна и не пересобирает левый аргумент, поэтому суммарная стоимость построения списка
из `n` кусков падает с $O(n^2)$ до $O(n)$. `toList d = runDList d []`.

## Код и демонстрация

В ячейке — `DList` с `emptyDL`, `singletonDL`, конкатенацией через `(.)` и `toList`.
Демонстрация показывает, что лево-вложенные склейки больше не деградируют.

## Пример из жизни

Сборка больших списков/строк по кускам: логирование, `ShowS` (`String -> String`),
рефлексия свободных монад — всюду difference lists убирают квадратичность.

## Границы применимости

Есть постоянный накладной расход на обёртку-функцию; выигрыш — только при **лево-вложенной**
ассоциации. Для право-ассоциированного кода обычный список уже оптимален.

## Мостик

Сведём всю карту расширений Кана воедино — в итоговой сводке.
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("## 9️⃣"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan sec9")

if __name__ == "__main__": main()
