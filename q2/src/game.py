import pygame as pg

# init pygame
pg.init()

from pygame import Surface
from src.resource import Res
from src.character import Player
from src.character import Enemy

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Window:
    def __init__(self, caption: str):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(caption)

        self.bg_img0 = pg.image.load(Res.get("image", "Mountains1.png"))
        self.bg_img1 = pg.image.load(Res.get("image", "Mountains2.png"))
        self.bg_img2 = pg.image.load(Res.get("image", "Mountains3.png"))
        # scale to screen square size
        self.bg_img = pg.transform.scale(self.bg_img1, (SCREEN_WIDTH, SCREEN_WIDTH))
        self.bg_index = 0

    def draw(self):
        self.screen.blit(
            self.bg_img, (self.bg_index, SCREEN_HEIGHT - self.bg_img.get_height())
        )
        if self.bg_index <= -SCREEN_WIDTH or self.bg_index >= SCREEN_WIDTH:
            self.bg_index = 0
        elif self.bg_index > 0:
            self.screen.blit(
                self.bg_img,
                (
                    self.bg_index - SCREEN_WIDTH,
                    SCREEN_HEIGHT - self.bg_img.get_height(),
                ),
            )
        elif self.bg_index < 0:
            self.screen.blit(
                self.bg_img,
                (
                    self.bg_index + SCREEN_WIDTH,
                    SCREEN_HEIGHT - self.bg_img.get_height(),
                ),
            )
        pass

    def scroll_bg(self, offset):
        self.bg_index += offset


class Game:

    # init game params
    def __init__(self, caption):
        self._run = False
        self.clock = pg.time.Clock()
        self.window = Window(caption)
        Res.init()
        # game status: 0-main menu, 1-in game, 2-gameover
        self.gameStatus = 0
        # init sound/music
        self.music = pg.mixer.music.load(Res.get("sound", "bg1.ogg"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.5)

        # init font
        self.headerFont = pg.font.SysFont("comicsans", 52, True)
        self.menuFont = pg.font.SysFont("comicsans", 26)
        self.statusFont = pg.font.SysFont("comicsans", 22)
        self.descFont = pg.font.SysFont("arial", 20)
        # print(pg.font.get_fonts())

    def run(self):
        self._run = True
        while self._run:
            self.clock.tick(FPS)
            self.handle_events()
            self.handle_keys()
            # draw window
            self.window.draw()
            match self.gameStatus:
                case 0:
                    self.main_menu()
                    pass
                case 1:
                    self.in_game()
                    pass
                case 2:
                    self.gameover()
                    pass
            pg.display.update()
        pass

    def main_menu(self):
        # draw title
        title = self.headerFont.render(
            f"{pg.display.get_caption()[0]}", 1, Res.LIGHT_GREEN
        )
        self.window.screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 120))
        # draw menu

        self.window.screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 120))
        # draw descriptions
        descText = "Press anykey to start \nPress W,A,S,D or ARROW keys to move \nPress SPACE to jump, \nPress J or ENTER to shoot\nPress F1 to mute/unmute"
        textSurfs: list[Surface] = []
        for text in descText.split("\n"):
            textSurfs.append(self.descFont.render(text, 1, Res.BLACK))
        height = 0

        for textSurf in reversed(textSurfs):
            height += textSurf.get_height()
            self.window.screen.blit(textSurf, (40, SCREEN_HEIGHT - height - 14))
        pass

    def in_game(self):
        # create character if none
        if not hasattr(self, "player"):
            self.player = Player(
                80, 420, 64, 64, 4, Res.get("image", "char_universal.png")
            )
        # update score
        statusText = self.statusFont.render(f"Score: {self.player.score}", 1, Res.BLACK)
        self.window.screen.blit(statusText, (40, 14))
        # todo enemies encounters
        if not hasattr(self, "enemies") or not self.enemies:
            self.enemies = [
                Enemy(
                    350,
                    420,
                    64,
                    64,
                    2,
                    (80, SCREEN_WIDTH - 96),
                    Res.get("image", "goblin1_universal.png"),
                )
            ]
        self.player.update()
        self.player.collision_check(self.enemies)
        for index, enemy in enumerate(self.enemies):
            if enemy.isDead:
                self.enemies.pop(index)
            enemy.update()
            enemy.collision_check([self.player])

        # draw characters
        self.player.draw(self.window.screen)
        for enemy in self.enemies:
            enemy.draw(self.window.screen)

    def gameover(self):
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._run = False
                return
            if event.type == pg.KEYUP:
                print(f"event key:{event.key}")
                print(f"f1 key:{pg.K_F1}")
                if event.key == pg.K_F1:
                    if Res.muted:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    Res.muted = not Res.muted
                    return
                # restart game
                if event.key == pg.K_r:
                    self.player.reset()
                    self.gameStatus = 1
                # back to menu
                if event.key == pg.K_ESCAPE:
                    self.gameStatus = 0
                    # todo reset bg, and enemies
            elif event.type == pg.KEYDOWN:
                match self.gameStatus:
                    case 0:
                        # press anykey to start game
                        self.gameStatus = 1
                        return
    pass

    def handle_keys(self):
        keys = pg.key.get_pressed()
        match self.gameStatus:
            case 1:
                if hasattr(self, "player"):
                    self.player.handle_keys(self, keys)
                return
            case 2:
                # restart game
                if keys[pg.K_r]:
                    self.player.reset()
                    self.gameStatus = 1
                    # todo reset bg, and enemies
                if keys[pg.K_ESCAPE]:
                    self.gameStatus = 0
                return
        pass

    def scroll(self, vel):
        self.window.scroll_bg(vel)
        for enemy in self.enemies:
            enemy.scroll(vel)
        pass
