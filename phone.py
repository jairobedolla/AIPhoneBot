import os

from flask import Flask, request, redirect, jsonify

from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

from dotenv import load_dotenv

#Get environment variables from .env file
load_dotenv()

#Set up twilio client
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
client = Client(account_sid, auth_token)

app = Flask(__name__)


@app.route("/missed_call", methods=['POST'])
def handle_missed_call():
    # Get details from Twilio webhook
    call_status = request.form.get('CallStatus')
    from_number = request.form.get('From')

    # If the call was missed
    if call_status == 'no-answer':
        # Send an SMS back to the caller
        message = client.messages.create(
            body="Sorry, I missed your call. Please leave a message or try again later.",
            from_="+18889156641",
            to=from_number
        )
        return jsonify({"message": "Missed call detected and SMS sent"}), 200
    else:
        return jsonify({"message": "Call not missed"}), 200

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a MMS message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("The Robots are coming! Head for the hills!")

    return str(msg)

"""""
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    msg = resp.message("The Robots are coming! Head for the hills!")

    return str(msg)
"""

if __name__ == "__main__":
    app.run(port=9000, debug=True)