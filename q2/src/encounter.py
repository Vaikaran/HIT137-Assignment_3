from src import game
from src.resource import Res


class Encounter:
    # 500 enemy1
    # 1000 enemy2 / item
    # 1400 enemy3
    # 1800 enemy4
    # 2000 item
    # 3000 boss

    ENEMY_VELOCITY_2 = 2
    MAX_DISTANCE = 3500
    ENEMY_PATH = (Res.CHAR_X, game.SCREEN_WIDTH - Res.CHAR_WIDTH - 16)

    def __init__(self) -> None:
        from src.character import Enemy

        self.distance = 0
        self._enemy_pool = [
            Enemy(
                game.SCREEN_WIDTH,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["goblin1"],
                500,
                Encounter.ENEMY_PATH,
                {
                    "health": 120,
                    "shootCD": 300,
                    "pPower": 50,
                    "point": 60,
                },
            ),
            Enemy(
                game.SCREEN_WIDTH,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["rat"],
                1200,
                Encounter.ENEMY_PATH,
                {
                    "health": 60,
                    "velocity": 4,
                    "pRadius": 4,
                    "pVelocity": 8,
                    "pPower": 20,
                    "shootCD": 120,
                    "point": 80,
                },
            ),
            Enemy(
                game.SCREEN_WIDTH + Res.CHAR_WIDTH + 150,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["rat"],
                1200,
                Encounter.ENEMY_PATH,
                {
                    "health": 60,
                    "velocity": 4,
                    "pRadius": 4,
                    "pVelocity": 8,
                    "pPower": 20,
                    "shootCD": 120,
                    "point": 80,
                },
            ),
            Enemy(
                game.SCREEN_WIDTH + Res.CHAR_WIDTH + 150,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["goblin1"],
                2100,
                Encounter.ENEMY_PATH,
                {
                    "health": 250,
                    "velocity": 3,
                    "pRadius": 6,
                    "pPower": 50,
                    "shootCD": 200,
                    "point": 80,
                },
            ),
            Enemy(
                game.SCREEN_WIDTH + Res.CHAR_WIDTH + 150,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["goblin2"],
                2500,
                Encounter.ENEMY_PATH,
                {
                    "health": 1000,
                    "velocity": 7,
                    "pPower": 20,
                    "shootCD": 100000,
                    "point": 250,
                },
            ),
            Enemy(
                game.SCREEN_WIDTH + Res.CHAR_WIDTH + 150,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Encounter.ENEMY_VELOCITY_2,
                Res.images["lizard"],
                3500,
                Encounter.ENEMY_PATH,
                {
                    "health": 800,
                    "velocity": 4,
                    "pPower": 40,
                    "pVelocity": 9,
                    "pRadius": 7,
                    "pColor": Res.GREEN,
                    "shootCD": 120,
                    "point": 300,
                },
            ),
        ]
        self.encountered_list: list[Enemy] = []
        self.encountered_count = 0
        pass

    def scrollable(self, offset) -> bool:
        for enemy in self.encountered_list:
            if self.distance >= enemy.position:
                if not enemy.dying or not enemy.isDead:
                    return False
        return (
            self.distance - offset > 0 and self.distance < self._enemy_pool[-1].position
        )

    def scroll(self, offset):
        self.distance -= offset
        while (
            self._enemy_pool
            and self.encountered_count < len(self._enemy_pool)
            and self._enemy_pool[self.encountered_count].position <= self.distance
        ):
            self.encountered_list.append(self._enemy_pool[self.encountered_count])
            self.encountered_count += 1
        for enemy in self.encountered_list:
            enemy.scroll(offset)

    pass
