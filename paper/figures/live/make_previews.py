import os, sys
from PIL import Image
prev = os.path.join(os.environ["LOCALAPPDATA"], "Temp", "opencode", "prev")
for n in sys.argv[1:]:
    im = Image.open(os.path.join(prev, n + ".png")).convert("RGB")
    im.convert("L").save(os.path.join(prev, n + "_gray.png"))
    w = int(6.15 * 110)   # 6.15 in wide, shown at 110 dpi so it is roughly what a reader sees on screen
    im.resize((w, int(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(prev, n + "_print.png"))
    print(n, im.size)
