import requests
import json
from datetime import datetime

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSD"

def get_ltp():
    try:
        url = "https://api.delta.exchange/v2/tickers"
        print("Fetching URL:", url)

        res = requests.get(url, timeout=10)
        print("Status Code:", res.status_code)

        data = res.json()

        # DEBUG: print ALL BTC-related symbols
        print("\n--- BTC RELATED SYMBOLS ---")
        for item in data["result"]:
            if "BTC" in item["symbol"]:
                print(item["symbol"], "->", item.get("last_price"))

        print("---------------------------\n")

        # pick first BTC market with valid price
        for item in data["result"]:
            if "BTC" in item["symbol"] and item.get("last_price"):
                price = float(item["last_price"])
                print("Matched symbol:", item["symbol"])
                return price

        print("❌ No BTC market found")
        return None

    except Exception as e:
        print("❌ ERROR:", e)
        return None

def save_data(price):
    data = {
        "price": price,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "RUNNING"
    }

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("🚀 Running bot...")

    price = get_ltp()

    if price is not None:
        print("✅ Price fetched:", price)
        save_data(price)
    else:
        print("❌ Failed to fetch price")
