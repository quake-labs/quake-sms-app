from flask import request, jsonify, Blueprint
from api.config import config_
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse, Message
from datetime import datetime
from uszipcode import SearchEngine


main_routes = Blueprint("main_routes", __name__)
search = SearchEngine(simple_zipcode=True)


class ZIPCodeNotFoundException(Exception):
    pass


def generate_message(zipcode: str):
    try:
        loc_info = search.by_zipcode(zipcode).to_dict()
        if loc_info["zipcode"] == None:
            raise ZIPCodeNotFoundException
    except ZIPCodeNotFoundException:
        return f"""
Sorry, {zipcode} is not a valid US ZIP code 😞

In meantime visit us at 👉 https://quake-ds-app.herokuapp.com
"""
    try:
        url = config_.QUAKE_API_URL + config_.ZIP + "/" + zipcode
        resp = requests.get(url).json()
        data = resp["message"][0]
    except:
        return f"""
Sorry, no recent earthquake reported for {zipcode} 😞

Please try another zipcode, or visit us at 👉 https://quake-ds-app.herokuapp.com
"""
    mag = data["mag"]
    ts = int(data["time"]) / 1000.0
    time = datetime.utcfromtimestamp(ts).strftime("%D %H:%M")
    place = data["place"]
    city = loc_info["major_city"]
    state = loc_info["state"]
    return f"""
Earthquake report 📰 for {city}, {state} 🇺🇲

Time 🕐: {time} 
Magnitude 🧿: {mag} 
Occured 🏙️: {place} 

For more info visit 👉 https: // quake-ds-app.herokuapp.com
"""


@main_routes.route("/")
def get_home():
    message = {"message": "SMS API is working"}
    return jsonify(message)


@main_routes.route("/sms", methods=["POST"])
def inbound_sms():
    # Grab the text from the received message.
    zipcode = request.form['Body'].strip()

    # Generate a TwiML Response object with the message we want to send.
    twiml_resp = MessagingResponse()
    msg = generate_message(zipcode)
    twiml_resp.message(msg)
    print(str(twiml_resp))
    return str(twiml_resp)
