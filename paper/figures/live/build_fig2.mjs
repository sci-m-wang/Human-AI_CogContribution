// Figure 2 of the ICIS PDW paper (version 2, after the human review I036), built live in draw.io.
//
//   node paper/figures/live/build_fig2.mjs
//
// A  Six interaction modes: one column per mode with its name, a one-line gloss, the earlier
//    unit and the later unit as actor-and-type pills (time runs downwards), and the transition
//    counts of the two coders as paired bars on a common baseline.
// B  Worked case: the recorded exchange that produced the typology, on a human lane and an
//    agent lane, time running to the right.
// C  Mixed contribution against bare approval.
//
// Counts are the reference counts of research/coding/final_v2/transitions.csv (run 2, 265 units), coder A (GPT) and
// coder B (Gemini):
//   1 Direction and drafting   H:D -> AI:P        9, 9
//   2 Proposal and commitment  AI:P -> H:D        9, 12
//   3 Supply and reframing     AI:K -> H:D        3, 4
//   4 Regulation and response  H:D|H:M -> AI:M    17, 17 (10,12 + 7,5)
//   5 Challenge                AI:P -> H:M        3, 4
//   6 Autonomous work          AI:M -> AI:M|AI:K  85, 62 (74,53 + 11,9)
// Canvas 1280 px wide, printed at 6.15 in: 1 px = 0.346 pt, so 20 px = 6.9 pt, 18 px = 6.2 pt.

import { connect, finish, T, Figure, textWidth } from "./dx2.mjs";

const FILE = "<project>/paper/figures/drawio/fig2_sivia.drawio";
const W = 1280;

const { call, close } = await connect({ clear: true });
const F = new Figure(call, W, 760);

const modes = [
  { id: "one", name: "Direction and drafting", gloss: "Human decides,\nagent drafts", first: ["human", ["D"]], then: ["agent", ["P"]], a: 9, b: 9 },
  { id: "two", name: "Proposal and commitment", gloss: "Agent proposes,\nhuman commits", first: ["agent", ["P"]], then: ["human", ["D"]], a: 9, b: 12 },
  { id: "three", name: "Supply and reframing", gloss: "Agent supplies,\nhuman reframes", first: ["agent", ["K"]], then: ["human", ["D"]], a: 3, b: 4 },
  { id: "four", name: "Regulation and response", gloss: "Human regulates,\nagent responds", first: ["human", ["D", "M"]], then: ["agent", ["M"]], a: 17, b: 17 },
  { id: "five", name: "Challenge", gloss: "Agent proposes,\nhuman challenges", first: ["agent", ["P"]], then: ["human", ["M"]], a: 3, b: 4 },
  { id: "six", name: "Autonomous work", gloss: "Agent verifies and\nreports alone", first: ["agent", ["M"]], then: ["agent", ["M", "K"]], a: 85, b: 62 },
];

