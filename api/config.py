from decouple import config
import os


class Config:

    ACCOUNT_SID = config("ACCOUNT_SID")
    AUTH_TOKEN = config("AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

    # endpoint
    QUAKE_API_URL = config("QUAKE_API_URL").rstrip("/")

    # routes
    ZIP = "/zip"


config_ = Config()
