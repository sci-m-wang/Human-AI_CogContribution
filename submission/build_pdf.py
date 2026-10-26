"""Build the single submission PDF: main paper (<= 8 pages), references, workflow appendix, in this order.
Inputs: paper/ICIS_PDW_paper.pdf (body + references), paper/ICIS_PDW_workflow_appendix.pdf.
Output: submission/ICIS2026_PDW_submission.pdf and submission/package_check.txt"""
import fitz, io, os, re, sys
from pypdf import PdfReader, PdfWriter
ROOT = r"<project>"
paper = os.path.join(ROOT, "paper", "ICIS_PDW_paper.pdf"); app = os.path.join(ROOT, "paper", "ICIS_PDW_workflow_appendix.pdf")
out = os.path.join(ROOT, "submission", "ICIS2026_PDW_submission.pdf")
d = fitz.open(paper)
ref_page = next(i for i, pg in enumerate(d) if re.search(r"(?m)^References\s*$", pg.get_text()))
rep = []
rep.append("paper pages: %d, References heading on page %d, so the main paper has %d pages" % (len(d), ref_page + 1, ref_page))
assert ref_page <= 8, "main paper exceeds 8 pages"
w = PdfWriter()
r1 = PdfReader(paper); r2 = PdfReader(app)
for pg in r1.pages: w.add_page(pg)
for pg in r2.pages: w.add_page(pg)
w.add_outline_item("Main paper", 0)
w.add_outline_item("References", ref_page)
w.add_outline_item("Workflow appendix", len(r1.pages))
w.add_metadata({"/Title": "Who Contributes What in Human-AI Research? A Qualitative Case Study of a Project That Analyses Itself", "/Author": "", "/Subject": "", "/Keywords": ""})
with open(out, "wb") as f: w.write(f)
size = os.path.getsize(out)
rep.append("output %s: %d pages, %.2f MB (limit 50 MB)" % (out, len(r1.pages) + len(r2.pages), size / 1e6))
# first page of each part and the page label printed in the footer
d2 = fitz.open(out)
for i in (0, ref_page - 1, ref_page, len(r1.pages), len(d2) - 1):
    t = d2[i].get_text()
    rep.append("pdf page %d: starts '%s' ... footer number %s" % (i + 1, re.sub(r"\s+", " ", t[:60]), re.findall(r"(\d+)\s*$", t.strip())[-1:]))
fonts = set()
for pg in d2:
    for f in pg.get_fonts(): fonts.add(f[3])
rep.append("fonts embedded: %s" % sorted(fonts))
io.open(os.path.join(ROOT, "submission", "package_check.txt"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
print("\n".join(rep))
