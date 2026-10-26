// Blank-space report for the live draw.io figures.
//
// The human review asked for panels without large empty regions. This script measures, for
// every panel, the widest empty horizontal band and the share of the panel area that is
// covered by content, so a hole in the layout is a number instead of an impression.
//
//   node paper/figures/live/check_blanks.mjs paper/figures/drawio/fig1_sivia.drawio

import fs from "node:fs";

const file = process.argv[2];
const xml = fs.readFileSync(file, "utf8");

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

const panels = cells.filter((cell) => /^panel-[a-z]$/.test(cell.id));
for (const panel of panels) {
  const key = panel.id.slice(-1);
  const inside = cells.filter((cell) =>
    cell.id !== panel.id &&
    !cell.id.startsWith(`panel-${key}`) &&
    cell.x >= panel.x && cell.x + cell.w <= panel.x + panel.w &&
    cell.y >= panel.y && cell.y + cell.h <= panel.y + panel.h);
  const inner = { x: panel.x + 12, y: panel.y + 48, w: panel.w - 24, h: panel.h - 60 };
  // Rows of the inner area that carry content.
  const covered = new Uint8Array(inner.h);
  for (const cell of inside) {
    const top = Math.max(inner.y, cell.y);
    const bottom = Math.min(inner.y + inner.h, cell.y + cell.h);
    for (let y = top; y < bottom; y += 1) covered[y - inner.y] = 1;
  }
  let band = 0;
  let run = 0;
  let runStart = inner.y;
  const bands = [];
  for (let y = inner.y; y < inner.y + inner.h; y += 1) {
    if (covered[y - inner.y]) {
      if (run) bands.push([runStart, y, run]);
      band = Math.max(band, run); run = 0;
    } else {
      if (!run) runStart = y;
      run += 1;
    }
  }
  if (run) bands.push([runStart, inner.y + inner.h, run]);
  band = Math.max(band, run);
  const rows = covered.reduce((sum, value) => sum + value, 0);
  const share = Math.round((rows / inner.h) * 100);
  console.log(`panel ${key}: content rows ${rows}/${inner.h} px (${share} %), largest empty band ${band} px`);
  for (const [from, to, size] of bands.filter((b) => b[2] >= 16)) {
    console.log(`   empty ${from} -> ${to} (${size} px)`);
  }
}
