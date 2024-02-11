from src import game
from src.resource import Res


class Encounter:
    # distance enemy/item
    # e.g.
    # 500 enemy1
    # 1200 enemy2
    # 1200 enemy3
    # 1500 item1
    # 2100 enemy4
    # 2500 enemy5
    # 2700 item2
    # 3500 enemy6

    ENEMY_VELOCITY_2 = 2
    MAX_DISTANCE = 3500
    ENEMY_PATH = (Res.CHAR_X, game.SCREEN_WIDTH - Res.CHAR_WIDTH - 16)

    def __init__(self) -> None:
        from src.character import Enemy, Collectible

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
                    "shootCD": 250,
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
                    "shootCD": 100,
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
                    "shootCD": 100,
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
                    "point": 100,
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
        self._item_pool = [
            # health boost
            Collectible(
                game.SCREEN_WIDTH,
                Res.DATUM_Y + Res.ICON_HEIGHT,
                Res.ICON_WIDTH,
                Res.ICON_HEIGHT,
                0,
                Res.icons[5][4],
                1500,
                (0, 0),
                {
                    "health": 20,
                },
            ),
            # protect shield
            Collectible(
                game.SCREEN_WIDTH,
                Res.DATUM_Y + Res.ICON_HEIGHT,
                Res.ICON_WIDTH,
                Res.ICON_HEIGHT,
                0,
                Res.icons[5][1],
                2200,
                (0, 0),
                {
                    "invulDuration": 4,
                },
            ),
            # health boost
            Collectible(
                game.SCREEN_WIDTH,
                Res.DATUM_Y + Res.ICON_HEIGHT,
                Res.ICON_WIDTH,
                Res.ICON_HEIGHT,
                0,
                Res.icons[5][4],
                2800,
                (0, 0),
                {
                    "health": 100,
                },
            ),
        ]
        self.enemy_list: list[Enemy] = []
        self.enemy_count = 0
        self.item_list: list[Collectible] = []
        self.item_count = 0
        pass

    def scrollable(self, offset) -> bool:
        for enemy in self.enemy_list:
            if self.distance >= enemy.position:
                if not enemy.dying or not enemy.isDead:
                    return False
        return self.distance - offset > 0

    def scroll(self, offset):
        self.distance -= offset
        # add enemies
        while (
            self._enemy_pool
            and self.enemy_count < len(self._enemy_pool)
            and self._enemy_pool[self.enemy_count].position <= self.distance
        ):
            self.enemy_list.append(self._enemy_pool[self.enemy_count])
            self.enemy_count += 1
        for enemy in self.enemy_list:
            enemy.scroll(offset)

        # add items
        while (
            self._item_pool
            and self.item_count < len(self._item_pool)
            and self._item_pool[self.item_count].position <= self.distance
        ):
            self.item_list.append(self._item_pool[self.item_count])
            self.item_count += 1
        for item in self.item_list:
            item.scroll(offset)

    pass

    def finished(self):
        result = self.distance >= self._enemy_pool[-1].position
        if result:
            for enemy in self.enemy_list:
                result = result and enemy.isDead
        return result
