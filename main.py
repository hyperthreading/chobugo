from env import PORT
from sanic import Sanic
from sanic.request import Request
import bolt

app = Sanic(name="cho-bu-go")

@app.post("/slack/events")
async def endpoint(req: Request):
    # app_handler internally runs the App's dispatch method
    return await bolt.handler.handle(req)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

