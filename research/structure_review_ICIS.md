# Structure and length review against ICIS papers

Date: 2026-10-22. Written by the primary agent (claude-sonnet-5.5) at the request of the human (I040). Scripts: `research/tools/icis_structure.py`, `icis_shares.py`, `check_citations.py`, `paper/_measure.py`. Raw numbers: `research/icis_refs/structure_raw.json`, `structure_shares.json`, `shares_output.txt`.

## 1. Verdicts

| Question | Finding | Action |
|---|---|---|
| No abstract in the paper | The ICIS 2026 template says authors and abstracts must not be in the file with the body of the paper, they are added in the review system. All 16 sampled ICIS papers carry an abstract (114 to 184 words, median 159) and 3 to 6 keywords, because they are camera-ready or author versions. | Abstract and keywords written separately (`paper/submission_form_abstract.txt`, 160 words). Not added to the paper file. |
| Introduction too short | 364 words, 8.7% of the body. Every sampled paper of 9 or more pages has 552 to 1,461 words (median 842). Papers of 9 to 11 pages, the closest in length, have 552 to 842 words (13.5% to 20.2%). | Rewritten to 562 words (12.6% of the body): setting of the call, three audiences, approach with corpus size, preview of findings, contributions. |
| Other proportions | Background 20.7%, method 14.6%, findings 36.8%, discussion 16.6% are inside the sample ranges. Conclusion 2.6% against a median of 5.1% (limitations included in the sample figure). | Conclusion extended with concrete further work. Findings trimmed of text duplicated in tables. |
| Literature engagement | 23 references. Sampled short papers have 31 to 58 (median 51), full papers 39 to 101 (median 61). | Eight sources added, each read in full or in part and tied to a claim. Now 31. |
| Citation integrity | A work cited in the text (Walker & Whittaker, 1990) was missing from the reference list in earlier versions. | Verified in Crossref and added. Citation audit script added. |
| White space | The Word export had gaps of 10.7, 6.8 and 8.0 lines on pages 2, 5 and 6 and 4.3 free lines on page 8. The cause was figures and tables that cannot split and moved whole to the next page. | Concrete content added (see 5). Tables of more than 8 rows may now break across pages with a repeated header. Largest remaining gap 4.6 lines. |

## 2. The benchmark and its limits

Source. AIS eLibrary returned HTTP 403 to scripted requests and to the desktop browser ("this request was blocked"), and the block was not circumvented. The sample was drawn from arXiv by searching the comment field for ICIS. Only papers whose comment names the AIS International Conference on Information Systems were kept (ICISSP, IEEE ICIS, ISD and Pre-ICIS workshop papers were dropped).

Limits.
- The sample is a convenience sample of 16 papers from ICIS 2019 to ICIS 2026 and says nothing about acceptance. Most are information-systems design, behavioural or technical papers. Seven are conceptual, qualitative, review or taxonomy papers.
- The arXiv versions are author versions and may differ from the proceedings versions.
- The submission type of each paper (completed paper, short paper, research in progress) could not be verified. Types are inferred from length: 6 to 11 pages including references, and 17 to 18 pages including references.
- Section boundaries were assigned by hand from the heading lists, and word counts include table text.
- A PDW submission is not a regular ICIS paper. It has an 8-page limit and a review rubric that includes the workflow appendix. The sample fixes proportions, not rules.

## 3. The sample

| arXiv id | ICIS | Pages | Kind | Abstract words | Body words | Intro words | Intro % | Refs |
|---|---|---|---|---|---|---|---|---|
| 2002.08777 | 2019 | 6 | experiment | 37 | 852 | 154 | 18.1 | 31 |
| 2602.11707 | 2025 | 9 | conceptual | 114 | 3,508 | 709 | 20.2 | 58 |
| 2210.02123 | 2022 | 9 | experiment | 162 | 4,177 | 842 | 20.2 | 52 |
| 2109.15067 | 2021 | 9 | experiment | 159 | 3,293 | 641 | 19.5 | 31 |
| 2201.05945 | 2020 | 11 | literature review | 170 | 4,101 | 552 | 13.5 | 51 |
| 2609.33754 | 2026 | 17 | technical design | 158 | 7,675 | 885 | 11.5 | 86 |
| 2606.17839 | 2025 | 17 | design patterns | 167 | 8,752 | 1,148 | 13.1 | 39 |
| 2606.17831 | 2025 | 17 | qualitative field study | 150 | 9,142 | 1,432 | 15.7 | 65 |
| 2510.08104 | 2025 | 17 | conceptual | 156 | 7,407 | 948 | 12.8 | 101 |
| 2510.00555 | 2025 | 17 | design science | 184 | 7,136 | 690 | 9.7 | 39 |
| 2510.00552 | 2025 | 17 | taxonomy from literature | 159 | 6,969 | 690 | 9.9 | 61 |
| 2412.13528 | 2024 | 17 | technical design | 160 | 6,564 | 838 | 12.8 | 59 |
| 2408.04317 | 2022 | 17 | qualitative multi-case | 165 | 12,385 | 985 | 8.0 | 60 |
| 2108.04766 | 2021 | 17 | qualitative think-aloud | 150 | 10,463 | 750 | 7.2 | 50 |
| 2405.01881 | 2023 | 18 | technical design | 155 | 8,437 | 1,411 | 16.7 | 61 |
| 2310.02568 | 2023 | 18 | technical design | 161 | 8,771 | 1,461 | 16.7 | 68 |

