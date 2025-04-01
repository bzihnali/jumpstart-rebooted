from flask import Flask, render_template, request, jsonify
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import re
import requests
import json

# Load environment variables
load_dotenv(dotenv_path=".env", override=True)

app = Flask(__name__)
client = WebClient(token=os.environ["SLACK_TOKEN"]) # Client for data retrieval from Slack

"""
Main page, what the client should see
"""
@app.route("/")
def index():
    return "NYI"

"""
Gets the most recent announcement sent and validated in the
announcements channel.
"""
@app.route("/get_latest_announcement", methods=["GET"])
def getLatestAnnouncement():
    # TODO: Get the most recent message from Slack
    if(request.method == 'GET'):
        channel_name = "announcements"
        conversation_id = None
        subteam_names = {}

        for subteam in client.usergroups_list(token=os.environ["SLACK_TOKEN"])['usergroups']:
            subteam_names[subteam['id']] = subteam['handle']    

        try:
            # Set conversation_id to the #announcements channel
            for result in client.conversations_list():
                if conversation_id is not None:
                    break
                for channel in result["channels"]:
                    if channel["name"] == channel_name:
                        conversation_id = channel["id"]
                        break
            
            # Set result to the array of the first limit (currently 1) announcements in #announcements
            result = client.conversations_history(
                channel=conversation_id,
                inclusive=True,
                oldest="0",
                limit=1
            )

            # Get the first message in results (the most recent) and return it as JSON
            message = result["messages"][0]
            return jsonify(message)
        except Exception as e:
            print(f"Error: {e}")
    
    # TODO: Get the most recent message from the proper JSON file (do after the Slack message grabbing is confirmed to work)
    return "NYI"

"""
Sends the announcement data to be saved to a JSON file.
This should be called via Slack hook.
"""
@app.route("/set_latest_announcement", methods=["GET"])
def setLatestAnnouncement():
    # TODO: Accept the most recent message from Slack via hook
    # TODO: Load the message to the JSON file properly
    """
    The JSON message object should have:
    sender_name: The sender's name
    timestamp: When the message was sent
    message_text: The text of the message
    """
    return "NYI"

"""
THIS IS A TEST FUNCTION, MEANT TO TEST PARSING OF SLACK MESSAGES
WILL BE REMOVED DOWN THE LINE

This function currently grabs the elements of the latest announcement.
"""
@app.route("/parse_latest_announcement")
def parseLatestAnnouncement():
    messageToParse = getLatestAnnouncement()
    # TODO: Parse message info
        # TODO: Check type infos for every block (valid known types: text, rich-text, emoji, usergroup)
        # TODO: Take into account style tag if it exists (valid known tags: bold=true)
    # TODO: Find a way to more easily parse roles, subgroups, etc. that doesn't require nested regular expressions
    # The above might work for this, more info needed
        # client.usergroups_list(token=os.environ["SLACK_TOKEN"])['usergroups']
        # returns a list of subgroups with keys id (hex value) and handle (@active, @frosh, etc.)

    return messageToParse.json['blocks'][0]['elements']

@app.route("/get_events", methods=["GET"])
def getEvents():
    # TODO: Set up environment variables such that the Google Calendar API can be accessed
    # TODO: Use the Google Calendar API to get a list of events
    return "NYI"