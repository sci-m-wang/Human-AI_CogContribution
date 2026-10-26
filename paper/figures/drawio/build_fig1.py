import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dxlib import *

F = Fig(1536, 1024)
GREY = "#8A97A8"
AV = {"human": "human", "agent": "agent", "sub": "subagents"}

# ---------------- Panel 1: Recorded project ----------------
F.panel(34, 8, 296, 592, "Recorded project", 40, 26)
for img, x, lab, w in (("human", 44, "Human", 80), ("primary_agent", 126, "Primary agent", 100), ("subagents", 228, "Sub-agents", 100)):
    F.img(img, x + 8, 52, 66, 62)
    F.text(x - 4 if img != "primary_agent" else x - 6, 114, 92 if img != "primary_agent" else 104, 24, lab, 15, True)
tx = 58
F.line([(tx, 150), (tx, 586)], GREY, 3, arrow=False)
rows = [("human", 150, "Record the whole process, including sessions."), ("agent", 202, "Read the call for papers. Summary below."),
        ("tools", 254, ""), ("agent", 288, "We observe traces, not cognition itself."),
        ("human", 340, "First survey the related research."), ("tools", 392, ""),
        ("agent", 426, "Dispatching three sub-agents."), ("sub", 480, "Notes on one source."),
        ("tools", 532, "")]
for kind, y, txt in rows:
    if kind == "tools":
        for k in range(3):
            F.img("gear_grey", 108 + k * 30, y, 24, 24)
        F.text(204, y - 2, 120, 28, "tool steps", 14, False, "#4B5563", "left", True)
        continue
    F.rect(tx - 5, y + 17, 10, 10, GREY, GREY, 1, 50)
    F.img(AV[kind], 72 if kind != "sub" else 84, y + 6, 32, 32)
    F.msg("h" if kind == "human" else "a", 112 if kind != "sub" else 120, y, 210 if kind != "sub" else 202, 52, txt, 14)

F.line([(334, 300), (356, 300)], LINE, 9)
F.line([(702, 300), (726, 300)], LINE, 9)

# ---------------- Panel 2: Units ----------------
F.panel(356, 8, 340, 592, "Units", 40, 26)
F.text(366, 48, 320, 28, "One model response is one unit", 19, True)
def card(y, h): F.rect(376, y, 308, h, "#FFFFFF", GREY, 1.5, 10)
card(82, 70)
F.img("human", 386, 92, 40, 40); F.msg("h", 432, 88, 244, 56, "Read the originals, for accuracy.", 15)
card(162, 122)
F.img("agent", 386, 172, 40, 40); F.msg("a", 432, 168, 244, 56, "Krippendorff's alpha corrects for chance agreement.", 15)
for k in range(3): F.img("gear_grey", 438 + k * 30, 238, 24, 24)
F.text(534, 236, 146, 28, "tool steps first", 15, False, NAVY, "left")
F.text(386, 260, 290, 20, "steps are kept as evidence", 14, False, "#4B5563", "left", True)
card(294, 98)
F.img("agent", 386, 304, 40, 40); F.msg("a", 432, 300, 244, 56, "Checking the sub-agent notes.", 15)
for k in range(2): F.img("gear_grey", 438 + k * 30, 364, 24, 24)
F.text(504, 362, 170, 28, "tool steps first", 15, False, NAVY, "left")
F.line([(530, 392), (530, 408)], NAVY, 2, False)
F.line([(450, 408), (610, 408)], NAVY, 2, False)
F.line([(450, 408), (450, 420)], NAVY, 2, True); F.line([(610, 408), (610, 420)], NAVY, 2, True)
F.rect(376, 422, 150, 74, "#FFFFFF", GREY, 1.5, 10); F.rect(534, 422, 150, 74, "#FFFFFF", GREY, 1.5, 10)
F.img("subagents", 382, 430, 48, 44); F.msg("a", 430, 428, 92, 62, "Source summary", 14, 8)
F.img("subagents", 540, 430, 48, 44); F.msg("a", 588, 428, 92, 62, "Source summary", 14, 8)
F.line([(440, 514), (684, 514)], NAVY, 2, False, True)
F.img("scissors", 386, 492, 40, 44)
F.text(376, 544, 308, 48, "Units are linked only within one session", 18)

