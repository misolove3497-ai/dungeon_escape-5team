class Unit:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def attack(self, target):
        target.take_damage(self.atk)

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)
        print(f"  → {self.name} 체력 {self.hp}")

class Warrior(Unit):
    def __init__(self, name):
        super().__init__(name, 150, 12)

    def attack(self, target):
        print(f"{self.name}: 파워 스트라이크! ⚔️")
        super().attack(target)
class Mage(Unit):
    def __init__(self, name):
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
            super().attack(target)
            

if __name__ == "__main__":
    dummy = Warrior("허수아비")
    w = Warrior("전사")
    w.attack(dummy)
