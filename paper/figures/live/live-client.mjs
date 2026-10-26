// Project-local copy of the Sivia live-client, with one addition: the launch can open an
// existing .drawio file, which is how a figure is re-opened after its page size was patched.
//
//   import { connect } from "./live-client.mjs";
//   const { call, close } = await connect({ filePath: "C:/.../fig1_sivia.drawio" });
//
// Original: <home>/.config/opencode/skills/sivia-figure-workflow/scripts/live-client.mjs
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import { createInterface } from "node:readline";

export const SIVIA_ROOT = process.env.SIVIA_ROOT || path.join(os.homedir(), "Tools", "Sivia");

export async function connect({ clear = true, filePath = null, port = 9333, sivia = SIVIA_ROOT } = {}) {
  const child = spawn(process.execPath, [path.join(sivia, "scripts", "live-server.mjs")], {
    stdio: ["pipe", "pipe", "inherit"],
    windowsHide: true,
    env: { ...process.env, SIVIA_HOME: process.env.SIVIA_HOME || path.join(os.homedir(), ".sivia") },
  });
  const lines = createInterface({ input: child.stdout });
  const pending = new Map();
  let nextId = 1;
  lines.on("line", (line) => {
    let message;
    try { message = JSON.parse(line); } catch { return; }
    pending.get(message.id)?.(message);
  });
  const rpc = (method, params) => new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, (message) => (message.error ? reject(new Error(JSON.stringify(message.error))) : resolve(message.result)));
    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`);
  });
  const call = async (name, args = {}) => {
    const result = await rpc("tools/call", { name, arguments: args });
    const text = (result.content ?? []).filter((item) => item.type === "text").map((item) => item.text).join("\n");
    if (result.isError) throw new Error(`${name} ${JSON.stringify(args).slice(0, 200)} -> ${text.slice(0, 500)}`);
    return text;
  };
  await rpc("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "sivia-script", version: "1" } });
  child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" })}\n`);
  const launch = { include_screenshot: false, maximize: false, step_delay_ms: 0 };
  if (filePath) { launch.file_path = filePath; launch.port = port; }
  await call("drawio_live_launch", launch);
  if (clear) await call("drawio_live_clear", { confirm: true });
  return { call, close: () => child.kill() };
}