# ---------------- Panel 3: Tags ----------------
F.panel(726, 8, 780, 592, "Tags", 40, 26)
F.rect(764, 58, 262, 110, "#FFFFFF", NAVY, 2, 10)
F.img("human", 772, 66, 46, 46); F.msg("h", 822, 62, 198, 58, "Report several agreement statistics.", 15)
for k in range(3): F.img("gear_grey", 800 + k * 36, 134, 26, 26)
F.text(912, 134, 110, 26, "tool steps", 14, False, "#4B5563", "left", True) if False else None
F.line([(850, 168), (800, 232)], NAVY, 2.5, True)
F.line([(940, 168), (1004, 232)], NAVY, 2.5, True)
F.img("coder_a", 743, 238, 104, 120); F.text(743, 358, 104, 26, "Coder A", 19, True)
F.img("coder_b", 959, 238, 104, 120); F.text(959, 358, 104, 26, "Coder B", 19, True)
def pair(x, y, kinds):
    F.actor("human", x, y, 46); F.chip(kinds[0], x + 56, y, 46)
    F.actor("agent", x, y + 54, 46); F.chip(kinds[1], x + 56, y + 54, 46)
pair(744, 396, ("D", "P")); pair(960, 396, ("D", "M"))
F.img("scales", 876, 394, 54, 54); F.text(850, 450, 110, 24, "Agreement", 18, True)
F.text(850, 474, 110, 44, "percent, kappa, alpha", 16)
cards = [("K", 1086, 56, "Knowledge", "a fact or concept enters"), ("P", 1296, 56, "Proposal", "a candidate is offered"),
         ("D", 1086, 210, "Decision", "the project is committed"), ("M", 1296, 210, "Metacognition", "the work is checked or steered")]
for k, x, y, t, cap in cards:
    f, s = COL[k]
    F.rect(x, y, 200, 146, f, s, 2.5, 8)
    F.text(x, y + 2, 200, 28, t, 21, True)
    F.img(ICON[k], x + 50, y + 32, 100, 66)
    F.text(x + 4, y + 100, 192, 44, cap, 17)
F.rect(1086, 366, 410, 46, COL["X"][0], COL["X"][1], 2, 10)
F.img("execution", 1096, 370, 40, 38); F.text(1142, 366, 350, 46, "Execution: a step is carried out", 19, True, NAVY, "left")
F.img("question_doc", 1090, 430, 48, 56)
F.line([(1142, 452), (1156, 452), (1156, 440), (1172, 440)], NAVY, 2, False)
F.line([(1142, 466), (1156, 466), (1156, 482), (1172, 482)], NAVY, 2, False)
F.text(1174, 426, 200, 30, "Product changes", 17, False, NAVY, "left")
F.text(1174, 468, 214, 30, "Only the process changes", 17, False, NAVY, "left")
F.line([(1380, 441), (1394, 441)], NAVY, 2); F.line([(1380, 483), (1394, 483)], NAVY, 2)
F.chip("K", 1398, 424, 32); F.chip("P", 1434, 424, 32); F.chip("D", 1470, 424, 32)
F.chip("M", 1398, 466, 32)
F.text(1086, 520, 172, 50, "A mixed output has content from both", 16, False, NAVY, "left")
F.actor("human", 1262, 526, 40); F.chip("D", 1306, 526, 40)
F.text(1348, 526, 20, 40, "+", 28, True)
F.actor("agent", 1372, 526, 40); F.chip("P", 1416, 526, 40)

F.line([(1110, 600), (1110, 626)], LINE, 5, False)
F.line([(300, 626), (1250, 626)], LINE, 5, False)
for x in (300, 790, 1250):
    F.line([(x, 626), (x, 648)], LINE, 5, True)

# ---------------- bottom row ----------------
BY = 650; BH = 300
F.panel(34, BY, 540, BH, "Existence", 40, 26)
F.panel(588, BY, 400, BH, "Distribution", 40, 26)
F.panel(1002, BY, 504, BH, "Transition", 40, 26)

cx = [188, 242, 296, 350, 404]
for k, x in zip("KPDMX", cx):
    F.chip(k, x + 1, 698, 44)
rowsy = [("human", "Human", 752, "KPDM"), ("agent", "Primary agent", 812, "KPDMX"), ("sub", "Sub-agents", 872, "KPMX")]
for who, lab, y, has in rowsy:
    F.img(AV[who], 42, y, 44, 44)
    F.text(88, y, 96, 46, lab, 17, True, NAVY, "left")
    for k, x in zip("KPDMX", cx):
        F.rect(x, y, 50, 48, "#FFFFFF", "#C5CEDA", 1.5, 8)
        if k in has:
            F.rect(x + 13, y + 12, 24, 24, COL[k][1], NAVY, 1, 50)
