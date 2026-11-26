class Unit:
    """모든 전투 유닛(캐릭터, 몬스터)의 부모 클래스.

    HP는 외부에서 직접 바꿀 수 없고 take_damage()로만 변경된다.
    """

    def __init__(self, name, hp, atk):
        """유닛을 생성한다.

        Args:
            name (str): 유닛 이름
            hp (int): 최대/현재 체력
            atk (int): 공격력
        """
        self.name = name
        self.__hp = hp
        self.atk = atk

    @property
    def hp(self):
        """현재 체력을 반환한다 (읽기 전용)."""
        return self.__hp

    def take_damage(self, amount):
        """피해를 받아 체력을 줄인다. 체력은 0 아래로 내려가지 않는다.

        Args:
            amount (int): 받는 피해량
        """
        self.__hp = max(0, self.__hp - amount)

    def is_alive(self):
        """생존 여부를 반환한다.

        Returns:
            bool: 체력이 0보다 크면 True
        """
        return self.__hp > 0

    def attack(self, target):
        """대상을 공격한다. 자식 클래스에서 오버라이딩한다.

        Args:
            target (Unit): 공격 대상

        Raises:
            NotImplementedError: 자식 클래스에서 구현하지 않은 경우
        """
        raise NotImplementedError
