"""
items/item.py
=============
아이템 클래스 모음: Item(부모), Potion(회복 물약), Weapon(무기)

이 파일에서 연습하는 OOP 개념
-----------------------------
1. 상속(Inheritance)   : Potion, Weapon 은 Item 을 상속받아 공통 기능(이름, 가격)을 재사용합니다.
2. 오버라이딩(Overriding): 부모의 use(), __str__() 를 자식 클래스가 자기 방식으로 다시 정의합니다.
3. 캡슐화(Encapsulation): 이름/가격/회복량 등을 __(언더바 2개) 비공개 속성으로 숨기고,
                          @property 로 '읽기'만 허용하거나 setter 에서 값 검증을 합니다.
4. 예외처리(Exception) : 잘못된 값이나 사용할 수 없는 상황에서 사용자 정의 예외를 발생(raise)시킵니다.
"""


# ============================================================
# 사용자 정의 예외는 공통 파일(core/exceptions.py)에서 가져옵니다.
# 이 파일에서 직접 쓰는 것은 ItemUseError 뿐이지만,
# items 패키지 사용자 편의를 위해 아이템 관련 예외를 함께 import 해 둡니다.
# ============================================================
from core.exceptions import ItemError, ItemUseError, InventoryFullError, ItemNotFoundError


# ============================================================
# 부모 클래스: Item
# ============================================================
class Item:
    """모든 아이템의 공통 부모 클래스.

    직접 사용하기보다는 Potion, Weapon 처럼 상속받아서 사용합니다.
    """

    def __init__(self, name, price):
        # __name, __price : 이름 앞에 __ 를 붙이면 '비공개(private)' 속성이 됩니다.
        # 클래스 밖에서 item.__price = -100 처럼 마음대로 바꾸는 것을 막아줍니다.
        # (파이썬 내부적으로 _Item__price 로 이름이 바뀌는 '네임 맹글링' 덕분)
        self.__name = name
        self.price = price  # ← 아래 setter 를 거치므로 값 검증이 자동으로 이루어집니다.

    # ---------- 캡슐화: getter (읽기 전용) ----------
    @property
    def name(self):
        """아이템 이름 (읽기 전용: setter 가 없으므로 수정 불가)"""
        return self.__name

    # ---------- 캡슐화: getter + setter (검증 포함) ----------
    @property
    def price(self):
        """아이템 가격 (상점에서 사용)"""
        return self.__price

    @price.setter
    def price(self, value):
        # setter 에서 잘못된 값을 걸러냅니다 → 객체가 항상 올바른 상태를 유지
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"가격은 0 이상의 정수여야 합니다. (입력값: {value})")
        self.__price = value

    @property
    def is_consumable(self):
        """사용하면 사라지는 아이템인지 여부. 기본값은 True (자식이 오버라이딩 가능)"""
        return True

    # ---------- 오버라이딩 대상 메서드 ----------
    def use(self, target):
        """아이템을 target(캐릭터)에게 사용합니다.

        부모 클래스에서는 '어떻게 사용할지' 모르므로 NotImplementedError 를 발생시킵니다.
        → 자식 클래스가 반드시 이 메서드를 오버라이딩(재정의)해야 한다는 뜻입니다.
        (core/unit.py 의 Unit.attack() 과 같은 방식)
        """
        raise NotImplementedError(f"{self.__class__.__name__} 클래스는 use() 를 구현해야 합니다.")

    def __str__(self):
        """print(item) 했을 때 보여줄 문자열. 자식 클래스에서 오버라이딩합니다."""
        return f"{self.name} ({self.price}G)"


