import json, re
from pathlib import Path

ROOT = Path('/home/jovyan/src')
NB_DIR = ROOT / 'notebooks'
DIAG_DIR = ROOT / 'diagrams'
existing_svgs = {str(f.relative_to(ROOT)) for f in DIAG_DIR.rglob('*.svg')}
svg_by_name = {Path(s).name: s for s in existing_svgs}

# Fix all SVG references in markdown and code cells
# Since notebooks live in notebooks/ subdir, path must be ../diagrams/...
MD_IMG_PAT   = re.compile(r'(!\[[^\]]*\])\(([^)]+\.svg)\)')
SVG_CALL_PAT = re.compile(r"(SVG\s*\(['\"])([^'\"]+\.svg)(['\"]\))")
OPEN_PAT     = re.compile(r"(open\s*\(['\"])([^'\"]+\.svg)(['\"])")

def fix_ref(ref, is_display=True):
    norm = ref.lstrip('../').lstrip('./')
    # If already starts with diagrams/ -> add ../
    if norm.startswith('diagrams/'):
        return '../' + norm
    # If it's just a bare filename.svg -> find in svg_by_name and add ../
    basename = Path(ref).name
    correct = svg_by_name.get(basename)
    if correct:
        return '../' + correct
    return None  # can't fix

total_fixed = 0

for nb_path in sorted(NB_DIR.glob('*.ipynb')):
    nb_name = nb_path.name
    nb = json.loads(nb_path.read_text())
    changed = False
    for ci, cell in enumerate(nb['cells']):
        src = cell.get('source', '')
        if isinstance(src, list):
            original = ''.join(src)
            is_list = True
        else:
            original = src
            is_list = False
        new_src = original
        # Fix markdown images
        def fix_md(m):
            prefix, ref = m.group(1), m.group(2)
            # skip if already ../diagrams/
            if ref.startswith('../diagrams/'): return m.group(0)
            fixed = fix_ref(ref)
            if fixed: return f'{prefix}({fixed})'
            return m.group(0)
        new_src = MD_IMG_PAT.sub(fix_md, new_src)
        # Fix SVG() calls
        def fix_svg(m):
            p1, ref, p3 = m.group(1), m.group(2), m.group(3)
            if ref.startswith('../diagrams/'): return m.group(0)
            fixed = fix_ref(ref)
            if fixed: return f'{p1}{fixed}{p3}'
            return m.group(0)
        new_src = SVG_CALL_PAT.sub(fix_svg, new_src)
        new_src = OPEN_PAT.sub(fix_svg, new_src)
        if new_src != original:
            print(f'  FIXED {nb_name} cell {ci}')
            total_fixed += 1
            changed = True
            cell['source'] = [new_src] if is_list else new_src
    if changed:
        nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1))
        print(f'  SAVED {nb_name}')

print(f'Done. Fixed cells: {total_fixed}')
