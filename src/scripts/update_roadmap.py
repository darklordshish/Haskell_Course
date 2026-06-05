import re

with open('ROADMAP.md', encoding='utf-8') as f:
    content = f.read()

# Обновляем строку "Общий итог"
old_total = '**Общий итог:** 626 ячеек, 24 SVG-файла, 0 ошибок, 16 ноутбуков готово.'
new_total = '**Общий итог:** 630 ячеек, 24 SVG-файла, 0 ошибок, 16 ноутбуков готово. Унификация структуры (setup+TOC+nav) завершена для всех 17 ноутбуков.'

if old_total in content:
    content = content.replace(old_total, new_total)
    print('Updated total line')
else:
    # Попробуем найти и заменить по regex
    content, n = re.subn(r'\*\*Общий итог:\*\*.*', new_total, content)
    print(f'Regex replace: {n} matches')

# Обновляем дату последнего обновления
content = re.sub(
    r'Последнее обновление: \d{4}-\d{2}-\d{2}',
    'Последнее обновление: 2026-05-31',
    content
)

# Добавляем прогресс унификации в тех. заметки
old_note = '- SVG: нельзя использовать unicode entities с кириллицей'
if old_note in content and '- Унификация структуры' not in content:
    content = content.replace(
        old_note,
        old_note + '\n- Унификация структуры завершена 2026-05-31: все 17 ноутбуков имеют SETUP + TOC + NAV. При записи ensure_ascii=False.'
    )
    print('Added unification note')

with open('ROADMAP.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('ROADMAP.md updated')
