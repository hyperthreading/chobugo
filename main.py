import asyncio
import nest_asyncio
nest_asyncio.apply()

from env import SANIC_PORT
from sanic import Sanic
from sanic.response import text

app = Sanic(name="cho-bu-go")


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


async def run_sanic():
    app.run(host="0.0.0.0", port=SANIC_PORT)


async def run_bolt():
    import bolt
    bolt.app.start()


async def main():
    bolt_task = asyncio.create_task(run_bolt())
    sanic_task = asyncio.create_task(run_sanic())
    await asyncio.gather(bolt_task, sanic_task)


if __name__ == "__main__":
    asyncio.run(main())
