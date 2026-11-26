from core.unit import Unit

class Player(Unit):
    def __init__(self, name, hp, atk):
        super().__init__(name, hp, atk)
        self.max_hp = hp

    def heal(self, amount):
        """HP를 amount만큼 회복한다 (max_hp를 넘지 않음). 실제 회복량을 반환한다.

        Unit의 __hp는 직접 바꿀 수 없으므로 take_damage(음수)로 HP를 올린다.
        """
        if amount <= 0 or not self.is_alive():
            return 0
        healed = min(amount, self.max_hp - self.hp)
        self.take_damage(-healed)
        return healed


class Warrior(Player):
    def __init__(self, name="전사"):
        super().__init__(name, 150, 12)

    def attack(self, target):
        print(f"{self.name}: 파워 스트라이크! ⚔️")
        target.take_damage(self.atk)


class Mage(Player):
    def __init__(self, name="마법사"):
        super().__init__(name, 90, 8)
        self.__mp = 50

    @property
    def mp(self):
        return self.__mp

    def attack(self, target):
        if self.__mp >= 10:
            self.__mp -= 10
            print(f"{self.name}: 파이어볼!🔥 (MP {self.__mp})")
            target.take_damage(self.atk * 2)
        else:
            print(f"{self.name}: 마나 부족... 지팡이로 툭")
            target.take_damage(self.atk)


class Archer(Player):
    def __init__(self, name="궁수"):
        super().__init__(name, 110, 10)

    def attack(self, target):
        print(f"{self.name}: 연속 사격! 🏹")
        target.take_damage(self.atk)


if __name__ == "__main__":
    dummy = Warrior("허수아비")
    for p in (Warrior(), Mage(), Archer()):
        p.attack(dummy)
        print(f"  → {dummy.name} 체력 {dummy.hp}")

    w = Warrior()
    print(w.max_hp)        # 150
    m = Mage()
    print(m.max_hp)        # 90