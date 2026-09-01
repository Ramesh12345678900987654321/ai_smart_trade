import pandas as pd

from ta.trend import SMAIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD

from ta.momentum import RSIIndicator

from ta.volatility import BollingerBands
from ta.volatility import AverageTrueRange


class IndicatorCalculator:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # -----------------------------
    # Moving Averages
    # -----------------------------
    def moving_average(self):

        self.df["MA5"] = SMAIndicator(
            close=self.df["Close"],
            window=5
        ).sma_indicator()

        self.df["MA20"] = SMAIndicator(
            close=self.df["Close"],
            window=20
        ).sma_indicator()

        self.df["MA50"] = SMAIndicator(
            close=self.df["Close"],
            window=50
        ).sma_indicator()

    # -----------------------------
    # Exponential Moving Average
    # -----------------------------
    def exponential_ma(self):

        self.df["EMA20"] = EMAIndicator(
            close=self.df["Close"],
            window=20
        ).ema_indicator()

        self.df["EMA50"] = EMAIndicator(
            close=self.df["Close"],
            window=50
        ).ema_indicator()

    # -----------------------------
    # RSI
    # -----------------------------
    def rsi(self):

        self.df["RSI"] = RSIIndicator(
            close=self.df["Close"],
            window=14
        ).rsi()

    # -----------------------------
    # MACD
    # -----------------------------
    def macd(self):

        macd = MACD(
            close=self.df["Close"]
        )

        self.df["MACD"] = macd.macd()
        self.df["MACD_SIGNAL"] = macd.macd_signal()
        self.df["MACD_HIST"] = macd.macd_diff()

    # -----------------------------
    # Bollinger Bands
    # -----------------------------
    def bollinger(self):

        bb = BollingerBands(
            close=self.df["Close"],
            window=20,
            window_dev=2
        )

        self.df["BB_UPPER"] = bb.bollinger_hband()
        self.df["BB_MIDDLE"] = bb.bollinger_mavg()
        self.df["BB_LOWER"] = bb.bollinger_lband()

    # -----------------------------
    # ATR
    # -----------------------------
    def atr(self):

        atr = AverageTrueRange(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=14
        )

        self.df["ATR"] = atr.average_true_range()

    # -----------------------------
    # Volume Average
    # -----------------------------
    def volume_average(self):

        self.df["VOL_MA20"] = (
            self.df["Volume"]
            .rolling(window=20)
            .mean()
        )

    # -----------------------------
    # Calculate Everything
    # -----------------------------
    def calculate(self):

        if self.df.empty:
            raise ValueError("Indicator input dataframe is empty.")

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        missing = [
            column
            for column in required
            if column not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        self.df = self.df.sort_values(
            "Datetime"
        ).drop_duplicates(
            subset=["Datetime"]
        ).reset_index(drop=True)

        self.moving_average()
        self.exponential_ma()
        self.rsi()
        self.macd()
        self.bollinger()
        self.atr()
        self.volume_average()

        self.df.dropna(inplace=True)

        self.df.reset_index(
            drop=True,
            inplace=True
        )

        if self.df.empty:
            raise ValueError(
                "Not enough candle data to calculate indicators."
            )

        return self.df