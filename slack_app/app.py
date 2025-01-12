from env import SLACK_BOT_TOKEN
from slack_bolt.async_app import AsyncApp

app = AsyncApp(token=SLACK_BOT_TOKEN)
