python 콘솔로 게임을 구현하려고 해

팀 역활
1. 캐릭터 담당 김재철
2. 몬스터 담당 임유빈
3. 아이템,인벤토리 담당 김도언(강사님)
4. 게임 진행 및 전투 담당 김경훈

요구사항
1. 캡슐화, 오버라이딩, 상속, 예외처리가 되어 있어야 하고 함수 주석은 잘 달아줘
2. 실행 방법 main.py 실행
3. 캐릭터 목록 -> 캐릭터 선택 -> 스테이지 선택 
4. Stage 를 깼을 때 같은 스테이지를 반복할 지 다음 스테이지를 넘어갈 지 고를수 있도록 하고 싶어
5. 스테이지가 올라갈 수록 몬스터는 쌔지는 방식
6. 몬스터를 깨면 다음 스테이지로 넘어가고 스테이지를 깨지못하면 이전 스테이지로 돌아가기
7. 전투는 턴제 방식으로 진행하고 캐릭터 순서일 때 인벤토리를 확인해서 장비 및 아이템 사용을 할 수 있어


해당 프로젝트 디렉토리
dungeon_escape/
├── main.py                  # ④ 실행 시작점 (python main.py)
├── README.md                # 팀 전체: 팀원/역할, 실행 방법
│
├── core/                    # 공통 (강사 제공, 수정 시 팀 합의)
│   ├── __init__.py
│   ├── unit.py              # Unit 부모 클래스
│   └── exceptions.py        # 사용자 정의 예외 모음
│
├── characters/              # ① 캐릭터 담당
│   ├── __init__.py
│   └── player.py            # Warrior, Mage, Archer
│
├── monsters/                # ② 몬스터 담당
│   ├── __init__.py
│   └── monster.py           # Slime, Goblin, Boss, create_monsters(floor)
│
├── items/                   # ③ 아이템·인벤토리 담당
│   ├── __init__.py
│   ├── item.py              # Item, Potion, Weapon
│   └── inventory.py         # Inventory
│
├── game/                    # ④ 게임 진행·전투 담당
│   ├── __init__.py
│   ├── game.py              # Game (메뉴, 층 이동, 통합)
│   └── battle.py            # Battle (턴제 전투 루프)
│
├── shop/                    # ⑤ 상점·기록 담당 (5인 팀만)
│   ├── __init__.py
│   ├── shop.py              # Shop
│   └── record.py            # 플레이 기록, 랭킹
│
└── data/                    # ⑤ (5인 팀만)
    └── records.txt          # 랭킹 저장 파일

# Unit 부모 클래스
unit.py
class Unit:
    def __init__(self, name, hp, atk):
        self.name = name
        self.__hp = hp
        self.atk = atk

    @property
    def hp(self):
        return self.__hp

    def take_damage(self, amount):   # HP는 이 메서드로만 변경
        self.__hp = max(0, self.__hp - amount)

    def is_alive(self):
        return self.__hp > 0

    def attack(self, target):        # 자식 클래스에서 오버라이딩
        raise NotImplementedError

