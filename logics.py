from enum import Enum
from typing import List
from datetime import datetime, timedelta
"""
slack_id

activity_segment [Insider, Outsider]

publicity [Private, Moderated, PostingToGroup, PrivateGroup]

sessions
    created_at
    
nudging_messages
    created_at
    
responses
    created_at
"""


class ActivitySegment(Enum):
    Insider = "Insider"
    Outsider = "Outsider"


class SocialPublicityLevel(Enum):
    Private = "Private"
    Moderated = "Moderated"
    PostingToGroup = "PostingToGroup"
    PrivateGroup = "PrivateGroup"


class Session(object):
    created_at: datetime
    user_id: int


class Message(object):
    created_at: datetime
    user_id: int
    message_id: str
    message: str


class NudgingMessage(Message):
    message_id: str
    responded_at: datetime
    responded_by: int


def get_today_startdate():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


class User(object):
    id: int
    slack_id: str
    username: str
    created_at: datetime

    activity_segment: ActivitySegment
    publicity: SocialPublicityLevel
    sessions: List[Session]

    nudging_messages: List[NudgingMessage]
    responses: List[Message]

    def __init__(self, slack_id):
        self.slack_id = slack_id
        self.activity_segment = ActivitySegment.Outsider
        self.publicity = SocialPublicityLevel.Private
        self.sessions = []

    def get_engagement_score(
        self,
        start_from: datetime = (get_today_startdate() - timedelta(days=7))
    ) -> float:
        return 0.2 * self._get_active_frequency_score(
            start_from) + 0.3 * self._get_responding_latency_score(
                start_from) + 0.5 * self._get_responding_frequency_score(
                    start_from)

    def get_publicity(self) -> SocialPublicityLevel:
        """
        * Publicity Promotion
        * promote if EngagementThreshold >= requiredScore(publicity)
            * Threshold { Private: 0, Moderated: 0.36, PostingToGroup: 0.6, PrivateGroup: 0.8 }
        """
        return SocialPublicityLevel.Private

    def _get_active_frequency_score(self, start_from: datetime) -> float:
        MAX_ACTIVE_FREQUENCY = 7 * 3  # 3 times a week

        active_session_count = len(
            list(filter(lambda s: (s.created_at >= start_from),
                        self.sessions)))
        active_frequency_score = min(
            active_session_count / MAX_ACTIVE_FREQUENCY, 1)
        return active_frequency_score

    def _get_responding_latency_score(self, start_from) -> float:
        filtered_nudges = list(
            filter(lambda m: m.created_at >= start_from,
                   self.nudging_messages))

        MAX_RESPONDING_LATENCY = 7 * 24 * 60

        latency_list = list(
            map(lambda m: m.responded_at - m.created_at,
                filter(lambda m: m.responded_at is not None, filtered_nudges)))
        avg_latency = sum(map(lambda d: d.seconds / 60,
                              latency_list)) / len(latency_list)

        return 1 - min(avg_latency / MAX_RESPONDING_LATENCY, 1)

    def _get_responding_frequency_score(self, start_from) -> float:
        filtered_nudges = list(
            filter(lambda m: m.created_at >= start_from,
                   self.nudging_messages))

        message_count = len(
            list(filter(lambda m: m.responded_at is not None,
                        filtered_nudges)))
        return min(message_count / len(filtered_nudges), 1)


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
