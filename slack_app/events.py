import re
from pprint import pprint

from . import app
from logics import messages
from logics import models
import json
from slack_app.enum import EnumResp


@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")


@app.message("hello")
async def message_hello(message, say):
    global message_timestamp
    await say(blocks=[{
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "오늘 수업 내용, 어떠셨나요?"
        },
    }, {
        "type":
        "actions",
        "elements": [{
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "재밌었어!",
            },
            "action_id": EnumResp.positive.value,
        }, {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "글쎄..좀 어렵던데",
            },
            "action_id": EnumResp.negative.value
        }]
    }],
              text="오늘 수업 내용, 어떠셨나요?")

    message_timestamp = message['ts']


@app.action(EnumResp.positive.value)
async def handle_positive_react(ack, event, say):
    await say("즐거운 소식이군요! :smile:")
    await ack()



@app.action(EnumResp.negative.value)
async def handle_negative_react(ack, event, say):
    await say("아쉬운 소식이군요.. :cry:")
    await ack()


@app.action(re.compile(f"^({EnumResp.correct.value}):.+"))
async def handle_correct_react(ack, action, say):
    await ack()
    await say("정답입니다! :smile:")


@app.action(re.compile(f"^{EnumResp.incorrect.value}:.+"))
async def handle_incorrect_react(ack, action, say):
    await ack()
    await say("틀렸습니다.. :cry:")
