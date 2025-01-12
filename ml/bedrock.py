import requests

BEDROCK_URL = "http://18.234.222.190:5000"
QUESTION_EMBEDDING_URL = f"{BEDROCK_URL}/question-embedding"
QUESTION_CLASSIFIER_URL = f"{BEDROCK_URL}/is-question"

def get_question_embedding(question: str) -> list[float]:
  payload = { 'text': question }

  response = requests.request("GET", QUESTION_EMBEDDING_URL, data=payload)

  return response.json().get("embedding")


def get_is_question(text: str) -> bool:
  payload = { 'text': text }

  response = requests.request("GET", QUESTION_CLASSIFIER_URL, data=payload)
  response_json = response.json()
  print(response_json)
  return response_json
