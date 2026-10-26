"""List the models that an Azure AI Services v1 endpoint exposes.

Only model ids are printed, never the key.
Usage: python list_models.py <env-file> <base-url> [key-name]
"""
import json
import sys
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
    env = load_env(sys.argv[1])
    base = sys.argv[2].rstrip("/")
    key = env.get(sys.argv[3] if len(sys.argv) > 3 else "AZURE_OPENAI_API_KEY", "")
    for url in (f"{base}/openai/v1/models", f"{base}/openai/models?api-version=2024-10-21", f"{base}/openai/deployments?api-version=2024-10-21"):
        request = urllib.request.Request(url, headers={"api-key": key})
        try:
            response = json.load(urllib.request.urlopen(request, timeout=60))
        except urllib.error.HTTPError as error:
            print(f"{url} -> HTTP {error.code} {error.read()[:160].decode('utf-8', 'replace')}")
            continue
        except Exception as error:  # noqa: BLE001
            print(f"{url} -> ERR {type(error).__name__}")
            continue
        print(f"== {url}")
        items = response.get("data") or response.get("value") or []
        for item in items:
            print("   ", item.get("id") or item.get("name"), "|", item.get("model") or item.get("status") or "")


if __name__ == "__main__":
    main()
