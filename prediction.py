class Prediction:

    def __init__(self, df):
        self.df = df

    def predict(self):

        if self.df is None or self.df.empty:

            raise ValueError(
                "Prediction received empty dataframe."
            )

        latest = self.df.iloc[-1]

        score = 0

        reasons = []

        # -------------------------
        # Trend
        # -------------------------

        if latest["TREND"] == 1:

            score += 25

            reasons.append(
                "Uptrend (MA20 > MA50)"
            )

        else:

            score -= 25

            reasons.append(
                "Downtrend"
            )

        # -------------------------
        # Price Above MA20
        # -------------------------

        if latest["PRICE_ABOVE_MA20"] == 1:

            score += 15

            reasons.append(
                "Price above MA20"
            )

        else:

            score -= 15

            reasons.append(
                "Price below MA20"
            )

        # -------------------------
        # MACD
        # -------------------------

        if latest["MACD_BULLISH"] == 1:

            score += 25

            reasons.append(
                "Bullish MACD"
            )

        else:

            score -= 25

            reasons.append(
                "Bearish MACD"
            )

        # -------------------------
        # Volume
        # -------------------------

        if latest["HIGH_VOLUME"] == 1:

            score += 15

            reasons.append(
                "High Volume"
            )

        else:

            reasons.append(
                "Normal Volume"
            )

        # -------------------------
        # RSI
        # -------------------------

        rsi = float(
            latest["RSI"]
        )

        if 55 <= rsi <= 70:

            score += 20

            reasons.append(
                "Healthy RSI"
            )

        elif rsi > 70:

            score -= 10

            reasons.append(
                "Overbought"
            )

        elif rsi < 30:

            score += 10

            reasons.append(
                "Oversold"
            )

        else:

            reasons.append(
                "Neutral RSI"
            )

        # -------------------------
        # Final Decision
        # -------------------------

        if score >= 60:

            signal = "BUY"

        elif score <= -40:

            signal = "SELL"

        else:

            signal = "HOLD"

        return {

            "signal": signal,

            "score": score,

            "reasons": reasons,

            "rsi": round(rsi, 2),

            "price": float(
                latest["Close"]
            )

        }