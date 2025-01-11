from datetime import datetime
from enum import Enum
from typing import List, Dict, Any


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
    responded_at: datetime
    responded_by: int
    continued_by: int
    is_starting_turn: bool


class MessageText(object):
    message: str

    def __init__(self, message) -> None:
        self.message = message


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

    bot_messages: List[Message]
    messages: List[Message]

    def __init__(self, slack_id):
        self.slack_id = slack_id
        self.activity_segment = ActivitySegment.Outsider
        self.publicity = SocialPublicityLevel.Private
        self.sessions = []
