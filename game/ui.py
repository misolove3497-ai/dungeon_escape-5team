"""콘솔 입력 공통 헬퍼.

game 패키지의 여러 화면(메뉴, 전투, 스테이지 선택)에서 공통으로 쓰는
숫자 입력 처리를 모아 둔다.
"""
from core.exceptions import InvalidChoiceError


def parse_choice(raw, low, high):
    """문자열을 정수로 바꾸고 허용 범위인지 검사한다.

    Args:
        raw (str): 사용자가 입력한 문자열
        low (int): 허용 최솟값 (포함)
        high (int): 허용 최댓값 (포함)

    Returns:
        int: 검증을 통과한 선택 번호

    Raises:
        InvalidChoiceError: 정수가 아니거나 범위를 벗어난 경우
    """
    try:
        value = int(raw.strip())
    except ValueError:
        raise InvalidChoiceError("숫자를 입력해 주세요.")
    if not low <= value <= high:
        raise InvalidChoiceError(f"{low}~{high} 사이의 번호를 입력해 주세요.")
    return value


def read_choice(prompt, low, high):
    """사용자에게 번호를 입력받는다. 잘못된 입력이면 다시 물어본다.

    Args:
        prompt (str): 입력 프롬프트 문자열
        low (int): 허용 최솟값 (포함)
        high (int): 허용 최댓값 (포함)

    Returns:
        int: 유효한 선택 번호

    Raises:
        EOFError: 입력 스트림이 끝난 경우 (호출한 쪽에서 종료 처리)
    """
    while True:
        try:
            return parse_choice(input(prompt), low, high)
        except InvalidChoiceError as e:
            print(f"[입력 오류] {e}")
