#!/usr/bin/env python3
# OwlPick — Step 6: Strategy panel mobile layout.
# Multi-file patch:
#   index.html  — add classes to the Advanced Settings (3-col) and Bench Distribution (4-col) grids
#   styles.css  — collapse both to 2 columns at <=640px (no more 57px-wide dropdowns)
# Privacy/Impressum modal needs no changes (text-only, already mobile-clean).
# Desktop layout unchanged (inline grid values preserved; overrides live in @media).
import os, sys

HTML_FILE = "index.html"
html_patches = [
    {
        "find": '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">',
        "replace": '<div class="strat-adv-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">',
        "desc": "Add .strat-adv-grid class to Advanced Settings grid",
    },
    {
        "find": '<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;">',
        "replace": '<div class="strat-bench-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;">',
        "desc": "Add .strat-bench-grid class to Bench Distribution grid",
    },
]

CSS_FILE = "styles.css"
CSS_ANCHOR = "  .pm-stats-grid{grid-template-columns:1fr !important;}\n}"
CSS_BLOCK = """  .pm-stats-grid{grid-template-columns:1fr !important;}

  /* ── STEP 6: strategy panel — collapse dense grids to 2 columns ── */
  .strat-adv-grid{grid-template-columns:1fr 1fr !important;}
  .strat-bench-grid{grid-template-columns:1fr 1fr !important;}
}"""

def patch_html():
    if not os.path.exists(HTML_FILE):
        sys.exit("ERROR: %s not found. Run this from the project root." % HTML_FILE)
    with open(HTML_FILE, "r", encoding="utf-8", newline="") as f:
        data = f.read()
    changed = False
    for i, p in enumerate(html_patches, 1):
        if p["replace"] in data:
            print("SKIP [%d] %s — already present." % (i, p["desc"]))
            continue
        if p["find"] not in data:
            print("SKIP [%d] %s — find-string not found." % (i, p["desc"]))
            continue
        data = data.replace(p["find"], p["replace"], 1)
        changed = True
        print("OK   [%d] %s." % (i, p["desc"]))
    if changed:
        with open(HTML_FILE, "w", encoding="utf-8", newline="") as f:
            f.write(data)

def patch_css():
    if not os.path.exists(CSS_FILE):
        sys.exit("ERROR: %s not found. Run this from the project root." % CSS_FILE)
    with open(CSS_FILE, "r", encoding="utf-8", newline="") as f:
        css = f.read()
    if "STEP 6: strategy panel" in css:
        print("SKIP [3] Step 6 strategy CSS already present.")
        return
    if CSS_ANCHOR not in css:
        print("SKIP [3] CSS anchor not found — is Step 5 applied? No change made.")
        return
    css = css.replace(CSS_ANCHOR, CSS_BLOCK, 1)
    with open(CSS_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(css)
    print("OK   [3] Extended mobile block with strategy grid rules.")

patch_html()
patch_css()
print("Done — index.html + styles.css updated.")
