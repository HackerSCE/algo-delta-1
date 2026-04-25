import requests
import json
import time
from datetime import datetime

BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSD"


def get_exchange_time():
    try:
        url = f"{BASE_URL}/v2/time"
        res = requests.get(url, timeout=10)
        data = res.json()

        # API returns epoch seconds
        return int(data["result"]["server_time"])
    except Exception as e:
        print("❌ Error getting server time:", e)
        return None


def get_ltp():
    try:
        server_time = get_exchange_time()

        if not server_time:
            print("❌ Could not get server time")
            return None

        url = f"{BASE_URL}/v2/history/candles"

        # SAFE window (15 minutes back)
        start = server_time - 900
        end = server_time

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

        data = res.json()
        print("Response preview:", str(data)[:200])

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
