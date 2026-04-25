import os
import time
from datetime import datetime
import requests

BASE_URL = "https://api.delta.exchange"

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

SYMBOL = "BTCUSDTPERP"

def get_candles():
    url = f"{BASE_URL}/v2/history/candles"
    params = {
        "symbol": SYMBOL,
        "resolution": "5m",
        "limit": 100
    }
    return requests.get(url, params=params).json()

def get_ltp():
    url = f"{BASE_URL}/v2/tickers/{SYMBOL}"
    return requests.get(url).json()['result']['last_price']

def place_order(side, size=1):
    url = f"{BASE_URL}/v2/orders"
    headers = {
        "api-key": API_KEY
    }
    data = {
        "symbol": SYMBOL,
        "side": side,
        "size": size,
        "order_type": "market"
    }
    res = requests.post(url, json=data, headers=headers)
    print(res.json())

def run_strategy():
    candles = get_candles()['result']

    # Find 9:05 candle close
    reference_price = None
    for c in candles:
        ts = datetime.fromtimestamp(c['time'] / 1000)
        if ts.hour == 9 and ts.minute == 5:
            reference_price = c['close']
            break

    if reference_price is None:
        print("Reference candle not found")
        return

    ltp = float(get_ltp())

    print("Reference:", reference_price, "LTP:", ltp)

    if ltp > reference_price:
        print("Price above reference, waiting for breakout logic...")
        last_candle = candles[-1]

        if last_candle['close'] > reference_price:
            if ltp > last_candle['high']:
                print("Breakout detected → LONG")
                place_order("buy")

    # Exit at 6 PM
    now = datetime.now()
    if now.hour == 18 and now.minute >= 0:
        print("6 PM exit condition")
        place_order("sell")

if __name__ == "__main__":
    run_strategy()
