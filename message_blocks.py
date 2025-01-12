import dataclasses


@dataclasses.dataclass
class ButtonElement:
    text: str
    action_id: str

def text_section(text: str):
    return {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": text
        }

    }


def button_actions_section(elements: list[ButtonElement]):
    def button_elem(text: str, action_id: str):
        return {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text
            },
            "action_id": action_id
        }

    return {
        "type": "actions",
        "elements": [button_elem(elem.text, elem.action_id) for elem in elements]
    }
