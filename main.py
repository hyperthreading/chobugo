import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from sanic import Sanic
from sanic.request import Request
import bolt

app = Sanic(name="cho-bu-go")

@app.post("/slack/events")
async def endpoint(req: Request):
    # app_handler internally runs the App's dispatch method
    return await bolt.handler.handle(req)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

