from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)

CORS(app)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ramesh",
        database="trading_db"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "message": "Trade History API is running"
    })


# =========================================================
# TRADE HISTORY
# =========================================================

@app.route("/trades")
def trades():

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                time,
                symbol,
                action,
                price,
                quantity,
                status
            FROM trade_history
            ORDER BY time DESC
        """)

        data = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(data),
            "trades": data
        })


    except mysql.connector.Error as e:

        print("MySQL Error:", e)

        return jsonify({
            "success": False,
            "count": 0,
            "trades": [],
            "error": str(e)
        }), 500


    except Exception as e:

        print("Error:", e)

        return jsonify({
            "success": False,
            "count": 0,
            "trades": [],
            "error": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       TRADE HISTORY API")
    print("==========================================")
    print()
    print("Health:")
    print("http://127.0.0.1:8000/health")
    print()
    print("Trades:")
    print("http://127.0.0.1:8000/trades")
    print()
    print("==========================================")
    print()

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )