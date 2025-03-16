from flask import Flask
app = Flask(__name__)

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

def parseAnnouncement(url: str):
    # TODO: Parse message info
    # TODO: Find a way to more easily parse roles, subgroups, etc. that doesn't require nested regular expressions
    return "NYI"

@app.route("/get_events", methods=["GET"])
def getEvents():
    # TODO: Set up environment variables such that the Google Calendar API can be accessed
    # TODO: Use the Google Calendar API to get a list of events
    return "NYI"