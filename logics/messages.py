from logics.models import MessageText, User, Message
from enum import Enum
from typing import List
from abc import ABC, abstractmethod
from bedrock import get_is_question


class NudgeMessage(Enum):
    AskLectureReaction = "AskLectureReaction"
    SuddenLectureQuiz = "SuddenLectureQuiz"
    AskConfusingConcepts = "AskConfusingConcepts"
    QuestionFromOthers = "QuestionFromOthers"
    PostAnonymizedQuestion = "PostAnonymizedQuestion"
    SuggestSharingAnswer = "SuggestSharingAnswer"


"""
대화를 어떤식으로 이끌지 결정
event:message -> process -> say

여기서 새로운 턴 시작하거나, 기존 턴 지속할 수 있음
예를 들어, 답변이 모호한 경우 더 자세히 물어볼 수 있음
연속된 새로운 턴이 발생하는 경도 있음
예) 답변 적었더니 너무 좋아서 다른 넛지 턴 시작하는 경우

case 0. EndTurn
case 1. Message, EndTurn
case 2. Message
case 3. EndTurn, Message (NewTurn)
"""


class TurnProcessingResult(object):
    output_messages: List[MessageText]
    unconsumed_messages: List[MessageText]
    next_turn: bool  # len(unconsumed_messages) > 0 일땐 무조건 True

    def __init__(self, output_messages: List[MessageText],
                 unconsumed_messages: List[MessageText], next_turn: bool):
        self.output_messages = output_messages
        self.unconsumed_messages = unconsumed_messages
        self.next_turn = next_turn


class TurnProcessor(ABC):

    @abstractmethod
    def consume(self, user: User,
                message: List[MessageText]) -> TurnProcessingResult:
        pass


class UserMessageTurnRouter(ABC):

    @abstractmethod
    def next_turn(self) -> TurnProcessor:
        pass


class TestTurnRouter(UserMessageTurnRouter):

    def next_turn(self) -> TurnProcessor:
        return AskReactionTurnProcessor()


class MessageProcessor(object):
    turnRouter: UserMessageTurnRouter
    currentTurnProcessor: TurnProcessor | None

    def __init__(self, turnRouter: UserMessageTurnRouter):
        self.turnRouter = turnRouter
        self.currentTurnProcessor = None

    def process_user_message(self, user: User,
                             message: List[MessageText]) -> List[MessageText]:
        rest_message = message
        output_message = []
        self.currentTurnProcessor = self.turnRouter.next_turn(
        ) if self.currentTurnProcessor is None else self.currentTurnProcessor

        while len(rest_message) > 0:
            turn_processing_result = self.currentTurnProcessor.consume(
                user, rest_message)
            output_message.extend(turn_processing_result.output_messages)
            rest_message = turn_processing_result.unconsumed_messages
            if turn_processing_result.next_turn:
                self.currentTurnProcessor = self.turnRouter.next_turn()

        return output_message

    def trigger_proactive_message(self, turn: TurnProcessor) -> List[Message]:
        return []


class AskReactionTurnProcessor(TurnProcessor):

    def consume(self, user: User,
                message: List[MessageText]) -> TurnProcessingResult:
        return TurnProcessingResult([MessageText("Hello")], [], True)


class AskQuestionTurnProcessor(TurnProcessor):
    pass


class SuggestSharingTurnProcessor(TurnProcessor):
    pass


processor = MessageProcessor(TestTurnRouter())
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
