class FeatureEngineering:

    def __init__(self, df):
        self.df = df.copy()

    def create_features(self):

        if self.df.empty:
            raise ValueError(
                "Feature engineering received empty dataframe."
            )

        # -----------------------
        # Candle Body
        # -----------------------
        self.df["BODY_SIZE"] = (
            self.df["Close"] -
            self.df["Open"]
        ).abs()

        # -----------------------
        # Candle Range
        # -----------------------
        self.df["RANGE"] = (
            self.df["High"] -
            self.df["Low"]
        )

        # -----------------------
        # Price Above MA20
        # -----------------------
        self.df["PRICE_ABOVE_MA20"] = (
            self.df["Close"] >
            self.df["MA20"]
        ).astype(int)

        # -----------------------
        # Price Above MA50
        # -----------------------
        self.df["PRICE_ABOVE_MA50"] = (
            self.df["Close"] >
            self.df["MA50"]
        ).astype(int)

        # -----------------------
        # Trend
        # -----------------------
        self.df["TREND"] = (
            self.df["MA20"] >
            self.df["MA50"]
        ).astype(int)

        # -----------------------
        # Bullish MACD
        # -----------------------
        self.df["MACD_BULLISH"] = (
            self.df["MACD"] >
            self.df["MACD_SIGNAL"]
        ).astype(int)

        # -----------------------
        # High Volume
        # -----------------------
        self.df["HIGH_VOLUME"] = (
            self.df["Volume"] >
            self.df["VOL_MA20"]
        ).astype(int)

        # -----------------------
        # RSI
        # -----------------------
        self.df["RSI_OVERBOUGHT"] = (
            self.df["RSI"] > 70
        ).astype(int)

        self.df["RSI_OVERSOLD"] = (
            self.df["RSI"] < 30
        ).astype(int)

        self.df.dropna(inplace=True)

        self.df.reset_index(
            drop=True,
            inplace=True
        )

        if self.df.empty:
            raise ValueError(
                "No data remaining after feature engineering."
            )

        return self.df