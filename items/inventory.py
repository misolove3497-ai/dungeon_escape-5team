"""
items/inventory.py
==================
Inventory: 캐릭터가 가진 아이템 목록을 관리하는 클래스

이 파일에서 연습하는 OOP 개념
-----------------------------
- 캡슐화 : 아이템 리스트(__items)를 비공개로 숨기고, add/remove/use 메서드로만 조작하게 합니다.
          → 밖에서 inventory.__items.append("아무거나") 같은 잘못된 조작을 막을 수 있습니다.
- 예외처리: 가득 참, 없는 번호, 잘못된 타입 등 상황별로 예외를 raise 하고,
           use_item() 안에서는 try / except / else / finally 구조를 보여줍니다.
- 오버라이딩: 파이썬 내장 메서드(__len__, __str__)를 재정의해서 len(), print() 를 지원합니다.
"""

from items.item import Item
from core.exceptions import ItemError, InventoryFullError, ItemNotFoundError


class Inventory:
    """아이템 보관함"""

    DEFAULT_MAX_SIZE = 10  # 클래스 변수: 모든 인벤토리가 공유하는 기본 최대 칸 수

    def __init__(self, max_size=DEFAULT_MAX_SIZE):
        if max_size <= 0:
            raise ValueError("인벤토리 크기는 1 이상이어야 합니다.")
        self.__items = []          # 비공개: 아이템 목록
        self.__max_size = max_size  # 비공개: 최대 칸 수

    # ---------- 캡슐화: 읽기 전용 프로퍼티 ----------
    @property
    def max_size(self):
        return self.__max_size

    @property
    def items(self):
        """아이템 목록의 '복사본'을 돌려줍니다.

        원본 리스트를 그대로 주면 밖에서 append/remove 로 몰래 바꿀 수 있으므로
        list(...) 로 복사본을 만들어 반환합니다. (캡슐화의 핵심 포인트!)
        """
        return list(self.__items)

    def is_full(self):
        return len(self.__items) >= self.__max_size

    def is_empty(self):
        return len(self.__items) == 0

    # ---------- 아이템 추가 ----------
    def add_item(self, item):
        """아이템을 추가합니다. 실패하면 예외가 발생합니다."""
        # isinstance: Item 또는 Item 을 상속한 자식(Potion, Weapon)인지 확인
        if not isinstance(item, Item):
            raise TypeError(f"Item 객체만 넣을 수 있습니다. (입력: {type(item).__name__})")

        if self.is_full():
            raise InventoryFullError(f"인벤토리가 가득 찼습니다! ({self.__max_size}칸)")

        self.__items.append(item)
        print(f"📦 {item.name}을(를) 획득했습니다.")

    # ---------- 아이템 꺼내기(제거) ----------
    def remove_item(self, index):
        """index 번째 아이템을 인벤토리에서 빼서 반환합니다. (상점 판매 등에 사용)"""
        self.__check_index(index)
        return self.__items.pop(index)

    def get_item(self, index):
        """index 번째 아이템을 제거하지 않고 확인만 합니다."""
        self.__check_index(index)
        return self.__items[index]

    # ---------- 아이템 사용 ----------
    def use_item(self, index, target):
        """index 번째 아이템을 target 에게 사용합니다.

        성공하면 True, 실패하면 False 를 반환합니다.
        (게임이 멈추지 않도록 아이템 관련 예외는 여기서 잡아서 메시지만 출력)
        """
        try:
            item = self.get_item(index)   # 잘못된 번호면 ItemNotFoundError
            item.use(target)              # 사용 불가 상황이면 ItemUseError
                                          # ↑ 다형성: Potion 이면 회복, Weapon 이면 장착
        except ItemError as e:
            # ItemError 의 자식 예외(ItemNotFoundError, ItemUseError ...)는 모두 여기서 잡힙니다.
            print(f"❌ 아이템 사용 실패: {e}")
            return False
        else:
            # else: try 블록에서 예외가 '안 났을 때만' 실행
            if item.is_consumable:
                self.__items.remove(item)
            return True
        finally:
            # finally: 성공/실패와 상관없이 '항상' 실행
            print(f"   (남은 아이템: {len(self.__items)}/{self.__max_size})")

    # ---------- 비공개 메서드 (클래스 내부에서만 사용) ----------
    def __check_index(self, index):
        """번호가 올바른지 검사합니다. 메서드 이름 앞의 __ 도 '외부에서 쓰지 말 것'이라는 의미."""
        if not isinstance(index, int) or not (0 <= index < len(self.__items)):
            raise ItemNotFoundError(f"{index}번 아이템이 없습니다.")

    # ---------- 화면 출력 ----------
    def show(self):
        """인벤토리 목록을 번호와 함께 출력합니다. (사용자는 1번부터 보도록 표시)"""
        print(f"===== 인벤토리 ({len(self.__items)}/{self.__max_size}) =====")
        if self.is_empty():
            print("  (비어 있음)")
        for i, item in enumerate(self.__items, start=1):
            print(f"  {i}. {item}")  # print 시 각 아이템의 오버라이딩된 __str__ 이 호출됨
        print("=" * 30)

    # ---------- 파이썬 내장 메서드 오버라이딩 ----------
    def __len__(self):
        """len(inventory) 를 사용할 수 있게 해줍니다."""
        return len(self.__items)

    def __str__(self):
        """print(inventory) 했을 때 간단한 요약을 보여줍니다."""
        names = ", ".join(item.name for item in self.__items) or "비어 있음"
        return f"Inventory[{len(self.__items)}/{self.__max_size}]: {names}"
