"""몬스터 패키지 (담당: 임유빈).

외부에서는 다음과 같이 사용한다:
    from monsters.monster import create_monsters
"""
from monsters.monster import Boss, Goblin, Monster, MonsterError, Slime, create_monsters

__all__ = ["Monster", "Slime", "Goblin", "Boss", "MonsterError", "create_monsters"]
