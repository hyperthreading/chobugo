import random

from env import SANIC_PORT
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

from nudge_logic import send_class_open_question, send_class_catchup, send_class_multi_choice

Sanic.START_METHOD_SET = True
app = Sanic(name="cho-bu-go")


def get_channel_from_request(request: Request):
    """
    demo request 에서 어떤 채널로 보낼 지는 body 에 JSON 으로 들어옴
    """
    return request.json.get("channel_id")


@app.get("/")
async def hello_world(request):
    return text("Hello chobugo~")

@app.get("/nudge")
async def nudging(request):
    return text("Nudging...")

@app.post("/nudge/class/catchup")
async def class_catchup(request: Request):
    send_class_catchup(channel=get_channel_from_request(request))
    return text("Class catchup...")


@app.post("/nudge/class/multi-choice")
async def class_multi_choice(request: Request):
    send_class_multi_choice(channel=get_channel_from_request(request))
    return text("Class multi-choice...")

@app.post("/nudge/class/open-question")
async def class_open_question(request: Request):
    send_class_open_question(channel=get_channel_from_request(request))
    return text("Class open-question...")

@app.post("/nudge/class/random")
async def class_random(request: Request):
    match random.randint(0, 2):
        case 0:
            send_class_catchup(channel=get_channel_from_request(request))
        case 1:
            send_class_multi_choice(channel=get_channel_from_request(request))
        case 2:
            send_class_open_question(channel=get_channel_from_request(request))
    return text("Class random...")


def run():
    app.run(host="0.0.0.0", port=SANIC_PORT)


async def run_async():
    server = await app.create_server("0.0.0.0", SANIC_PORT)
    await server.startup()
    await server.serve_forever()


if __name__ == "__main__":
    run()
