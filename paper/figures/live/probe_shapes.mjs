// List the registered draw.io shapes that could replace clip-art icons with native vector glyphs.
import { connect } from "./live-client.mjs";

const { call, close } = await connect({ clear: true });
try {
  const raw = await call("drawio_live_get_capabilities", { include_registered_edge_styles: true, include_registered_markers: true, include_registered_shapes: true });
  const data = JSON.parse(raw);
  const shapes = (data.registered_shapes || data.shapes || data.registeredShapes || []).map((s) => (typeof s === "string" ? s : s.name));
  console.log("keys:", Object.keys(data).join(", "));
  console.log("shape count:", shapes.length);
  const pick = (re) => shapes.filter((s) => re.test(s)).slice(0, 40);
  console.log("gear:", pick(/gear|cog/i).join(" | "));
  console.log("curly/brace:", pick(/curly|brace|bracket/i).join(" | "));
  console.log("note/doc:", pick(/^(note|document|card|folder)|document|note$/i).join(" | "));
  console.log("tick/check/cross:", pick(/tick|check|cross|xmark|x_mark/i).join(" | "));
  console.log("arrows:", pick(/arrow/i).join(" | "));
  console.log("markers:", JSON.stringify(data.markers || data.registered_markers || data.edge_markers || []).slice(0, 400));
} catch (error) {
  console.log("ERROR", error.message);
} finally {
  close();
}
