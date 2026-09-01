class OrderManager:

    def __init__(
        self,
        api,
        paper_trading=True
    ):

        self.api = api

        self.paper_trading = (
            paper_trading
        )

    # --------------------------------
    # Place order
    # --------------------------------
    def place_order(
        self,
        symbol,
        symboltoken,
        signal,
        quantity
    ):

        signal = str(
            signal
        ).upper()

        quantity = int(
            quantity
        )

        if signal not in [
            "BUY",
            "SELL"
        ]:

            return {

                "status": "failed",

                "message":
                    "Invalid trading signal."
            }

        if quantity <= 0:

            return {

                "status": "failed",

                "message":
                    "Quantity must be greater than zero."
            }

        # -------------------------
        # PAPER TRADING
        # -------------------------

        if self.paper_trading:

            print(
                "=" * 50
            )

            print(
                "PAPER TRADE"
            )

            print(
                f"Symbol   : {symbol}"
            )

            print(
                f"Signal   : {signal}"
            )

            print(
                f"Quantity : {quantity}"
            )

            print(
                "=" * 50
            )

            return {

                "status": "success",

                "mode": "paper",

                "signal": signal,

                "quantity": quantity,

                "orderid": "PAPER"
            }

        # -------------------------
        # LIVE ORDER
        # -------------------------

        transaction = signal

        orderparams = {

            "variety": "NORMAL",

            "tradingsymbol": symbol,

            "symboltoken": symboltoken,

            "transactiontype": transaction,

            "exchange": "NSE",

            "ordertype": "MARKET",

            "producttype": "INTRADAY",

            "duration": "DAY",

            "price": "0",

            "squareoff": "0",

            "stoploss": "0",

            "quantity": str(
                quantity
            )
        }

        try:

            print(
                "Sending LIVE order..."
            )

            response = self.api.placeOrder(
                orderparams
            )

            print(
                "SmartAPI order response:"
            )

            print(response)

            # -------------------------
            # Validate response
            # -------------------------

            if response is None:

                return {

                    "status": "failed",

                    "mode": "live",

                    "message":
                        "SmartAPI returned None."
                }

            # placeOrder in some SmartAPI
            # versions returns an order ID
            # directly.

            if isinstance(
                response,
                str
            ):

                if response.strip():

                    return {

                        "status": "success",

                        "mode": "live",

                        "signal": signal,

                        "quantity": quantity,

                        "orderid": response
                    }

                return {

                    "status": "failed",

                    "mode": "live",

                    "message":
                        "Empty order ID."
                }

            # Some responses may be dicts.

            if isinstance(
                response,
                dict
            ):

                if response.get(
                    "status"
                ) is False:

                    return {

                        "status": "failed",

                        "mode": "live",

                        "message":
                            response.get(
                                "message",
                                "Order rejected."
                            )
                    }

                order_id = (
                    response.get(
                        "data",
                        {}
                    )
                    if isinstance(
                        response.get(
                            "data"
                        ),
                        dict
                    )
                    else response.get(
                        "data"
                    )
                )

                if order_id:

                    return {

                        "status": "success",

                        "mode": "live",

                        "signal": signal,

                        "quantity": quantity,

                        "orderid": order_id
                    }

                return {

                    "status": "failed",

                    "mode": "live",

                    "message":
                        response.get(
                            "message",
                            "Unknown order response."
                        )
                }

            return {

                "status": "failed",

                "mode": "live",

                "message":
                    "Unknown SmartAPI response."
            }

        except Exception as e:

            print(
                "ORDER FAILED"
            )

            print(e)

            return {

                "status": "failed",

                "mode": "live",

                "message": str(e)
            }

    # --------------------------------
    # Get broker positions
    # --------------------------------
    def get_positions(self):

        if self.paper_trading:

            return []

        try:

            response = self.api.position()

            if not response:

                return []

            if not response.get(
                "status"
            ):

                print(
                    "Unable to retrieve positions:"
                )

                print(
                    response
                )

                return []

            return response.get(
                "data",
                []
            ) or []

        except Exception as e:

            print(
                "Position API error:"
            )

            print(e)

            return []