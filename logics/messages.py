from logics.models import MessageText, User, Message
from typing import List
from abc import ABC, abstractmethod
from ml.bedrock import get_is_question, get_is_explanation, get_is_smalltalk, get_answer
from logics.llm import determine_message_type, determine_message_intent, determine_message_validity

# class NudgeMessage(Enum):
#     AskLectureReaction = "AskLectureReaction"
#     SuddenLectureQuiz = "SuddenLectureQuiz"
#     FindConfusingConcepts = "FindConfusingConcepts"
#     QuestionFromOthers = "QuestionFromOthers"
#     PostAnonymizedQuestion = "PostAnonymizedQuestion"
#     SuggestSharingAnswer = "SuggestSharingAnswer"
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

    consumable: bool = False
    proactive: bool = False

    def consume_messages(self, user: User,
                         messages: List[MessageText]) -> TurnProcessingResult:
        raise NotImplementedError()

    def proactive_messages(self, user: User) -> List[MessageText]:
        raise NotImplementedError()

    def is_my_turn(self, user: User, messages: List[MessageText]) -> bool:
        raise NotImplementedError()


class UserMessageTurnRouter(ABC):

    @abstractmethod
    def next_turn(self, messages: List[MessageText]) -> TurnProcessor:
        pass


class TestTurnRouter(UserMessageTurnRouter):

    def next_turn(self, messages: List[MessageText]) -> TurnProcessor:
        print(f"Analyzing messages: {messages[0].message}")
        print(determine_message_intent(messages[0].message))

        if (messages[0].message == "test"):
            return AskReactionTurnProcessor()

        is_question = get_is_question(messages[0].message)
        is_explanation = get_is_explanation(messages[0].message)
        is_smalltalk = get_is_smalltalk(messages[0].message)

        if is_question:
            return FindConfusingConceptsTurnProcessor()
        elif is_explanation:
            return HelpClassmateTurnProcessor()
        elif is_smalltalk:
            return EndTurnTurnProcessor()
        return FindConfusingConceptsTurnProcessor()


class MessageProcessor(object):
    turnRouter: UserMessageTurnRouter
    currentTurnProcessor: TurnProcessor | None

    def __init__(self, turnRouter: UserMessageTurnRouter):
        self.turnRouter = turnRouter
        self.currentTurnProcessor = None

    def process_user_message(self, user: User,
                             message: List[MessageText]) -> List[MessageText]:

        # Testing
        print('intent', determine_message_type(message[0].message))
        print('validity', determine_message_validity(message[0].message))

        rest_message = message
        output_message = []
        if self.currentTurnProcessor is None:
            self.currentTurnProcessor = self.turnRouter.next_turn(rest_message)

        turn_processing_result: TurnProcessingResult | None = None

        while len(rest_message) > 0:

            if turn_processing_result is not None and turn_processing_result.next_turn:
                self.currentTurnProcessor = self.turnRouter.next_turn(
                    rest_message)

            turn_processing_result = self.currentTurnProcessor.consume_messages(
                user, rest_message)
            output_message.extend(turn_processing_result.output_messages)
            rest_message = turn_processing_result.unconsumed_messages

        return output_message

    def trigger_proactive_message(self, user: User,
                                  turn: TurnProcessor) -> List[MessageText]:
        self.currentTurnProcessor = turn
        return turn.proactive_messages(user)


"""
수업 어떘어요
"""


class AskReactionTurnProcessor(TurnProcessor):
    """
    테스트
    """

    def consume_messages(self, user: User,
                         messages: List[MessageText]) -> TurnProcessingResult:
        return TurnProcessingResult([MessageText("수업 어땠어요?")], [], True)

    def proactive_messages(self, user: User) -> List[MessageText]:
        return [MessageText("수업 어땠어요?")]

    def is_my_turn(self, user: User, messages: List[MessageText]) -> bool:
        return messages[0].message == "test"


"""
헷갈리는 거 있으세요?
"""


class FindConfusingConceptsTurnProcessor(TurnProcessor):

    def consume_messages(self, user: User, messages: List[MessageText]):
        get_answer(messages[0].message)
        return TurnProcessingResult([MessageText("아이고 그렇군요 제가 도와드릴게요!")], [],
                                    True)

    def proactive_messages(self, user: User) -> List[MessageText]:
        return [MessageText("요새 헷갈리는 부분은 없으세요?")]

    def is_my_turn(self, user: User, messages: List[MessageText]) -> bool:
        return messages[0].message == "test2"


class HelpClassmateTurnProcessor(TurnProcessor):

    def proactive_messages(self, user: User) -> List[MessageText]:
        return [MessageText("클래스메이트가 도움을 요청하고 있어요 ㅠㅠ 좀 도와주실래요?")]


"""
혹시 질문하고 싶은데, 좀 부담스러우면 제가 한번 조용히 물어볼까요?
"""


class AnonymousQuestionTurnProcessor(TurnProcessor):

    def consume_messages(self, user: User,
                         messages: List[MessageText]) -> TurnProcessingResult:
        return TurnProcessingResult([], [], True)

    def proactive_messages(self, user: User) -> List[MessageText]:
        return [MessageText("혹시 질문하고 싶은데, 좀 부담스러우면 제가 한번 조용히 물어볼까요?")]


"""
저는 잡담에는 소질이 없어요 ㅠㅠ
"""


class EndTurnTurnProcessor(TurnProcessor):

    def consume_messages(self, user: User, messages: List[MessageText]):
        return TurnProcessingResult([MessageText("저는 잡담에는 소질이 없어요 ㅠㅠ")], [],
                                    True)

    def is_my_turn(self, user: User, messages: List[MessageText]) -> bool:
        return messages[0].message == "test2"


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


# """
# 여기서 점수 계산 ㄱㄱ
# """

# def scheduled_analyze():
#     for user in get_all_users():
#         score = user.get_engagement_score()
#         publicity = user.get_publicity()

# def get_all_users() -> list[User]:
#     return []
