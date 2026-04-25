import requests
import json
import time
from datetime import datetime

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSD"


def get_ltp():
    try:
        url = f"{BASE_URL}/v2/history/candles"

        now = int(time.time())

        # 🔥 VERY IMPORTANT FIX
        # Go 30 minutes back to avoid empty data
        end = now - 60
        start = end - 1800  # 30 min window

        params = {
            "symbol": SYMBOL,
            "resolution": "1m",
            "start": start,
            "end": end
        }

        print("Fetching candles...")
        print("Params:", params)

        res = requests.get(url, params=params, timeout=10)
        print("Status Code:", res.status_code)
        print("Response preview:", res.text[:200])

        data = res.json()

        if data.get("result") and len(data["result"]) > 0:
            last_candle = data["result"][-1]

            price = float(last_candle["close"])
            print("✅ Price fetched:", price)

            return price
        else:
            print("❌ No candle data returned")
            return None

    except Exception as e:
        print("❌ ERROR:", e)
        return None


def save_data(price):
    try:
        data = {
            "price": price,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "RUNNING"
        }

        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ data.json updated")

    except Exception as e:
        print("❌ ERROR saving data:", e)


def main():
    print("🚀 Running bot...")

    price = get_ltp()

    if price is not None:
        save_data(price)
    else:
        print("❌ Failed to fetch price")


if __name__ == "__main__":
    main()
