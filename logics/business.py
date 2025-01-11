from logics.models import User, Message, Session

"""
보낼 메시지 알려줌
"""
def get_messages_to_send(user: User):
    """
        * if (Outsider)
        * Private -> sendCheeringMessage
        * Moderated -> forwardQuestions, suggestForwarding, suggestPostingToGroup 
        * PostingToGroup -> recommendGroupContent, recommendJoiningGroup
        * PrivateGroup -> askBotPosting, askSelfPosting
    """
    pass


def process_received_message(user: User, message: Message):
    pass


def is_new_turn(user: User, message: Message) -> bool:
    return True


"""
질문, 답변 포워딩 로직
"""


def forward_message():
    """
    * 파랑새 메시지 포워딩
        * Outsider 질문 
            * 쉬움 → Outsider 답변
            * 어려움 → Insider 답변
        * Insider 답변 → Outsider
        * Middleware에서 LLM으로 말투 변경
    """
    pass


"""
여기서 점수 계산 ㄱㄱ
"""


def scheduled_analyze():
    for user in get_all_users():
        score = user.get_engagement_score()
        publicity = user.get_publicity()


def get_all_users() -> list[User]:
    return []
