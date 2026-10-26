// Figure 3 of the ICIS PDW paper (version 2): the delegation and commitment account in four columns, built live in draw.io.
//
//   node paper/figures/live/build_fig3.mjs      (run in the foreground, it needs about a minute)
//
// Four steps in one row, so that no lane stays empty: 1 Delegate a scope (human), 2 Generate (AI), 3 Report back (AI),
// 4 Commit or reframe (human). Each column carries the contribution types of the step and one real message from the
// recorded project (S01-U020, S01-U021 to S01-U031, S01-U031, S01-U032), abridged into English. Under the columns the
// three propositions of Table 3 are marked on the steps they cover. The loop arrow closes the cycle.

import { connect, finish, T, Figure, textWidth } from "./dx2.mjs";

const FILE = "<project>/paper/figures/drawio/fig3_sivia.drawio";
const W = 1280;
const { call, close } = await connect({ clear: true });
const F = new Figure(call, W, 420);

const COLS = [
  { id: "s1", n: 1, actor: "human", title: "Delegate a scope", types: ["D", "M"], quote: "\u201CRead the originals as far as possible, to build the framework accurately.\u201D", note: "Human, S01-U020" },
  { id: "s2", n: 2, actor: "agent", title: "Generate", types: ["K", "P", "M"], quote: "\u201CSeven sub-agents fetched the originals. I spot-checked their notes.\u201D", note: "Primary agent, S01-U021 to U031" },
  { id: "s3", n: 3, actor: "agent", title: "Report back", types: ["M"], quote: "\u201C25 sources read in full, 9 in part, 12 by abstract only, 8 not found.\u201D", note: "Primary agent, S01-U031" },
  { id: "s4", n: 4, actor: "human", title: "Commit or reframe", types: ["D", "P"], quote: "\u201CKnowledge should count as a contribution. Design becomes Proposal.\u201D", note: "Human, S01-U032" },
];
const X0 = [12, 330, 648, 966];
const CW = 302;
const colTop = 12;

