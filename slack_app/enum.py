import enum
import uuid


class EnumResp(enum.Enum):
    positive = "positive"
    negative = "negative"
    incorrect = "incorrect"
    correct = "correct"

    @staticmethod
    def correct_id() -> str:
        """Slack button 에서는 동일한 action id 를 허용하지 않음"""
        return f"{EnumResp.correct.value}:{uuid.uuid1()}"

    @staticmethod
    def incorrect_id() -> str:
        """Slack button 에서는 동일한 action id 를 허용하지 않음"""
        return f"{EnumResp.incorrect.value}:{uuid.uuid1()}"

    def is_correct(self, action_id: str):
        return action_id.startswith(self.correct.value)

    def is_incorrect(self, action_id: str):
        return action_id.startswith(self.incorrect.value)
