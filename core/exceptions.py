"""
core/exceptions.py
==================
게임 전체에서 사용하는 사용자 정의 예외 모음

왜 예외를 직접 만들까?
---------------------
- ValueError, TypeError 같은 기본 예외만 쓰면 '무슨 오류인지' 구분하기 어렵습니다.
- 클래스로 만들어 두면 except 에서 원하는 오류만 골라 잡을 수 있습니다.
- 예외도 클래스이므로 '상속'으로 계층(족보)을 만들 수 있습니다.

    Exception                (파이썬 기본)
    └── GameError            (우리 게임의 모든 예외)
        └── ItemError        (아이템/인벤토리 관련)
            ├── ItemUseError
            ├── InventoryFullError
            └── ItemNotFoundError

  → except ItemError:  아이템 관련 오류만 잡기
  → except GameError:  게임에서 발생한 모든 오류 잡기

다른 담당자도 필요한 예외를 GameError 를 상속해서 이 파일에 추가하면 됩니다.
예) class NotEnoughGoldError(GameError): ...   # ⑤ 상점 담당
"""


class GameError(Exception):
    """게임에서 발생하는 모든 사용자 정의 예외의 최상위 부모"""
    pass


# ============================================================
# ③ 아이템 · 인벤토리 관련 예외
# ============================================================
class ItemError(GameError):
    """아이템/인벤토리 관련 모든 예외의 부모 클래스"""
    pass


class ItemUseError(ItemError):
    """아이템을 사용할 수 없는 상황 (예: HP가 이미 가득 참, 대상이 사망)"""
    pass


class InventoryFullError(ItemError):
    """인벤토리가 가득 차서 더 넣을 수 없을 때"""
    pass


class ItemNotFoundError(ItemError):
    """없는 아이템(잘못된 번호 등)을 찾으려 할 때"""
    pass
