// Test how multi-line labels survive the live draw.io path: "\n" versus "<br>".
import { connect } from "file:///<home>/.config/opencode/skills/sivia-figure-workflow/scripts/live-client.mjs";

const { call, close } = await connect();
try {
  await call("drawio_live_add_shape", {
    id: "panel-t",
    x: 0, y: 0, width: 400, height: 300,
    style: "rounded=1;arcSize=4;html=1;fillColor=#FFFFFF;strokeColor=#9FB3C8;strokeWidth=1.5;",
  });
  await call("drawio_live_add_shape", {
    id: "txt-nl",
    x: 20, y: 40, width: 200, height: 60,
    label: "Alpha\nBeta",
    style: "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=22;fontFamily=Helvetica;fontColor=#1F2937;",
  });
  await call("drawio_live_add_shape", {
    id: "txt-br",
    x: 20, y: 140, width: 200, height: 60,
    label: "Alpha<br>Beta",
    style: "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=22;fontFamily=Helvetica;fontColor=#1F2937;",
  });
  await call("drawio_live_save_snapshot", {
    output_path: "<home>/AppData/Local/Temp/opencode/multiline_test.drawio",
    overwrite: true,
  });
  console.log("snapshot written");
} catch (error) {
  console.log("ERROR", error.message);
} finally {
  close();
}
