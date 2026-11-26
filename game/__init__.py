"""게임 진행·전투 패키지 (담당: 김경훈).

외부에서는 다음과 같이 사용한다:
    from game import Game
"""
from game.game import Game
from game.battle import Battle, BattleResult

__all__ = ["Game", "Battle", "BattleResult"]
