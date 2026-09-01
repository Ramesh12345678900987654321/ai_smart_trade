import csv
import os
from datetime import datetime
from SmartApi import SmartConnect
import pyotp
import time

# -----------------------------
# Login
# -----------------------------
API_KEY = "G05ydKtV"
CLIENT_ID = "AACI674575"
PASSWORD = "2006"
TOTP = "ZP3KW65O2M4HLAOM2QYKQVX3OI"

obj = SmartConnect(api_key=API_KEY)

session = obj.generateSession(
    CLIENT_ID,
    PASSWORD,
    pyotp.TOTP(TOTP).now()
)

# -----------------------------
# CSV File
# -----------------------------
csv_file = "reliance_1m.csv"

# Create file with header if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Datetime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ])

# Previous price
previous_price = None

print("Recording live prices...")

while True:
    try:
        data = obj.ltpData("NSE", "RELIANCE", "2885")

        price = float(data["data"]["ltp"])
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if previous_price is None:
            previous_price = price

        # Since LTP gives only one price, use it for OHLC
        open_price = previous_price
        high = max(previous_price, price)
        low = min(previous_price, price)
        close = price
        volume = 0

        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                now,
                open_price,
                high,
                low,
                close,
                volume
            ])

        previous_price = price

        print(now, price)

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)