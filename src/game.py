import pygame as pg
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

        self.bg_img0 = pg.image.load(Res.get("background", "Mountains1.png"))
        self.bg_img1 = pg.image.load(Res.get("background", "Mountains2.png"))
        self.bg_img2 = pg.image.load(Res.get("background", "Mountains3.png"))
        # scale to screen square size
        self.bg_img = pg.transform.scale(self.bg_img0, (SCREEN_WIDTH, SCREEN_WIDTH))
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
        self.player = Player(
            80, 420, 64, 64, Res.get("characters", "char_universal.png"), 4
        )
        self.enemy = Enemy(
            350, 420, 64, 64, Res.get("characters", "goblin1_universal.png"), 3
        )

    def render_game(self):
        self.window.draw()
        self.player.draw(self.window.screen)
        self.enemy.draw(self.window.screen)
        pg.display.update()
        pass

    def run(self):
        self._run = True
        while self._run:
            self.clock.tick(FPS)
            self.handle_events()
            self.handle_keys()
            self.render_game()
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._run = False

    def handle_keys(self):
        keys = pg.key.get_pressed()
        if self.player:
            self.player.handle_keys(keys, self.window)
        pass
