// Shared helpers for the live Sivia draw.io figure builds (Figures 1 and 2).
//
// The figures are drawn through the Sivia live draw.io MCP tools (drawio_live_*),
// driven from one script per figure so that the script stays the source of the figure.
//
// Text is measured with the Helvetica AFM advance widths. draw.io on Windows maps
// fontFamily=Helvetica to Arial, whose metrics are the same, so measured widths
// match the rendered widths closely enough to size every label cell before drawing.

import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

export const HERE = path.dirname(fileURLToPath(import.meta.url));
export const FIGDIR = path.resolve(HERE, "..");
export const ROOT = path.resolve(FIGDIR, "..", "..");
export const ASSET_DIRS = [
  path.join(FIGDIR, "elements_c", "assets"),
  path.join(FIGDIR, "elements_b", "assets"),
  path.join(FIGDIR, "elements", "assets"),
];

export function assetPath(name) {
  for (const dir of ASSET_DIRS) {
    const candidate = path.join(dir, `${name}.png`);
    if (fs.existsSync(candidate)) return candidate;
  }
  throw new Error(`Missing generated asset: ${name}`);
}

/** Pixel size of a PNG, read from the IHDR chunk. */
export function imageSize(file) {
  const buffer = fs.readFileSync(file);
  if (buffer.readUInt32BE(0) !== 0x89504e47) throw new Error(`Not a PNG file: ${file}`);
  return { w: buffer.readUInt32BE(16), h: buffer.readUInt32BE(20) };
}

// ---------------------------------------------------------------- design tokens
export const T = {
  canvasW: 1440,
  text: "#1F2937",
  muted: "#4B5563",
  faint: "#6B7280",
  header: "#3E6FA3",
  headerText: "#FFFFFF",
  panelFill: "#F4F8FC",
  panelStroke: "#A9BDD1",
  line: "#4E79A7",
  rule: "#C7D4E1",
  card: "#FFFFFF",
  cardStroke: "#9FB3C8",
  type: {
    K: { fill: "#DCEBFA", stroke: "#4E79A7", name: "Knowledge" },
    P: { fill: "#DFF1D8", stroke: "#59A14F", name: "Proposal" },
    D: { fill: "#FCE5CC", stroke: "#E08A1E", name: "Decision" },
    M: { fill: "#E9DDF2", stroke: "#8E6BB0", name: "Metacognition" },
    X: { fill: "#E5E7EB", stroke: "#7B8794", name: "Execution" },
  },
  typeIcon: { K: "knowledge", P: "proposal", D: "decision", M: "metacognition", X: "execution" },
  actorIcon: { human: "human", agent: "primary_agent", sub: "subagents", coderA: "coder_a", coderB: "coder_b" },
  actorStroke: { human: "#4E79A7", agent: "#7B8794", sub: "#3DAA9A", coderA: "#4E79A7", coderB: "#3DAA9A" },
  // font ladder, canvas 1440 px printed at 6.15 in => 0.3075 pt per px
  fPanel: 24,   // 7.4 pt
  fTitle: 22,   // 6.8 pt
  fBody: 21,    // 6.5 pt
  fSmall: 20,   // 6.2 pt
};

