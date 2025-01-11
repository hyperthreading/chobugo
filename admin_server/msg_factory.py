class MsgFactory:
    def __init__(self):
        self.blocks = []

    def render(self):
        return {
            "blocks": self.blocks
        }

    def attach_text(self, text):
        self.blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text,
            },
        })

    


def msg_factory(level: Level, context: LogContextSchema):
    container_name, text, addr, else_context = context.container_name, context.msg, context.addr, context.else_context
    else_context = json.dumps(else_context)
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*`[{level}]`* {text}",
                },
            }
        ]
    }
