"""
monsters/monster.py
===================
몬스터 클래스 모음: Monster(부모), Slime, Goblin, Boss 와 층별 생성 함수 create_monsters()

이 파일에서 연습하는 OOP 개념
-----------------------------
1. 상속(Inheritance)     : Monster 는 core.unit.Unit 을 상속받고, Slime/Goblin/Boss 는 Monster 를 상속받습니다.
2. 오버라이딩(Overriding): Goblin.attack(), Boss.attack(), Monster.__str__() 을 자식이 자기 방식으로 다시 정의합니다.
3. 캡슐화(Encapsulation) : 층(floor), 공격 횟수는 __ 비공개 속성으로 숨기고, 체력은 Unit 의 take_damage() 로만 바뀝니다.
4. 예외처리(Exception)   : 잘못된 층 번호나 공격 대상이 없을 때 MonsterError 를 발생시킵니다.

층이 올라갈수록 강해지는 방식
-----------------------------
- 능력치: 기본 체력/공격력에 층마다 일정 비율을 곱해 강해집니다. (HP_GROWTH, ATK_GROWTH)
- 구성  : STAGE_TABLE 에서 층마다 나오는 몬스터 종류와 마리 수가 달라집니다.
- 밸런스 수치(BASE_HP, BASE_ATK, *_GROWTH)는 클래스 상단에서 쉽게 조정할 수 있습니다.
"""
from core.exceptions import GameError
from core.unit import Unit

MAX_FLOOR = 5  # 마지막 층 번호 (game/game.py 의 MAX_STAGE 와 같은 값이어야 합니다)


# ============================================================
# 몬스터 관련 예외
# ============================================================
class MonsterError(GameError):
    """몬스터 생성·전투 중 발생하는 오류 (예: 존재하지 않는 층 번호)"""
    pass


# ============================================================
# 부모 클래스: Monster
# ============================================================
class Monster(Unit):
    """모든 몬스터의 공통 부모 클래스.

    자식 클래스는 DISPLAY_NAME, BASE_HP, BASE_ATK 만 정하면
    층(floor)에 따라 강해진 능력치가 자동으로 계산됩니다.
    직접 생성하기보다는 Slime, Goblin, Boss 를 사용합니다.
    """

    DISPLAY_NAME = "몬스터"   # 화면에 표시되는 종류 이름
    BASE_HP = 30              # 1층 기준 기본 체력
    BASE_ATK = 5              # 1층 기준 기본 공격력
    HP_GROWTH = 0.25          # 층이 1 올라갈 때마다 체력이 늘어나는 비율 (25%)
    ATK_GROWTH = 0.15         # 층이 1 올라갈 때마다 공격력이 늘어나는 비율 (15%)

    def __init__(self, name, floor=1):
        """층 번호에 맞춰 강화된 몬스터를 만든다.

        Args:
            name (str): 몬스터 이름 (화면 표시용, 예: "슬라임 1")
            floor (int): 등장하는 층 번호 (1 ~ MAX_FLOOR)

        Raises:
            MonsterError: 층 번호가 정수가 아니거나 범위를 벗어난 경우
        """
        if not isinstance(name, str) or not name.strip():
            raise MonsterError("몬스터 이름은 비어 있지 않은 문자열이어야 합니다.")
        # 비공개 속성: 층 번호는 생성 후 바꿀 수 없습니다.
        self.__floor = _check_floor(floor)
        hp = self._scaled(self.BASE_HP, self.HP_GROWTH)
        atk = self._scaled(self.BASE_ATK, self.ATK_GROWTH)
        super().__init__(name, hp, atk)

    @property
    def floor(self):
        """몬스터가 등장한 층 번호 (읽기 전용)."""
        return self.__floor

    def _scaled(self, base, growth):
        """층에 따른 강화 수치를 계산한다.

        Args:
            base (int): 1층 기준 수치
            growth (float): 층당 증가 비율

        Returns:
            int: 강화된 수치 (반올림)
        """
        return round(base * (1 + growth * (self.__floor - 1)))

    def attack(self, target):
        """대상을 기본 방식으로 공격한다. 자식 클래스에서 오버라이딩할 수 있다.

        Args:
            target (Unit): 공격 대상 (플레이어 캐릭터)

        Raises:
            MonsterError: 공격 대상이 없거나 피해를 받을 수 없는 경우
        """
        if target is None or not hasattr(target, "take_damage"):
            raise MonsterError(f"{self.name}이(가) 공격할 대상이 올바르지 않습니다.")
        target.take_damage(self.atk)

    def __str__(self):
        """몬스터 상태를 한 줄 문자열로 돌려준다."""
        return f"{self.name} (HP {self.hp}, ATK {self.atk})"


