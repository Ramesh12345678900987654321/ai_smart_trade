from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, jsonify, render_template
from SmartApi import SmartConnect
import pyotp

app = Flask(__name__)
CORS(app)

# -----------------------------
# Login
# -----------------------------
API_KEY = "G05ydKtV"
CLIENT_CODE = "AACI674575"
PIN = "2006"
TOTP = "ZP3KW65O2M4HLAOM2QYKQVX3OI"

obj = SmartConnect(api_key=API_KEY)

data = obj.generateSession(
    CLIENT_CODE,
    PIN,
    pyotp.TOTP(TOTP).now()
)
print(data)

feedToken = obj.getfeedToken()
@app.route("/")
def home():
    return render_template("index.html")

    
# --------------------------------
# Your Watchlist
# --------------------------------

WATCHLIST = [

    {
        "company":"Reliance Industries",
        "symbol":"RELIANCE",
        "exchange":"NSE",
        "token":"2885"
    },

    {
        "company":"TCS",
        "symbol":"TCS",
        "exchange":"NSE",
        "token":"11536"
    },

    {
        "company":"Infosys",
        "symbol":"INFY",
        "exchange":"NSE",
        "token":"1594"
    },

    {
        "company":"HDFC Bank",
        "symbol":"HDFCBANK",
        "exchange":"NSE",
        "token":"1333"
    },

    {
        "company":"ICICI Bank",
        "symbol":"ICICIBANK",
        "exchange":"NSE",
        "token":"4963"
    },

    {
        "company":"SBI",
        "symbol":"SBIN",
        "exchange":"NSE",
        "token":"3045"
    }

]



@app.route("/prices")
def prices():

    result = []

    for stock in WATCHLIST:

        try:

            data = obj.ltpData(
                stock["exchange"],
                stock["symbol"],
                stock["token"]
            )

            ltp = data["data"]["ltp"]

            result.append({

                "company":stock["company"],
                "symbol":stock["symbol"],
                "price":ltp

            })

        except:

            result.append({

                "company":stock["company"],
                "symbol":stock["symbol"],
                "price":"Error"

            })

    return jsonify(result)


app.run(debug=True)