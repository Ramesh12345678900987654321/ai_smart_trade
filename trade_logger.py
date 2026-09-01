import csv
import os

from datetime import datetime


class TradeLogger:

    def __init__(
        self,
        file="logs/trades.csv"
    ):

        self.file = file

        folder = os.path.dirname(
            file
        )

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )

        self.create_file()

    # --------------------------------
    # Create CSV
    # --------------------------------
    def create_file(self):

        if os.path.exists(
            self.file
        ):

            return

        with open(
            self.file,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow(
                [
                    "Time",
                    "Symbol",
                    "Action",
                    "Price",
                    "Quantity",
                    "StopLoss",
                    "Target",
                    "Status",
                    "OrderID",
                    "Reason"
                ]
            )

    # --------------------------------
    # Log trade
    # --------------------------------
    def log_trade(
        self,
        symbol,
        action,
        price,
        quantity,
        stoploss,
        target,
        status,
        order_id="",
        reason=""
    ):

        with open(
            self.file,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow(
                [
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    symbol,

                    action,

                    price,

                    quantity,

                    stoploss,

                    target,

                    status,

                    order_id,

                    reason
                ]
            )

        print(
            "Trade Logged Successfully"
        )