# ============================================================
# 자식 클래스 1: Potion (회복 물약)
# ============================================================
class Potion(Item):  # ← 괄호 안에 부모 클래스를 쓰면 '상속'
    """HP를 회복시키는 물약 (사용하면 사라짐)"""

    def __init__(self, name="회복 물약", price=30, heal_amount=30):
        # super().__init__() : 부모(Item)의 생성자를 호출해서 name, price 설정을 재사용
        super().__init__(name, price)

        if heal_amount <= 0:
            raise ValueError("회복량은 1 이상이어야 합니다.")
        self.__heal_amount = heal_amount  # Potion 만의 비공개 속성

    @property
    def heal_amount(self):
        """회복량 (읽기 전용)"""
        return self.__heal_amount

    # ---------- 오버라이딩: 부모의 use() 를 물약 방식으로 재정의 ----------
    def use(self, target):
        """target 의 HP를 회복시킵니다. 실제로 회복된 양을 반환합니다."""

        # 1) 죽은 대상에게는 사용할 수 없음 → 예외 발생
        if not target.is_alive():
            raise ItemUseError(f"{target.name}은(는) 이미 쓰러져서 물약을 사용할 수 없습니다.")

        # 2) 최대 HP 확인
        #    공통 Unit 클래스에는 max_hp 가 없으므로 getattr 로 '있으면 쓰고, 없으면 None'
        max_hp = getattr(target, "max_hp", None)
        if max_hp is not None and target.hp >= max_hp:
            raise ItemUseError(f"{target.name}의 HP가 이미 가득 찼습니다.")

        # 3) 실제 회복량 계산 (최대 HP를 넘지 않도록)
        amount = self.heal_amount
        if max_hp is not None:
            amount = min(amount, max_hp - target.hp)

        # 4) HP 회복
        #    Unit 의 __hp 는 캡슐화되어 있어서 target.hp = 100 같은 직접 수정이 불가능합니다.
        #    → 캐릭터 담당이 heal() 메서드를 만들었다면 그것을 사용하고,
        #      없다면 take_damage(음수) 로 회복합니다. (HP는 메서드로만 변경 규칙 준수)
        before = target.hp
        if hasattr(target, "heal"):
            target.heal(amount)
        else:
            target.take_damage(-amount)

        healed = target.hp - before
        print(f"🧪 {target.name}이(가) {self.name}을(를) 사용! HP +{healed} (현재 HP: {target.hp})")
        return healed

    # ---------- 오버라이딩: 출력 형식 재정의 ----------
    def __str__(self):
        # super().__str__() 로 부모의 출력 결과를 가져와 뒤에 정보를 덧붙임
        return f"[물약] {super().__str__()} - HP {self.heal_amount} 회복"


# ============================================================
# 자식 클래스 2: Weapon (무기)
# ============================================================
class Weapon(Item):
    """장착하면 공격력(atk)을 올려주는 무기"""

    def __init__(self, name="낡은 검", price=50, atk_bonus=5):
        super().__init__(name, price)

        if atk_bonus <= 0:
            raise ValueError("공격력 보너스는 1 이상이어야 합니다.")
        self.__atk_bonus = atk_bonus

    @property
    def atk_bonus(self):
        """추가 공격력 (읽기 전용)"""
        return self.__atk_bonus

    # ※ is_consumable 은 부모의 기본값(True)을 그대로 상속받습니다.
    #   → 장착한 무기는 캐릭터가 들고 있으므로 인벤토리에서는 빠집니다.

    # ---------- 오버라이딩: 부모의 use() 를 '장착' 동작으로 재정의 ----------
    def use(self, target):
        """target 에게 무기를 장착시켜 공격력을 올립니다. 올라간 공격력을 반환합니다."""
        if not target.is_alive():
            raise ItemUseError(f"{target.name}은(는) 이미 쓰러져서 무기를 장착할 수 없습니다.")

        # Unit 의 atk 는 공개 속성이므로 직접 더할 수 있습니다.
        target.atk += self.atk_bonus
        print(f"⚔️  {target.name}이(가) {self.name}을(를) 장착! 공격력 +{self.atk_bonus} (현재 공격력: {target.atk})")
        return self.atk_bonus

    def __str__(self):
        return f"[무기] {super().__str__()} - 공격력 +{self.atk_bonus}"
