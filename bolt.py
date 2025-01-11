
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.sanic import AsyncSlackRequestHandler

app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")

handler = AsyncSlackRequestHandler(app)

# Start your app
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # take environment variables from .env.
    app.start(3000)