# ============================================================
# 자식 클래스: 일반 몬스터
# ============================================================
class Slime(Monster):
    """가장 약한 몬스터. 기본 공격만 한다 (부모 attack 그대로 사용)."""

    DISPLAY_NAME = "슬라임"
    BASE_HP = 25
    BASE_ATK = 4


class Goblin(Monster):
    """몽둥이를 휘두르는 몬스터. attack() 을 오버라이딩해 공격 메시지를 바꾼다."""

    DISPLAY_NAME = "고블린"
    BASE_HP = 40
    BASE_ATK = 7

    def attack(self, target):
        """몽둥이로 공격한다. 공격 연출 메시지를 출력한 뒤 부모 방식으로 피해를 준다.

        Args:
            target (Unit): 공격 대상
        """
        print(f"  {self.name}: 몽둥이를 휘두릅니다!")
        super().attack(target)


# ============================================================
# 자식 클래스: 보스 몬스터
# ============================================================
class Boss(Monster):
    """마지막 층의 보스. 세 번째 공격마다 강타(공격력 1.5배)를 날린다."""

    DISPLAY_NAME = "오거 보스"
    BASE_HP = 60
    BASE_ATK = 8
    HEAVY_EVERY = 3        # 몇 번째 공격마다 강타를 쓸지
    HEAVY_MULTIPLIER = 1.5 # 강타 배율

    def __init__(self, name, floor=1):
        """보스를 만들고 공격 횟수 카운터를 0으로 시작한다.

        Args:
            name (str): 보스 이름
            floor (int): 등장 층 번호
        """
        super().__init__(name, floor)
        self.__attack_count = 0  # 비공개: 외부에서 임의로 바꿀 수 없음

    def attack(self, target):
        """보스 공격. 일정 횟수마다 강타를 하고, 나머지는 기본 공격을 한다.

        Args:
            target (Unit): 공격 대상

        Raises:
            MonsterError: 공격 대상이 올바르지 않은 경우 (부모 attack 에서 검사)
        """
        self.__attack_count += 1
        if self.__attack_count % self.HEAVY_EVERY == 0:
            heavy = round(self.atk * self.HEAVY_MULTIPLIER)
            print(f"  {self.name}: 강타!! ({heavy} 피해 예정)")
            if target is None or not hasattr(target, "take_damage"):
                raise MonsterError(f"{self.name}이(가) 공격할 대상이 올바르지 않습니다.")
            target.take_damage(heavy)
        else:
            super().attack(target)


# ============================================================
# 층별 등장 구성표: 층 번호 -> [(몬스터 클래스, 마리 수), ...]
# 층이 올라갈수록 몬스터 종류가 강해지고 수가 늘어납니다.
# ============================================================
STAGE_TABLE = {
    1: [(Slime, 2)],
    2: [(Slime, 3)],
    3: [(Goblin, 2)],
    4: [(Goblin, 2), (Slime, 1)],
    5: [(Boss, 1), (Goblin, 1)],
}


# ============================================================
# 외부 공개 함수
# ============================================================
def create_monsters(floor):
    """층 번호에 맞는 몬스터 무리를 만들어 목록으로 돌려준다.

    game/game.py 의 Game._fight() 에서 호출합니다.
    같은 종류가 여러 마리면 "슬라임 1", "슬라임 2"처럼 번호를 붙입니다.

    Args:
        floor (int): 스테이지(층) 번호 (1 ~ MAX_FLOOR)

    Returns:
        list[Monster]: 이번 층에 등장하는 몬스터 목록

    Raises:
        MonsterError: 층 번호가 올바르지 않은 경우
    """
    _check_floor(floor)
    monsters = []
    for monster_cls, count in STAGE_TABLE[floor]:
        for i in range(1, count + 1):
            name = monster_cls.DISPLAY_NAME if count == 1 else f"{monster_cls.DISPLAY_NAME} {i}"
            monsters.append(monster_cls(name, floor))
    return monsters


def _check_floor(floor):
    """층 번호가 정수이고 1 ~ MAX_FLOOR 사이인지 검사한다.

    Args:
        floor: 검사할 층 번호

    Returns:
        int: 검증을 통과한 층 번호

    Raises:
        MonsterError: 정수가 아니거나 범위를 벗어난 경우
    """
    if isinstance(floor, bool) or not isinstance(floor, int):
        raise MonsterError(f"층 번호는 정수여야 합니다. (입력값: {floor!r})")
    if not 1 <= floor <= MAX_FLOOR:
        raise MonsterError(f"층 번호는 1~{MAX_FLOOR} 사이여야 합니다. (입력값: {floor})")
    return floor
