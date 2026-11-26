"""게임 전체 진행을 담당하는 Game 클래스.

흐름:
    메인 메뉴 → 캐릭터 선택 → 스테이지 선택 → 전투
    - 승리: 다음 스테이지 / 같은 스테이지 반복 중 선택
    - 패배: 이전 스테이지로 돌아가고 HP 회복 후 스테이지 선택 화면으로

외부 모듈 계약 (담당자와 맞춰야 하는 부분):
    characters.player : Warrior, Mage, Archer  (Unit 자식, 인자 없이 생성 가능)
    monsters.monster  : create_monsters(floor) -> list[Monster]
    items.item        : Potion (인자 없이 생성 가능)
    items.inventory   : Inventory()
                        .items                 -> 아이템 목록 복사본 (list)
                        .add_item(item)        -> 아이템 추가
                        .use_item(index, user) -> 성공 True / 실패 False
                                                  (실패 사유는 내부에서 출력)
"""
from characters.player import Archer, Mage, Warrior
from game.battle import Battle, BattleResult
from game.ui import GameQuitRequested, confirm_quit, read_choice
from items.inventory import Inventory
from items.item import Potion
from monsters.monster import create_monsters
from core.exceptions import StageLockedError

MAX_STAGE = 5  # 마지막 스테이지 번호 (이것을 클리어하면 게임 클리어)
CHARACTER_CLASSES = [
    ("전사 (Warrior)", Warrior),
    ("마법사 (Mage)", Mage),
    ("궁수 (Archer)", Archer),
]


