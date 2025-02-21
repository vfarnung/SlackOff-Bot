"""
Authors: Will Escamilla, Zack Edwards, Grace Miguel, Viviane Farnung

This is the main code for our slack bot
"""
import os
import random
import data
import time
from slack_bolt import App
from slack_bolt.oauth.internals import get_or_create_default_installation_store
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

users = data.users_database
userClass = data.user
#our database
link = 'https://sheetdb.io/api/v1/7a4208wp8ee6d'


#what is ngrok.exe???

# Initializes your app with your bot token and signing secret
#what is a signing secret?
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"

"""
This function returns a default message for various inputs
"""
@app.message("!distract me")
def default_message(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        {
            "attachments": [
                {
                    "color": "#f2c744",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Distraction Time!"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Please select a distraction <@{message['user']}>:*"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Joke"
                                    },
                                    "action_id": "wants_joke"
                                },
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Website"
                                    },
                                    "action_id": "wants_web"
                                },
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Video"
                                    },
                                    "action_id": "wants_video"
                                },
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Quote"
                                    },
                                    "action_id": "wants_quote"
                                }
                            ]
                        }
                    ],
                }
            ]
        }
    )


@app.message("stress")
def stress_message(message, say):
    say(
       {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Time for a Break"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hi <@{message['user']}> :wave:"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "You seem to be a tad stressed. Stretch your legs and go for a walk!",
					
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You seem a tad stressed. You're working so hard, it's time you take a break. May I suggest one of the following:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "• Go for a walk \n • Meditate \n • Talk to a friend"
			}
		}
	]
}
    )

@app.message("!distract web")
def web_message(message, say):
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'link':
            answer = i['content']
    say(
        {
        "attachments": [
            {
                "color": "#572dd6",
                "blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Relax on the web",
				
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hey <@{message['user']}>! You've been working so hard, here is a website to get your mind off work: {answer} "
			}
		}
	]
            }
        ]
        }
    )


@app.message("!distract quote")
def quote_message(message, say):
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'quote':
            answer = i['content']
    say(
        {
            "attachments": [
                {
                    "color": "#f09d30",
                    "blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Words of Wisdom",
				
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hey <@{message['user']}>!  :herb: You've been working so hard, here is a quote to ease your mind: {answer}"
			}
		}
	]
                }
            ]
        }
    )

@ app.action("wants_joke")
def joke_requested(body, ack, say):
    # Acknowledge the action
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'joke':
            answer = i['content']
    reply=f"*Okay <@{body['user']['id']}>, here's your joke:* " + answer
    ack()
    say(
        {
            "attachments": [
                {
                    "color": "#f2c744",
                    "text": reply
                }
            ]
        }
    )


@ app.action("wants_web")
def web_requested(body, ack, say):
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'link':
            answer = i['content']
    #acknowledge the answer
    reply=f"*Okay <@{body['user']['id']}>, here's your link:* " + answer
    ack()
    say(
        {
            "attachments":[
                {
                    "color": "#f2c744",
                    "text": reply
                }
            ]
        }
    )
@ app.action("wants_video")
def video_requested(body, ack, say):
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'video':
            answer = i['content']
    #acknowledge the answer
    reply=f"*Okay <@{body['user']['id']}>, here's your video:* " + answer
    ack()
    say(
        {
            "attachments":[
                {
                    "color": "#f2c744",
                    "text": reply
                }
            ]
        }
    )


@ app.action("wants_quote")
def quote_requested(body, ack, say):
    r = requests.get(link).json()
    for i in r:
        if i['type'] == 'quote':
            answer = i['content']
    #acknowledge the answer
    reply=f"*Okay <@{body['user']['id']}>, here's your quote:* " + answer
    ack()
    say(
        {
            "attachments":[
                {
                    "color": "#f2c744",
                    "text": reply
                }
            ]
        }
    )
'''this is to send a scheduled message'''

@app.message("wake me up")
def say_hello(client, message):
    # Unix Epoch time for September 30, 2020 11:59:59 PM
    when_september_ends = time.time()+2
    print(when_september_ends)
    channel_id = message["channel"]
    client.chat_scheduleMessage(
        channel=channel_id,
        post_at=when_september_ends,
        text=" this is a scheduled message for 2 seconds after I send 'wake me up'"
    )
    when_september_ends = time.time()

# #counts numbers of messages per user 
# @app.message()
# def message_counter(message, say):
#     for x in users:
#         if message["user"] in x:
#             current_user = message["user"]
#             print(current_user)
#             current_user.messageCount+1
#             break
#         if [x == len(users)-1] and message["user"] not in users:
#             user = userClass(message["user"], 1)
#             current_user = user

#     if(current_user.messageCount >= 5):
#         say(
#             {
#                 "blocks" : [
#                     {
#                         "type": "header",
#                         "text": {
#                             "type": "plain_text",
#                             "text": "Stop talking so much!"
#                         }

#                     },
#                     {
#                         "type": "section",
#                         "text": {
#                             "type": "mrkdown",
#                             "text": f" Hey @<{message['user']}, your message count is {current_user.messageCount}. This is too much, you gotta chill out."
#                         }
#                     }
#                 ]
                
#             }

#         )
            
        

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
