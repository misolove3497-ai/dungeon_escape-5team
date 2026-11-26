"""턴제 전투 루프를 담당하는 Battle 클래스.

한 라운드의 진행 순서:
    1) 플레이어 턴  : 공격 또는 인벤토리(아이템/장비) 사용 중 하나를 선택
    2) 몬스터 턴    : 살아있는 몬스터가 순서대로 플레이어를 공격

플레이어가 모든 몬스터를 쓰러뜨리면 WIN, 플레이어가 쓰러지면 LOSE.
"""
from enum import Enum

from game.ui import confirm_quit, read_choice


class BattleResult(Enum):
    """전투 결과 값."""

    WIN = "win"
    LOSE = "lose"


class Battle:
    """플레이어와 몬스터 무리 사이의 턴제 전투를 진행한다.

    Attributes:
        player: 플레이어 캐릭터 (Unit 자식 클래스 인스턴스)
        monsters (list): 이번 스테이지의 몬스터 목록
        inventory: 플레이어가 가진 Inventory 객체
        stage (int): 현재 스테이지 번호 (화면 표시용)
    """

    def __init__(self, player, monsters, inventory, stage):
        """전투를 준비한다.

        Args:
            player: 플레이어 캐릭터
            monsters (list): 몬스터 목록 (create_monsters 결과)
            inventory: 플레이어 인벤토리
            stage (int): 스테이지 번호
        """
        self._player = player
        self._monsters = list(monsters)
        self._inventory = inventory
        self._stage = stage
        self._round = 0

    def start(self):
        """전투를 시작하고 결과가 날 때까지 라운드를 반복한다.

        Returns:
            BattleResult: 승리(WIN) 또는 패배(LOSE)
        """
        print(f"\n===== 스테이지 {self._stage} 전투 시작 =====")
        while True:
            self._round += 1
            print(f"\n--- 라운드 {self._round} ---")
            self._show_status()

            self._player_turn()
            if not self._alive_monsters():
                print("\n모든 몬스터를 물리쳤습니다!")
                return BattleResult.WIN

            self._monster_turn()
            if not self._player.is_alive():
                print(f"\n{self._player.name}이(가) 쓰러졌습니다...")
                return BattleResult.LOSE

    # ------------------------------------------------------------------
    # 내부 헬퍼
    # ------------------------------------------------------------------
    def _alive_monsters(self):
        """살아있는 몬스터 목록을 반환한다.

        Returns:
            list: 체력이 남아 있는 몬스터들
        """
        return [m for m in self._monsters if m.is_alive()]

    def _show_status(self):
        """플레이어와 몬스터들의 현재 상태를 출력한다."""
        p = self._player
        print(f"[나] {p.name}  HP {p.hp}  ATK {p.atk}")
        for i, m in enumerate(self._alive_monsters(), start=1):
            print(f"  [{i}] {m.name}  HP {m.hp}  ATK {m.atk}")

    def _player_turn(self):
        """플레이어 턴을 처리한다. 공격 또는 아이템 사용 중 하나를 끝낼 때까지 반복한다.

        3번(게임 종료)을 고르고 확인하면 GameQuitRequested가 발생해 전투가 중단된다.
        """
        while True:
            print("\n[내 턴] 1. 공격  2. 인벤토리(아이템/장비)  3. 게임 종료")
            choice = read_choice("선택: ", 1, 3)
            if choice == 1:
                self._do_attack()
                return
            if choice == 3:
                confirm_quit()  # '아니오'면 반환되어 메뉴를 다시 보여 준다.
                continue
            if self._do_inventory():
                return
            # 인벤토리에서 취소한 경우 턴을 넘기지 않고 다시 메뉴를 보여 준다.

    def _do_attack(self):
        """살아있는 몬스터 중 하나를 골라 공격한다. 피해량을 출력한다."""
        targets = self._alive_monsters()
        if len(targets) == 1:
            target = targets[0]
        else:
            print("공격할 대상을 고르세요.")
            for i, m in enumerate(targets, start=1):
                print(f"  {i}. {m.name} (HP {m.hp})")
            target = targets[read_choice("대상 번호: ", 1, len(targets)) - 1]

        before = target.hp
        self._player.attack(target)
        dealt = before - target.hp
        print(f"{self._player.name}의 공격! {target.name}에게 {dealt} 피해를 입혔습니다.")
        if not target.is_alive():
            print(f"{target.name} 처치!")

    def _do_inventory(self):
        """인벤토리에서 아이템/장비를 골라 사용한다.

        Returns:
            bool: 아이템을 실제로 사용해 턴을 소비했으면 True,
                  취소했으면 False
        """
        items = self._inventory.items
        if not items:
            print("인벤토리가 비어 있습니다.")
            return False

        print("\n[인벤토리] 사용할 아이템을 고르세요.")
        for i, item in enumerate(items, start=1):
            print(f"  {i}. {item.name}")
        print("  0. 취소")
        index = read_choice("번호: ", 0, len(items))
        if index == 0:
            return False

        # use_item은 성공 시 True, 실패 시 False를 반환하고 사유를 직접 출력한다.
        # 실패하면 턴을 소비하지 않고 메뉴로 돌아간다.
        return self._inventory.use_item(index - 1, self._player)

    def _monster_turn(self):
        """살아있는 몬스터가 차례로 플레이어를 공격한다."""
        print("\n[몬스터 턴]")
        for monster in self._alive_monsters():
            if not self._player.is_alive():
                break
            before = self._player.hp
            monster.attack(self._player)
            dealt = before - self._player.hp
            print(f"{monster.name}의 공격! {self._player.name}에게 {dealt} 피해"
                  f" (남은 HP {self._player.hp})")
