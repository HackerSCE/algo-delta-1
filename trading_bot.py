import requests
import json
from datetime import datetime

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSD"

def get_ltp():
    try:
        url = "https://api.delta.exchange/v2/tickers/BTCUSD"
        print("Fetching URL:", url)

        res = requests.get(url, timeout=10)
        print("Status Code:", res.status_code)
        print("Response:", res.text)

        data = res.json()

        if data.get("result"):
            price = float(data["result"]["last_price"])
            print("✅ Price:", price)
            return price
        else:
            print("❌ No result in response")
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