try {
  // ------------------------------------------------------------------ A: six interaction modes
  const gTop = 12;
  const colX = 28;
  const colW = 204;
  const yName = 76;
  const yGloss = 132;
  const yPillOne = 184;
  const pillH = 44;
  const yPillTwo = 262;
  const barScale = 0.9;
  const baseline = 410;
  const gBottom = baseline + 14;

  await F.panel({ id: "a", letter: "A", title: "Six interaction modes", x: 12, y: gTop, w: 1256, h: gBottom - gTop });

  // Legend for the paired bars, right in the header.
  const legendRight = 1252;
  const tB = await F.text({ id: "txt-a-legend-b", x: legendRight, y: gTop + 14, text: "Coder B", size: T.fNote, color: T.soft, align: "right" });
  await F.box({ id: "bg-a-legend-b", x: tB.x - 22, y: gTop + 19, w: 16, h: 16, fill: T.coderB, stroke: T.coderB, sw: 1, radius: 4 });
  const tA = await F.text({ id: "txt-a-legend-a", x: tB.x - 36, y: gTop + 14, text: "Coder A", size: T.fNote, color: T.soft, align: "right" });
  await F.box({ id: "bg-a-legend-a", x: tA.x - 22, y: gTop + 19, w: 16, h: 16, fill: T.coderA, stroke: T.coderA, sw: 1, radius: 4 });
  await F.text({ id: "txt-a-legend-note", x: tA.x - 36, y: gTop + 14, text: "transitions found by", size: T.fNote, color: T.muted, align: "right" });

  for (const [i, mode] of modes.entries()) {
    const x0 = colX + i * colW;
    const cx = x0 + colW / 2;
    if (i > 0) await F.line({ id: `line-a-sep-${mode.id}`, pts: [[x0, yName + 2], [x0, baseline + 4]], color: T.hair, width: 1.5 });

    // number and name
    await F.box({
      id: `bg-a-${mode.id}-num`, x: x0 + 12, y: yName + 1, w: 28, h: 28, fill: T.navy, stroke: T.navy, sw: 1, radius: 14, label: String(i + 1),
      extra: `fontSize=${T.fBody};fontFamily=${T.font};fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;`,
    });
    await F.text({ id: `txt-a-${mode.id}-name`, x: x0 + 46, y: yName, text: mode.name, size: T.fBody, bold: true, color: T.ink, maxW: colW - 46 - 8 });
    await F.text({ id: `txt-a-${mode.id}-gloss`, x: x0 + 14, y: yGloss, text: mode.gloss, size: T.fNote, color: T.soft });

    // earlier unit above, later unit below, centred on the column
    const one = await F.chip({ id: `a-${mode.id}-first`, actor: mode.first[0], types: mode.first[1], x: cx - (8 + 34 + 8 + mode.first[1].length * 30 + (mode.first[1].length - 1) * 4 + 8) / 2, y: yPillOne, h: pillH });
    const two = await F.chip({ id: `a-${mode.id}-then`, actor: mode.then[0], types: mode.then[1], x: cx - (8 + 34 + 8 + mode.then[1].length * 30 + (mode.then[1].length - 1) * 4 + 8) / 2, y: yPillTwo, h: pillH });
    await F.flow(`line-a-${mode.id}-step`, [[cx, one.bottom + 3], [cx, two.y - 4]]);
    if (i === 0) {
      // Row labels, so that the order of the two pills reads without the arrow.
      await F.text({ id: "txt-a-first", x: x0 + 14, y: yPillOne + 10, text: "first", size: T.fNote, color: T.muted });
      await F.text({ id: "txt-a-then", x: x0 + 14, y: yPillTwo + 10, text: "then", size: T.fNote, color: T.muted });
    }

    // paired bars on a common baseline
    const bar = async (key, value, bx, color) => {
      const h = Math.max(3, Math.round(value * barScale));
      await F.box({ id: `bg-a-${mode.id}-bar-${key}`, x: bx, y: baseline - h, w: 38, h, fill: color, stroke: color, sw: 1, radius: 3 });
      await F.text({ id: `txt-a-${mode.id}-val-${key}`, x: bx + 19, y: baseline - h - 26, text: String(value), size: T.fBody, bold: true, color: T.ink, align: "center" });
    };
    await bar("a", mode.a, cx - 44, T.coderA);
    await bar("b", mode.b, cx + 6, T.coderB);
    await F.line({ id: `line-a-${mode.id}-base`, pts: [[cx - 56, baseline + 1], [cx + 56, baseline + 1]], color: T.muted, width: 1.5 });
  }

  // ------------------------------------------------------------------ B: worked case
  const hTop = gBottom + 12;
  const laneH = 104;
  const hHeight = 62 + laneH + 22 + laneH + 12;
  await F.panel({ id: "b", letter: "B", title: "Worked case", x: 12, y: hTop, w: 812, h: hHeight });

  const humanBand = hTop + 62;
  const agentBand = humanBand + laneH + 22;
  await F.box({ id: "bg-b-band-human", x: 28, y: humanBand, w: 576, h: laneH, fill: T.white, stroke: T.white, sw: 1, radius: 10 });
  await F.box({ id: "bg-b-band-agent", x: 28, y: agentBand, w: 576, h: laneH, fill: T.white, stroke: T.white, sw: 1, radius: 10 });

  await F.avatar({ id: "b-lane-human", kind: "human", x: 62, y: humanBand + 18, d: 40 });
  await F.text({ id: "txt-b-lane-human", x: 82, y: humanBand + 62, text: "Human", size: T.fNote, bold: true, color: T.navy, align: "center" });
  await F.avatar({ id: "b-lane-agent", kind: "agent", x: 62, y: agentBand + 10, d: 40 });
  await F.text({ id: "txt-b-lane-agent", x: 82, y: agentBand + 52, text: "Primary\nagent", size: T.fNote, bold: true, color: T.slate, align: "center" });

  const steps = [
    { id: "one", actor: "agent", type: "K", caption: "25 sources\nread in full" },
    { id: "two", actor: "human", type: "P", caption: "Knowledge is\na type" },
    { id: "three", actor: "agent", type: "P", caption: "Framework\nv0.1 drafted" },
    { id: "four", actor: "human", type: "D", caption: "One round\nis a unit" },
  ];
  const stepX = [142, 252, 362, 472];
  const placed = [];
  for (const [i, step] of steps.entries()) {
    const human = step.actor === "human";
    const chipY = human ? humanBand + 54 : agentBand + 6;
    const chip = await F.chip({ id: `b-${step.id}`, actor: step.actor, types: [step.type], x: stepX[i], y: chipY, h: 44 });
    await F.text({
      id: `txt-b-${step.id}-caption`, x: chip.cx, y: human ? humanBand + 4 : agentBand + 54,
      text: step.caption, size: T.fNote, color: T.ink, align: "center",
    });
    placed.push(chip);
  }
  // zigzag between the lanes: out of one chip sideways, then into the next chip from below or above
  for (let i = 0; i < placed.length - 1; i += 1) {
    const from = placed[i];
    const to = placed[i + 1];
    const up = steps[i].actor === "agent";
    await F.flow(`line-b-step-${["one", "two", "three"][i]}`, [
      [from.right + 4, from.cy], [to.cx, from.cy], [to.cx, up ? to.bottom + 4 : to.y - 4],
    ]);
  }

  // the typology, built by both actors, sits beside the lanes on the panel wash
  const outCx = 664;
  const outTop = placed[3].cy + 30;
  await F.doc({ id: "b-typology", x: outCx - 22, y: outTop, w: 44, h: 56, stroke: T.navy });
  await F.text({ id: "txt-b-typology", x: outCx + 34, y: outTop + 2, text: "Typology", size: T.fBody, bold: true, color: T.navy });
  await F.text({ id: "txt-b-typology-note", x: outCx + 34, y: outTop + 28, text: "built by both\nactors", size: T.fNote, color: T.soft });
  await F.flow("line-b-step-out", [[placed[3].right + 4, placed[3].cy], [outCx, placed[3].cy], [outCx, outTop - 4]]);

  // ------------------------------------------------------------------ C: mixed contribution
  const cX = 836;
  await F.panel({ id: "c", letter: "C", title: "Mixed contribution", x: cX, y: hTop, w: 432, h: hHeight });
  await F.line({ id: "line-c-mid", pts: [[cX + 216, hTop + 66], [cX + 216, hTop + 204]], color: T.hair, width: 1.5 });

  const half = async (key, label, left, second, verdict) => {
    const hx = left;
    await F.text({ id: `txt-c-${key}-label`, x: hx, y: hTop + 62, text: label, size: T.fBody, bold: true, color: T.ink });
    const top = await F.chip({ id: `c-${key}-top`, actor: "agent", types: ["P"], x: hx, y: hTop + 102, h: 44 });
    let bottom;
    if (second === "human") {
      bottom = await F.chip({ id: `c-${key}-bottom`, actor: "human", types: ["D"], x: hx, y: hTop + 158, h: 44 });
    } else {
      bottom = { x: hx, y: hTop + 158, w: 88, h: 44, right: hx + 88, bottom: hTop + 202, cy: hTop + 180 };
      await F.box({ id: `bg-c-${key}-bottom`, x: hx, y: hTop + 158, w: 88, h: 44, fill: T.white, stroke: T.slate, sw: 1.75, radius: 22, dashed: true });
      await F.avatar({ id: `c-${key}-bottom-who`, kind: "human", x: hx + 6, y: hTop + 163, d: 34 });
      await F.text({ id: `txt-c-${key}-ok`, x: hx + 48, y: hTop + 169, text: "OK.", size: T.fNote, bold: true, color: T.soft });
    }
    const docX = hx + 140;
    const docY = hTop + 112;
    await F.doc({ id: `c-${key}-doc`, x: docX, y: docY, w: 40, h: 54, stroke: verdict === "check" ? T.navy : T.slate, fill: verdict === "check" ? T.white : T.slateTint });
    await F.flow(`line-c-${key}-in-top`, [[top.right + 4, top.cy], [docX - 6, docY + 16]]);
    if (second === "human") await F.flow(`line-c-${key}-in-bottom`, [[bottom.right + 4, bottom.cy], [docX - 6, docY + 38]]);
    else await F.line({ id: `line-c-${key}-in-bottom`, pts: [[bottom.right + 4, bottom.cy], [docX - 6, docY + 38]], color: T.muted, width: 2, head: "classic", dashed: true });
    await F.mark({ id: `c-${key}-verdict`, kind: verdict, cx: docX + 20, cy: hTop + 202 - 6, d: 30 });
  };
  await half("both", "Both add content", cX + 20, "human", "check");
  await half("bare", "Bare approval", cX + 236, "approval", "cross");

  await F.text({
    id: "txt-c-rule", x: cX + 20, y: hTop + 238,
    text: "A contribution is mixed only when both actors\nadd explicit content to the same output.",
    size: T.fNote, color: T.soft,
  });

  const height = hTop + hHeight + 12;
  F.h = height;
  console.log("canvas", W, "x", height);
  const report = await finish({ call, close, file: FILE, w: W, h: height, name: "Figure 2" });
  if (F.warnings.length) console.log("fit warnings:\n" + F.warnings.join("\n"));
  if (report.hard_failure_count) process.exitCode = 1;
} catch (error) {
  console.log("ERROR", error.message);
  close();
}
