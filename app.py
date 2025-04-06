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

# Preloads usergroups to prevent overuse of Slack API
usergroups = client.usergroups_list(token=os.environ["SLACK_TOKEN"])['usergroups'] 

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

def getPastAnnouncements(count : int = 1):
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
            limit=count
        )

        # Get the first message in results (the most recent) and return it as a JSON
        message = result["messages"]
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
def parseLatestAnnouncement(messageToParse : dict = {}):
    # TODO: Parse message info
        # TODO: Check type infos for every block (valid known types: text, rich-text, emoji, usergroup)
        # TODO: Take into account style tag if it exists (valid known tags: bold=true)
    # TODO: Find a way to more easily parse roles, subgroups, etc. that doesn't require nested regular expressions
    # The above might work for this, more info needed
        # client.usergroups_list(token=os.environ["SLACK_TOKEN"])['usergroups']
        # returns a list of subgroups with keys id (hex value) and handle (@active, @frosh, etc.)

    return parseAnnouncement(getLatestAnnouncement())

def parseAnnouncement(messageToParse : dict = {}):
    # TODO: Parse message info
        # TODO: Check type infos for every block (valid known types: text, rich-text, emoji, usergroup)
        # TODO: Take into account style tag if it exists (valid known tags: bold=true)
    # TODO: Find a way to more easily parse roles, subgroups, etc. that doesn't require nested regular expressions
    # The above might work for this, more info needed
        # client.usergroups_list(token=os.environ["SLACK_TOKEN"])['usergroups']
        # returns a list of subgroups with keys id (hex value) and handle (@active, @frosh, etc.)

    if messageToParse == {}:
        print("No message to parse!")
        return "No message to parse!"
    
    message = ""

    # Converts JSON responses to dictionary
    if type(messageToParse) == Flask.response_class:
        messageToParse = messageToParse.json

    blocksToParse = []
    if "blocks" in messageToParse:
        blocksToParse = messageToParse["blocks"]
        
    for block in blocksToParse:
        if "elements" in block:
            message += parseElementList(block['elements'])

    return message

@app.route("/test_parse")
def testParseFunction():
    messagesToParse = getPastAnnouncements(25)
    for message in messagesToParse.json:
        parseAnnouncement(message)

    return "NYI"

# TODO: Change this to return a built string
def parseElementList(elementList : list, htmlString : str = ""):
    for element in elementList:
        if "elements" in element:
            htmlString += parseElementList(element["elements"])
        else:
            #print(buildHTMLfromElement(element))
            htmlString += buildHTMLfromElement(element)

    return htmlString

def parseStyleList(styleDict : dict):
    html = "style=\""
    for key in styleDict.keys():
        html += f"{key}: true"

    html += "\""
        

def buildHTMLfromElement(element : dict):
    html = ""
    styleHTML = ""

    if "style" in element:
        styleHTML = f" {parseStyleList(element['style'])}"
    
    match element['type']:
        case "usergroup":
            html += (f"<span class=\"usergroup\"{styleHTML}>@" + 
                    usergroups[next(i for i, usergroup in enumerate(usergroups) if usergroup['id'] == element["usergroup_id"])]["handle"]
                 + "</span>")
        case "user":
            html += (f"<span class=\"user\" {styleHTML}>@" + 
                     client.users_info(token=os.environ["SLACK_TOKEN"], user=element["user_id"])["user"]["real_name"] + 
                     "</span>")
        case "channel":
            channel_name = ""
            # TODO: Make it so that this gets a pregenerated list of channels at runtime, and only reloads it if channel isn't found
            for channel_sublist in client.conversations_list(types="public_channel", exclude_archived=True):
                for channel in channel_sublist["channels"]:
                    if element["channel_id"] == channel['id']:
                        channel_name = channel['name']
                        break
                if channel_name != "":
                    break
            html += (f"<span class=\"channel\" {styleHTML}>#" + channel_name + "</span>")
        case "text":
            html += element["text"]
        case "link":
            html += f"<a href=\"{element["url"]}\">\'" + element["url"] + "</a>"
        case _:
            print(f"NYI - \'{element['type']}\' - {element}")
    
    return html
        

@app.route("/get_events", methods=["GET"])
def getEvents():
    # TODO: Set up environment variables such that the Google Calendar API can be accessed
    # TODO: Use the Google Calendar API to get a list of events
    return "NYI"