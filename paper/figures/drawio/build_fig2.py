import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dxlib import *

F = Fig(1536, 1024)
GREY = "#8A97A8"
AV = {"human": "human", "agent": "agent", "sub": "subagents"}

# ---------------- left: six interaction modes ----------------
F.panel(10, 8, 780, 650, "Six interaction modes", 44, 28)
F.text(560, 10, 220, 40, "reference counts", 16, False, "#FFFFFF", "right", True)
F.img("human", 66, 60, 44, 44); F.text(112, 60, 80, 44, "Human", 19, True, NAVY, "left")
F.img("agent", 436, 60, 44, 44); F.text(484, 60, 40, 44, "AI", 19, True, NAVY, "left")
F.img("coder_a", 664, 52, 44, 50); F.text(656, 102, 62, 22, "Coder A", 14, True)
F.img("coder_b", 728, 52, 44, 50); F.text(720, 102, 62, 22, "Coder B", 14, True)
F.line([(24, 128), (776, 128)], "#B8C4D2", 1.2, False)

modes = [  # human chip, direction, ai chip, label, A, B
    ("D", "R", "P", "Direction and drafting", 8, 6),
    ("D", "L", "P", "Proposal and commitment", 7, 6),
    ("D", "L", "K", "Supply and reframing", 1, 3),
    ("M", "R", "M", "Regulation and response", 8, 9),
    ("M", "L", "P", "Challenge", 2, 4),
    (None, "S", "K", "Autonomous work", 39, 22),
]
def pill(kind, x, y, w=170, h=44):
    f, s = COL[kind]
    F.rect(x, y, w, h, f, s, 2, 22)
    F.img(ICON[kind], x + 8, y + 5, 34, h - 10)
    F.text(x + 44, y, w - 46, h, NAME[kind], 16, True, NAVY, "left")
y0 = 142
for n, (hk, d, ak, label, a, b) in enumerate(modes):
    y = y0 + n * 84
    F.rect(24, y + 8, 34, 34, "#6B87A8", "#6B87A8", 1, 50)
    F.text(24, y + 8, 34, 34, str(n + 1), 20, True, "#FFFFFF")
    if hk:
        F.img("human", 64, y + 4, 38, 44); pill(hk, 106, y + 3)
    else:
        F.rect(66, y + 3, 210, 44, "#F1F3F6", "#B8C0CC", 1.5, 10, dash=True)
        F.text(66, y + 3, 210, 44, "no human unit", 16, False, "#6B7280", "center", True)
    if d == "R":
        F.line([(284, y + 44), (430, y + 44)], LINE, 4)
    elif d == "L":
        F.line([(430, y + 44), (284, y + 44)], LINE, 4)
    else:
        F.line([(284, y + 44), (430, y + 44)], LINE, 4)
    F.text(280, y - 8, 154, 50, label, 17, False, NAVY, "center", False, "bottom")
    F.img("agent", 436, y + 3, 38, 44); pill(ak, 478, y + 3)
    for cx, v in ((660, a), (724, b)):
        F.rect(cx, y + 4, 54, 42, "#FFFFFF", "#9AA5B4", 1.5, 10)
        F.text(cx, y + 4, 54, 42, str(v), 21, True)
    F.line([(24, y + 74), (776, y + 74)], "#D5DCE6", 1, False) if n < 5 else None

# ---------------- right: worked case ----------------
F.panel(804, 8, 722, 650, "Worked case", 44, 28)
F.img("human", 826, 140, 70, 70); F.text(814, 210, 94, 24, "Human", 19, True)
F.img("agent", 826, 430, 70, 70); F.text(814, 500, 94, 24, "AI", 19, True)
F.line([(900, 176), (958, 176)], "#8A97A8", 2.5, False, True); F.line([(900, 466), (928, 466)], "#8A97A8", 2.5, False, True)

def case_card(n, kind, x, y, w, h, title, actor):
    f, s = COL[kind]
    F.rect(x, y, w, h, f, s, 3, 12)
    F.img("human" if actor == "h" else "agent", x + 8, y + 8, 40, 40)
    F.img(ICON[kind], x + w / 2 - 44, y + 46, 88, h - 92)
    F.text(x + 4, y + h - 52, w - 8, 50, title, 17, True)
    F.rect(x + w - 20, y - 18, 38, 38, "#B8C4D2", "#8A97A8", 1.5, 50)
    F.text(x + w - 20, y - 18, 38, 38, str(n), 20, True)

