from openai import OpenAI
from typing import Literal
import json


def determine_message_intent(message):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role":
                "system",
                "content":
                "You should evaluate the message to find user's conversation intention.\n"
                "Score fitness of intention among pre-defined conversation intentions, maximum score is 100.\n"
                "Below are the intention presets.\n"
                "```json\n"
                "[\n"
                "    { \"intent\": \"강의 내용 중에 모르는 것을 알고 싶어함\", \"intent_id\":  \"lecture-driven-question\"},\n"
                "    { \"intent\": \"강의 내용 중에 헷갈리는 것에 대해 이야기하고 싶어함\", \"intent_id\":  \"confusion\"},\n"
                "    { \"intent\": \"어떤 내용에 대한 설명을 하고 있음\", \"intent_id\":  \"description\"},\n"
                "    { \"intent\": \"학습에 어려움을 겪는 학우를 돕고 싶어함\", \"intent_id\":  \"help-willing\"},\n"
                "    { \"intent\": \"위 intent 중에 해당하는 것 없음\", \"intent_id\":  \"none\"}\n"
                "]\n"
                "```"
            },
            {
                "role":
                "user",
                "content":
                f"Evaluate the scores for each below messages.\n{{ \"message\": \"{message}\" }}"
            },
        ],
        # response_format={
        #     "type": "json_schema",
        #     "json_schema": {
        #         "name": "intent_score_list",
        #         "strict": True,
        #         "schema": {
        #             "type": "object",
        #             "required": ["scores"],
        #             "properties": {
        #                 "scores": {
        #                     "type": "array",
        #                     "items": {
        #                         "type":
        #                         "object",
        #                         "required": [
        #                             "intent_description", "intent_fit_score",
        #                             "reason", "intent_id"
        #                         ],
        #                         "properties": {
        #                             "reason": {
        #                                 "type": "string"
        #                             },
        #                             "intent_fit_score": {
        #                                 "type": "number"
        #                             },
        #                             "intent_description": {
        #                                 "type": "string"
        #                             },
        #                             "intent_id": {
        #                                 "type": "string"
        #                             }
        #                         },
        #                         "additionalProperties":
        #                         False
        #                     }
        #                 }
        #             },
        #             "additionalProperties": False
        #         }
        #     }
        # },
        temperature=0.67,
        max_completion_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    content_json = response.choices[0].message.content
    return content_json
    if content_json:
        # intent_id = ""
        # max_score = 0
        # for intent in json.loads(content_json)['scores']:
        #     if max_score < intent['intent_fit_score']:
        #         intent_id = intent['intent_id']
        #         max_score = intent['intent_fit_score']
        # return intent_id
        return json.loads(content_json)['scores']


def determine_message_validity(message):

    system_prompt = f"""
    You should evaluate the validity of the message provided by the user. The user is a student in a lecture.
    You will be provided a message as the below format.
    ```json
    {json.dumps([{ "message": "스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같은데, 둘 다 사용법이 비슷하지 않나요?" }])}
    ```
    """

    json_schema: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "required": ["topic_prediction", "reasoning", "score"],
                "additionalProperties": False,
                "properties": {
                    "topic_prediction": {
                        "type": "string",
                    },
                    "reasoning": {
                        "type": "string",
                    },
                    "score": {
                        "type": "number",
                        "description": "score from min 0 to max 100"
                    }
                }
            }
        }
    }

    client = OpenAI()

    response = client.chat.completions.create(model="gpt-4o",
                                              messages=[
                                                  {
                                                      "role":
                                                      "system",
                                                      "content": [{
                                                          "type":
                                                          "text",
                                                          "text":
                                                          system_prompt
                                                      }]
                                                  },
                                                  {
                                                      "role":
                                                      "user",
                                                      "content": [{
                                                          "type":
                                                          "text",
                                                          "text":
                                                          json.dumps([{
                                                              "message":
                                                              message
                                                          }])
                                                      }]
                                                  },
                                              ],
                                              response_format=json_schema,
                                              temperature=0.67,
                                              max_completion_tokens=10000,
                                              top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0)
    content_json = response.choices[0].message.content
    if content_json:
        # intent_id = ""
        # max_score = 0
        # for intent in json.loads(content_json)['scores']:
        #     if max_score < intent['intent_fit_score']:
        #         intent_id = intent['intent_id']
        #         max_score = intent['intent_fit_score']
        # return intent_id
        return json.loads(content_json)['score']


def determine_message_type(
    message
) -> Literal["explanation"] | Literal["question"] | Literal["other"]:

    system_prompt = f"""
    You should classify the message's intent provided by the user in the three class.
    The three class includes "explanation", "question", and "other".
    You will be provided a message as the below format.
    ```json
    {json.dumps([{ "message": "스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같은데, 둘 다 사용법이 비슷하지 않나요?" }])}
    ```
    """

    json_schema: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "required": ["topic_prediction", "reasoning", "class"],
                "additionalProperties": False,
                "properties": {
                    "topic_prediction": {
                        "type": "string",
                    },
                    "reasoning": {
                        "type": "string",
                    },
                    "class": {
                        "type": "string",
                        "enum": ["explanation", "question", "other"],
                    }
                }
            }
        }
    }

    client = OpenAI()

    response = client.chat.completions.create(model="gpt-4o",
                                              messages=[
                                                  {
                                                      "role":
                                                      "system",
                                                      "content": [{
                                                          "type":
                                                          "text",
                                                          "text":
                                                          system_prompt
                                                      }]
                                                  },
                                                  {
                                                      "role":
                                                      "user",
                                                      "content": [{
                                                          "type":
                                                          "text",
                                                          "text":
                                                          json.dumps([{
                                                              "message":
                                                              message
                                                          }])
                                                      }]
                                                  },
                                              ],
                                              response_format=json_schema,
                                              temperature=0.67,
                                              max_completion_tokens=10000,
                                              top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0)
    content_json = response.choices[0].message.content
    if content_json:
        # intent_id = ""
        # max_score = 0
        # for intent in json.loads(content_json)['scores']:
        #     if max_score < intent['intent_fit_score']:
        #         intent_id = intent['intent_id']
        #         max_score = intent['intent_fit_score']
        # return intent_id
        return json.loads(content_json)['class']


def scoring_message(message):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "system",
            "content": [{
                "type":
                "text",
                "text":
                "Evaluate the correctness of the following explanation on a scale from 0 (wrong) to 100 (clearly correct).  Also evaluate confidence score of explanation. input_explanation should be summary of explanation, in korean."
            }]
        }, {
            "role":
            "user",
            "content": [{
                "type":
                "text",
                "text":
                "Evaluate the scores for each messages.\n{ \"message\": \"스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같다.\" }\n{ \"message\": \"1+5는 7일지도 모른다.\" }\n{ \"message\": \"분명히 해는 서쪽에서 뜬다.\" }"
            }]
        }],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "correctness_score_list",
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
                                    "input_explanation", "correctness_score",
                                    "confidence_score"
                                ],
                                "properties": {
                                    "input_explanation": {
                                        "type": "string"
                                    },
                                    "correctness_score": {
                                        "type": "number"
                                    },
                                    "confidence_score": {
                                        "type": "number"
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
