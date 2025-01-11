import os

from dotenv import load_dotenv


load_dotenv()

SLACK_BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN=os.environ.get("SLACK_APP_TOKEN")
PORT=int(os.environ.get("PORT", 3000))