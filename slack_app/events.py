from . import app
from logics import messages
from logics import models
import json
from slack.enum import EnumResp


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
async def handle_button_click(ack, body, say):
    global message_timestamp
    await ack()
    response_timestamp = body['actions'][0]['action_ts']
    time_difference = float(response_timestamp) - float(message_timestamp)
    await say(f"응답하는데 {int(time_difference)}초 걸렸습니다!")  # 버튼 클릭 후 메시지를 보냄


@app.message("test")
async def message_test(message, say):
    global message_timestamp

    message_list = messages.processor.process_user_message(
        models.User.mock_data(), message["text"])

    await say(blocks=[{
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": ",".join(map(lambda m: m.message, message_list))
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
            "action_id": "reponse_positive"
        }, {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "글쎄..좀 어렵던데",
            },
            "action_id": "response_negative"
        }]
    }],
        text="오늘 수업 내용, 어떠셨나요?")

    message_timestamp = message['ts']


@app.message("proactive_confusing")
async def message_confusing(message, say):
    output_messages = messages.processor.trigger_proactive_message(
        models.User.mock_data(), messages.FindConfusingConceptsTurnProcessor())
    await say(
<<<<<<< HEAD:slack/events.py
        text={
            "type": "plain_text",
            "text": ",".join(map(lambda m: m.message, output_messages))
        },
    )
=======
        blocks={
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": ",".join(map(lambda m: m.message, output_messages))
            },
        })


@app.message()
async def every_message(message, say):
    if message.get("subtype", None) is not None:
        return

    user = models.UserRepository.create_or_get_user(message["user"])
    user.add_messages([models.MessageText(message["text"])], False)
    # output_messages = messages.processor.process_user_message(
    #     user, message["text"])


@app.message()
async def every_bot_message(message, say):
    if message.get("subtype", None) != "bot_message":
        return

    user = models.UserRepository.create_or_get_user(message["user"])
    user.add_bot_messages([models.MessageText(message["text"])], True)
>>>>>>> cc9f1ff (update):slack_app/events.py