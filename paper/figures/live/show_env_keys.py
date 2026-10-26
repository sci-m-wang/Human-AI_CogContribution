"""Print the key names, value lengths and host hints of a .env file without leaking secrets."""
import sys

path = sys.argv[1]
for line in open(path, encoding="utf-8", errors="replace"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    value = value.strip().strip('"').strip("'")
    host = value.split("//", 1)[-1].split("/", 1)[0] if "//" in value else ("SET" if value else "EMPTY")
    print(f"{key:36s} len={len(value):4d} host={host}")