class Game:
    """게임의 메뉴, 캐릭터/스테이지 선택, 층 이동, 전투 호출을 통합 관리한다.

    Attributes:
        player: 현재 플레이어 캐릭터 (캐릭터 선택 후 설정)
        inventory: 플레이어 인벤토리
    """

    def __init__(self):
        """게임 상태를 초기화한다. 실제 진행은 run()에서 시작한다."""
        self._player = None
        self._player_max_hp = 0
        self._inventory = None
        self._highest_unlocked = 1   # 지금까지 열린 가장 높은 스테이지
        self._cleared = set()        # 클리어한 스테이지 번호 집합

    # ------------------------------------------------------------------
    # 공개 메서드
    # ------------------------------------------------------------------
    def run(self):
        """메인 메뉴 루프를 실행한다. 종료를 고르거나 입력이 끝나면 반환한다."""
        print("=" * 40)
        print("         DUNGEON ESCAPE")
        print("=" * 40)
        try:
            while True:
                print("\n1. 게임 시작  2. 종료")
                if read_choice("선택: ", 1, 2) == 2:
                    break
                self._new_run()
                self._play_run()
        except GameQuitRequested:
            pass  # 게임 도중 종료를 확정한 경우
        print("게임을 종료합니다.")

    # ------------------------------------------------------------------
    # 게임 진행 흐름
    # ------------------------------------------------------------------
    def _new_run(self):
        """새 게임을 시작할 때 상태를 초기화하고 캐릭터를 고르게 한다."""
        self._select_character()
        self._highest_unlocked = 1
        self._cleared = set()

    def _play_run(self):
        """전투 → 클리어/패배 처리를 반복하다가 게임이 끝나면 반환한다.

        - 승리: 다음 스테이지 또는 같은 스테이지 반복을 고른다.
        - 패배: 이전 스테이지로 자동 이동하고 HP를 회복한 뒤 바로 재도전한다.
        """
        stage = self._select_stage()
        while True:
            result = self._fight(stage)

            if result == BattleResult.LOSE:
                stage = self._on_defeat(stage)
                continue

            self._on_clear(stage)
            if stage == MAX_STAGE:
                print("\n*** 모든 스테이지를 클리어했습니다! 게임 클리어! ***")
                return
            stage = self._choose_next_stage(stage)

    def _select_character(self):
        """캐릭터 목록에서 캐릭터를 고르고 플레이어와 인벤토리를 만든다.

        캐릭터 생성 시 최대 HP를 기록해 두어 패배 후 회복에 사용한다.
        """
        print("\n[캐릭터 선택]")
        for i, (label, _) in enumerate(CHARACTER_CLASSES, start=1):
            print(f"  {i}. {label}")
        index = read_choice("선택: ", 1, len(CHARACTER_CLASSES)) - 1

        _, player_class = CHARACTER_CLASSES[index]
        self._player = player_class()
        self._player_max_hp = self._player.hp

        # 시작 아이템: 포션 1개 (아이템 담당 구현에 맞춰 조정)
        self._inventory = Inventory()
        self._inventory.add_item(Potion())
        print(f"\n{self._player.name}을(를) 선택했습니다.")

    def _select_stage(self):
        """열려 있는 스테이지 목록을 보여 주고 하나를 고르게 한다.

        Returns:
            int: 선택한 스테이지 번호
        """
        print("\n[스테이지 선택]")
        for stage in range(1, self._highest_unlocked + 1):
            mark = "클리어" if stage in self._cleared else "미클리어"
            print(f"  {stage}. 스테이지 {stage} ({mark})")
        print("  0. 게임 종료")
        while True:
            choice = read_choice("스테이지 번호: ", 0, self._highest_unlocked)
            if choice == 0:
                confirm_quit()  # '아니오'면 스테이지 목록으로 돌아간다.
                continue
            return self._check_stage_unlocked(choice)

    def _check_stage_unlocked(self, stage):
        """선택한 스테이지가 열려 있는지 확인한다.

        Args:
            stage (int): 선택한 스테이지 번호

        Returns:
            int: 검증을 통과한 스테이지 번호

        Raises:
            StageLockedError: 아직 열리지 않은 스테이지인 경우
        """
        if not 1 <= stage <= self._highest_unlocked:
            raise StageLockedError(f"스테이지 {stage}은(는) 아직 열리지 않았습니다.")
        return stage

    def _fight(self, stage):
        """해당 스테이지의 몬스터를 만들어 전투를 진행한다.

        몬스터 강도는 create_monsters(stage) 안에서 스테이지에 따라 정해진다.

        Args:
            stage (int): 스테이지 번호

        Returns:
            BattleResult: 전투 결과
        """
        monsters = create_monsters(stage)
        battle = Battle(self._player, monsters, self._inventory, stage)
        return battle.start()

    def _on_clear(self, stage):
        """스테이지 클리어 처리: 클리어 기록과 다음 스테이지 개방.

        Args:
            stage (int): 방금 클리어한 스테이지 번호
        """
        self._cleared.add(stage)
        self._highest_unlocked = max(self._highest_unlocked,
                                     min(stage + 1, MAX_STAGE))
        print(f"\n스테이지 {stage} 클리어!")

    def _choose_next_stage(self, stage):
        """클리어 후 다음 스테이지로 갈지 같은 스테이지를 반복할지 고르게 한다.

        Args:
            stage (int): 방금 클리어한 스테이지 번호

        Returns:
            int: 다음 전투를 진행할 스테이지 번호
        """
        print("\n어떻게 진행할까요?")
        print(f"  1. 다음 스테이지로 (스테이지 {stage + 1})")
        print(f"  2. 같은 스테이지 반복 (스테이지 {stage})")
        print("  3. 게임 종료")
        while True:
            choice = read_choice("선택: ", 1, 3)
            if choice == 1:
                return stage + 1
            if choice == 2:
                return stage
            confirm_quit()  # '아니오'면 같은 선택 화면을 다시 보여 준다.

    def _on_defeat(self, stage):
        """패배 처리: HP를 전부 회복하고 이전 스테이지 번호를 돌려준다.

        Args:
            stage (int): 패배한 스테이지 번호

        Returns:
            int: 다음에 도전할 스테이지 번호 (이전 스테이지, 최소 1)
        """
        previous = max(1, stage - 1)
        print(f"\n패배했습니다. 이전 스테이지({previous})로 돌아갑니다.")
        self._restore_hp()
        return previous

    def _restore_hp(self):
        """플레이어 HP를 최대치로 되돌린다.

        Unit의 HP는 take_damage()로만 바꿔야 하므로, 회복량을 음수 피해로
        전달해 체력을 채운다.
        """
        missing = self._player_max_hp - self._player.hp
        if missing > 0:
            self._player.take_damage(-missing)
