import os
import pyotp
from SmartApi import SmartConnect
from dotenv import load_dotenv

load_dotenv()


class SmartAPILogin:

    def __init__(self):

        self.api_key = "****"
        self.client_code = "******"
        self.pin = "****"
        self.totp_secret = "***************"

        self.obj = None


    def login(self):

        self.obj = SmartConnect(
            api_key=self.api_key
        )

        totp = pyotp.TOTP(
            self.totp_secret
        ).now()


        session = self.obj.generateSession(
            self.client_code,
            self.pin,
            totp
        )


        if session["status"]:

            print("LOGIN SUCCESS")

            return self.obj

        else:

            print("LOGIN FAILED")
            return None