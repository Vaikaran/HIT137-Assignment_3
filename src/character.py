import pygame as pg
from pygame import Surface
from pygame.key import ScancodeWrapper
from src.resource import Res
from src.img import SpriteSheet
from src import game


class Character:
    WALK_IMG_NUM = 10
    ATTACK_IMG_NUM = 12
    DYING_IMG_NUM = 8

    # animation speed: finish total animations within specifc second(s)
    WALK_ANIMATE_DURATION = 1.0
    ATTACK_ANIMATE_DURATION = 0.4
    DYING_ANIMATE_DURATION = 1

    def __init__(self, x, y, width, height, img_path, vel) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.imgSheet = SpriteSheet(pg.image.load(img_path))
        self.frames = self.imgSheet.get_frames(width, height)
        self.vel = vel
        self.actionCount = 0
        # facing direction based on sprite image: 0-up, 1-left, 2-down, 3-right
        self.facing_diraction = 3
        # action of character: 0-standing, 1-walking, 2-attacking, 3-dying
        self.action = 0
        self.isJump = False
        pass

    def draw(self, win: Surface):
        # standing
        if self.action == 0:
            self.actionCount = 0
            win.blit(self.frames[8 + self.facing_diraction][0], (self.x, self.y))
        # walk
        elif self.action == 1:
            self.actionCount %= game.FPS * self.WALK_ANIMATE_DURATION
            win.blit(
                self.frames[8 + self.facing_diraction][
                    int(
                        self.actionCount
                        // (game.FPS * self.WALK_ANIMATE_DURATION / self.WALK_IMG_NUM)
                    )
                    + 1
                ],
                (self.x, self.y),
            )
        # attacking
        elif self.action == 2:
            self.actionCount %= game.FPS * self.ATTACK_ANIMATE_DURATION
            win.blit(
                self.frames[16 + self.facing_diraction][
                    int(
                        self.actionCount
                        // (
                            game.FPS
                            * self.ATTACK_ANIMATE_DURATION
                            / self.ATTACK_IMG_NUM
                        )
                    )
                    + 1
                ],
                (self.x, self.y),
            )
        # dying
        else:
            self.actionCount %= game.FPS * self.DYING_ANIMATE_DURATION
            win.blit(
                self.frames[20][
                    int(
                        self.actionCount
                        // (game.FPS * self.DYING_ANIMATE_DURATION / self.DYING_IMG_NUM)
                    )
                ],
                (self.x, self.y),
            )
        self.actionCount += 1


class Player(Character):
    ATTACK_ANIMATE_DURATION = 0.4

    def __init__(self, x, y, width, height, img_path, vel) -> None:
        super().__init__(x, y, width, height, img_path, vel)
        self.boundary = (width / 2, game.SCREEN_WIDTH / 2 - width / 2)

    def handle_keys(self, keys: ScancodeWrapper, window):
        if keys[pg.K_SPACE]:
            self.isJump = True
        if keys[pg.K_j]:
            if self.action != 2:
                self.actionCount = 0
                self.action = 2
        # elif keys[pg.K_UP] or keys[pg.K_w]:
        #     self.y -= self.vel
        #     if self.action != 1:
        #         self.actionCount = 0
        #         self.action = 1
        #     self.facing_diraction = 0
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.x -= self.vel
            if self.x < self.boundary[0]:
                self.x = self.boundary[0]
                window.scroll_bg(self.vel)

            if self.action != 1:
                self.actionCount = 0
                self.action = 1
            self.facing_diraction = 1
        # elif keys[pg.K_DOWN] or keys[pg.K_s]:
        #     self.y += self.vel
        #     if self.action != 1:
        #         self.actionCount = 0
        #         self.action = 1
        #     self.facing_diraction = 2
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x += self.vel
            if self.x > self.boundary[1]:
                self.x = self.boundary[1]
                window.scroll_bg(-self.vel)
            if self.action != 1:
                self.actionCount = 0
                self.action = 1
            self.facing_diraction = 3
        else:
            if self.action != 3:
                self.action = 0
                self.actionCount = 0


class Enemy(Character):

    ATTACK_ANIMATE_DURATION = 0.8
