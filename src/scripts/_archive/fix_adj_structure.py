import json

nb_path = '/home/jovyan/src/Adjunctions.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

def get_src(cell):
    s = cell['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(cell, text):
    cell['source'] = text

# Текущая структура разделов:
# [18] ## 9⃣ Законы и итоги  <- это старый раздел 9 (итоги)
# [20] ## 6.5 State => Store  <- дубликат/расширение  
# [22] ## 7⃣ Representable    <- нумерация конфликтует с [14]
# [24] ## 8⃣ Limits и Colimits
# [26] ## 9⃣ Расширения Кана
# [28] ## 10⃣ Зоопарк
# [30] ## Диаграмма: структура сопряжения  <- нужно убрать как отдельную ячейку, слить с [31]

# Переименуем разделы 20-28:
# [20] 6.5 -> 10⃣ State Monad / Store Comonad: глубокое погружение
# [22] 7⃣ -> 11⃣ Representable функторы
# [24] 8⃣ -> 12⃣ Limits и Colimits
# [26] 9⃣ -> 13⃣ Расширения Кана
# [28] 10⃣ -> 14⃣ Зоопарк сопряжений

replacements = {
    20: ('## 6.5 State', '## 1️⃣0️⃣ State Monad / Store Comonad: глубокое погружение'),
    22: ('## 7️⃣ Representable', '## 1️⃣1️⃣ Representable'),
    24: ('## 8️⃣ Limits', '## 1️⃣2️⃣ Limits'),
    26: ('## 9️⃣ Расширения Кана', '## 1️⃣3️⃣ Расширения Кана'),
    28: ('## 🔟 Зоопарк', '## 1️⃣4️⃣ Зоопарк'),
}

for idx, (old_prefix, new_prefix) in replacements.items():
    src = get_src(cells[idx])
    # Найти строку с заголовком и заменить
    lines = src.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('## ') and old_prefix.split(' ', 1)[1] in line:
            lines[i] = new_prefix + line[line.index(old_prefix.split(' ', 1)[1]) + len(old_prefix.split(' ', 1)[1]):]
            break
    set_src(cells[idx], '\n'.join(lines))
    print(f'  Ячейка {idx}: {old_prefix!r} -> {new_prefix!r}')

# Слить ячейки 30 и 31 (заголовок "Диаграмма" + SVG)
src30 = get_src(cells[30])
src31 = get_src(cells[31])
merged = src30.rstrip() + '\n\n' + src31
set_src(cells[30], merged)
cells.pop(31)
print(f'  Объединены ячейки 30 и 31 (Диаграмма + SVG)')
print(f'  Итого ячеек: {len(cells)}')

# Обновляем TOC в ячейке 1
toc_cell_idx = 1
src1 = get_src(cells[toc_cell_idx])

new_toc = '''# 🔗 Сопряжения в Haskell

## Универсальные конструкции через категориальные отношения

---

### 📋 Содержание

| # | Тема | Суть |
|---|------|------|
| 1 | **Что такое сопряжение** | Интуиция, определение, биекция Hom |
| 2 | **Единица и коединица** | Естественные преобразования η, ε, треугольные тождества |
| 3 | **curry/uncurry** | Каноническое сопряжение (−×A) ⊣ (A→−) |
| 4 | **Free ⊣ Forgetful** | Свободные и забывающие функторы |
| 5 | **Δ ⊣ (×) и (+) ⊣ Δ** | Два сопряжённых у одного функтора |
| 6 | **State ⊣ Store** | Монада и комонада из сопряжения |
| 7 | **Adjunction² = Monad** | Сопряжения порождают монады |
| 8 | **Зоопарк Reader/Writer** | Сравнение левых и правых сопряжённых |
| 9 | **Законы и итоги** | Проверка законов, сводная таблица |
| 10 | **State/Store: глубоко** | Детальный разбор монады и комонады |
| 11 | **Representable функторы** | Функторы, изоморфные Hom(x,−) |
| 12 | **Limits и Colimits** | Пределы через сопряжения с Δ |
| 13 | **Расширения Кана** | Ran и Lan как универсальные конструкции |
| 14 | **Зоопарк сопряжений** | Полная сводная таблица |

> **Главная идея:** Сопряжение — это «оптимальный перевод» между двумя категориями.
> **Левый** сопряжённый *F ⊣ G* строит **наименьшую** структуру, **правый** — **наибольшую**.'''

set_src(cells[toc_cell_idx], new_toc)
print(f'  TOC обновлён: 14 разделов')

nb['cells'] = cells
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Готово! Adjunctions.ipynb сохранён.')
