"""프로젝트 공통 사용자 정의 예외 모음.

모든 게임 예외는 GameError를 상속한다. 호출하는 쪽에서는
except GameError 하나로 게임 관련 오류를 한꺼번에 잡을 수 있다.
"""


class GameError(Exception):
    """게임에서 발생하는 모든 사용자 정의 예외의 부모 클래스."""


class InvalidChoiceError(GameError):
    """메뉴에서 허용되지 않은 값을 입력했을 때 발생한다."""


class InventoryError(GameError):
    """인벤토리 조작이 불가능할 때 발생한다 (잘못된 번호, 빈 인벤토리 등)."""


class StageLockedError(GameError):
    """아직 열리지 않은 스테이지를 선택했을 때 발생한다."""
