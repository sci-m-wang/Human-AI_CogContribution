# Programmatic native draw.io builder for the two figures (see records E045 for the method deviation).
import base64, io, os, sys
from xml.sax.saxutils import escape
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIRS = [os.path.join(ROOT, "elements_b", "assets"), os.path.join(ROOT, "elements_c", "assets")]
_cache = {}

def asset(name):
    if name in _cache:
        return _cache[name]
    for d in ASSET_DIRS:
        p = os.path.join(d, name + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            w, h = im.size
            s = 420 / max(w, h)
            if s < 1:
                im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "PNG", optimize=True)
            b64 = base64.b64encode(buf.getvalue()).decode()
            _cache[name] = (b64, im.size)
            return _cache[name]
    raise FileNotFoundError(name)

NAVY = "#1F2937"; HDR = "#44709E"; PANEL = "#F3F7FB"; PBORDER = "#7F97B3"; LINE = "#4E79A7"
COL = {  # fill, stroke
    "K": ("#DCEBFA", "#4E79A7"), "P": ("#DFF1D8", "#59A14F"), "D": ("#FCE5CC", "#E08A1E"),
    "M": ("#E9DDF2", "#8E6BB0"), "X": ("#E5E7EB", "#7B8794"),
}
ICON = {"K": "knowledge", "P": "proposal", "D": "decision", "M": "metacognition", "X": "execution"}
NAME = {"K": "Knowledge", "P": "Proposal", "D": "Decision", "M": "Metacognition", "X": "Execution"}


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.cells = []
        self.n = 2

    def _id(self):
        self.n += 1
        return "c%d" % self.n

    def add(self, style, x, y, w, h, value="", parent="1"):
        i = self._id()
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"><mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (i, escape(value, {'"': "&quot;"}), style, parent, round(x, 1), round(y, 1), round(w, 1), round(h, 1)))
        return i

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=NAVY, sw=1.5, r=8, dash=False, value="", extra=""):
        st = "rounded=1;arcSize=%d;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;strokeWidth=%s;%s%s" % (
            r, fill, stroke, sw, "dashed=1;dashPattern=4 3;" if dash else "", extra)
        return self.add(st, x, y, w, h, value)

    def text(self, x, y, w, h, s, size=18, bold=False, color=NAVY, align="center", italic=False, valign="middle"):
        st = "text;html=1;strokeColor=none;fillColor=none;align=%s;verticalAlign=%s;whiteSpace=wrap;overflow=hidden;fontSize=%s;fontFamily=Helvetica;fontColor=%s;%s%s" % (
            align, valign, size, color, "fontStyle=%d;" % ((1 if bold else 0) + (2 if italic else 0)) if (bold or italic) else "", "")
        return self.add(st, x, y, w, h, s)

    def img(self, name, x, y, w, h=None):
        b64, (iw, ih) = asset(name)
        if h is None:
            h = w * ih / iw
        # fit inside w x h preserving aspect, centred
        s = min(w / iw, h / ih)
        pw, ph = iw * s, ih * s
        st = "shape=image;html=1;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=1;aspect=fixed;image=data:image/png,%s;" % b64
        return self.add(st, x + (w - pw) / 2, y + (h - ph) / 2, pw, ph)

    def bubble(self, kind, x, y, h, lines=2, hl="#9AA5B4"):
        w = h * 1.27
        self.img("bubble_h" if kind == "h" else "bubble_a", x, y, w, h)
        bw = w * 0.56
        for k in range(lines):
            self.rect(x + w * 0.22, y + h * (0.26 + 0.2 * k), bw * (1 - 0.3 * k), max(3, h * 0.07), hl, hl, 0, 50)
        return x + w

    def msg(self, who, x, y, w, h, text, size=15, tail=9):
        fill, stroke = ("#CFE3F7", "#4E79A7") if who == "h" else ("#E9ECF0", "#7B8794")
        st = ("shape=callout;perimeter=calloutPerimeter;rounded=1;arcSize=18;whiteSpace=wrap;html=1;size=%d;position=0.12;base=22;"
              "fillColor=%s;strokeColor=%s;strokeWidth=1.8;fontSize=%s;fontFamily=Helvetica;fontColor=%s;align=left;verticalAlign=middle;"
              "spacingLeft=6;spacingRight=4;spacingTop=0;spacingBottom=%d;") % (tail, fill, stroke, size, NAVY, tail)
        return self.add(st, x, y, w, h, text)

    def line(self, pts, color=LINE, sw=3, arrow=True, dash=False, both=False):
        i = self._id()
        st = "edgeStyle=none;html=1;rounded=0;strokeColor=%s;strokeWidth=%s;endArrow=%s;endFill=1;startArrow=%s;startFill=1;%s" % (
            color, sw, "block" if arrow else "none", "block" if both else "none", "dashed=1;dashPattern=6 4;" if dash else "")
        mid = ""
        if len(pts) > 2:
            mid = '<Array as="points">' + "".join('<mxPoint x="%s" y="%s"/>' % p for p in pts[1:-1]) + "</Array>"
        self.cells.append(
            '<mxCell id="%s" style="%s" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="%s" y="%s" as="sourcePoint"/><mxPoint x="%s" y="%s" as="targetPoint"/>%s</mxGeometry></mxCell>'
            % (i, st, pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], mid))
        return i

    # composite helpers
    def panel(self, x, y, w, h, title, hdr_h=40, fs=28):
        self.rect(x, y, w, h, PANEL, PBORDER, 1.2, 4, dash=True)
        self.rect(x, y, w, hdr_h, HDR, HDR, 1, 30, extra="")
        self.text(x + 12, y, w - 24, hdr_h, title, fs, True, "#FFFFFF", "left")

    def chip(self, kind, x, y, s=44, label=False):
        f, st = COL[kind]
        self.rect(x, y, s, s, f, st, 2, 14)
        self.img(ICON[kind], x + 4, y + 4, s - 8, s - 8)

    def actor(self, who, x, y, s=44):
        stroke = {"human": "#4E79A7", "agent": "#7B8794", "sub": "#3DAA9A"}[who]
        self.rect(x, y, s, s, "#FFFFFF", stroke, 2, 14)
        self.img({"human": "human", "agent": "agent", "sub": "subagents"}[who], x + 3, y + 3, s - 6, s - 6)

    def save(self, path, name="Page-1"):
        xml = ('<mxfile host="app.diagrams.net"><diagram name="%s" id="d1"><mxGraphModel dx="1200" dy="800" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" math="0" shadow="0" background="#FFFFFF"><root><mxCell id="0"/><mxCell id="1" parent="0"/>%s</root></mxGraphModel></diagram></mxfile>'
               % (name, self.w, self.h, "".join(self.cells)))
        open(path, "w", encoding="utf-8").write(xml)