F.text(44, 700, 110, 22, "schematic", 15, False, "#6B7280", "left", True)
F.line([(468, 696), (468, 940)], PBORDER, 1.2, False)
F.actor("human", 478, 700, 36); F.text(514, 700, 16, 36, "+", 22, True); F.actor("agent", 530, 700, 36)
F.line([(522, 740), (522, 758)], NAVY, 2.5, True)
F.img("doc_gears", 488, 762, 66, 70)
F.text(466, 836, 106, 44, "Mixed contribution", 16, True)
F.img("bubble_a", 484, 888, 42, 34); F.img("cross_badge", 514, 892, 28, 28)
F.text(470, 922, 100, 22, "Bare approval", 15)

base = 818
bc = ["#4E79A7", "#59A14F", "#F28E2B", "#8E6BB0"]
groups = [("human", 624, (9, 3, 18, 14)), ("agent", 724, (28, 15, 6, 46)), ("sub", 834, (10, 1, 0, 9))]
F.line([(608, base), (972, base)], NAVY, 2, False); F.line([(608, 704), (608, base)], NAVY, 2, False)
for who, x0, hs in groups:
    for j, hh in enumerate(hs):
        if hh:
            F.rect(x0 + j * 22, base - hh * 2.0, 18, hh * 2.0, bc[j], NAVY, 1, 0)
    F.img(AV[who], x0 + 22, base + 6, 44, 38)
F.text(840, 700, 130, 20, "schematic", 15, False, "#6B7280", "right", True)
F.text(600, 868, 380, 22, "Eight research stages", 17, True)
st = ["st_lit", "st_theory", "st_design", "st_analysis", "st_interp", "st_write", "st_verify", "st_revise"]
for k, n in enumerate(st):
    F.rect(598 + k * 48, 894, 42, 48, "#EEF2F7", GREY, 1.5, 12)
    F.img(n, 602 + k * 48, 900, 34, 36)

F.img("human", 1014, 716, 52, 52); F.img("agent", 1014, 812, 52, 52)
F.chip("D", 1100, 714, 54); F.chip("D", 1210, 714, 54); F.chip("M", 1312, 714, 54)
F.chip("P", 1130, 824, 54); F.chip("K", 1250, 824, 54)
F.line([(1070, 742), (1096, 742)], NAVY, 2.5)
F.line([(1158, 741), (1206, 741)], NAVY, 2.5); F.line([(1268, 741), (1308, 741)], NAVY, 2.5)
F.line([(1150, 772), (1168, 820)], NAVY, 2.5); F.line([(1226, 826), (1242, 772)], NAVY, 2.5)
F.line([(1190, 851), (1246, 851)], NAVY, 2.5); F.line([(1312, 826), (1340, 772)], NAVY, 2.5)
F.line([(1072, 838), (1126, 851)], NAVY, 2.5)
F.text(1100, 912, 230, 20, "schematic", 15, False, "#6B7280", "left", True)
F.line([(1396, 700), (1396, 936)], PBORDER, 1.2, False)
F.text(1402, 698, 100, 44, "Interaction modes", 17, True)
F.img("st_revise", 1428, 748, 40, 40); F.text(1402, 790, 96, 22, "Loop", 16)
F.line([(1412, 836), (1440, 836)], NAVY, 2.5, False)
F.line([(1440, 836), (1476, 818)], NAVY, 2.5, True); F.line([(1440, 836), (1476, 854)], NAVY, 2.5, True)
F.text(1402, 862, 96, 22, "Hand-off", 16)
F.line([(1416, 906), (1480, 906)], NAVY, 2.5)
F.text(1402, 916, 96, 22, "Solo run", 16)

# return lane
F.line([(18, 984), (18, 300), (31, 300)], LINE, 5, True)
F.img("pages", 36, 956, 40, 46)
F.line([(18, 984), (36, 984)], LINE, 5, False)
F.line([(80, 982), (470, 982)], LINE, 5, False)
F.rect(470, 962, 596, 40, "#FFFFFF", NAVY, 2, 50)
F.text(478, 962, 580, 40, "A later revision may add sessions and repeat the coding", 19, True)
F.line([(1066, 982), (1430, 982)], LINE, 5, True)
F.img("manuscript", 1436, 950, 56, 60)

F.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig1.drawio"), "Figure 1")
print("cells", len(F.cells))
