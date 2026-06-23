import re
from datetime import date

roadmap_path = '/home/jovyan/src/ROADMAP.md'
with open(roadmap_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Обновляем дату
today = date.today().isoformat()
content = re.sub(r'Дата: \d{4}-\d{2}-\d{2}', f'Дата: {today}', content)

# Добавляем запись о работе с Adjunctions
adj_note = '''
### Adjunctions.ipynb — выполнено (2026-06-01)
- ✅ ASCII-диаграмма треугольных тождеств заменена на SVG (`adj_triangle.svg`)
- ✅ Мусорная ячейка с `import json` удалена
- ✅ 3 пустые ячейки в начале удалены
- ✅ Структура разделов исправлена: 14 разделов вместо путаницы 9+6.5+7+8+9+10
- ✅ TOC обновлён: таблица из 14 строк
- ✅ Ячейки "Диаграмма" и SVG объединены
- ✅ Все ячейки выполнены без ошибок, Haskell | Idle
'''

# Вставим после секции про Adjunctions в роудмапе
if '### Adjunctions.ipynb — выполнено' not in content:
    # Найдём место после строки про adj_adjunction.svg
    insert_after = 'adj_triangle.svg'
    if insert_after not in content:
        # Добавим в конец раздела SVG файлов
        content += adj_note
    else:
        idx = content.find(insert_after)
        idx_nl = content.find('\n\n', idx)
        if idx_nl > 0:
            content = content[:idx_nl] + '\n' + adj_note + content[idx_nl:]
        else:
            content += adj_note

with open(roadmap_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'ROADMAP.md обновлён ({today})')
