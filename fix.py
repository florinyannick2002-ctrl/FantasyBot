import subprocess
import os

print("Schritt 1: Aktuelle index.html sichern...")
if os.path.exists('index.html'):
    os.rename('index.html', 'index.html.broken')

print("Schritt 2: Letzte funktionierende Version von GitHub holen...")
result = subprocess.run(['git', 'checkout', 'HEAD~3', '--', 'index.html'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

print("Schritt 3: Prüfen ob index.html jetzt da ist...")
if os.path.exists('index.html'):
    size = os.path.getsize('index.html')
    print(f"OK! index.html wiederhergestellt, {size} bytes")
else:
    print("Fehler — index.html nicht gefunden")

print("\nFertig! Jetzt im Terminal:")
print("  git add .")
print("  git commit -m 'Revert to working version'")
print("  git push")
