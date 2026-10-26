// Probe of the Sivia live draw.io tools: callout shape, text shape, image cell, audit.
import path from "node:path";
import { fileURLToPath } from "node:url";
import { connect } from "file:///<home>/.config/opencode/skills/sivia-figure-workflow/scripts/live-client.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const icon = path.join(root, "elements_c", "assets", "human.png");

const { call, close } = await connect();
const out = [];
try {
  await call("drawio_live_add_shape", {
    id: "panel-a",
    x: 0, y: 0, width: 320, height: 220,
    style: "rounded=1;arcSize=6;html=1;fillColor=#F4F8FC;strokeColor=#A9BDD1;strokeWidth=1.5;",
  });
  out.push(await call("drawio_live_add_shape", {
    id: "bub-1",
    x: 30, y: 40, width: 240, height: 64,
    label: "Read the originals.",
    style: "shape=callout;perimeter=calloutPerimeter;rounded=1;arcSize=18;whiteSpace=wrap;html=1;size=10;position=0.12;base=20;fillColor=#CFE3F7;strokeColor=#4E79A7;strokeWidth=1.8;fontSize=21;fontFamily=Helvetica;fontColor=#1F2937;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=6;",
  }));
  out.push(await call("drawio_live_add_shape", {
    id: "txt-1",
    x: 30, y: 140, width: 240, height: 30,
    label: "One model response is one unit",
    style: "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=21;fontFamily=Helvetica;fontColor=#1F2937;spacing=0;",
  }));
  out.push(await call("drawio_live_add_image", {
    id: "img-1",
    image_path: icon,
    x: 250, y: 20, width: 48, height: 48,
    raster_reason: "Illustrated human researcher icon has no editable draw.io primitive.",
    source_is_tightly_cropped: true,
    atomic_raster_unit: true,
    contains_reconstructable_content: false,
    decomposition_note: "Single cut-out icon from a generated sheet; all surrounding sheet background removed.",
  }));
  const audit = await call("drawio_live_audit_figure", { max_findings: 50 });
  out.push(audit);
} catch (error) {
  out.push(`ERROR: ${error.message}`);
} finally {
  close();
}
console.log(out.join("\n---\n"));
