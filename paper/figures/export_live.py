import os, subprocess, sys
from PIL import Image
D = r"<project>\paper\figures"
name = sys.argv[1]; out_final = sys.argv[2]
src = os.path.join(D, "drawio", name + ".drawio"); png = os.path.join(D, "drawio", name + ".png")
r = subprocess.run([r"C:\Program Files\draw.io\draw.io.exe", "-x", "-f", "png", "-s", "2", "-b", "0", "-o", png, src], capture_output=True, text=True, timeout=240)
print(name, r.returncode, os.path.exists(png))
im = Image.open(png).convert("RGB"); print("export", im.size)
w = 2400
im2 = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
im2.save(os.path.join(D, out_final), dpi=(300, 300), optimize=True); print("saved", out_final, im2.size)
