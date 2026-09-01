import os
import time

import pandas as pd

from datetime import datetime, timedelta


class MarketData:

    def __init__(
        self,
        api,
        lookback_minutes=120
    ):

        self.api = api

        # 120 minutes gives enough data
        # for MA50 + indicators.
        self.lookback_minutes = lookback_minutes

        self.last_candle_time = None

    # ---------------------------------
    # Get candles
    # ---------------------------------
    def get_candles(
        self,
        exchange="NSE",
        symboltoken="2885",
        interval="ONE_MINUTE"
    ):

        to_date = datetime.now()

        from_date = (
            to_date -
            timedelta(
                minutes=self.lookback_minutes
            )
        )

        params = {
            "exchange": exchange,
            "symboltoken": symboltoken,
            "interval": interval,
            "fromdate": from_date.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "todate": to_date.strftime(
                "%Y-%m-%d %H:%M"
            )
        }

        try:

            response = self.api.getCandleData(
                params
            )

        except Exception as e:

            print(
                "SmartAPI market-data error:"
            )

            print(e)

            # IMPORTANT:
            # Do not automatically call the
            # API again after an API error.
            return None

        if not isinstance(response, dict):

            print(
                "Invalid SmartAPI response."
            )

            return None

        if not response.get("status"):

            print(
                "SmartAPI candle request failed:"
            )

            print(
                response.get(
                    "message",
                    response
                )
            )

            return None

        data = response.get("data")

        if not data:

            print(
                "SmartAPI returned no candle data."
            )

            return None

        try:

            df = pd.DataFrame(
                data,
                columns=[
                    "Datetime",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume"
                ]
            )

            df["Datetime"] = pd.to_datetime(
                df["Datetime"],
                errors="coerce"
            )

            numeric_columns = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]

            for column in numeric_columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

            df.dropna(
                inplace=True
            )

            df.drop_duplicates(
                subset=["Datetime"],
                inplace=True
            )

            df.sort_values(
                "Datetime",
                inplace=True
            )

            df.reset_index(
                drop=True,
                inplace=True
            )

            if len(df) < 60:

                print(
                    f"Not enough candles: {len(df)}"
                )

                return None

            return df

        except Exception as e:

            print(
                "Candle processing error:"
            )

            print(e)

            return None

    # ---------------------------------
    # Check whether a new candle exists
    # ---------------------------------
    def is_new_candle(self, df):

        if df is None or df.empty:
            return False

        latest_time = df.iloc[-1]["Datetime"]

        if self.last_candle_time is None:

            self.last_candle_time = latest_time

            return True

        if latest_time > self.last_candle_time:

            self.last_candle_time = latest_time

            return True

        return False

    # ---------------------------------
    # Save CSV
    # ---------------------------------
    def save_csv(
        self,
        df,
        path="data/live_data.csv"
    ):

        if df is None or df.empty:

            print(
                "Nothing to save."
            )

            return

        folder = os.path.dirname(path)

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )

        df.to_csv(
            path,
            index=False
        )

        print(
            f"{len(df)} candles saved."
        )