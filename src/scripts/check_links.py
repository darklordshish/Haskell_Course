import json, re
from pathlib import Path

ROOT = Path('/home/jovyan/src')
NB_DIR = ROOT / 'notebooks'
DIAG_DIR = ROOT / 'diagrams'
existing_svgs = {str(f.relative_to(ROOT)) for f in DIAG_DIR.rglob('*.svg')}

# From notebooks/ subdir, correct path is ../diagrams/...
# So normalize: strip ../ prefix then check against existing_svgs
def normalize(ref):
    n = ref.lstrip('../').lstrip('./')
    return n

PATTERNS = [
    ('MD_IMG',    re.compile(r'(!\[[^\]]*\])\(([^)]+\.svg)\)')),
    ('SVG_CALL',  re.compile(r"SVG\s*\(['\"]([^'\"]+\.svg)['\"]\)")),
    ('OPEN_CALL', re.compile(r"open\s*\(['\"]([^'\"]+\.svg)['\"]")),
]

all_bad = []
all_ok_count = 0

for nb_path in sorted(NB_DIR.glob('*.ipynb')):
    nb_name = nb_path.name
    nb = json.loads(nb_path.read_text())
    for ci, cell in enumerate(nb['cells']):
        src = cell.get('source', '')
        if isinstance(src, list): src = ''.join(src)
        for pat_name, pat in PATTERNS:
            for m in pat.finditer(src):
                ref = m.group(1) if pat_name == 'MD_IMG' else m.group(1)
                if pat_name == 'MD_IMG': ref = m.group(2)
                norm = normalize(ref)
                if norm in existing_svgs:
                    all_ok_count += 1
                else:
                    all_bad.append((nb_name, ci, pat_name, ref, norm))

print(f'OK: {all_ok_count}  BROKEN: {len(all_bad)}')
if all_bad:
    print('BROKEN REFS:')
    for nb, ci, pat, ref, norm in all_bad:
        print(f'  {nb} cell {ci} [{pat}]: {repr(ref)} (normalized: {repr(norm)})')
else:
    print('All SVG refs are valid!')
