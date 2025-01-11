from . import app
from logics import messages
from logics import models


@app.shortcut("open_modal")
async def open_modal(ack, body, client):
    # Acknowledge the command request
    await ack()
    # Call views_open with the built-in client
    await client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type":
            "modal",
            # View identifier
            "callback_id":
            "view_1",
            "title": {
                "type": "plain_text",
                "text": "My App"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "blocks": [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Welcome to a modal with _blocks_"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click me!"
                    },
                    "action_id": "button_abc"
                }
            }, {
                "type": "input",
                "block_id": "input_c",
                "label": {
                    "type": "plain_text",
                    "text": "What are your hopes and dreams?"
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "dreamy_input",
                    "multiline": True
                }
            }]
        })


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


@app.action("reponse_positive")
async def handle_button_click(ack, body, say):
    global message_timestamp
    await ack()
    response_timestamp = body['actions'][0]['action_ts']
    time_difference = float(response_timestamp) - float(message_timestamp)
    await say(f"응답하는데 {int(time_difference)}초 걸렸습니다!")  # 버튼 클릭 후 메시지를 보냄


@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")


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
