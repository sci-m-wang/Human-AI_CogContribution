// Figure 1 of the ICIS PDW paper (version 4), built live in draw.io with the second-generation
// drawing library dx2.mjs, so that it shares the visual system of Figure 2.
//
//   node paper/figures/live/build_fig1.mjs
//
// Why a fourth version: the human rated the aesthetics of version 3 as poor (I036) and the session
// that was to redraw both figures stopped after Figure 2 (output truncated at 17:28, see
// records/incidents and event E057).
//
// Content (all taken from the recorded project):
//   A  the opening of session S01: U001 (human), U004 (agent), U017 (human), U018 (agent, dispatches
//      sub-agents), a sub-agent note, U020 (human); human turns left, agent turns right.
//   B  what a unit is: one human message (U045), one agent response with its tool-only steps (U044),
//      a spawning response with two sub-agent units, and the rule that units link only inside a session.
//   C  the unit U045 coded by two blind coders. Tags from research/coding/final/_s01_timeline.txt:
//      Coder A (GPT) D primary with M and P, Coder B (Gemini) D primary with M. Then the four types
//      plus Execution with one-line definitions, and the product-or-process rule.
//   D  existence matrix from research/coding/final/existence.csv (agreed pairs)
//   E  distribution: agreed units per actor and type, same file, drawn as a schematic
//   F  transition: a short zigzag of unit chips and the six interaction modes of Figure 2
// Canvas 1280 px wide, printed at 6.15 in: 1 px = 0.346 pt, so 18 px = 6.2 pt.

import { connect, finish, T, Figure, textWidth } from "./dx2.mjs";

const FILE = "<project>/paper/figures/drawio/fig1_sivia.drawio";
const W = 1280;

const { call, close } = await connect({ clear: true });
const F = new Figure(call, W, 940);
const ellipse = (fill, stroke, sw = 1.5) => `ellipse;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=${sw};`;
const gridX = (i, left, step) => left + i * step;

