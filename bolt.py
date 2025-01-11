
from env import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.sanic import AsyncSlackRequestHandler

app = AsyncApp(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")

handler = AsyncSlackRequestHandler(app)


@app.message("hello")
async def message_hello(message, say):
    user = message["user"]
    await say(blocks=[
        {
            "type": "section",
            "fields": [
                {
                    "type": "plain_text",
                    "text": "오늘 수업 내용, 어떠셨나요?",
                    "emoji": True
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "재밌었어!",
                        "emoji": True
                    },
                    "value": "reponse_positive"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "글쎄..좀 어렵던데",
                        "emoji": True
                    },
                    "value": "response_negative"
                }
            ]
        }
    ],
        text="오늘 수업 내용, 어떠셨나요?"
    )


# # Start your app
if __name__ == "__main__":
    app.start(3000)