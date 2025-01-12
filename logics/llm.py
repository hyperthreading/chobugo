from openai import OpenAI


def determine_message_intent(message):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role":
                "system",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "You should evaluate the message to find user's conversation intention.\nScore fitness of intention among pre-defined conversation intentions, maximum score is 100.\nBelow are the intention presets.\n```json\n[\n    { \"intent\": \"강의 내용 중에 모르는 것을 알고 싶어함\", \"intent_id\":  \"lecture-driven-question\"},\n    { \"intent\": \"강의 내용 중에 헷갈리는 것에 대해 이야기하고 싶어함\" , \"intent_id\":  \"\bconfusion\"},\n    { \"intent\": \"설명하고 있는 내용이 정확하고 사실에 부합함\" , \"intent_id\":  \"clear-answer\"},\n    { \"intent\": \"학습에 어려움을 겪는 학우를 돕고 싶어함\", \"intent_id\":  \"help-willing\"}\n    { \"intent\": \"설명하고 있는 내용이 불분명하거나 정확한 정보가 부족함\" , \"intent_id\":  \"unclear\"},\n    { \"intent\": \"설명하고 있는 내용이 명백하게 틀림\", \"intent_id\":  \"wrong-answer\"}\n    { \"intent\": \"위 intent 중에 해당하는 것 없음\", \"intent_id\":  \"none\"}\n]\n```"
                }]
            },
            {
                "role":
                "user",
                "content": [{
                    "type":
                    "text",
                    "text":
                    f"Evaluate the scores for each below messages.\n{{ \"message\": \"{message}\" }}"
                }]
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "intent_score_list",
                "strict": True,
                "schema": {
                    "type": "object",
                    "required": ["scores"],
                    "properties": {
                        "scores": {
                            "type": "array",
                            "items": {
                                "type":
                                "object",
                                "required": [
                                    "intent_description", "intent_fit_score",
                                    "reason", "intent_id"
                                ],
                                "properties": {
                                    "reason": {
                                        "type": "string"
                                    },
                                    "intent_fit_score": {
                                        "type": "number"
                                    },
                                    "intent_description": {
                                        "type": "string"
                                    },
                                    "intent_id": {
                                        "type": "string"
                                    }
                                },
                                "additionalProperties":
                                False
                            }
                        }
                    },
                    "additionalProperties": False
                }
            }
        },
        temperature=0.67,
        max_completion_tokens=10000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response
