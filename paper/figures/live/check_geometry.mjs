// Geometry self-check for the live draw.io figures.
//
// The live audit covers text overflow, connector paths and page bounds, but it does not
// report two shapes that overlap each other. This script parses the saved uncompressed
// .drawio file and reports overlapping cells, so a layout mistake is caught before the
// figure is handed to the human reviewer.
//
//   node paper/figures/live/check_geometry.mjs paper/figures/drawio/fig1_sivia.drawio
//
// Allowed overlaps: a panel with its own head bar, a type tile with its letter cell, and
// a bubble with the triangle tail that forms its pointer (the body hides the tail base).

import fs from "node:fs";

const file = process.argv[2];
if (!file) {
  console.log("usage: node check_geometry.mjs <file.drawio>");
  process.exit(1);
}
const xml = fs.readFileSync(file, "utf8");

// The file is split on the opening tags, because an embedded image cell wraps its vertex in
// an outer cell whose style carries the whole base64 payload.
const cells = [];
const chunks = xml.split("<mxCell");
for (const chunk of chunks.slice(1)) {
  const tag = chunk.slice(0, chunk.indexOf(">") + 1);
  const id = tag.match(/\bid="([^"]+)"/)?.[1];
  if (!id) continue;
  const geometry = chunk.match(/<mxGeometry\b([^>]*)/)?.[1];
  if (!geometry) continue;
  const attr = (name) => {
    const found = geometry.match(new RegExp(`${name}="([^"]+)"`));
    return found ? Number(found[1]) : 0;
  };
  cells.push({ id, x: attr("x"), y: attr("y"), w: attr("width"), h: attr("height") });
}

const isText = (cell) => cell.id.startsWith("txt-");
const isPanel = (cell) => cell.id.startsWith("panel-");
const isTile = (cell) => /^(bg|txt)-(c|d|e|f|legend)-[a-z-]*[kpdmp]$/i.test(cell.id);
const isTail = (cell) => cell.id.endsWith("-tail");
const isPair = (a, b) =>
  (isTile(a) && isTile(b) && a.id.replace(/^(bg|txt)-/, "") === b.id.replace(/^(bg|txt)-/, "")) ||
  (isTail(a) && !isTail(b) && b.id === a.id.replace(/-tail$/, "")) ||
  (isTail(b) && !isTail(a) && a.id === b.id.replace(/-tail$/, ""));

const overlap = (a, b) => {
  const dx = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
  const dy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
  return dx > 2 && dy > 2 ? Math.min(dx, dy) : 0;
};

const contains = (outer, inner) =>
  outer.x <= inner.x + 1 && outer.y <= inner.y + 1 &&
  outer.x + outer.w >= inner.x + inner.w - 1 && outer.y + outer.h >= inner.y + inner.h - 1;

let problems = 0;
for (let i = 0; i < cells.length; i += 1) {
  for (let j = i + 1; j < cells.length; j += 1) {
    const a = cells[i];
    const b = cells[j];
    if (isPanel(a) || isPanel(b)) continue;
    if (isPair(a, b)) continue;
    // A container that fully holds its content (a card with a bubble, a panel with a label)
    // is a normal composite, not a collision.
    if (contains(a, b) || contains(b, a)) continue;
    const amount = overlap(a, b);
    if (!amount) continue;
    // A label cell sitting on a filled shape is a normal composite (a tile letter, a
    // headline on a card). Only report the pairs where two different payloads collide.
    if (isText(a) || isText(b)) continue;
    problems += 1;
    console.log(`overlap ${a.id} [${a.x},${a.y},${a.w},${a.h}] <-> ${b.id} [${b.x},${b.y},${b.w},${b.h}] by ${amount} px`);
  }
}

const bounds = cells.reduce((acc, cell) => ({
  x0: Math.min(acc.x0, cell.x),
  y0: Math.min(acc.y0, cell.y),
  x1: Math.max(acc.x1, cell.x + cell.w),
  y1: Math.max(acc.y1, cell.y + cell.h),
}), { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity });
console.log(`cells ${cells.length} bounds ${bounds.x0},${bounds.y0} -> ${bounds.x1},${bounds.y1}`);
console.log(problems ? `PROBLEMS ${problems}` : "no payload overlap");
