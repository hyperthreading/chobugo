import asyncio
from env import SLACK_APP_TOKEN
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from aiohttp import web
from .app import app
from . import events


def run(loop=asyncio.get_event_loop()):
    loop.run_until_complete(run_async())


async def run_async():
    handler = AsyncSocketModeHandler(app,
                                     app_token=SLACK_APP_TOKEN,
                                     loop=asyncio.get_event_loop())

    return (asyncio.gather(handle_slack_web_app(handler),
                           handle_socket_mode(handler)))


async def handle_socket_mode(handler):
    await handler.connect_async()
    await handler.client.message_processor


async def handle_slack_web_app(handler):
    webapp = web.Application()
    webapp.add_subapp("/slack/events", handler.app.server().web_app)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 3000)
    await site.start()
    # wait for finish signal
    await runner.cleanup()


if __name__ == "__main__":
    run()
