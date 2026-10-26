// Re-open a saved live snapshot in the visible draw.io and audit it (second generation, for dx2 builds).
//
//   node paper/figures/live/reopen2.mjs paper/figures/drawio/fig1_sivia.drawio
//
// The page size is already in the model (finish() in dx2.mjs writes it), so this only reopens and audits.

import { connect } from "./dx2.mjs";

const file = process.argv[2];
const wait = Number(process.argv[3] ?? 8000);
const { call, close } = await connect({ clear: false, filePath: file });
try {
  await new Promise((resolve) => setTimeout(resolve, wait));
  const report = JSON.parse(await call("drawio_live_audit_figure", { max_findings: 300 }));
  console.log(`page ${report.page_size.width}x${report.page_size.height} visible=${report.page_size.visible}`);
  console.log(`objects ${JSON.stringify(report.object_counts)}`);
  console.log(`hard ${report.hard_failure_count} warnings ${report.warning_count} passed=${report.passed}`);
  for (const finding of report.findings || []) console.log(`[${finding.severity}] ${finding.category}: ${finding.objects.join(", ")} :: ${finding.evidence}`);
} catch (error) {
  console.log("ERROR", error.message);
} finally {
  close();
  setTimeout(() => process.exit(0), 500);
}
