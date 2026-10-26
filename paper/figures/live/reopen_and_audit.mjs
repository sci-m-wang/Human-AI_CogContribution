// Patch the page size of a saved live snapshot, then re-open it in the visible draw.io and audit it.
//
//   node paper/figures/live/reopen_and_audit.mjs paper/figures/drawio/fig1_sivia.drawio 1440 1000
//
// The draw.io page format lives in the mxGraphModel attributes. The live snapshot is written
// without them, so draw.io falls back to A4 and the audit reports every object as outside the
// page. Writing the intended size into the model fixes the page, the PNG export and the audit
// at the same time.

import fs from "node:fs";
import { connect } from "./live-client.mjs";
import { summariseAudit } from "./dxlib.mjs";

const file = process.argv[2] ?? "<project>/paper/figures/drawio/fig1_sivia.drawio";
const width = Number(process.argv[3] ?? 1440);
const height = Number(process.argv[4] ?? 1000);

const source = fs.readFileSync(file, "utf8");
if (!source.includes("<mxGraphModel")) throw new Error("mxGraphModel tag not found");
const patched = source.replace(/<mxGraphModel([^>]*)>/, (match, attributes) => {
  const kept = attributes.replace(/\s*page(Width|Height|Scale)?="[^"]*"/g, "");
  return `<mxGraphModel${kept} pageWidth="${width}" pageHeight="${height}" pageScale="1" page="1">`;
});
fs.writeFileSync(file, patched, "utf8");
console.log(`page size written: ${width} x ${height}`);

const { call, close } = await connect({ clear: false, filePath: file });
try {
  await new Promise((resolve) => setTimeout(resolve, Number(process.argv[5] ?? 8000)));
  const status = await call("drawio_live_status", {});
  console.log("status:", String(status).slice(0, 600));
  const audit = await call("drawio_live_audit_figure", { max_findings: 200 });
  const { report } = summariseAudit(audit);
  console.log(`page ${report.page_size.width}x${report.page_size.height} visible=${report.page_size.visible}`);
  console.log(`objects ${JSON.stringify(report.object_counts)}`);
  console.log(`hard ${report.hard_failure_count} warnings ${report.warning_count} passed=${report.passed}`);
  for (const finding of report.findings || []) {
    console.log(`[${finding.severity}] ${finding.category}: ${finding.objects.join(", ")} :: ${finding.evidence}`);
  }
} catch (error) {
  console.log("ERROR", error.message);
} finally {
  close();
}
