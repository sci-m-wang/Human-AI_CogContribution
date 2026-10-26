"""Probe which image deployment names exist on an Azure OpenAI resource.

An empty body is posted to /images/generations. A missing deployment answers 404, an existing
deployment answers 400 (the body is rejected) or 401. Only status codes are printed.
Usage: python probe_azure_deployments.py <env-file> <deployment-name> [...]
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
    key = env.get("AZURE_OPENAI_API_KEY", "")
    endpoint = env.get("AZURE_OPENAI_ENDPOINT", "").split("/openai/")[0].rstrip("/")
    versions = ["2024-02-01", "2025-04-01-preview", "2023-12-01-preview"]
    for name in sys.argv[2:]:
        for version in versions:
            url = f"{endpoint}/openai/deployments/{name}/images/generations?api-version={version}"
            request = urllib.request.Request(url, data=b"{}", headers={"api-key": key, "Content-Type": "application/json"})
            try:
                urllib.request.urlopen(request, timeout=60)
                print(f"{name:26s} {version} -> 200 (deployment exists)")
                break
            except urllib.error.HTTPError as error:
                body = error.read()[:200].decode("utf-8", "replace")
                code = ""
                try:
                    code = json.loads(body).get("error", {}).get("code", "")
                except Exception:  # noqa: BLE001
                    pass
                print(f"{name:26s} {version} -> HTTP {error.code} {code}")
                if error.code == 400:
                    break
            except Exception as error:  # noqa: BLE001
                print(f"{name:26s} {version} -> ERR {type(error).__name__}")


if __name__ == "__main__":
    main()
