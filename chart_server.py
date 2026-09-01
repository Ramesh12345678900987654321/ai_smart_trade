from flask import Flask, jsonify
from flask_cors import CORS
from SmartApi import SmartConnect
import pyotp
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -------------------------
# SmartAPI Login
# -------------------------
API_KEY = "G05ydKtV"
CLIENT_CODE = "AACI674575"
PIN = "2006"
TOTP = "ZP3KW65O2M4HLAOM2QYKQVX3OI"

obj = SmartConnect(api_key=API_KEY)

obj.generateSession(
    CLIENT_CODE,
    PIN,
    pyotp.TOTP(TOTP).now()
)

# -------------------------
# Chart Data
# -------------------------
chart_data = []

@app.route("/chart")
def chart():

    data = obj.ltpData("NSE", "RELIANCE", "2885")

    price = data["data"]["ltp"]

    chart_data.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": price
    })

    # Keep only the latest 300 points
    if len(chart_data) > 300:
        chart_data.pop(0)

    return jsonify(chart_data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    app = Flask(__name__)

latest_prediction = {
    "prediction": "Waiting...",
    "up_probability": 0,
    "down_probability": 0
}