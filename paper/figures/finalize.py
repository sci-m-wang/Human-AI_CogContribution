import os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
for n in ("fig1", "fig2"):
    im = Image.open(os.path.join(here, "drawio", n + ".png")).convert("RGB")
    w = 2400
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    out = os.path.join(here, n + "_final.png")
    im.save(out, dpi=(300, 300), optimize=True)
    print(out, im.size, os.path.getsize(out))
