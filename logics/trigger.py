
"""
원래 ScheduledTrigger에서 알맞는 타이밍에 넛지를 트리거해야함
예) 
- 수업이 끝나고 10분 뒤
- 사용자의 active turn이 종료된 상황 (active -> away 등)
"""
class ScheduledTrigger(object):
    pass


"""
어떤 score를 가진 사람이 어떤 메시지를 받아야 하는지 결정함
"""
class TargetUserSelector(object):
    pass


"""
TODO
Messaging Event에 기반해서 자동으로 다음 스텝으로 넛지 트리거 + 프로모션
"""
class AutomatedTrigger(object):
    pass


class TestHTTPTrigger(object):
    pass


