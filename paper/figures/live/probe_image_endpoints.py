"""Probe every image endpoint that the local .env files point at.

For each candidate URL and model name one small image is requested. Only the status, the
elapsed time and the byte count are printed, never the key. The first success is written to
disk so the result can be inspected.
Usage: python probe_image_endpoints.py <env-file> [outfile]
"""
import base64
import json
import sys
import time
import urllib.error
import urllib.request

PROMPT = "A single flat grey gear icon with a thin dark outline, centred on a plain white background, minimal technical illustration, no text."


def load_env(path):
    values = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def try_url(url, body_obj, key, label, out_path):
    body = json.dumps(body_obj).encode()
    headers = {"api-key": key, "Content-Type": "application/json"}
    start = time.time()
    try:
        response = json.load(urllib.request.urlopen(urllib.request.Request(url, data=body, headers=headers), timeout=600))
    except urllib.error.HTTPError as error:
        print(f"{label:58s} -> HTTP {error.code} {error.read()[:200].decode('utf-8', 'replace')}")
        return False
    except Exception as error:  # noqa: BLE001
        print(f"{label:58s} -> ERR {type(error).__name__}")
        return False
    payload = (response.get("data") or [{}])[0]
    if "b64_json" in payload:
        blob = base64.b64decode(payload["b64_json"])
    elif "url" in payload:
        blob = urllib.request.urlopen(payload["url"], timeout=300).read()
    else:
        print(f"{label:58s} -> no image in response")
        return False
    print(f"{label:58s} -> OK {round(time.time() - start, 1)}s {len(blob)} bytes")
    if out_path:
        with open(out_path, "wb") as handle:
            handle.write(blob)
        print("saved", out_path)
    return True


def main():
    env = load_env(sys.argv[1])
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    key = env.get(sys.argv[4] if len(sys.argv) > 4 else "AZURE_OPENAI_API_KEY", "")
    [resource] = "https://[resource]"
    coding = "https://[resource]"
    attempts = [
        (f"{[resource]}/openai/deployments/gpt-image-2/images/generations?api-version=2024-02-01", {"prompt": PROMPT, "size": "1024x1024", "quality": "low", "n": 1}, "[resource] gpt-image-2 deployment 2024-02-01"),
        (f"{[resource]}/openai/deployments/gpt-image-2/images/generations?api-version=2025-04-01-preview", {"prompt": PROMPT, "size": "1024x1024", "quality": "low", "n": 1}, "[resource] gpt-image-2 deployment 2025-04-01-preview"),
        (f"{[resource]}/openai/v1/images/generations", {"model": "gpt-image-2", "prompt": PROMPT, "size": "1024x1024"}, "[resource] v1 gpt-image-2"),
    ]
    for model in ("gpt-image-2.5-flare", "gpt-image-2.5-flare-2026-09-08", "gpt-image-2.5", "gpt-image-2.5-sunburst", "gpt-image-2", "gpt-image-1.5"):
        attempts.append((f"{coding}/openai/v1/images/generations", {"model": model, "prompt": PROMPT, "size": "1024x1024"}, f"[resource] v1 {model}"))
    only = sys.argv[3] if len(sys.argv) > 3 else ""
    for url, body, label in attempts:
        if only and only not in label:
            continue
        if try_url(url, body, key, label, out_path):
            return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
