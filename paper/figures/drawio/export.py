import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
exe = r"C:\Program Files\draw.io\draw.io.exe"
for n in sys.argv[1:]:
    out = os.path.join(here, n + ".png")
    r = subprocess.run([exe, "-x", "-f", "png", "-s", "2", "-b", "10", "-o", out, os.path.join(here, n + ".drawio")], capture_output=True, text=True, timeout=180)
    print(n, r.returncode, (r.stdout + r.stderr)[-300:], os.path.exists(out))
