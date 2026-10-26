// Drawing library, second generation, for the live Sivia draw.io builds of Figures 1 and 2.
//
// What changed against dxlib.mjs (archived in archive/dxlib_v1.mjs), after the human review I036:
//   - arrowheads are passed through the end_arrow argument. drawio_live_add_line forces
//     end_arrow to "none" unless the argument is given, so an endArrow written into the style
//     string was silently dropped and no arrow carried a head;
//   - text widths come from the Helvetica and Helvetica-Bold AFM tables (Arial has the same
//     advance widths), instead of the regular table multiplied by an estimated bold factor;
//   - text cells are tight to their text, so the overlap check can look at text cells too;
//   - one visual system: neutral ink for who speaks, colour only for the four contribution
//     types, light washes instead of header bands, one family of avatars, no clip-art icons.

import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import { connect } from "./live-client.mjs";

export const HERE = path.dirname(fileURLToPath(import.meta.url));
export const FIGDIR = path.resolve(HERE, "..");
export const ASSETS = path.join(HERE, "assets_small");
export const ROOT = path.resolve(FIGDIR, "..", "..");

// ---------------------------------------------------------------- design tokens
export const T = {
  font: "Arial",
  ink: "#1F2A37",
  soft: "#4B5563",
  muted: "#6B7280",
  hair: "#D5DBE3",
  wash: "#F3F5F8",
  white: "#FFFFFF",
  navy: "#25446B",
  navyTint: "#E4ECF6",
  slate: "#6F7A89",
  slateTint: "#EEF0F4",
  // Colour carries the contribution type only (Okabe-Ito based, readable without hue).
  type: {
    K: { fill: "#DCEBF6", stroke: "#0072B2", ink: "#004F7D", name: "Knowledge" },
    P: { fill: "#D9F0E7", stroke: "#009E73", ink: "#006548", name: "Proposal" },
    D: { fill: "#FCEBCB", stroke: "#D98A00", ink: "#835300", name: "Decision" },
    M: { fill: "#F3DEEB", stroke: "#B5568F", ink: "#7A3060", name: "Metacognition" },
    X: { fill: "#ECEEF1", stroke: "#8A94A3", ink: "#566070", name: "Execution" },
  },
  coderA: "#374151",
  coderB: "#A3ABB7",
  // type ladder on a 1280 px canvas printed at 6.15 in, so 1 px = 0.346 pt
  fTitle: 24, // 8.3 pt
  fBody: 20,  // 6.9 pt
  fNote: 18,  // 6.2 pt
};

