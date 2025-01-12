import requests
import json

BEDROCK_URL = "http://18.234.222.190:5000"
QUESTION_EMBEDDING_URL = f"{BEDROCK_URL}/question-embedding"
QUESTION_CLASSIFIER_URL = f"{BEDROCK_URL}/is-question"
EXPLANATION_CLASSIFIER_URL = f"{BEDROCK_URL}/is-explanation"
SMALLTALK_CLASSIFIER_URL = f"{BEDROCK_URL}/is-smalltalk"
ANSWER_URL = f"{BEDROCK_URL}/answer"

def get_question_embedding(question: str) -> list[float]:
  payload = { 'text': question }

  response = requests.request("GET", QUESTION_EMBEDDING_URL, data=payload)

  return response.json().get("embedding")


def get_is_question(text: str) -> bool:
  params = {"text": text}

  response = requests.get(QUESTION_CLASSIFIER_URL, params=params)
  print(response.json())
  return response.json().get("is_question")

def get_is_explanation(text: str) -> bool:
  params = {"text": text}

  response = requests.get(EXPLANATION_CLASSIFIER_URL, params=params)
  print(response.json())
  return response.json().get("is_explanation")

def get_is_smalltalk(text: str) -> bool:
  params = {"text": text}

  response = requests.get(SMALLTALK_CLASSIFIER_URL, params=params)
  print(response.json())
  return response.json().get("is_smalltalk")

def get_answer(question: str) -> str:
  params = { "question": question }
  response = requests.get(ANSWER_URL, params=params)
  print(response.json())
  return response.json().get("answer")