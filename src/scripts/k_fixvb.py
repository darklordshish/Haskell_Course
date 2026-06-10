#!/usr/bin/env python3
"""Task 13: add viewBox (matching width/height) to kan SVGs that lack it; ensure white bg."""
import os, re, sys

DIR = "/home/jovyan/src/diagrams/kan"
FILES = ["ran_diagram.svg", "lan_diagram.svg", "kan_codensity.svg", "kan_density.svg",
         "kan_yoneda.svg", "kan_adjunction.svg", "kan_examples.svg"]

def main():
    for fn in FILES:
        p = os.path.join(DIR, fn)
        with open(p, encoding="utf-8") as f:
            s = f.read()
        orig = s
        m = re.search(r"<svg\b[^>]*>", s)
        if not m:
            print(f"SKIP {fn}: no <svg> tag"); continue
        tag = m.group(0)
        if "viewBox" not in tag:
            w = re.search(r'width="(\d+)"', tag)
            h = re.search(r'height="(\d+)"', tag)
            if w and h:
                new_tag = tag[:-1] + f' viewBox="0 0 {w.group(1)} {h.group(1)}">'
                s = s.replace(tag, new_tag, 1)
        # ensure a white full-size bg rect exists
        if 'fill="#ffffff"' not in s and 'fill="#fff"' not in s:
            w = re.search(r'width="(\d+)"', tag); h = re.search(r'height="(\d+)"', tag)
            if w and h:
                bg = f'<rect width="{w.group(1)}" height="{h.group(1)}" fill="#ffffff"/>'
                # insert after </defs> if present else right after svg tag
                if "</defs>" in s:
                    s = s.replace("</defs>", "</defs>\n" + bg, 1)
                else:
                    cur = re.search(r"<svg\b[^>]*>", s).group(0)
                    s = s.replace(cur, cur + "\n" + bg, 1)
        if s != orig:
            with open(p, "w", encoding="utf-8") as f:
                f.write(s)
            print(f"fixed {fn}")
        else:
            print(f"unchanged {fn}")

if __name__ == "__main__":
    main()
