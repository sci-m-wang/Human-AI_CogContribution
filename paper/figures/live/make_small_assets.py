"""Make small copies of the actor illustrations for the figure builds.

The live figures place each illustration at 36 to 60 px on a 1280 px canvas that is exported at
2000 px, so a 320 px copy is far more than enough. Small copies keep the .drawio files light
(the earlier version embedded 57 full-size copies and reached 10 MB).
"""
import os
from PIL import Image

FIG = r"<project>\paper\figures"
OUT = os.path.join(FIG, "live", "assets_small")
os.makedirs(OUT, exist_ok=True)

WANT = {
    "human": "elements_c",
    "primary_agent": "elements_c",
    "subagents": "elements_c",
    "coder_a": "elements_b",
    "coder_b": "elements_b",
    "gear_grey": "elements_b",
}
for name, folder in WANT.items():
    src = os.path.join(FIG, folder, "assets", name + ".png")
    if not os.path.exists(src):
        src = os.path.join(FIG, "elements", "assets", name + ".png")
    im = Image.open(src).convert("RGBA")
    im.thumbnail((320, 320), Image.LANCZOS)
    dst = os.path.join(OUT, name + ".png")
    im.save(dst, optimize=True)
    print(name, im.size, os.path.getsize(dst), "bytes")