// ---------------------------------------------------------------- text metrics (AFM, Helvetica = Arial)
const REG = {
  " ": 278, "!": 278, '"': 355, "#": 556, $: 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
  "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
  ">": 584, "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, _: 556, "`": 333, "{": 334,
  "|": 260, "}": 334, "~": 584, "\u2019": 222, "\u2018": 222, "\u201C": 333, "\u201D": 333,
  A: 667, B: 667, C: 722, D: 722, E: 667, F: 611, G: 778, H: 722, I: 278, J: 500, K: 667, L: 556,
  M: 833, N: 722, O: 778, P: 667, Q: 778, R: 722, S: 667, T: 611, U: 722, V: 667, W: 944, X: 667,
  Y: 667, Z: 611,
  a: 556, b: 556, c: 500, d: 556, e: 556, f: 278, g: 556, h: 556, i: 222, j: 222, k: 500, l: 222,
  m: 833, n: 556, o: 556, p: 556, q: 556, r: 333, s: 500, t: 278, u: 556, v: 500, w: 722, x: 500,
  y: 500, z: 500,
};
const BOLD = {
  " ": 278, "!": 333, '"': 474, "#": 556, $: 556, "%": 889, "&": 722, "'": 238, "(": 333, ")": 333,
  "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 333, ";": 333, "<": 584, "=": 584,
  ">": 584, "?": 611, "@": 975, "[": 333, "\\": 278, "]": 333, "^": 584, _: 556, "`": 333, "{": 389,
  "|": 280, "}": 389, "~": 584, "\u2019": 278, "\u2018": 278, "\u201C": 500, "\u201D": 500,
  A: 722, B: 722, C: 722, D: 722, E: 667, F: 611, G: 778, H: 722, I: 278, J: 556, K: 722, L: 611,
  M: 833, N: 722, O: 778, P: 667, Q: 778, R: 722, S: 667, T: 611, U: 722, V: 667, W: 944, X: 667,
  Y: 667, Z: 611,
  a: 556, b: 611, c: 556, d: 611, e: 556, f: 333, g: 611, h: 611, i: 278, j: 278, k: 556, l: 278,
  m: 889, n: 611, o: 611, p: 611, q: 611, r: 389, s: 556, t: 333, u: 611, v: 556, w: 778, x: 556,
  y: 556, z: 500,
};
for (let d = 0; d <= 9; d += 1) { REG[String(d)] = 556; BOLD[String(d)] = 556; }

export function textWidth(text, size, bold = false) {
  const table = bold ? BOLD : REG;
  let units = 0;
  for (const ch of String(text)) units += table[ch] ?? 556;
  return (units * size) / 1000;
}

export function wrapLines(text, size, maxWidth, bold = false) {
  const out = [];
  for (const paragraph of String(text).split("\n")) {
    const words = paragraph.split(/\s+/).filter(Boolean);
    if (!words.length) { out.push(""); continue; }
    let line = "";
    for (const word of words) {
      const candidate = line ? `${line} ${word}` : word;
      if (line && textWidth(candidate, size, bold) > maxWidth) { out.push(line); line = word; } else { line = candidate; }
    }
    if (line) out.push(line);
  }
  return out;
}

export const LINE = 1.2;
const r = (value) => Math.round(value);

function setStyle(style, key, value) {
  if (value === undefined || value === null) return style;
  const kept = style.split(";").filter(Boolean).filter((entry) => entry.split("=")[0] !== key);
  kept.push(`${key}=${value}`);
  return `${kept.join(";")};`;
}

export function imageSize(file) {
  const buffer = fs.readFileSync(file);
  return { w: buffer.readUInt32BE(16), h: buffer.readUInt32BE(20) };
}

// ---------------------------------------------------------------- the figure builder
export class Figure {
  constructor(call, w, h) {
    this.call = call;
    this.w = w;
    this.h = h;
    this.warnings = [];
  }

  async shape({ id, x, y, w, h, label = "", style }) {
    return this.call("drawio_live_add_shape", { id, x: r(x), y: r(y), width: r(w), height: r(h), label, style });
  }

  /**
   * A text cell that is tight to its text. `x` is the left edge, the centre or the right edge
   * depending on `align`. Lines are broken by the caller or by `maxW`; the cell never wraps.
   */
  async text({ id, x, y, text, size = T.fBody, bold = false, color = T.ink, align = "left", maxW = null, minH = 0 }) {
    const lines = maxW ? wrapLines(text, size, maxW, bold) : String(text).split("\n");
    const widest = Math.max(...lines.map((line) => textWidth(line, size, bold)));
    const w = Math.ceil(widest * 1.02) + 6;
    const h = Math.max(minH, Math.ceil(lines.length * size * LINE) + 4);
    const left = align === "left" ? x : align === "center" ? x - w / 2 : x - w;
    const style = `text;html=1;strokeColor=none;fillColor=none;align=${align};verticalAlign=middle;whiteSpace=nowrap;` +
      `fontSize=${size};fontFamily=${T.font};fontColor=${color};fontStyle=${bold ? 1 : 0};spacing=0;spacingLeft=0;spacingRight=0;`;
    await this.shape({ id, x: left, y, w, h, label: lines.join("\n"), style });
    return { x: r(left), y, w, h, right: r(left + w), bottom: y + h, lines: lines.length, widest };
  }

  async box({ id, x, y, w, h, fill = T.white, stroke = T.hair, sw = 1.5, radius = 10, dashed = false, label = "", extra = "" }) {
    const style = `rounded=1;absoluteArcSize=1;arcSize=${radius};html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=${sw};` +
      (dashed ? "dashed=1;dashPattern=6 4;" : "") + extra;
    return this.shape({ id, x, y, w, h, label, style });
  }

  async line({ id, pts, color = T.hair, width = 1.5, dashed = false, head = "none", tail = "none", clearance = 0 }) {
    const style = "edgeStyle=none;rounded=0;html=1;endFill=1;startFill=1;endSize=5;startSize=5;" + (dashed ? "dashPattern=6 4;" : "");
    return this.call("drawio_live_add_line", {
      id,
      begin_x: r(pts[0][0]), begin_y: r(pts[0][1]),
      end_x: r(pts.at(-1)[0]), end_y: r(pts.at(-1)[1]),
      waypoints: pts.slice(1, -1).map(([x, y]) => ({ x: r(x), y: r(y) })),
      color, width, dashed,
      end_arrow: head, start_arrow: tail,
      end_clearance: clearance,
      style,
    });
  }

  /** Primary flow arrow: navy, 3 px, closed head. */
  async flow(id, pts, extra = {}) {
    return this.line({ id, pts, color: T.navy, width: 3, head: "block", ...extra });
  }

  /** Secondary relation arrow: grey, 2 px, open head. */
  async relate(id, pts, extra = {}) {
    return this.line({ id, pts, color: T.muted, width: 2, head: "classic", ...extra });
  }

  /** Panel: a light wash, a lettered badge, a bold title and a hairline under the header. */
  async panel({ id, letter, title, x, y, w, h, note = null }) {
    await this.box({ id: `panel-${id}`, x, y, w, h, fill: T.wash, stroke: T.wash, sw: 1, radius: 14 });
    await this.box({ id: `bg-${id}-letter`, x: x + 14, y: y + 11, w: 28, h: 28, fill: T.navy, stroke: T.navy, sw: 1, radius: 8, label: letter,
      extra: `fontSize=${T.fBody};fontFamily=${T.font};fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;` });
    await this.text({ id: `txt-${id}-title`, x: x + 52, y: y + 10, text: title, size: T.fTitle, bold: true, color: T.ink });
    if (note) await this.text({ id: `txt-${id}-note`, x: x + w - 16, y: y + 14, text: note, size: T.fNote, color: T.muted, align: "right" });
    await this.line({ id: `line-${id}-head`, pts: [[x + 14, y + 50], [x + w - 14, y + 50]], color: T.hair, width: 1.5 });
    return { x, y, w, h, top: y + 62, left: x + 16, right: x + w - 16 };
  }

  /** Contribution type tile: a rounded square carrying the type letter. */
  async tile({ id, type, x, y, s = 44, fs = null, dim = false }) {
    const t = T.type[type];
    const size = fs ?? Math.round(s * 0.52);
    return this.box({
      id, x, y, w: s, h: s, fill: dim ? T.white : t.fill, stroke: dim ? T.hair : t.stroke, sw: s >= 40 ? 2 : 1.75, radius: Math.round(s * 0.22), label: type,
      extra: `fontSize=${size};fontFamily=${T.font};fontColor=${dim ? T.hair : t.ink};fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;`,
    });
  }

  /** Actor avatar: a tinted disc with the actor's illustration on it. */
  async avatar({ id, kind, x, y, d = 40 }) {
    const human = kind === "human";
    const sub = kind === "sub";
    const asset = { human: "human", agent: "primary_agent", sub: "subagents", coderA: "coder_a", coderB: "coder_b" }[kind];
    const stroke = human ? T.navy : kind === "coderA" ? T.coderA : kind === "coderB" ? T.coderB : T.slate;
    const fill = human ? T.navyTint : T.slateTint;
    const wDisc = sub ? Math.round(d * 1.45) : d;
    if (sub) await this.box({ id: `bg-${id}`, x, y, w: wDisc, h: d, fill, stroke, sw: 1.75, radius: Math.round(d / 2) });
    else await this.shape({ id: `bg-${id}`, x, y, w: d, h: d, style: `ellipse;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.75;` });
    const file = path.join(ASSETS, `${asset}.png`);
    const { w: iw, h: ih } = imageSize(file);
    const room = d * (sub ? 0.78 : 0.74);
    const scale = Math.min((sub ? wDisc * 0.84 : room) / iw, room / ih);
    const dw = r(iw * scale);
    const dh = r(ih * scale);
    await this.call("drawio_live_add_image", {
      id: `img-${id}`, image_path: file,
      x: r(x + (wDisc - dw) / 2), y: r(y + (d - dh) / 2 + (sub ? 0 : d * 0.02)), width: dw, height: dh,
      raster_reason: `Generated flat illustration of the ${kind} actor; no draw.io primitive reproduces a character.`,
      source_is_tightly_cropped: true, atomic_raster_unit: true, contains_reconstructable_content: false,
      decomposition_note: "One cut-out character from a generated sheet (paper/figures/elements_*); background and neighbours removed, copy reduced to 320 px.",
    });
    return { x, y, w: wDisc, h: d, right: x + wDisc, bottom: y + d };
  }

  /** A unit token: who acted (avatar) and what type it carries (one or two tiles) in a pill. */
  async chip({ id, actor, types, x, y, h = 44, ts = 30 }) {
    const human = actor === "human";
    const d = h - 10;
    const w = 8 + d + 8 + types.length * ts + (types.length - 1) * 4 + 8;
    await this.box({ id: `bg-${id}`, x, y, w, h, fill: T.white, stroke: human ? T.navy : T.slate, sw: 1.75, radius: Math.round(h / 2) });
    await this.avatar({ id: `${id}-who`, kind: actor, x: x + 6, y: y + 5, d });
    for (const [i, type] of types.entries()) {
      await this.tile({ id: `${id}-t-${type.toLowerCase()}`, type, x: x + 6 + d + 8 + i * (ts + 4), y: y + (h - ts) / 2, s: ts, fs: 18 });
    }
    return { x, y, w, h, right: x + w, bottom: y + h, cx: x + w / 2, cy: y + h / 2 };
  }

  /**
   * A message bubble: a rounded body with a wedge tail on the side of its speaker. The tail is
   * drawn first, so the body outline hides the wedge base.
   */
  async bubble({ id, actor, x, y, w, text, size = T.fNote, tail = "left", minH = 0 }) {
    const human = actor === "human";
    const fill = human ? T.navyTint : T.slateTint;
    const stroke = human ? T.navy : T.slate;
    const lines = wrapLines(text, size, (w - 22) / 1.04);
    const h = Math.max(minH, Math.ceil(lines.length * size * LINE) + 16);
    const ty = y + Math.min(18, Math.round(h / 2)) - 9;
    if (tail === "left") {
      await this.shape({ id: `bg-${id}-tail`, x: x - 11, y: ty, w: 14, h: 18, style: `shape=triangle;direction=west;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.5;` });
    } else if (tail === "right") {
      await this.shape({ id: `bg-${id}-tail`, x: x + w - 3, y: ty, w: 14, h: 18, style: `shape=triangle;direction=east;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.5;` });
    }
    await this.box({
      id, x, y, w, h, fill, stroke, sw: 1.5, radius: 14, label: lines.join("\n"),
      extra: `fontSize=${size};fontFamily=${T.font};fontColor=${T.ink};align=left;verticalAlign=middle;whiteSpace=nowrap;spacingLeft=11;spacingRight=8;spacingTop=2;spacingBottom=2;`,
    });
    return { x, y, w, h, right: x + w, bottom: y + h, cy: y + h / 2 };
  }

  /** Height a bubble will have, so a stack can be laid out before it is drawn. */
  bubbleHeight(text, w, size = T.fNote, minH = 0) {
    const lines = wrapLines(text, size, (w - 22) / 1.04);
    return Math.max(minH, Math.ceil(lines.length * size * LINE) + 16);
  }

  /** Vector glyphs, so no raster icon is needed for a check or a cross. */
  async mark({ id, kind, cx, cy, d = 30 }) {
    const color = kind === "check" ? "#2E8B57" : "#C0504D";
    const label = kind === "cross" ? "\u00D7" : "";
    await this.shape({
      id: `bg-${id}`, x: cx - d / 2, y: cy - d / 2, w: d, h: d, label,
      style: `ellipse;html=1;fillColor=${color};strokeColor=${color};strokeWidth=1;fontSize=${Math.round(d * 0.7)};fontFamily=${T.font};fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;whiteSpace=nowrap;spacing=0;spacingBottom=2;`,
    });
    if (kind === "check") {
      const u = d / 30;
      await this.line({ id: `line-${id}-tick`, pts: [[cx - 7 * u, cy + 0.5 * u], [cx - 2 * u, cy + 6 * u], [cx + 8 * u, cy - 6 * u]], color: "#FFFFFF", width: 3 });
    }
  }

  /** A document glyph with text rows, built only from native shapes (the rows are thin bars, not lines). */
  async doc({ id, x, y, w = 34, h = 42, fill = T.white, stroke = T.navy, lines = 3 }) {
    await this.shape({ id, x, y, w, h, style: `shape=note;size=10;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.75;backgroundOutline=1;` });
    for (let i = 0; i < lines; i += 1) {
      const yy = y + 15 + i * 8;
      const width = w - 14 - (i === lines - 1 ? 8 : 0);
      await this.box({ id: `bg-${id}-row-${["a", "b", "c", "d"][i]}`, x: x + 7, y: yy, w: width, h: 3, fill: stroke, stroke, sw: 0.5, radius: 1 });
    }
  }

  /** The small grey gear used for a tool step. */
  async gear({ id, x, y, s = 24 }) {
    const file = path.join(ASSETS, "gear_grey.png");
    return this.call("drawio_live_add_image", {
      id, image_path: file, x: r(x), y: r(y), width: s, height: s,
      raster_reason: "Generated flat grey gear; no draw.io primitive reproduces it.",
      source_is_tightly_cropped: true, atomic_raster_unit: true, contains_reconstructable_content: false,
      decomposition_note: "One cut-out gear from a generated sheet; reduced to 320 px.",
    });
  }

  fit(id, text, size, width, bold = false) {
    for (const word of String(text).split(/\s+/).filter(Boolean)) {
      if (textWidth(word, size, bold) > width) this.warnings.push(`${id}: word "${word}" needs ${Math.round(textWidth(word, size, bold))} px, room is ${width} px`);
    }
  }
}

// ---------------------------------------------------------------- finish: save, patch the page, reopen, audit
export function summariseAudit(json) {
  const report = typeof json === "string" ? JSON.parse(json) : json;
  return report;
}

/**
 * Save the live canvas, write the page size into the model (a fresh snapshot carries none, so
 * draw.io falls back to A4 and the audit flags everything), reopen the file and audit it.
 */
export async function finish({ call, close, file, w, h, name }) {
  await call("drawio_live_save_snapshot", { output_path: file, page_name: name, overwrite: true });
  close();
  const source = fs.readFileSync(file, "utf8");
  const patched = source.replace(/<mxGraphModel([^>]*)>/, (match, attributes) => {
    const kept = attributes.replace(/\s*(page(Width|Height|Scale)?|background)="[^"]*"/g, "");
    return `<mxGraphModel${kept} pageWidth="${w}" pageHeight="${h}" pageScale="1" page="1" background="#FFFFFF">`;
  });
  fs.writeFileSync(file, patched, "utf8");
  const again = await connect({ clear: false, filePath: file });
  try {
    await new Promise((resolve) => setTimeout(resolve, 7000));
    const report = summariseAudit(await again.call("drawio_live_audit_figure", { max_findings: 300 }));
    console.log(`page ${report.page_size.width}x${report.page_size.height} visible=${report.page_size.visible}`);
    console.log(`objects ${JSON.stringify(report.object_counts)}`);
    console.log(`hard ${report.hard_failure_count} warnings ${report.warning_count} passed=${report.passed}`);
    for (const finding of report.findings || []) console.log(`[${finding.severity}] ${finding.category}: ${finding.objects.join(", ")} :: ${finding.evidence}`);
    return report;
  } finally {
    again.close();
  }
}

export { connect };
