class Strategy:

    def __init__(self):

        self.position = None

        self.entry_price = None

        self.quantity = 0

        self.stop_loss = None

        self.take_profit = None

        self.last_price = None

        self.down_count = 0

        self.last_action_candle = None

    # --------------------------------
    # Generate trading decision
    # --------------------------------
    def execute(
        self,
        prediction,
        current_price,
        candle_time=None
    ):

        signal = prediction["signal"]

        current_price = float(
            current_price
        )

        # -------------------------
        # Already holding
        # -------------------------

        if self.position == "LONG":

            # Stop loss
            if (
                self.stop_loss is not None
                and current_price <= self.stop_loss
            ):

                return {

                    "action": "SELL",

                    "price": current_price,

                    "reason": "STOP_LOSS"
                }

            # Target
            if (
                self.take_profit is not None
                and current_price >= self.take_profit
            ):

                return {

                    "action": "SELL",

                    "price": current_price,

                    "reason": "TAKE_PROFIT"
                }

            # AI SELL
            if signal == "SELL":

                return {

                    "action": "SELL",

                    "price": current_price,

                    "reason": "AI_SELL"
                }

            # Falling candle count
            if (
                self.last_price is not None
                and current_price < self.last_price
            ):

                self.down_count += 1

            else:

                self.down_count = 0

            self.last_price = current_price

            # Two consecutive lower prices
            if self.down_count >= 2:

                return {

                    "action": "SELL",

                    "price": current_price,

                    "reason": "TWO_DOWN_MOVES"
                }

            return {

                "action": "HOLD",

                "message": "Holding Position"
            }

        # -------------------------
        # No position
        # -------------------------

        if self.position is None:

            if signal == "BUY":

                return {

                    "action": "BUY",

                    "price": current_price,

                    "reason": "AI_BUY"
                }

            return {

                "action": "HOLD",

                "message": "Waiting for AI BUY"
            }

        return {

            "action": "HOLD"
        }

    # --------------------------------
    # Confirm BUY
    # --------------------------------
    def confirm_buy(
        self,
        entry_price,
        quantity,
        stop_loss,
        take_profit
    ):

        self.position = "LONG"

        self.entry_price = float(
            entry_price
        )

        self.quantity = int(
            quantity
        )

        self.stop_loss = float(
            stop_loss
        )

        self.take_profit = float(
            take_profit
        )

        self.last_price = float(
            entry_price
        )

        self.down_count = 0

        print(
            "Strategy position updated: LONG"
        )

    # --------------------------------
    # Confirm SELL
    # --------------------------------
    def confirm_sell(self):

        print(
            "Strategy position closed."
        )

        self.position = None

        self.entry_price = None

        self.quantity = 0

        self.stop_loss = None

        self.take_profit = None

        self.last_price = None

        self.down_count = 0

    # --------------------------------
    # Reset
    # --------------------------------
    def reset(self):

        self.confirm_sell()