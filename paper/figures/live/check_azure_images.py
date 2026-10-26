"""Load the Azure OpenAI image credentials from a local .env and check the endpoint.

Only the endpoint, deployment and the response status are printed. The key is never printed.
Usage: python check_azure_images.py <env-file> [outfile]
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request


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


def main():
    env_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    env = load_env(env_path)
    key = env.get("AZURE_OPENAI_API_KEY", "")
    endpoint = env.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = env.get("AZURE_OPENAI_DEPLOYMENT", "")
    version = env.get("AZURE_OPENAI_API_VERSION", "")
    if not key or not endpoint:
        print("FAIL missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")
        return 1
    print(f"endpoint   {endpoint}")
    print(f"deployment {deployment}  api-version {version}")
    if "/images/generations" in endpoint:
        url = endpoint
    else:
        url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/images/generations?api-version={version}"
    body = json.dumps({
        "model": deployment,
        "prompt": "A single flat grey gear icon with a thin dark outline, centred on a plain white background, minimal technical illustration, no text.",
        "size": "1024x1024",
        "quality": "low",
        "n": 1,
    }).encode()
    request = urllib.request.Request(url, data=body, headers={"api-key": key, "Content-Type": "application/json"})
    start = time.time()
    try:
        response = json.load(urllib.request.urlopen(request, timeout=600))
    except urllib.error.HTTPError as error:
        print("HTTP", error.code, error.read()[:400].decode("utf-8", "replace"))
        return 2
    except Exception as error:  # noqa: BLE001
        print("ERR", type(error).__name__, error)
        return 3
    payload = response.get("data", [{}])[0]
    print(f"OK {round(time.time() - start, 1)}s revised={response.get('data', [{}])[0].get('revised_prompt') is not None}")
    if "b64_json" in payload:
        blob = base64.b64decode(payload["b64_json"])
    elif "url" in payload:
        blob = urllib.request.urlopen(payload["url"], timeout=300).read()
    else:
        print("no image in response", json.dumps(response)[:300])
        return 4
    print(f"bytes {len(blob)}")
    if out_path:
        with open(out_path, "wb") as handle:
            handle.write(blob)
        print("saved", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
