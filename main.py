"""게임 실행 시작점.

실행 방법:
    python main.py
"""
from game import Game


def main():
    """게임을 시작한다. Ctrl+C 또는 입력 종료(EOF) 시 안전하게 끝낸다."""
    try:
        Game().run()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")


if __name__ == "__main__":
    main()
