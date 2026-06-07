import sys, os

TARGET = 'styles.css'
if not os.path.exists(TARGET):
    sys.exit(f'ERROR: {TARGET} not found.')

with open(TARGET, encoding='utf-8') as f:
    src = f.read()

patches = [
  {
    'desc': 'Restore pcard-rank (was hidden)',
    'find': '.pcard-rank{display:none;}',
    'replace': '.pcard-rank{font-family:var(--mono);font-size:11px;font-weight:600;color:var(--intel-mid);min-width:22px;text-align:right;flex-shrink:0;}',
  },
]

for i, p in enumerate(patches, 1):
    if p['find'] in src:
        src = src.replace(p['find'], p['replace'], 1)
        print(f'OK    [{i}] {p["desc"]}')
    else:
        print(f'SKIP  [{i}] {p["desc"]} — string not found')

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(src)

print('\nDone — styles.css updated.')
