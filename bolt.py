
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Start your app
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # take environment variables from .env.
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

