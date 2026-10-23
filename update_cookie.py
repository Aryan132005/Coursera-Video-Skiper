import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".skipera" / "config.json"

def main():
    print("\n--- Coursera Cookies Setup ---")
    cauth = input("1. CAUTH cookie paste karein: ").strip()
    csrf = input("2. CSRF3-Token cookie paste karein: ").strip()

    if not cauth or not csrf:
        print("[Error] Dono cookies daalna zaroori hai!")
        return

    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cookies": {},
            "perplexity_api_key": "",
            "gemini_api_key": "",
            "perplexity_model": "sonar-pro",
            "gemini_model": "gemini-3.1-flash-lite"
        }
    else:
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {"cookies": {}}

    if "cookies" not in data or not isinstance(data["cookies"], dict):
        data["cookies"] = {}

    data["cookies"]["CAUTH"] = cauth
    data["cookies"]["CSRF3-Token"] = csrf

    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"\n[SUCCESS] Cookies successfully save ho gayi hain yahaan: {CONFIG_FILE}\n")

if __name__ == "__main__":
    main()
