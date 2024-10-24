import os

from flask import Flask, request, redirect, jsonify

import dialogueflow_v2 as dialogueflow

app = Flask(__name__)

DIALOGFLOW_PROJECT_ID = 'aichatbot-438218'
DIALOGFLOW_LANGUAGE_CODE = 'en'
DIALOGFLOW_SESSION_ID = 'tester'  # For each user, use their phone number as session ID
DIALOGFLOW_URL = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{DIALOGFLOW_SESSION_ID}:detectIntent"
ACCESS_TOKEN = 'AIzaSyBnea7rL1a939YAU7n7ZbAPpUxVdL-ipKw'  # Use your Dialogflow API access token here

@app.route("/webhook", methods=['POST'])
def webhook():
    while True:
        incoming_message = request.form.['text']
        from_number = 'tester'

        # Forward the message to Dialogflow
        dialogflow_response = send_to_dialogflow(incoming_message, from_number)

        # Extract the response from Dialogflow
        dialogflow_reply = dialogflow_response['queryResult']['fulfillmentText']

        # Create a response message to be sent back via Twilio
        print(dialogflow_reply)
        
        if dialogflow_reply == "Goodbye":
            break

    return 

def send_to_dialogflow(message, session_id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "query_input": {
            "text": {
                "text": message,
                "language_code": DIALOGFLOW_LANGUAGE_CODE
            }
        },
        "query_params": {
            "time_zone": "America/New_York",  # Adjust as needed
        }
    }

    response = request.post(DIALOGFLOW_URL, headers=headers, json=data)
    return response.json()


if __name__ == "__main__":
    app.run(port=9000, debug=True)