case_card(1, "K", 930, 400, 180, 190, "Literature summary", "a")
case_card(2, "K", 960, 112, 190, 200, "Knowledge as a type", "h")
F.img("proposal", 1090, 130, 56, 50) if False else None
case_card(3, "P", 1180, 400, 180, 190, "Framework draft", "a")
case_card(4, "D", 1200, 112, 190, 212, "Rulings on unit and evaluation", "h")
# typology
F.rect(1412, 270, 98, 220, "#FFFFFF", NAVY, 2.5, 10)
F.img("knowledge", 1420, 284, 82, 50); F.img("proposal", 1420, 338, 82, 56); F.img("doc_gears", 1424, 398, 74, 54)
F.text(1414, 452, 94, 34, "Typology", 18, True)

# flows
F.line([(1020, 400), (1020, 314)], LINE, 4)                      # 1 -> 2
F.line([(1150, 212), (1250, 212), (1250, 340), (1270, 340), (1270, 400)], LINE, 4) if False else None
F.line([(1150, 232), (1220, 232)], "#FFFFFF", 0, False) if False else None
F.line([(1150, 260), (1230, 260), (1230, 380), (1265, 380), (1265, 400)], LINE, 4) if False else None
F.line([(1150, 212), (1170, 212), (1170, 360), (1250, 360), (1250, 400)], LINE, 4) if False else None
F.line([(1150, 240), (1170, 240), (1170, 380), (1230, 380), (1230, 398)], LINE, 4)      # 2 -> 3
F.line([(1330, 400), (1330, 314)], LINE, 4) if False else None
F.line([(1340, 400), (1340, 326)], LINE, 4)                                            # 3 -> 4
F.line([(1360, 450), (1412, 450)], LINE, 4)                                            # 3 -> Typology
F.line([(1390, 200), (1440, 200), (1440, 268)], LINE, 4)                              # 4 -> Typology
F.line([(1055, 112), (1055, 74), (1480, 74), (1480, 268)], LINE, 4)                   # 2 -> Typology (outer lane)

# ---------------- bottom: mixed contribution ----------------
F.panel(10, 672, 1516, 330, "Mixed contribution", 44, 28)
# left: both add content
F.rect(50, 736, 290, 108, "#FFFFFF", "#4E79A7", 2, 14); F.img("human", 58, 746, 56, 70)
F.msg("h", 120, 744, 214, 62, "Treat knowledge as another dimension.", 16)
F.chip("P", 130, 810, 28); F.text(162, 810, 170, 28, "human Proposal", 15, False, NAVY, "left")
F.rect(50, 858, 290, 108, "#FFFFFF", "#7B8794", 2, 14); F.img("agent", 58, 868, 56, 70)
F.msg("a", 120, 866, 214, 62, "Summary of the related research on cognition.", 16)
F.chip("K", 130, 932, 28); F.text(162, 932, 170, 28, "AI Knowledge", 15, False, NAVY, "left")
F.line([(344, 790), (380, 790), (380, 850), (412, 850)], LINE, 5)
F.line([(344, 912), (380, 912), (380, 884), (412, 884)], LINE, 5)
F.img("doc_gears", 420, 760, 160, 170)
F.img("check_badge", 560, 748, 54, 54)
F.text(150, 970, 540, 30, "Both add content to the same output", 19, True)
F.line([(700, 700), (700, 990)], PBORDER, 1.2, False, True)
# right: bare approval
F.rect(730, 780, 250, 112, "#FFFFFF", "#7B8794", 2, 14); F.img("agent", 738, 790, 56, 70)
F.msg("a", 800, 788, 174, 62, "Draft of the unit definition.", 16)
F.chip("P", 806, 854, 28); F.text(838, 854, 140, 28, "AI Proposal", 15, False, NAVY, "left")
F.line([(984, 836), (1020, 836)], LINE, 5)
F.rect(1024, 780, 250, 112, "#FFFFFF", "#4E79A7", 2, 14); F.img("human", 1032, 790, 56, 70)
F.msg("h", 1094, 788, 174, 62, "I think that works. OK.", 16)
F.text(1100, 854, 170, 28, "no new content", 15, False, "#6B7280", "left", True)
F.line([(1280, 836), (1380, 836)], "#8A97A8", 4, True, True)
F.img("cross_badge", 1304, 810, 52, 52)
F.img("pages", 1390, 770, 110, 140)
F.text(730, 940, 790, 30, "A bare approval adds no content, so the output is not mixed", 19, True)
F.text(1380, 972, 140, 22, "schematic", 15, False, "#6B7280", "right", True)

F.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig2.drawio"), "Figure 2")
print("cells", len(F.cells))
