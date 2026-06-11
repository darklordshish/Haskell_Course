import json
PATH = "/home/jovyan/src/notebooks/Adjunctions.ipynb"
with open(PATH, encoding="utf-8") as f: nb = json.load(f)
c = nb["cells"][6]
s = "".join(c["source"])
s = s.replace("`$f, a) -> f a`", "`(f, a) -> f a`")
c["source"] = s.splitlines(keepends=True)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1); f.write("\n")
print("restored code span in cell 6")
