import requests
import os

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSDTPERP"

def get_public_ip():
    try:
        return requests.get("https://api64.ipify.org?format=json", timeout=5).json()['ip']
    except:
        return "Unable to fetch IP"

def safe_request(url, method="GET", **kwargs):
    try:
        if method == "GET":
            res = requests.get(url, timeout=10, **kwargs)
        else:
            res = requests.post(url, timeout=10, **kwargs)

        # Raise HTTP errors
        res.raise_for_status()

        return res.json()

    except requests.exceptions.HTTPError as e:
        print("\n❌ HTTP ERROR")
        print("Status Code:", res.status_code)
        print("Response:", res.text)

        if res.status_code in [401, 403]:
            print("\n🚫 POSSIBLE IP BLOCK / AUTH ISSUE")
            print("👉 Current Public IP:", get_public_ip())
            print("👉 Action: Whitelist this IP in Delta Exchange")

    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR (Network issue or blocked)")
        print("👉 Current Public IP:", get_public_ip())

    except requests.exceptions.Timeout:
        print("\n❌ REQUEST TIMEOUT")

    except Exception as e:
        print("\n❌ UNKNOWN ERROR:", str(e))

    return None


def get_ltp():
    url = f"{BASE_URL}/v2/tickers/{SYMBOL}"
    data = safe_request(url)
    if data:
        return data['result']['last_price']
    return None


if __name__ == "__main__":
    print("🚀 Running bot...")

    ltp = get_ltp()

    if ltp:
        print("✅ LTP:", ltp)
    else:
        print("⚠️ Failed to fetch price")