Reference counts are approximate (year patterns in the reference section). The 6-page paper has an extended-abstract format and an abstract measured at 37 words, which probably reflects extraction.

## 4. Proportions

Share of body words (introduction, background, method, results, discussion, conclusion), medians.

| Group | n | Intro | Background | Method | Results | Discussion | Conclusion |
|---|---|---|---|---|---|---|---|
| All | 16 | 13.3% | 18.6% | 18.0% | 17.0% | 11.3% | 5.4% |
| 6 to 11 pages | 5 | 19.5% | 33.3% | 12.4% | 14.5% | 0.0% | 6.7% |
| 17 to 18 pages | 11 | 12.8% | 17.9% | 20.5% | 19.5% | 12.7% | 5.1% |
| Conceptual, qualitative, review, taxonomy | 7 | 12.8% | 17.5% | 10.7% | 33.8% | 16.8% | 5.1% |
| This paper, before | | 8.7% | 20.7% | 14.6% | 36.8% | 16.6% | 2.6% |
| This paper, after | | 12.6% | 19.6% | 17.1% | 31.7% | 16.2% | 2.9% |

The short papers fold discussion into results or conclusion, so their zero is a coding effect. The comparison that matters is the line for non-technical papers, which the manuscript now matches except for method (a new coding excerpt table sits there) and conclusion.

## 5. What was added to fill space, and why these items

The human asked for concrete content and not for longer sentences. Every addition below states something that was not in the paper.
- Introduction: the nine research functions that the call requires an account for (taken from the call), the three audiences of a contribution vocabulary, the size of the corpus and coders, and a preview of the principal findings.
- Background: the position of fully automated research pipelines, whose human share is unmeasured (Lu et al., 2024), and cognitive offloading as the link between delegation and Metacognition (Risko & Gilbert, 2016).
- Method: Table 1, five consecutive units from the project with the abridged content and the tags of both coders. It shows the unit, the actor rule, multi-label tagging and the residual code in use. A sentence on LLM coders working from the codebook (Gilardi et al., 2023, Xiao et al., 2023).
- Limitations: annotation studies find that an LLM agrees less with experts than experts agree with each other (Xiao et al., 2023) and call for validation against human labels (Pangakis et al., 2023, Ziems et al., 2024).
- Conclusion: further work on projects with several authors, a human validation subsample and recoding at each revision.
- Reference list: Walker and Whittaker (1990) was cited and missing.

Text removed because a table or the method section already carried it: examples repeated from Table 3, the count of tool-only messages repeated in the findings, the actor rule repeated in the typology, a synthesis sentence of RQ2 that the introduction and conclusion state, a table row without content, and values in the discussion that Table 5 shows.

## 6. Layout

All tables of more than 8 rows may break across pages, the header repeats, rows do not split. Figures are 6.0 in wide. The final Word export has 8 body pages. Gaps at the bottom of pages 3 to 8 are 0.8, 0.7, 0.5, 4.6, 1.5 and 2.4 lines. Page 8 has about 2.4 free lines, so another reader with different line breaks could push a few lines onto a ninth page. The pages named by the human (3, 5 and 6) differ from those of the Word export (2, 5 and 6), which suggests a different viewer. The delivered PDF is the Word export.

## 7. Remaining points for the human

1. Reference count 31 is at the bottom of the range for short papers. More sources would need to be read before they are cited.
2. S01-U032 in Figure 2 shows Proposal, a type both coders tag, while its primary tags are Decision (Coder A) and Knowledge (Coder B). Table 1 shows all three.
3. The abstract in `paper/submission_form_abstract.txt` is for the form. If the human wants it inside the PDF, that departs from the template.
