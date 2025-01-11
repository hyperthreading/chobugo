from datetime import datetime, timedelta
from typing import List

from logics.models import Session, Message, User, get_today_startdate


class UserScorer(object):
    sessions: List[Session]
    messages: List[Message]
    bot_messages: List[Message]

    def __init__(self, sessions: List[Session], messages: List[Message],
                 bot_messages: List[Message]):
        self.sessions = sessions
        self.messages = messages
        self.bot_messages = bot_messages

    @staticmethod
    def from_user(user: User) -> "UserScorer":
        return UserScorer(user.sessions, user.messages, user.bot_messages)

    def get_engagement_score(
        self,
        start_from: datetime = (get_today_startdate() - timedelta(days=7))
    ) -> float:
        active_frequency_score = self._get_active_frequency_score(start_from)
        responding_latency_score = self._get_responding_latency_score(
            start_from)
        responding_frequency_score = self._get_responding_frequency_score(
            start_from)
        user_starting_message_frequency_score = self._get_user_starting_message_frequency_score(
            start_from)

        return 0.2 * active_frequency_score + 0.2 * responding_latency_score + 0.3 * responding_frequency_score + 0.3 * user_starting_message_frequency_score

    def _get_active_frequency_score(self, start_from: datetime) -> float:
        MAX_ACTIVE_FREQUENCY = 7 * 3  # 3 times a day

        active_session_count = len(
            list(filter(lambda s: (s.created_at >= start_from),
                        self.sessions)))
        active_frequency_score = min(
            active_session_count / MAX_ACTIVE_FREQUENCY, 1)
        return active_frequency_score

    def _get_responding_latency_score(self, start_from) -> float:
        filtered_nudges = self._get_nudging_bot_messages(start_from)

        if len(filtered_nudges) == 0:
            return 0

        responeded_messages = self._get_responded_messages(filtered_nudges)

        MAX_RESPONDING_LATENCY = 7 * 24 * 60

        latency_list = list(
            map(lambda m: m.responded_at - m.created_at, responeded_messages))
        avg_latency = sum(map(lambda d: d.seconds / 60,
                              latency_list)) / len(latency_list)

        return 1 - min(avg_latency / MAX_RESPONDING_LATENCY, 1)

    def _get_responding_frequency_score(self, start_from) -> float:
        filtered_nudges = self._get_nudging_bot_messages(start_from)

        if len(filtered_nudges) == 0:
            return 0

        message_count = len(self._get_responded_messages(filtered_nudges))
        return min(message_count / len(filtered_nudges), 1)

    def _get_user_starting_message_frequency_score(
            self, start_from: datetime) -> float:
        user_starting_messages = self._get_user_starting_messages(start_from)
        if len(user_starting_messages) == 0:
            return 0

        MAX_ACTIVE_FREQUENCY = 7 * 3  # 3 times a day

        return len(user_starting_messages) / MAX_ACTIVE_FREQUENCY

    def _get_nudging_bot_messages(self, start_from: datetime):
        return list(
            filter(lambda m: m.created_at >= start_from and m.is_starting_turn,
                   self.bot_messages))

    def _get_user_starting_messages(self, start_from: datetime):
        return list(
            filter(lambda m: m.created_at >= start_from and m.is_starting_turn,
                   self.messages))

    def _get_responded_messages(
        self,
        messages: List[Message],
    ):
        return list(filter(lambda m: m.responded_at is not None, messages))
