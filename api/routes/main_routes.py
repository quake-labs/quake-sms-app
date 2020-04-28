from flask import request, jsonify, Blueprint
from api.config import config_, sms
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse, Message
from datetime import datetime
from uszipcode import SearchEngine
import logging

route = ".".join(["api.app", __name__.strip("api.")])
routelogger = logging.getLogger(route)
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
    routelogger.info(f"[ROUTE] / called, {message}")
    return jsonify(message)


@main_routes.route("/sms", methods=["POST"])
def inbound_sms():
    # Grab the text from the received message.
    routelogger.info("[ROUTE] /sms called")
    zipcode = request.form["Body"].strip()
    routelogger.info(f"Inboud SMS message - {zipcode}")
    # Generate a TwiML Response object with the message we want to send.
    twiml_resp = MessagingResponse()
    msg = generate_message(zipcode)
    routelogger.info(f"Outbout SMS response - {msg}")
    twiml_resp.message(msg)
    return str(twiml_resp)


@main_routes.route("/web", methods=["POST"])
def inbound_web_sms():

    # Parse phone number and zipcode
    routelogger.info("[ROUTE] /web called")
    data = request.get_json()
    routelogger.info(f"[ROUTE] /web parsing {data}")
    phonenumber = data["phonenumber"].strip()
    zipcode = data["zipcode"].strip()

    # Generate message
    msg = generate_message(zipcode)
    routelogger.info(f"[ROUTE] /web message generated {msg}")
    # Send message to user
    try:
        res = sms.send_message(msg, phonenumber)
    except Exception as ex:
        routelogger.warning(
            "[ROUTE] /web error when trying to use twilio client to send message"
        )
        routelogger.warning(ex)
        return {
            "message": "Failure!, there was error on our end, please check back soon!"
        }
    routelogger.info("[ROUTE] /web twilio response: ")
    routelogger.info(res.sid)
    return {"message": "Success!, you should recieve a text from us soon."}
