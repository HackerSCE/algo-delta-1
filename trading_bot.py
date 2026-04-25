import requests
import json
from datetime import datetime

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSDTPERP"

def get_ltp():
    try:
        url = f"{BASE_URL}/v2/tickers/{SYMBOL}"
        print("Fetching URL:", url)

        res = requests.get(url, timeout=10)
        print("Status Code:", res.status_code)
        print("Raw Response:", res.text)

        res.raise_for_status()
        data = res.json()

        price = float(data['result']['last_price'])
        return price

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