const AFM = {
  " ": 278, "!": 278, '"': 355, "#": 556, $: 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
  "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
  ">": 584, "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, _: 556, "`": 333, "{": 334,
  "|": 260, "}": 334, "~": 584, "’": 191, "‘": 191, "“": 333, "”": 333,
  A: 667, B: 667, C: 722, D: 722, E: 667, F: 611, G: 778, H: 722, I: 278, J: 500, K: 667, L: 556,
  M: 833, N: 722, O: 778, P: 667, Q: 778, R: 722, S: 667, T: 611, U: 722, V: 667, W: 944, X: 667,
  Y: 667, Z: 611,
  a: 556, b: 556, c: 500, d: 556, e: 556, f: 278, g: 556, h: 556, i: 222, j: 222, k: 500, l: 222,
  m: 833, n: 556, o: 556, p: 556, q: 556, r: 333, s: 500, t: 278, u: 556, v: 500, w: 722, x: 500,
  y: 500, z: 500,
};
for (let d = 0; d <= 9; d += 1) AFM[String(d)] = 556;

export function textWidth(text, fontSize, bold = false) {
  let units = 0;
  for (const ch of String(text)) units += AFM[ch] ?? 556;
  // Arial Bold is a little wider than Helvetica Bold, so the bold factor is deliberately generous.
  return (units * fontSize) / 1000 * (bold ? 1.09 : 1);
}

export function wrapLines(text, fontSize, maxWidth, bold = false) {
  const out = [];
  for (const paragraph of String(text).split("\n")) {
    const words = paragraph.split(/\s+/).filter(Boolean);
    if (!words.length) { out.push(""); continue; }
    let line = "";
    for (const word of words) {
      const candidate = line ? `${line} ${word}` : word;
      if (line && textWidth(candidate, fontSize, bold) > maxWidth) {
        out.push(line);
        line = word;
      } else {
        line = candidate;
      }
    }
    if (line) out.push(line);
  }
  return out;
}

export function lineHeight(fontSize) {
  return fontSize * 1.22;
}

export function textBlockHeight(text, fontSize, maxWidth, bold = false) {
  const lines = wrapLines(text, fontSize, maxWidth, bold);
  return { lines, height: lines.length * lineHeight(fontSize) };
}

// ---------------------------------------------------------------- figure builder
export class Figure {
  constructor(call, canvasW, canvasH) {
    this.call = call;
    this.w = canvasW;
    this.h = canvasH;
    this.warnings = [];
    this.counter = 0;
  }

  id(prefix) {
    this.counter += 1;
    return `${prefix}-${this.counter}`;
  }

  async shape({ id, x, y, w, h, label = "", style, fill, stroke, fontSize, fontColor, strokeWidth }) {
    let finalStyle = style;
    if (!finalStyle) {
      finalStyle = "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#9FB3C8;strokeWidth=1.5;";
    }
    if (fill) finalStyle = setStyle(finalStyle, "fillColor", fill);
    if (stroke) finalStyle = setStyle(finalStyle, "strokeColor", stroke);
    if (fontSize) finalStyle = setStyle(finalStyle, "fontSize", fontSize);
    if (fontColor) finalStyle = setStyle(finalStyle, "fontColor", fontColor);
    if (strokeWidth !== undefined) finalStyle = setStyle(finalStyle, "strokeWidth", strokeWidth);
    return this.call("drawio_live_add_shape", { id, x, y, width: w, height: h, label, style: finalStyle });
  }

  /** A text cell whose height is computed from the measured text so nothing overflows. */
  async text({ id, x, y, w, text, size = T.fBody, bold = false, color = T.text, align = "left", valign = "middle", minH = 0 }) {
    const inner = w - 8;
    const { lines, height } = textBlockHeight(text, size, inner, bold);
    const h = Math.max(minH, Math.round(height + 6));
    const style = `text;html=1;strokeColor=none;fillColor=none;align=${align};verticalAlign=${valign};whiteSpace=wrap;` +
      `fontSize=${size};fontFamily=Helvetica;fontColor=${color};fontStyle=${bold ? 1 : 0};spacing=0;`;
    await this.shape({ id, x, y, w, h, label: lines.join("\n"), style });
    return { x, y, w, h, lines: lines.length, height };
  }

  async panel({ id, x, y, w, h, title, subtitle = null }) {
    await this.shape({
      id: `panel-${id}`,
      x, y, w, h,
      style: `rounded=1;arcSize=4;html=1;fillColor=${T.panelFill};strokeColor=${T.panelStroke};strokeWidth=1.5;`,
    });
    await this.shape({
      id: `panel-${id}-head`,
      x, y, w, h: 42,
      style: `rounded=1;arcSize=30;html=1;fillColor=${T.header};strokeColor=${T.header};strokeWidth=1;`,
    });
    await this.shape({
      id: `panel-${id}-title`,
      x: x + 14, y: y + 6, w: subtitle ? Math.round(w * 0.5) : w - 28, h: 30,
      label: title,
      style: `text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=${T.fPanel};fontFamily=Helvetica;fontColor=${T.headerText};fontStyle=1;spacing=0;`,
    });
    if (subtitle) {
      await this.shape({
        id: `panel-${id}-subtitle`,
        x: x + Math.round(w * 0.5), y: y + 6, w: Math.round(w * 0.5) - 14, h: 30,
        label: subtitle,
        style: `text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;fontSize=${T.fSmall};fontFamily=Helvetica;fontColor=#D6E6F7;fontStyle=0;spacing=0;`,
      });
    }
  }

  async rule({ id, x1, y1, x2, y2, color = T.rule, width = 1.5, arrow = "none", dashed = false }) {
    const style = `edgeStyle=none;rounded=0;html=1;strokeColor=${color};strokeWidth=${width};endArrow=${arrow};endFill=1;startArrow=none;` +
      (dashed ? "dashed=1;dashPattern=6 4;" : "");
    return this.call("drawio_live_add_line", {
      id, begin_x: x1, begin_y: y1, end_x: x2, end_y: y2, style,
    });
  }

  async polyline({ id, points, color = T.line, width = 3, arrow = "block", dashed = false, startArrow = "none" }) {
    const style = `edgeStyle=none;rounded=0;html=1;strokeColor=${color};strokeWidth=${width};endArrow=${arrow};endFill=1;startArrow=${startArrow};startFill=1;` +
      (dashed ? "dashed=1;dashPattern=6 4;" : "");
    return this.call("drawio_live_add_line", {
      id,
      begin_x: points[0][0], begin_y: points[0][1],
      end_x: points.at(-1)[0], end_y: points.at(-1)[1],
      waypoints: points.slice(1, -1).map(([x, y]) => ({ x, y })),
      style,
    });
  }

  async icon({ id, name, x, y, w, h = null, note = null }) {
    const image = assetPath(name);
    return this.call("drawio_live_add_image", {
      id,
      image_path: image,
      x, y,
      width: w,
      height: h ?? w,
      raster_reason: note ?? `Generated flat illustration of ${name.replace(/_/g, " ")}; no editable draw.io primitive reproduces it.`,
      source_is_tightly_cropped: true,
      atomic_raster_unit: true,
      contains_reconstructable_content: false,
      decomposition_note: `One cut-out icon from a generated sheet (paper/figures/elements_*); the sheet background and every neighbouring icon were removed before insertion.`,
    });
  }

  /** Icon fitted into a box with its aspect preserved and centred. */
  async iconIn({ id, name, x, y, w, h = null, note = null }) {
    const file = assetPath(name);
    const { w: iw, h: ih } = imageSize(file);
    const boxH = h ?? w;
    const scale = Math.min(w / iw, boxH / ih);
    const dw = Math.round(iw * scale);
    const dh = Math.round(ih * scale);
    return this.icon({
      id, name,
      x: Math.round(x + (w - dw) / 2),
      y: Math.round(y + (boxH - dh) / 2),
      w: dw, h: dh, note,
    });
  }

  /** Icon with a fixed width, natural height, standing on a baseline. */
  async iconOnBase({ id, name, x, y, w, note = null }) {
    const file = assetPath(name);
    const { w: iw, h: ih } = imageSize(file);
    const dh = Math.round(w * (ih / iw));
    return this.icon({ id, name, x, y: Math.round(y - dh), w, h: dh, note });
  }

  /** Icon placed inside a square frame, used for actors and type badges. */
  async actorBadge({ id, actor, x, y, size = 44, letter = null, type = null }) {
    const stroke = type ? T.type[type].stroke : T.actorStroke[actor];
    const fill = type ? T.type[type].fill : "#FFFFFF";
    await this.shape({
      id: `bg-${id}`,
      x, y, w: size, h: size,
      style: `rounded=1;arcSize=22;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=2;`,
    });
    const iconName = type ? T.typeIcon[type] : T.actorIcon[actor];
    const inset = type ? Math.round(size * 0.16) : Math.round(size * 0.09);
    await this.icon({ id: `img-${id}`, name: iconName, x: x + inset, y: y + inset, w: size - 2 * inset });
    if (letter) {
      await this.shape({
        id: `txt-${id}-letter`,
        x, y: y + size - 16, w: size, h: 16,
        label: letter,
        style: `text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontSize=${T.fSmall - 4};fontFamily=Helvetica;fontColor=${stroke};fontStyle=1;spacing=0;`,
      });
    }
  }

  /**
   * A type tile: a rounded square in the type colour carrying the type letter.
   * The letter stays crisp at print size, unlike a rasterised type icon.
   */
  async typeTile({ id, type, x, y, size = 44, fontSize = null, letter = null }) {
    const t = T.type[type];
    await this.shape({
      id: `bg-${id}`,
      x, y, w: size, h: size,
      style: `rounded=1;arcSize=18;html=1;fillColor=${t.fill};strokeColor=${t.stroke};strokeWidth=2;`,
    });
    const glyph = letter ?? type;
    await this.shape({
      id: `txt-${id}`,
      x, y, w: size, h: size,
      label: glyph,
      style: `text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=${fontSize ?? Math.round(size * 0.55)};fontFamily=Helvetica;fontColor=${t.stroke};fontStyle=1;spacing=0;`,
    });
  }

  /** Warn when a word is wider than the cell that must hold it. */
  fit(id, text, size, width, bold = false) {
    for (const word of String(text).split(/\s+/).filter(Boolean)) {
      if (textWidth(word, size, bold) > width) {
        this.warnings.push(`${id}: word "${word}" needs ${Math.round(textWidth(word, size, bold))} px, cell is ${width} px`);
      }
    }
  }

  async letterBadge({ id, letter, x, y, size = 34, type = null, fontSize = T.fBody }) {
    const t = type ? T.type[type] : { fill: "#6B87A8", stroke: "#6B87A8" };
    await this.shape({
      id: `bg-${id}`,
      x, y, w: size, h: size,
      style: `rounded=1;arcSize=50;html=1;fillColor=${t.fill};strokeColor=${t.stroke};strokeWidth=2;`,
    });
    await this.shape({
      id: `txt-${id}`,
      x, y, w: size, h: size,
      label: letter,
      style: `text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=${fontSize};fontFamily=Helvetica;fontColor=${T.text};fontStyle=1;spacing=0;`,
    });
  }

  /**
   * A message bubble: a plain rounded rectangle whose tail points at the speaker on the side.
   *
   * The draw.io callout shape was dropped because its wavy speech-bubble outline and its
   * downward pointer read as an odd shape in print. The tail is a triangle drawn first and
   * covered by the body, so the outline of the body hides the base edge of the triangle.
   */
  async bubble({ id, actor, x, y, w, h = null, text, size = T.fBody, tail = "left" }) {
    const human = actor === "human";
    const fill = human ? "#CFE3F7" : "#E9ECF0";
    const stroke = human ? "#4E79A7" : "#7B8794";
    const inner = w - 24;
    const { lines, height } = textBlockHeight(text, size, inner);
    const boxH = h ?? Math.max(36, Math.round(height + 12));
    if (h && height + 6 > h) this.warnings.push(`bubble ${id}: text needs ${Math.round(height + 6)} px, box is ${h} px`);
    if (tail === "left") {
      await this.shape({
        id: `bg-${id}-tail`,
        x: x - 10, y: Math.round(y + boxH / 2 - 9), w: 12, h: 18,
        style: `shape=triangle;direction=west;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.8;`,
      });
    } else if (tail === "right") {
      await this.shape({
        id: `bg-${id}-tail`,
        x: x + w - 2, y: Math.round(y + boxH / 2 - 9), w: 12, h: 18,
        style: `shape=triangle;direction=east;html=1;fillColor=${fill};strokeColor=${stroke};strokeWidth=1.8;`,
      });
    }
    const style = `rounded=1;arcSize=18;html=1;whiteSpace=wrap;` +
      `fillColor=${fill};strokeColor=${stroke};strokeWidth=1.8;fontSize=${size};fontFamily=Helvetica;fontColor=${T.text};` +
      `align=left;verticalAlign=middle;spacingLeft=12;spacingRight=10;spacingTop=4;spacingBottom=4;`;
    return this.shape({ id, x, y, w, h: boxH, label: lines.join("\n"), style });
  }

  /** Height a bubble needs for its text, so rows can be laid out without overlap. */
  bubbleHeight(text, w, size = T.fBody) {
    const { height } = textBlockHeight(text, size, w - 24);
    return Math.max(36, Math.round(height + 12));
  }
}

