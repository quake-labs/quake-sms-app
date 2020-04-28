from decouple import config
import os
from twilio.rest import Client


class Config:

    ACCOUNT_SID = config("ACCOUNT_SID")
    AUTH_TOKEN = config("AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

    # endpoint
    QUAKE_API_URL = config("QUAKE_API_URL").rstrip("/")
    print(ACCOUNT_SID)
    print(AUTH_TOKEN)
    print(TWILIO_PHONE_NUMBER)
    print(QUAKE_API_URL)
    # routes
    ZIP = "/zip"


class SMSHelper:
    def __init__(self, twilio_phone_number):
        self.client = Client(config_.ACCOUNT_SID, config_.AUTH_TOKEN)
        self.twilio_phone_number = twilio_phone_number

    def send_message(self, message, user_phone):
        if not user_phone.startswith("+1"):
            user_phone = f"+1{user_phone}"
        print(f"From: {self.twilio_phone_number}")
        print(f"Message: {message}")
        print(f"To: {user_phone}")
        sms = self.client.messages.create(
            from_=self.twilio_phone_number, body=message, to=user_phone
        )
        return sms


config_ = Config()

# SMS Client
sms = SMSHelper(config_.TWILIO_PHONE_NUMBER)
