import asyncio
from env import SANIC_PORT
from sanic import Sanic
from sanic.response import text

Sanic.START_METHOD_SET = True
app = Sanic(name="cho-bu-go")


@app.get("/")
async def hello_world(request):
    return text("Hello chobugo~")


def run(loop=asyncio.get_event_loop()):
    app.run(host="0.0.0.0", port=SANIC_PORT, loop=loop)


async def run_async():
    server = await app.create_server("0.0.0.0", SANIC_PORT)
    await server.startup()
    await server.serve_forever()


if __name__ == "__main__":
    run()