try {
  const qW = CW - 28;
  const qH = Math.max(...COLS.map((c) => F.bubbleHeight(c.quote, qW, T.fNote)));
  const bubbleY = colTop + 106;
  const colH = 106 + qH + 8 + 22 + 10;
  const colBottom = colTop + colH;
  const humanFill = "#EEF3FA";
  const aiFill = "#F3F4F7";

  const chips = [];
  for (const [i, c] of COLS.entries()) {
    const x0 = X0[i];
    const human = c.actor === "human";
    await F.box({ id: `bg-${c.id}-col`, x: x0, y: colTop, w: CW, h: colH, fill: human ? humanFill : aiFill, stroke: human ? "#C9D6E8" : T.hair, sw: 1.5, radius: 14 });
    await F.box({
      id: `bg-${c.id}-num`, x: x0 + 14, y: colTop + 12, w: 28, h: 28, fill: T.navy, stroke: T.navy, sw: 1, radius: 14, label: String(c.n),
      extra: `fontSize=${T.fBody};fontFamily=${T.font};fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;`,
    });
    await F.text({ id: `txt-${c.id}-title`, x: x0 + 50, y: colTop + 12, text: c.title, size: T.fTitle - 2, bold: true, color: T.ink });
    chips.push(await F.chip({ id: c.id, actor: c.actor, types: c.types, x: x0 + 14, y: colTop + 50, h: 44 }));
    await F.bubble({ id: `${c.id}-quote`, actor: c.actor, x: x0 + 14, y: bubbleY, w: qW, text: c.quote, size: T.fNote, tail: "none", minH: qH });
    await F.text({ id: `txt-${c.id}-note`, x: x0 + 16, y: bubbleY + qH + 6, text: c.note, size: T.fNote - 2, color: T.muted });
  }

  // the cycle runs along the chip row
  for (let i = 0; i < 3; i += 1) {
    await F.flow(`line-${COLS[i].id}-${COLS[i + 1].id}`, [[chips[i].right + 4, chips[i].cy], [chips[i + 1].x - 4, chips[i + 1].cy]]);
  }
  // the output of step 4: a mixed output with a check
  const docX = X0[3] + 168;
  await F.doc({ id: "out-doc", x: docX, y: colTop + 48, w: 36, h: 46, stroke: T.navy });
  await F.mark({ id: "out-check", kind: "check", cx: docX + 47, cy: colTop + 88, d: 22 });
  await F.text({ id: "txt-out-title", x: docX + 64, y: colTop + 50, text: "Mixed\noutput", size: T.fNote, bold: true, color: T.navy });
  await F.flow("line-s4-out", [[chips[3].right + 4, chips[3].cy], [docX - 6, chips[3].cy]]);

  // loop back to the next delegation
  const loopY = colBottom + 24;
  await F.flow("line-loop", [[X0[3] + 150, colBottom + 3], [X0[3] + 150, loopY], [X0[0] + 150, loopY], [X0[0] + 150, colBottom + 5]]);
  const loopLabel = "next delegation";
  const lw = Math.ceil(textWidth(loopLabel, T.fNote) * 1.04) + 26;
  await F.box({
    id: "bg-loop-label", x: Math.round(640 - lw / 2), y: loopY - 13, w: lw, h: 26, fill: T.white, stroke: T.hair, sw: 1.5, radius: 13, label: loopLabel,
    extra: `fontSize=${T.fNote};fontFamily=${T.font};fontColor=${T.soft};align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;`,
  });

  // propositions
  const stripH = 50;
  const y1 = colBottom + 46;
  const y2 = y1 + stripH + 8;
  const strip = async (id, x, y, w, name, claim) => {
    await F.box({ id: `bg-${id}`, x, y, w, h: stripH, fill: T.navyTint, stroke: T.navy, sw: 1.5, radius: 10 });
    await F.text({ id: `txt-${id}-name`, x: x + 12, y: y + 3, text: name, size: T.fBody, bold: true, color: T.navy });
    await F.text({ id: `txt-${id}-claim`, x: x + 12, y: y + 26, text: claim, size: T.fNote, color: T.soft });
    F.fit(id, claim, T.fNote, w - 24);
  };
  await strip("p1", X0[0], y1, X0[2] + CW - X0[0], "P1 Bounded delegation", "A run of AI work opens with a human scope and ends in a hand-back to the human.");
  await strip("p2", X0[3], y1, CW, "P2 Retained commitment", "Direction stays with the human.");
  await strip("p3", X0[1], y2, X0[3] + CW - X0[1], "P3 Knowledge-induced reframing", "Knowledge from one party changes the other party\u2019s construct when a decision is pending.");

  // legend of the type tiles in the free corner under step 1
  const lx = X0[0] + 4;
  const types = [["K", "Knowledge", lx, y2 + 2], ["P", "Proposal", lx + 124, y2 + 2], ["D", "Decision", lx, y2 + 27], ["M", "Metacognition", lx + 124, y2 + 27]];
  for (const [t, label, x, y] of types) {
    await F.tile({ id: `legend-${t.toLowerCase()}`, type: t, x, y, s: 22, fs: 14 });
    await F.text({ id: `txt-legend-${t.toLowerCase()}`, x: x + 28, y: y + 1, text: label, size: T.fNote - 1, color: T.soft });
  }

  const H = y2 + stripH + 12;
  F.h = H;
  console.log("canvas", W, "x", H, "colH", colH, "qH", qH);
  const report = await finish({ call, close, file: FILE, w: W, h: H, name: "Figure 3" });
  if (F.warnings.length) console.log("fit warnings:\n" + F.warnings.join("\n"));
  if (report.hard_failure_count) process.exitCode = 1;
} catch (error) {
  console.log("ERROR", error.message);
  close();
}
