"""List the model deployments of an Azure OpenAI resource from a local .env file.

Only the endpoint and the deployment names and their model ids are printed, never the key.
Usage: python list_azure_deployments.py <env-file>
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
    version = env.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    for api_version in (version, "2025-04-01-preview", "2024-02-01"):
        url = f"{endpoint}/openai/deployments?api-version={api_version}"
        request = urllib.request.Request(url, headers={"api-key": key})
        try:
            response = json.load(urllib.request.urlopen(request, timeout=60))
        except urllib.error.HTTPError as error:
            print(f"{endpoint} api-version={api_version} -> HTTP {error.code}")
            continue
        except Exception as error:  # noqa: BLE001
            print(f"{endpoint} api-version={api_version} -> ERR {type(error).__name__}")
            continue
        print(f"== {endpoint} api-version={api_version}")
        for item in response.get("data", []):
            print(f"   deployment={item.get('id'):28s} model={item.get('model')} status={item.get('status')}")
        break


if __name__ == "__main__":
    main()