try {
  const topY = 12;
  const topH = 500;
  const botY = topY + topH + 24;
  const botH = 362;
  const botBottom = botY + botH;

  // ================================================================ A  Recorded project
  const aX = 28;
  const aW = 330;
  await F.panel({ id: "a", letter: "A", title: "Recorded project", x: aX, y: topY, w: aW, h: topH });
  let y = topY + 64;
  const gap = 8;
  const bw = 216;
  const turn = async (id, who, text) => {
    const h = F.bubbleHeight(text, bw);
    if (who === "human") {
      await F.avatar({ id: `a-${id}-who`, kind: "human", x: aX + 16, y: y + Math.max(0, (h - 36) / 2), d: 36 });
      await F.bubble({ id: `a-${id}`, actor: "human", x: aX + 66, y, w: bw, text, tail: "left" });
    } else {
      const sub = who === "sub";
      await F.bubble({ id: `a-${id}`, actor: "agent", x: aX + 28, y, w: bw, text, tail: "right" });
      await F.avatar({ id: `a-${id}-who`, kind: sub ? "sub" : "agent", x: sub ? aX + 258 : aX + 264, y: y + Math.max(0, (h - 36) / 2), d: 36 });
    }
    y += h + gap;
  };
  await turn("one", "human", "Record every step, sessions included.");
  await turn("two", "agent", "I read the call for papers.");
  for (let k = 0; k < 3; k += 1) await F.gear({ id: `a-gear-${k}`, x: aX + 40 + k * 30, y: y + 2, s: 24 });
  await F.text({ id: "txt-a-gears", x: aX + 138, y: y + 3, text: "tool steps", size: T.fNote, color: T.muted });
  y += 24 + gap + 4;
  await turn("three", "human", "First survey the related research.");
  await turn("four", "agent", "Dispatching three sub-agents.");
  await turn("five", "sub", "Notes on one source.");
  y += 6;
  await F.doc({ id: "a-export", x: aX + 18, y, w: 30, h: 38 });
  await F.text({ id: "txt-a-export", x: aX + 62, y: y + 2, text: "Every session is exported\nwith its model and parent", size: T.fNote, color: T.soft });

  // ================================================================ B  Units
  const bX = 370;
  const bW = 300;
  await F.panel({ id: "b", letter: "B", title: "Units", x: bX, y: topY, w: bW, h: topH });
  await F.text({ id: "txt-b-rule", x: bX + 16, y: topY + 62, text: "One response is one unit", size: T.fNote, bold: true, color: T.ink });
  const cardX = bX + 16;
  const cardW = bW - 32;
  const card = (id, cy, ch) => F.box({ id: `bg-b-${id}`, x: cardX, y: cy, w: cardW, h: ch, fill: T.white, stroke: T.hair, sw: 1.5, radius: 10 });
  const sbw = 196;

  let by = topY + 94;
  const t1 = "Report several agreement statistics.";
  const h1 = F.bubbleHeight(t1, sbw);
  await card("human", by, h1 + 20);
  await F.avatar({ id: "b-human-who", kind: "human", x: cardX + 10, y: by + 10 + (h1 - 34) / 2, d: 34 });
  await F.bubble({ id: "b-human", actor: "human", x: cardX + 58, y: by + 10, w: sbw, text: t1, tail: "left" });
  by += h1 + 20 + 8;

  const t2 = "Alpha corrects for chance agreement.";
  const h2 = F.bubbleHeight(t2, sbw);
  const c2 = 32 + h2 + 12;
  await card("agent", by, c2);
  for (let k = 0; k < 3; k += 1) await F.gear({ id: `b-gear-${k}`, x: cardX + 62 + k * 30, y: by + 6, s: 24 });
  await F.text({ id: "txt-b-gears", x: cardX + 62 + 96, y: by + 7, text: "tool steps", size: T.fNote, color: T.muted });
  await F.avatar({ id: "b-agent-who", kind: "agent", x: cardX + 10, y: by + 32 + (h2 - 34) / 2, d: 34 });
  await F.bubble({ id: "b-agent", actor: "agent", x: cardX + 58, y: by + 32, w: sbw, text: t2, tail: "left" });
  by += c2 + 8;

  const t3 = "Dispatching three sub-agents.";
  const h3 = F.bubbleHeight(t3, sbw);
  const c3 = 10 + h3 + 12 + 48 + 8;
  await card("spawn", by, c3);
  await F.avatar({ id: "b-spawn-who", kind: "agent", x: cardX + 10, y: by + 10 + (h3 - 34) / 2, d: 34 });
  await F.bubble({ id: "b-spawn", actor: "agent", x: cardX + 58, y: by + 10, w: sbw, text: t3, tail: "left" });
  const subY = by + 10 + h3 + 12;
  const subW = (cardW - 30) / 2;
  for (const [i, key] of ["one", "two"].entries()) {
    const sx = cardX + 10 + i * (subW + 10);
    await F.box({ id: `bg-b-sub-${key}`, x: sx, y: subY, w: subW, h: 48, fill: T.slateTint, stroke: T.slate, sw: 1.5, radius: 10 });
    await F.avatar({ id: `b-sub-${key}-who`, kind: "sub", x: sx + 6, y: subY + 9, d: 30 });
    await F.text({ id: `txt-b-sub-${key}`, x: sx + 56, y: subY + 5, text: "Source\nnotes", size: T.fNote, color: T.ink });
    await F.relate(`line-b-sub-${key}`, [[sx + subW / 2, by + 10 + h3 + 3], [sx + subW / 2, subY - 3]]);
  }
  by += c3 + 10;
  await F.line({ id: "line-b-cut", pts: [[cardX, by], [cardX + cardW, by]], color: T.muted, width: 2, dashed: true });
  await F.text({ id: "txt-b-cut", x: cardX, y: by + 8, text: "Units are linked only\nwithin one session", size: T.fNote, color: T.soft });

  // ================================================================ C  Tags
  const cX = 682;
  const cW = 586;
  await F.panel({ id: "c", letter: "C", title: "Tags", x: cX, y: topY, w: cW, h: topH });
  const lx = cX + 16;
  const lw = 262;
  await F.text({ id: "txt-c-two", x: lx, y: topY + 62, text: "Two blind coders per unit", size: T.fNote, bold: true, color: T.ink });
  const ucY = topY + 94;
  const ubw = 200;
  const uh = F.bubbleHeight("Report several agreement statistics.", ubw);
  await F.box({ id: "bg-c-unit", x: lx, y: ucY, w: lw, h: uh + 38, fill: T.white, stroke: T.navy, sw: 2, radius: 10 });
  await F.avatar({ id: "c-unit-who", kind: "human", x: lx + 8, y: ucY + 10 + (uh - 32) / 2, d: 32 });
  await F.bubble({ id: "c-unit", actor: "human", x: lx + 54, y: ucY + 10, w: ubw, text: "Report several agreement statistics.", tail: "left" });
  await F.text({ id: "txt-c-unit-id", x: lx + 12, y: ucY + 10 + uh + 4, text: "unit S01-U045", size: T.fNote, color: T.muted });
  const ucBottom = ucY + uh + 38;

  const avY = ucBottom + 40;
  const aCx = lx + 66;
  const bCx = lx + 192;
  await F.avatar({ id: "c-coder-a", kind: "coderA", x: aCx - 24, y: avY, d: 48 });
  await F.avatar({ id: "c-coder-b", kind: "coderB", x: bCx - 24, y: avY, d: 48 });
  await F.relate("line-c-fork-a", [[lx + 100, ucBottom + 3], [aCx + 6, avY - 4]]);
  await F.relate("line-c-fork-b", [[lx + 156, ucBottom + 3], [bCx - 6, avY - 4]]);
  await F.text({ id: "txt-c-coder-a", x: aCx, y: avY + 52, text: "Coder A", size: T.fNote, bold: true, color: T.coderA, align: "center" });
  await F.text({ id: "txt-c-coder-b", x: bCx, y: avY + 52, text: "Coder B", size: T.fNote, bold: true, color: "#5B6573", align: "center" });
  const tlY = avY + 84;
  const ts = 34;
  const setA = ["D", "M", "P"];
  const setB = ["D", "M"];
  for (const [i, k] of setA.entries()) await F.tile({ id: `c-a-${k.toLowerCase()}`, type: k, x: aCx - 55 + i * (ts + 4), y: tlY, s: ts, fs: 18 });
  for (const [i, k] of setB.entries()) await F.tile({ id: `c-b-${k.toLowerCase()}`, type: k, x: bCx - 36 + i * (ts + 4), y: tlY, s: ts, fs: 18 });
  await F.text({ id: "txt-c-primary", x: lx + lw / 2, y: tlY + ts + 8, text: "D is the primary tag for both", size: T.fNote, color: T.muted, align: "center" });
  const agY = tlY + ts + 8 + 52;
  await F.relate("line-c-to-agree", [[lx + lw / 2, tlY + ts + 8 + 28], [lx + lw / 2, agY - 4]]);
  await F.box({ id: "bg-c-agree", x: lx, y: agY, w: lw, h: 58, fill: T.navyTint, stroke: T.navy, sw: 1.5, radius: 10 });
  await F.text({ id: "txt-c-agree", x: lx + lw / 2, y: agY + 6, text: "Agreement", size: T.fBody, bold: true, color: T.navy, align: "center" });
  await F.text({ id: "txt-c-agree-sub", x: lx + lw / 2, y: agY + 31, text: "percent, kappa, alpha", size: T.fNote, color: T.soft, align: "center" });

  // right zone: the four types and Execution, then the rule
  const rx = cX + 296;
  const rw = cW - 312;
  await F.line({ id: "line-c-split", pts: [[rx - 12, topY + 62], [rx - 12, topY + topH - 16]], color: T.hair, width: 1.5 });
  const defs = [
    ["K", "Knowledge", "a fact or concept enters"],
    ["P", "Proposal", "a candidate is offered"],
    ["D", "Decision", "the project is committed"],
    ["M", "Metacognition", "checks or steers the work"],
    ["X", "Execution", "a step is carried out"],
  ];
  const rowH = 58;
  for (const [i, [k, name, def]] of defs.entries()) {
    const ry = topY + 64 + i * rowH;
    await F.tile({ id: `c-def-${k.toLowerCase()}`, type: k, x: rx, y: ry + 3, s: 46, fs: 24 });
    await F.text({ id: `txt-c-def-${k.toLowerCase()}-name`, x: rx + 58, y: ry, text: name, size: T.fBody, bold: true, color: T.type[k].ink });
    await F.text({ id: `txt-c-def-${k.toLowerCase()}`, x: rx + 58, y: ry + 25, text: def, size: T.fNote, color: T.soft, maxW: rw - 60 });
  }
  const ruleY = topY + 64 + 5 * rowH + 12;
  await F.box({ id: "bg-c-rule", x: rx, y: ruleY, w: rw, h: 62, fill: T.white, stroke: T.hair, sw: 1.5, radius: 10 });
  await F.text({ id: "txt-c-rule", x: rx + 12, y: ruleY + 8, text: "Product changes: K, P or D.\nOnly the process changes: M.", size: T.fNote, color: T.ink });
  await F.text({ id: "txt-c-multi", x: rx, y: ruleY + 72, text: "A unit may carry several tags,\none of them primary.", size: T.fNote, color: T.muted });

  // ---------------------------------------------------------------- trunk from Tags to the three analyses
  const trunkY = topY + topH + 11;
  const cxs = [28 + 204, 448 + 204, 868 + 200];
  await F.line({ id: "line-trunk-down", pts: [[cX + cW / 2, topY + topH + 2], [cX + cW / 2, trunkY]], color: T.navy, width: 3 });
  await F.line({ id: "line-trunk-bar", pts: [[cxs[0] - 1.5, trunkY], [cxs[2] + 1.5, trunkY]], color: T.navy, width: 3 });
  for (const [i, cx] of cxs.entries()) await F.flow(`line-trunk-${["d", "e", "f"][i]}`, [[cx, trunkY - 1], [cx, botY - 3]]);

  // ================================================================ D  Existence
  const dX = 28;
  const dW = 408;
  await F.panel({ id: "d", letter: "D", title: "Existence", x: dX, y: botY, w: dW, h: botH, note: "agreed pairs" });
  const types5 = ["K", "P", "D", "M", "X"];
  const gx = dX + 140;
  const step = 52;
  const hy = botY + 62;
  for (const [i, k] of types5.entries()) await F.tile({ id: `d-h-${k.toLowerCase()}`, type: k, x: gridX(i, gx, step), y: hy, s: 40, fs: 22 });
  const actors = [
    ["human", "Human", "KPDM"],
    ["agent", "Primary\nagent", "KPDMX"],
    ["sub", "Sub-\nagents", "KPMX"],
  ];
  const ry0 = hy + 50;
  for (const [r, [kind, label, has]] of actors.entries()) {
    const ry = ry0 + r * 56;
    await F.avatar({ id: `d-row-${kind}`, kind, x: dX + 14, y: ry + 6, d: 38 });
    await F.text({ id: `txt-d-row-${kind}`, x: dX + (kind === "sub" ? 14 + 58 : 14 + 46), y: ry + (label.includes("\n") ? 5 : 12), text: label, size: T.fNote, bold: true, color: kind === "human" ? T.navy : T.slate });
    for (const [i, k] of types5.entries()) {
      const cx = gridX(i, gx, step);
      await F.box({ id: `bg-d-cell-${kind}-${k.toLowerCase()}`, x: cx - 2, y: ry, w: 44, h: 50, fill: T.white, stroke: T.hair, sw: 1.5, radius: 8 });
      if (has.includes(k)) await F.shape({ id: `bg-d-dot-${kind}-${k.toLowerCase()}`, x: cx + 8, y: ry + 12, w: 24, h: 24, style: ellipse(T.type[k].stroke, T.type[k].ink, 1.5) });
    }
  }
  const mxY = ry0 + 3 * 56 + 12;
  await F.line({ id: "line-d-mixed-rule", pts: [[dX + 14, mxY - 6], [dX + dW - 14, mxY - 6]], color: T.hair, width: 1.5 });
  await F.chip({ id: "d-mix-h", actor: "human", types: ["D"], x: dX + 14, y: mxY + 8, h: 42, ts: 28 });
  await F.text({ id: "txt-d-plus", x: dX + 110, y: mxY + 14, text: "+", size: T.fBody, bold: true, color: T.ink, align: "center" });
  await F.chip({ id: "d-mix-a", actor: "agent", types: ["P"], x: dX + 122, y: mxY + 8, h: 42, ts: 28 });
  await F.flow("line-d-mix-arrow", [[dX + 210, mxY + 29], [dX + 230, mxY + 29]]);
  await F.doc({ id: "d-mix-doc", x: dX + 236, y: mxY + 6, w: 30, h: 38 });
  await F.mark({ id: "d-mix-ok", kind: "check", cx: dX + 282, cy: mxY + 26, d: 26 });
  await F.text({ id: "txt-d-mix", x: dX + 302, y: mxY + 8, text: "Mixed\ncontribution", size: T.fNote, bold: true, color: T.ink });

  // ================================================================ E  Distribution
  const eX = 448;
  const eW = 408;
  await F.panel({ id: "e", letter: "E", title: "Distribution", x: eX, y: botY, w: eW, h: botH, note: "agreed units" });
  const counts = { human: [9, 3, 18, 14, 0], agent: [28, 15, 6, 46, 32], sub: [10, 1, 0, 9, 17] };
  const scale = 1.9;
  const base = botY + 62 + 96;
  await F.line({ id: "line-e-base", pts: [[eX + 16, base], [eX + eW - 16, base]], color: T.muted, width: 1.5 });
  const groupW = 124;
  for (const [g, kind] of ["human", "agent", "sub"].entries()) {
    const gx0 = eX + 16 + g * groupW + 8;
    for (const [i, k] of types5.entries()) {
      const v = counts[kind][i];
      if (!v) continue;
      const hgt = Math.max(3, Math.round(v * scale));
      await F.box({ id: `bg-e-bar-${kind}-${k.toLowerCase()}`, x: gx0 + i * 22, y: base - hgt, w: 18, h: hgt, fill: T.type[k].stroke, stroke: T.type[k].stroke, sw: 1, radius: 3 });
    }
    await F.avatar({ id: `e-grp-${kind}`, kind, x: gx0 + 28, y: base + 6, d: 36 });
    await F.text({ id: `txt-e-grp-${kind}`, x: gx0 + 54, y: base + 46, text: kind === "human" ? "Human" : kind === "agent" ? "Primary agent" : "Sub-agents", size: T.fNote, bold: true, color: kind === "human" ? T.navy : T.slate, align: "center" });
  }
  const stages = ["Problem", "Literature", "Theory", "Design", "Analysis", "Writing", "Verification", "Revision", "Governance", "Tooling"];
  for (const [i, k] of types5.entries()) await F.tile({ id: `e-leg-${k.toLowerCase()}`, type: k, x: eX + eW - 16 - 5 * 26 + i * 26 + 2, y: botY + 62, s: 22, fs: 13 });
  await F.text({ id: "txt-e-stage", x: eX + 16, y: base + 76, text: "Each tag also carries a stage", size: T.fNote, bold: true, color: T.ink });
  let sx = eX + 16;
  let sy = base + 104;
  let srow = 0;
  const maxX = eX + eW - 16;
  for (const [i, name] of stages.entries()) {
    const w = Math.ceil(textWidth(name, T.fNote)) + 16;
    if (sx + w > maxX) { sx = eX + 16; sy += 32; srow += 1; }
    await F.box({ id: `bg-e-stage-r${srow}-${i}`, x: sx, y: sy, w, h: 26, fill: T.white, stroke: T.hair, sw: 1.5, radius: 13, label: name,
      extra: `fontSize=${T.fNote};fontFamily=${T.font};fontColor=${T.soft};align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;` });
    sx += w + 5;
  }

  // ================================================================ F  Transition
  const fX = 868;
  const fW = 400;
  await F.panel({ id: "f", letter: "F", title: "Transition", x: fX, y: botY, w: fW, h: botH, note: "schematic" });
  const laneH = 76;
  const lh = botY + 62;
  const la = lh + laneH + 8;
  await F.box({ id: "bg-f-lane-h", x: fX + 14, y: lh, w: fW - 28, h: laneH, fill: T.navyTint, stroke: T.navyTint, sw: 1, radius: 10 });
  await F.box({ id: "bg-f-lane-a", x: fX + 14, y: la, w: fW - 28, h: laneH, fill: T.slateTint, stroke: T.slateTint, sw: 1, radius: 10 });
  const seq = [
    { id: "one", actor: "human", t: "D", cap: "sets direction" },
    { id: "two", actor: "agent", t: "P", cap: "drafts" },
    { id: "three", actor: "human", t: "D", cap: "commits" },
    { id: "four", actor: "agent", t: "M", cap: "checks" },
  ];
  const chips = [];
  for (const [i, s] of seq.entries()) {
    const human = s.actor === "human";
    const chip = await F.chip({ id: `f-${s.id}`, actor: s.actor, types: [s.t], x: fX + 30 + i * 84, y: human ? lh + 32 : la + 10, h: 40, ts: 26 });
    await F.text({ id: `txt-f-${s.id}-cap`, x: chip.cx, y: human ? lh + 6 : la + 54, text: s.cap, size: T.fNote, color: T.ink, align: "center" });
    chips.push(chip);
  }
  for (let i = 0; i < chips.length - 1; i += 1) {
    const from = chips[i];
    const to = chips[i + 1];
    const down = seq[i].actor === "human";
    await F.flow(`line-f-step-${i}`, [[from.right + 3, from.cy], [to.cx, from.cy], [to.cx, down ? to.y - 3 : to.bottom + 3]]);
  }
  const modes = ["Direction", "Commitment", "Supply", "Regulation", "Challenge", "Autonomous"];
  await F.text({ id: "txt-f-modes", x: fX + 16, y: la + laneH + 6, text: "Six interaction modes recur", size: T.fNote, bold: true, color: T.ink });
  const mw = (fW - 32 - 8) / 2;
  for (const [i, name] of modes.entries()) {
    const mx = fX + 16 + (i % 2) * (mw + 8);
    const my = la + laneH + 36 + Math.floor(i / 2) * 34;
    const col = i % 2;
    await F.box({ id: `bg-f-mode-c${col}-${i}`, x: mx, y: my, w: mw, h: 28, fill: T.white, stroke: T.hair, sw: 1.5, radius: 14 });
    await F.box({ id: `bg-f-mode-c${col}-${i}-n`, x: mx + 4, y: my + 4, w: 20, h: 20, fill: T.navy, stroke: T.navy, sw: 1, radius: 10, label: String(i + 1),
      extra: `fontSize=15;fontFamily=${T.font};fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;` });
    await F.text({ id: `txt-f-mode-c${col}-${i}`, x: mx + 30, y: my + 3, text: name, size: T.fNote, color: T.ink });
  }

  // ================================================================ return lane
  const laneY = botBottom + 28;
  const label = "Each revision adds sessions and the coding is repeated";
  const pillW = Math.ceil(textWidth(label, T.fBody, true)) + 40;
  const pillX = 640 - pillW / 2;
  await F.box({ id: "bg-return-pill", x: pillX, y: laneY - 20, w: pillW, h: 40, fill: T.white, stroke: T.navy, sw: 2, radius: 20 });
  await F.text({ id: "txt-return", x: 640, y: laneY - 13, text: label, size: T.fBody, bold: true, color: T.navy, align: "center" });
  await F.doc({ id: "return-doc", x: 1222, y: laneY - 21, w: 32, h: 42 });
  await F.line({ id: "line-return-right", pts: [[1216, laneY], [pillX + pillW + 2, laneY]], color: T.navy, width: 3 });
  await F.flow("line-return-left", [[pillX - 2, laneY], [14, laneY], [14, topY + topH / 2], [aX - 2, topY + topH / 2]]);

  const height = laneY + 34;
  F.h = height;
  console.log("canvas", W, "x", height, "| top band bottom", topY + topH, "| bottom band", botY, "to", botBottom);
  const report = await finish({ call, close, file: FILE, w: W, h: height, name: "Figure 1" });
  if (F.warnings.length) console.log("fit warnings:\n" + F.warnings.join("\n"));
  if (report.hard_failure_count) process.exitCode = 1;
} catch (error) {
  console.log("ERROR", error.message);
  close();
}
