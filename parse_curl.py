import json
import re
from pathlib import Path
from http.cookies import SimpleCookie

CONFIG_FILE = Path.home() / ".skipera" / "config.json"

def extract_cookies(text: str) -> dict:
    cookies = {}
    
    # 1. Check if user pasted full curl command
    match = re.search(r"-H\s+['\"]cookie:\s*([^'\"]+)['\"]", text, re.IGNORECASE)
    if not match:
        match = re.search(r"--header\s+['\"]cookie:\s*([^'\"]+)['\"]", text, re.IGNORECASE)
    
    cookie_str = match.group(1) if match else text
    
    # 2. Parse cookie string
    cookie = SimpleCookie()
    try:
        cookie.load(cookie_str)
        for key, morsel in cookie.items():
            cookies[key] = morsel.value
    except Exception:
        pass
        
    # Fallback regex parsing if SimpleCookie fails on weird characters
    if not cookies or "CAUTH" not in cookies:
        pairs = re.findall(r'([a-zA-Z0-9_\-\.]+)=([^;\s]+)', cookie_str)
        for k, v in pairs:
            cookies[k] = v
            
    return cookies

def main():
    print("=" * 50)
    print(" Coursera Cookie Auto-Importer")
    print("=" * 50)
    print("DevTools (F12) -> Network tab -> Right click any request -> 'Copy as cURL'")
    print("Aur yahaan pura cURL paste karke Enter dabayein:\n")
    
    lines = []
    try:
        while True:
            line = input()
            if not line and lines:
                break
            lines.append(line)
    except EOFError:
        pass
        
    raw_text = "\n".join(lines).strip()
    if not raw_text:
        print("[Error] Kuch paste nahi kiya!")
        return

    cookies = extract_cookies(raw_text)
    
    if "CAUTH" not in cookies:
        print("\n[WARNING] CAUTH cookie nahi mili! Make sure aapne logged-in Coursera request copy ki hai.")
    else:
        print(f"\n[OK] Found CAUTH and {len(cookies)} other cookies!")

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

    data["cookies"] = cookies
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Config file updated at {CONFIG_FILE}!\n")

if __name__ == "__main__":
    main()
