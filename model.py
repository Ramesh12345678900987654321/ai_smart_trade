import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import time
import json
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# ==========================
# 1. LOAD DATA
# ==========================
df = pd.read_csv(r"C:\Users\RAMESH\Desktop\app\reliance_1m.csv")

# Remove Datetime column (not needed for training)
if "Datetime" in df.columns:
    df = df.drop(columns=["Datetime"])

# ==========================
# 2. CREATE FEATURES
# ==========================
df["MA5"] = df["Close"].rolling(5).mean()
df["MA20"] = df["Close"].rolling(20).mean()
df["Return"] = df["Close"].pct_change()
df["High_Low"] = df["High"] - df["Low"]
df["Open_Close"] = df["Close"] - df["Open"]

# Safe Volume Change
df["Volume_Change"] = (
    df["Volume"].replace(0, np.nan).pct_change()
)

# ==========================
# 3. TARGET
# ==========================
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Remove NaN & Inf
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# ==========================
# 4. FEATURES
# ==========================
features = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "MA5",
    "MA20",
    "Return",
    "High_Low",
    "Open_Close",
    "Volume_Change"
]

X = df[features]
y = df["Target"]

# ==========================
# 5. TRAIN / TEST SPLIT
# ==========================
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# ==========================
# 6. TRAIN MODEL
# ==========================
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================
# 7. EVALUATE
# ==========================
pred = model.predict(X_test)

print("=" * 50)
print("Accuracy :", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

# ==========================
# 8. SAVE MODEL
# ==========================
joblib.dump(model, "stock_model.pkl")
print("Model Saved Successfully")

# ==========================
# 9. PREDICT NEXT CANDLE
# ==========================
last = X.iloc[[-1]]

prediction = model.predict(last)[0]
prob = model.predict_proba(last)[0]

print("=" * 50)

if prediction == 1:
    print("Prediction : UP 📈")
else:
    print("Prediction : DOWN 📉")

print(f"UP Probability   : {prob[1]*100:.2f}%")
print(f"DOWN Probability : {prob[0]*100:.2f}%")
print("\nLive Prediction Started... Press Ctrl+C to Stop.\n")

print("\nWaiting for new candle...\n")

last_rows = len(df)
latest_prediction = {
    "prediction": "Waiting...",
    "up_probability": 0,
    "down_probability": 0
}
app = Flask(__name__)
CORS(app)
@app.route("/prediction")
def prediction():
    return jsonify(latest_prediction)
threading.Thread(
    target=lambda: app.run(
        host="127.0.0.1",
        port=5002,
        debug=False,
        use_reloader=False
    ),
    daemon=True
).start()
while True:
    try:
        # Read latest CSV
        new_df = pd.read_csv(r"C:\Users\RAMESH\Desktop\app\reliance_1m.csv")

        # Check if a new candle has arrived
        if len(new_df) > last_rows:

            print("\nNew Candle Detected!")

            last_rows = len(new_df)

            # Remove Datetime column
            if "Datetime" in new_df.columns:
                new_df = new_df.drop(columns=["Datetime"])

            # Recalculate features
            new_df["MA5"] = new_df["Close"].rolling(5).mean()
            new_df["MA20"] = new_df["Close"].rolling(20).mean()
            new_df["Return"] = new_df["Close"].pct_change()
            new_df["High_Low"] = new_df["High"] - new_df["Low"]
            new_df["Open_Close"] = new_df["Close"] - new_df["Open"]
            new_df["Volume_Change"] = (
                new_df["Volume"].replace(0, np.nan).pct_change()
            )

            # Clean data
            new_df.replace([np.inf, -np.inf], np.nan, inplace=True)
            new_df.fillna(0, inplace=True)

            # Get latest candle
            last_candle = new_df[features].iloc[[-1]]

            # Predict
            prediction = model.predict(last_candle)[0]
            prob = model.predict_proba(last_candle)[0]

            # Convert prediction to text
            direction = "UP" if prediction == 1 else "DOWN"

            # Save latest prediction for Flask API
            latest_prediction = {
                "prediction": direction,
                "up_probability": round(prob[1] * 100, 2),
                "down_probability": round(prob[0] * 100, 2)
            }

            # Print in terminal
            print("=" * 50)
            print(f"Prediction : {direction}")
            print(f"UP Probability   : {latest_prediction['up_probability']}%")
            print(f"DOWN Probability : {latest_prediction['down_probability']}%")

        time.sleep(1)

    except KeyboardInterrupt:
        print("Stopped.")
        break