export function setStyle(style, key, value) {
  if (value === undefined || value === null) return style;
  const entries = style.split(";").filter(Boolean);
  const kept = entries.filter((entry) => entry.split("=")[0] !== key);
  kept.push(`${key}=${value}`);
  return `${kept.join(";")};`;
}

/** Compact audit summary so the raw JSON stays readable in the transcript. */
export function summariseAudit(json) {
  const report = typeof json === "string" ? JSON.parse(json) : json;
  const byCategory = new Map();
  for (const finding of report.findings || []) {
    const key = `${finding.severity}:${finding.category}`;
    if (!byCategory.has(key)) byCategory.set(key, []);
    byCategory.get(key).push(finding);
  }
  const lines = [
    `page ${report.page_size.width}x${report.page_size.height} visible=${report.page_size.visible}`,
    `objects ${JSON.stringify(report.object_counts)}`,
    `hard ${report.hard_failure_count} warnings ${report.warning_count} passed=${report.passed}`,
  ];
  for (const [key, items] of byCategory) {
    lines.push(`${key} x${items.length}`);
    for (const item of items.slice(0, 12)) {
      lines.push(`   ${item.objects.join(",")} :: ${item.evidence}`);
    }
    if (items.length > 12) lines.push(`   ... ${items.length - 12} more`);
  }
  return { text: lines.join("\n"), report };
}
