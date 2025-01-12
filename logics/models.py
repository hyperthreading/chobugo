from datetime import datetime
from enum import Enum
from typing import List
from replit import db
from uuid import uuid4
from pydantic import BaseModel, field_serializer


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


class Message(BaseModel):
    created_at: datetime
    user_id: int
    message_id: str
    message: str
    responded_at: datetime | None
    responded_by: str | None
    continued_by: str | None
    is_starting_turn: bool

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        # Customize the output as needed
        return value.isoformat()  # e.g. drop microseconds


class MessageText(object):
    message: str

    def __init__(self, message) -> None:
        self.message = message


def get_today_startdate():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


class User(BaseModel):
    id: int
    slack_id: str
    username: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        # Customize the output as needed
        return value.isoformat()  # e.g. drop microseconds

    # activity_segment: ActivitySegment
    # publicity: SocialPublicityLevel
    # sessions: List[Session]

    bot_messages: List[Message]
    messages: List[Message]

    @staticmethod
    def mock_data():
        return User(id=0,
                    slack_id="user1",
                    username="user1",
                    created_at=get_today_startdate(),
                    bot_messages=[],
                    messages=[])

    @staticmethod
    def create(slack_id: str):
        return User(id=0,
                    slack_id=slack_id,
                    username=slack_id,
                    created_at=get_today_startdate(),
                    bot_messages=[],
                    messages=[])

    def add_messages(self, message_text_list: List[MessageText],
                     is_starting_turn: bool):
        self.messages.extend(
            self._build_message_text_list(message_text_list, None, None,
                                          is_starting_turn))

        UserRepository.save_user(self)

    def add_bot_messages(self, message_text_list: List[MessageText],
                         is_starting_turn: bool):
        self.bot_messages.extend(
            self._build_message_text_list(message_text_list, None, None,
                                          is_starting_turn))

        UserRepository.save_user(self)

    def get_chat_history_with_bot(self):
        return sorted(self.messages + self.bot_messages,
                      key=lambda m: m.created_at)

    def _build_message_text_list(self, message_text_list: List[MessageText],
                                 responded_at: datetime | None,
                                 responded_by: str | None,
                                 is_starting_turn: bool):
        result = []
        prev_message_id = None
        for message_text in message_text_list:
            message_id = str(uuid4())

            result.append(
                Message(
                    created_at=datetime.now(),
                    user_id=self.id,
                    message_id=message_id,
                    message=message_text.message,
                    responded_at=None,
                    responded_by=None,
                    continued_by=prev_message_id,
                    is_starting_turn=True,
                ))
            prev_message_id = message_id

        return result


_user_cache: dict[str, User] = {}


class UserRepository(object):

    @staticmethod
    def get_user(slack_id: str) -> User | None:
        user_json = db.get(slack_id, None)
        if user_json is None:
            return None
        return User(**user_json)

    @staticmethod
    def create_or_get_user(slack_id: str) -> User:
        user = UserRepository.get_user(slack_id)
        if user is not None:
            return user
        user = User.create(slack_id)
        db[slack_id] = user.model_dump()
        return user

    @staticmethod
    def save_user(user: User):
        _user_cache[user.slack_id] = user
        db[user.slack_id] = user.model_dump()
