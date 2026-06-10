#!/usr/bin/env python3
"""Phase 11 Pass-2: embed diagram refs into sections 4, 7, 15."""
import json, sys
PATH = "/home/jovyan/src/notebooks/Optics.ipynb"

IMG = {
    "opt-s4-md":  "\n\n![Законы линз](../diagrams/optics/op_lens_laws.svg)\n",
    "opt-s7-md":  "\n\n![Решётка мощности оптик](../diagrams/optics/op_lattice.svg)\n",
    "opt-s15-md": "\n\n![Lens как коалгебра Store](../diagrams/optics/op_lens_store.svg)\n",
}

def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    by_id = {c.get("id"): c for c in nb["cells"]}
    n = 0
    for cid, img in IMG.items():
        c = by_id.get(cid)
        if c is None:
            print(f"ERROR missing {cid}", file=sys.stderr); sys.exit(1)
        s = "".join(c["source"])
        if img.strip() in s:
            continue
        s = s.rstrip("\n") + img
        c["source"] = s.splitlines(keepends=True)
        n += 1
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"embedded {n} images")

if __name__ == "__main__":
    main()
