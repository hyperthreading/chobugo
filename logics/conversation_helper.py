from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat
from typing import Literal, List
import json


def analyze_intent(question: str, enums: List[str], message: str) -> str:
    system_prompt = f"""
    {question}
    You will be provided a message as the below format.
    ```json
    {json.dumps([{ "message": "스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같은데, 둘 다 사용법이 비슷하지 않나요?" }])}
    ```
    """

    json_schema: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "intent",
            "strict": True,
            "schema": {
                "type": "object",
                "required": ["reasoning", "intent"],
                "additionalProperties": False,
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "The reasoning behind the conclusion.",
                    },
                    "intent": {
                        "type": "string",
                        "description": "user's intent",
                        "enum": enums
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
    return json.loads(content_json)['intent']


def ask_followup_question(message, count: int) -> List[str]:

    system_prompt = f"""
    You should ask a number of tail questions about the claims they are making.
    The number of questions should be {count}.
    You will be provided a message as the below format.
    ```json
    {json.dumps([{ "message": "스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같은데, 둘 다 사용법이 비슷하지 않나요?" }])}
    ```
    """

    json_schema: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "followup_questions",
            "strict": True,
            "schema": {
                "type": "object",
                "required": ["topic_prediction", "reasoning", "questions"],
                "additionalProperties": False,
                "properties": {
                    "topic_prediction": {
                        "type": "string",
                    },
                    "reasoning": {
                        "type":
                        "string",
                        "description":
                        "The reasoning behind the choice of questions.",
                    },
                    "questions": {
                        "type": "array",
                        "description": "List of questions to get to the point",
                        "items": {
                            "type": "string",
                        }
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
    return json.loads(content_json)['questions']


def get_validity(message):

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

def explain(message: str) -> str:
    system_prompt = f"""
    You should answer their questions in a friendly way and make sure they don't have any more questions.
    You will be provided a message as the below format.
    ```json
    {json.dumps([{ "message": "스택은 데이터를 쌓는 구조고 큐는 아마 뭔가 먼저 넣은 것부터 꺼내는 거 같은데, 둘 다 사용법이 비슷하지 않나요?" }])}
    ```
    """

    json_schema: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "explanation",
            "strict": True,
            "schema": {
                "type": "object",
                "required": ["reasoning", "explanation"],
                "additionalProperties": False,
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "The reasoning behind the conclusion.",
                    },
                    "explanation": {
                        "type": "string",
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
    return json.loads(content_json)['explanation']
