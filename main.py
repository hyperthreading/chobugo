"""
* Business Logic
* 유저별 Segmentation 및 Publicity Scope 저장
    * type UserActivitySeg = Insider | Outsider 
    * type SocialPublicityLevel = Private | Moderated | PostingToGroup | PrivateGroup
* Notification Cronjob → Outsider Nudge
    * Publicity 올라갈수록 순차적으로 액션 추가
    * if (Outsider)
        * Private -> sendCheeringMessage
        * Moderated -> forwardQuestions, suggestForwarding, suggestPostingToGroup 
        * PostingToGroup -> recommendGroupContent, recommendJoiningGroup
        * PrivateGroup -> askBotPosting, askSelfPosting
* Engagement Score 계산
    * 접속 빈도: ActiveFrequency (per week)
    * 답변 속도: RespondingLatency (minutes)
    * 답변 횟수: RespondingFrequency (per week)
    * ActiveFrequencyScore = min(ActiveFrequency / (7 * 3), 1) 
        * 일주일 1번: 0
        * 하루 한번: 0.3
        * 하루 세번: 1
    * RespondingLatencyScore = 1 - min(RespondingLatencyScore / 7 * 24 * 60, 1) 
        * 일주일만에 답변: 0
        * 3일만에 답변: 0.5
        * 1시간만에 답변: ~= 1
    * RespondingFrequencyScore = min(RespondingFrequencyScore / WeeklyMessageCount, 1)
        * 메시지 10개 일 때
        * 1개: 0.1
        * 3개: 0.3 (0.8 정도로 easeOut)
        * 10개: 1
    * Score = 0.2 * ActiveFrequencyScore + 0.3 * RespondingLatencyScore + 0.5 * RespondingFrequencyScore 
* Publicity Promotion
    * promote if EngagementThreshold >= requiredScore(publicity)
        * Threshold { Private: 0, Moderated: 0.36, PostingToGroup: 0.6, PrivateGroup: 0.8 }
* 파랑새 메시지 포워딩
    * Outsider 질문 
        * 쉬움 → Outsider 답변
        * 어려움 → Insider 답변
    * Insider 답변 → Outsider
    * Middleware에서 LLM으로 말투 변경
"""
import 


class User(object):
  def get_engagement_score(self) -> int:
    return 0
  
  def get_publicity(self) -> int:
    return 0
  
"""
보낼 메시지 알려줌
"""
def get_messages_to_send(user: User):
  pass

"""
질문, 답변 포워딩 로직
"""
def forward_message():
  pass

"""
여기서 점수 계산 ㄱㄱ
"""
def scheduled_analyze():
  for user in get_all_users():
    score = user.get_engagement_score()
    publicity = user.get_publicity()


def get_all_users()-> list[User]:
  return []


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