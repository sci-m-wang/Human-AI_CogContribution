// Print the geometry of the cells whose id starts with a prefix.
//
//   node paper/figures/live/list_cells.mjs paper/figures/drawio/fig1_sivia.drawio txt-c-

import fs from "node:fs";

const [file, prefix = ""] = process.argv.slice(2);
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
for (const cell of cells.filter((c) => c.id.startsWith(prefix)).sort((a, b) => a.y - b.y || a.x - b.x)) {
  console.log(`${cell.id.padEnd(24)} x ${String(cell.x).padStart(4)} y ${String(cell.y).padStart(4)} w ${String(cell.w).padStart(4)} h ${String(cell.h).padStart(3)}  -> ${cell.y + cell.h}`);
}
