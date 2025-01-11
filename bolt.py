from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from env import SLACK_BOT_TOKEN, SLACK_APP_TOKEN


app = App(token=SLACK_BOT_TOKEN)


@app.message("hello")
def message_hello(message, say):
    user = message["user"]
    say(blocks=[
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
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
