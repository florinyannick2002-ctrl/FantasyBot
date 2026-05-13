#!/usr/bin/env python3
"""
Daily ADP updater — fetches Sleeper ADP from BeatADP and updates fantasy-draft.html
Run automatically via GitHub Actions every day at 6:00 UTC
"""

import urllib.request
import json
import re
import sys
from datetime import datetime

def fetch_beatadp():
    """Fetch Sleeper PPR Redraft ADP from BeatADP"""
    url = "https://www.beatadp.com/platform-adp/sleeper/redraft/ppr"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.beatadp.com/',
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8')

def parse_adp(html):
    """Parse ADP table from BeatADP HTML"""
    adp = {}
    # Match table rows: | 1 | [Name](url)TEAM | consensus | sleeper | ...
    # Pattern for markdown table rows with player data
    row_pattern = re.compile(
        r'\|\s*\d+\s*\|\s*\[([^\]]+)\]\([^)]+\)[A-Z]*\s*\|\s*[\d.]+\s*\|\s*([\d.]+)\s*\|',
        re.MULTILINE
    )
    for m in row_pattern.finditer(html):
        name = m.group(1).strip()
        sleeper_adp = float(m.group(2))
        if name and sleeper_adp:
            adp[name] = sleeper_adp
    return adp

def update_html(adp_data):
    """Update SLEEPER_ADP object in fantasy-draft.html"""
    with open('fantasy-draft.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new SLEEPER_ADP JS object
    lines = []
    items = sorted(adp_data.items(), key=lambda x: x[1])
    for name, adp in items:
        # Escape single quotes in names
        safe_name = name.replace("'", "\\'")
        lines.append(f'  "{safe_name}":{adp}')

    new_adp_block = 'var SLEEPER_ADP = {\n' + ',\n'.join(lines) + '\n};'

    # Replace existing SLEEPER_ADP block
    pattern = re.compile(r'var SLEEPER_ADP = \{[^}]+\};', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_adp_block, content)
        with open('fantasy-draft.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {len(adp_data)} players — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        return True
    else:
        print("ERROR: SLEEPER_ADP block not found in HTML")
        return False

if __name__ == '__main__':
    print(f"Fetching BeatADP Sleeper PPR data...")
    try:
        html = fetch_beatadp()
        adp = parse_adp(html)
        if len(adp) < 50:
            print(f"WARNING: Only found {len(adp)} players, skipping update")
            sys.exit(1)
        print(f"Found {len(adp)} players")
        success = update_html(adp)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
