"""
TODO: 현재는 유저에게 보내는 넛지 메세지가 항상 같은 형태로만 보내지고 있습니다.
        이를 다양하게 보내기 위해 다양한 메세지를 보내는 함수를 만들어주세요.
        현재는 literal string으로 메세지를 보내고 있습니다.
        이를 LLM 모델을 통해 생성된 문장으로 바꾸어주세요.
"""
from pprint import pprint

from env import SLACK_BOT_TOKEN

from slack_sdk import WebClient

from slack_app.enum import EnumResp
import message_blocks as blocks

client = WebClient(token=SLACK_BOT_TOKEN)


def send_message(channel: str, text: str):
    response = client.chat_postMessage(
        channel=channel,
        text=text
    )
    return response

def send_class_catchup(channel: str):
    response = client.chat_postMessage(
        channel=channel,
        blocks=[
            blocks.text_section("오늘 수업 내용, 어떠셨나요?"),
            blocks.button_actions_section(
                [
                    blocks.ButtonElement("재밌었어!", EnumResp.positive.value),
                    blocks.ButtonElement("글쎄..좀 어렵던데", EnumResp.negative.value)
                ]
            )
        ]
    )
    return response


def send_class_multi_choice(channel: str):
    response = client.chat_postMessage(
        channel=channel,
        blocks=[
            blocks.text_section("오늘 수업에서 다뤘던 주제를 다 골라보시오~"),
            blocks.button_actions_section(
                [
                    blocks.ButtonElement("네트워크 7계층", EnumResp.correct_id()),
                    blocks.ButtonElement("TCP", EnumResp.correct_id()),
                    blocks.ButtonElement("SSL", EnumResp.incorrect_id()),
                ]
            )
        ]    )
    return response

def send_class_open_question(channel: str):
    response = client.chat_postMessage(
        channel=channel,
        blocks=[
            blocks.text_section("오늘 수업에서 이해가 안됐던 부분이 있나요?"),
        ]
    )
    return response

if __name__ == "__main__":
    # only for test
    response = client.chat_postMessage(
        channel="U0885JJRGLD",
        text="Hello world!"
    )
    send_class_catchup("U0885JJRGLD")
