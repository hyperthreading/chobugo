from scipy.spatial.distance import cosine



"""
input: 질문 - output: text embedding vector
"""
def get_embedding(question: str) -> list[float]:
  return []


"""
db 에 올라가 있는 question 들 임베딩 가져오기 
"""
def get_question_embeddings() -> list[list[float]]:
  return []

def cosine_similarity(a: list[float], b: list[float]) -> float:
  return 1 - cosine(a, b)

"""
input: 질문, threshold 
output: cosine similarity 가 threshold 이하인 질문 리스트
"""
def get_similar_questions(question: str, threshold: float) -> list[str]:

  input_embedding = get_embedding(question)
  similar_questions: list[str] = []
  for question_embedding in get_question_embeddings():
    similarity = cosine_similarity(input_embedding, question_embedding)
    if similarity <= threshold:
      similar_questions.append(question)

  return similar_questions
