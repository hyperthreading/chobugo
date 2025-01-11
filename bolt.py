import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from env import SLACK_BOT_TOKEN, SLACK_APP_TOKEN

load_dotenv()

app = App(token=SLACK_BOT_TOKEN)

@app.message("hello")
def message_hello(message, say):
    user = message["user"]
    say(f"Hello, <@{user}>!")


# # Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
