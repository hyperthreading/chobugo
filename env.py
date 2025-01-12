import os

from dotenv import load_dotenv


load_dotenv()

SLACK_BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN=os.environ.get("SLACK_APP_TOKEN")
SANIC_PORT=int(os.environ.get("PORT", 3001))

SLACK_CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
