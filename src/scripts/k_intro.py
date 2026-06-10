#!/usr/bin/env python3
"""Pass-1 prose: KanExtensions intro framing."""
import json, sys
PATH = "/home/jovyan/src/notebooks/KanExtensions.ipynb"

MD = r"""# 🔭 Расширения Кана в Haskell

Расширения Кана — наиболее общие конструкции в теории категорий.
МакЛейн: *«Все концепции — это расширения Кана».*

**Сквозная идея ноутбука.** Есть всего **две** универсальные операции продолжения функтора `h`
вдоль функтора `g`: правое расширение `Ran g h` (наилучшее приближение справа, *end*,
кодируется `forall`) и левое `Lan g h` (слева, *coend*, кодируется экзистенциалом). Почти всё
остальное в этой главе — их частные случаи:

- **лемма Ёнеды** = `Ran Id h ≅ h`;
- **сопряжённые функторы** = расширения Кана тождественного функтора (`g ≅ Ran f Id`);
- **монада/комонада плотности** (Codensity/Density) = расширение функтора *вдоль самого себя*;
- **монада из сопряжения** `T = g∘f` — отсюда же берутся State, Maybe, список;
- практический выхлоп: **fmap-fusion** (Yoneda) и **right-association `>>=`** (Codensity/DList).

## Содержание
1. **Правое расширение Кана (Ran)** — приближение справа, *end*, `forall b. (a->g b)->h b`
2. **Левое расширение Кана (Lan)** — приближение слева, *coend*, экзистенциал
3. **Конкретные примеры** — Ran/Lan восстанавливают `Maybe`, `[]`, `Either`
4. **Монада плотности (Codensity)** — `Ran f f`: любой функтор → монада, CPS
5. **Комонада плотности (Density)** — `Lan f f`: двойственная комонада
6. **Лемма Ёнеды как Ran Id** — частный случай при `g = Id`
7. **Сопряжения через Ran** — `g ≅ Ran f Id`, `f ≅ Lan g Id`
8. **Монада из сопряжения** — `f ⊣ g ⇒ T = g∘f`
9. **Оптимизация через Codensity** — DList, `O(n²) → O(n)`

> **Как читать.** Каждый раздел построен по единой схеме: *мотивация → идея и категорный смысл →
> формализм → код и демонстрация → пример из жизни → границы применимости → мостик к следующему
> разделу*. Итоговая сводка сводит все конструкции в одну карту, таблицу и абзац.
---
"""

def main():
    with open(PATH, encoding="utf-8") as f: nb = json.load(f)
    n = 0
    for c in nb["cells"]:
        if c["cell_type"] == "markdown" and "".join(c["source"]).startswith("# 🔭"):
            c["source"] = MD.splitlines(keepends=True); n += 1
    if n != 1:
        print(f"ERROR matched {n}", file=sys.stderr); sys.exit(1)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print("patched kan intro")

if __name__ == "__main__": main()
