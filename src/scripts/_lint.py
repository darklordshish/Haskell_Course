#!/usr/bin/env python3
"""Lint markdown cells: no \\(...\\) delimiters, balanced $ per cell."""
import json, sys

PATH = "/home/jovyan/src/notebooks/Uncertainty.ipynb"

def main():
    with open(PATH, encoding="utf-8") as f:
        nb = json.load(f)
    bad_delim = []
    unbalanced = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "markdown":
            continue
        s = "".join(c["source"])
        if "\\(" in s or "\\)" in s:
            bad_delim.append(i)
        # count unescaped $ (treat $$ display as two $, still even overall)
        if s.count("$") % 2 != 0:
            unbalanced.append((i, s.count("$")))
    print("bad_delim cells:", bad_delim if bad_delim else "none")
    print("unbalanced $ cells:", unbalanced if unbalanced else "none")
    if bad_delim or unbalanced:
        sys.exit(1)
    print("LINT OK")

if __name__ == "__main__":
    main()
