class RiskManager:

    def __init__(
        self,
        capital=100000,
        risk_percent=1,
        reward_ratio=2,
        max_capital_usage_percent=100
    ):

        self.capital = float(capital)

        self.risk_percent = float(
            risk_percent
        )

        self.reward_ratio = float(
            reward_ratio
        )

        self.max_capital_usage_percent = float(
            max_capital_usage_percent
        )

    def calculate(
        self,
        signal,
        entry_price,
        atr
    ):

        signal = str(
            signal
        ).upper()

        entry_price = float(
            entry_price
        )

        atr = float(
            atr
        )

        # -------------------------
        # Validate
        # -------------------------

        if entry_price <= 0:

            raise ValueError(
                "Entry price must be greater than zero."
            )

        if atr <= 0:

            raise ValueError(
                "Invalid ATR. Trade rejected."
            )

        # -------------------------
        # Maximum money risk
        # -------------------------

        max_risk = (
            self.capital *
            self.risk_percent /
            100
        )

        # -------------------------
        # Risk-based quantity
        # -------------------------

        risk_quantity = int(
            max_risk / atr
        )

        # -------------------------
        # Capital-based quantity
        # -------------------------

        max_position_value = (
            self.capital *
            self.max_capital_usage_percent /
            100
        )

        capital_quantity = int(
            max_position_value /
            entry_price
        )

        # -------------------------
        # Final quantity
        # -------------------------

        quantity = min(
            risk_quantity,
            capital_quantity
        )

        # -------------------------
        # Safety
        # -------------------------

        if quantity <= 0:

            raise ValueError(
                "Calculated quantity is zero. "
                "Trade rejected."
            )

        # -------------------------
        # BUY
        # -------------------------

        if signal == "BUY":

            stop_loss = (
                entry_price -
                atr
            )

            take_profit = (
                entry_price +
                (
                    atr *
                    self.reward_ratio
                )
            )

        # -------------------------
        # SELL
        # -------------------------

        elif signal == "SELL":

            stop_loss = (
                entry_price +
                atr
            )

            take_profit = (
                entry_price -
                (
                    atr *
                    self.reward_ratio
                )
            )

        else:

            return None

        if stop_loss <= 0:

            raise ValueError(
                "Invalid stop-loss price."
            )

        return {

            "signal": signal,

            "entry": round(
                entry_price,
                2
            ),

            "stop_loss": round(
                stop_loss,
                2
            ),

            "take_profit": round(
                take_profit,
                2
            ),

            "quantity": quantity,

            "risk_amount": round(
                max_risk,
                2
            ),

            "risk_quantity": risk_quantity,

            "capital_quantity": capital_quantity
        }