import pygame as pg
from pygame import Surface
from pygame.key import ScancodeWrapper
from src.resource import Res
from src.img import SpriteSheet
from src import game


class _characterBase:
    class _projectile:
        def __init__(self, x, y, radius, color, vel, facing, power=10) -> None:
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.facing = facing
            self.power = power
            neg = 1
            if facing == 1:
                neg = -1
            self.vel = vel * neg

        def draw(self, win):
            pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

    WALK_IMG_NUM = 10
    ATTACK_IMG_NUM = 12
    DYING_IMG_NUM = 8

    # animation speed: finish total animations within specifc second(s)
    WALK_ANIMATE_DURATION = 1.0
    ATTACK_ANIMATE_DURATION = 0.4
    DYING_ANIMATE_DURATION = 1

    def __init__(self, x, y, width, height, vel, img_path) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.imgSheet = SpriteSheet(pg.image.load(img_path))
        self.frames = self.imgSheet.get_frames(width, height)
        self.bullets: list[Character._projectile] = []
        self.hitbox = (self.x + 12, self.y + 4, 40, 60)
        self.actionCount = 0
        # facing direction based on sprite image: 0-up, 1-left, 2-down, 3-right
        self.facing_diraction = 3
        # action of character: 0-standing, 1-walking, 2-attacking, 3-dying
        self.action = 0
        self.shootCD = 300
        self.maxhealth = 100
        self.health = self.maxhealth
        self.invulnerableFrames = 0
        pass

    pass


class Character(_characterBase):

    def draw(self, win: Surface):
        # update projectiles
        if self.shootCD > 0:
            self.shootCD -= 1
        for index, bullet in enumerate(self.bullets):
            if bullet.x < game.SCREEN_WIDTH and bullet.x > 0:
                bullet.x += bullet.vel
                bullet.draw(win)
            else:
                self.bullets.pop(index)

        # draw health bar
        pg.draw.rect(win, (255, 8, 8), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pg.draw.rect(
            win,
            (8, 250, 200),
            (
                self.hitbox[0],
                self.hitbox[1] - 20,
                50 - (50 / self.maxhealth) * (self.maxhealth - self.health),
                10,
            ),
        )

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
        # update hitbox
        self.hitbox = (self.x + 12, self.y + 4, 40, 60)

    def collision_check(self, enemies: list[_characterBase]):
        for enemy in enemies:
            if (
                self.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3]
                and self.hitbox[1] + self.hitbox[3] > enemy.hitbox[1]
            ):
                if (
                    self.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]
                    and self.hitbox[0] + self.hitbox[2] > enemy.hitbox[0]
                ):
                    self.hit_by_enemy(enemy)
            result = self.check_bullets(enemy.bullets)
            if result[0]:
                self.hit_by_bullet(enemy, result[1])
            pass
        pass

    def hit_by_enemy(self, enemy: _characterBase):
        pass

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        pass

    def check_bullets(
        self, bullets: list[_characterBase._projectile]
    ) -> tuple[bool, _characterBase._projectile]:
        for bullet in bullets:
            if (
                bullet.y - bullet.radius < self.hitbox[1] + self.hitbox[3]
                and bullet.y + bullet.radius > self.hitbox[1]
            ):
                if (
                    bullet.x + bullet.radius > self.hitbox[0]
                    and bullet.x - bullet.radius < self.hitbox[0] + self.hitbox[2]
                ):
                    bullets.pop(bullets.index(bullet))
                    return True, bullet
        return False, None
    def update(self):
        pass

class Player(Character):
    ATTACK_ANIMATE_DURATION = 0.4
    # invulnerable duration after being damaged
    INVULNERABLE_DURATION = 1

    def __init__(self, x, y, width, height, vel, img_path) -> None:
        super().__init__(x, y, width, height, vel, img_path)
        self.boundary = (width / 2, game.SCREEN_WIDTH / 2 - width / 2)
        self.isJump = False
        self.jumpCount = 15
        self.shootCD = 0

    def draw(self, win: Surface):
        # update jump
        if self.isJump:
            if self.jumpCount >= -15:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= abs(self.jumpCount) ** 1.3 * 0.8 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 15
            pass

        return super().draw(win)

    def handle_keys(self, keys: ScancodeWrapper, game):
        if keys[pg.K_SPACE]:
            self.isJump = True
        if keys[pg.K_j]:
            if self.action != 2:
                self.actionCount = 0
                self.action = 2
            self.shoot()
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
                game.scroll_bg(self.vel)

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
                game.scroll_bg(-self.vel)
            if self.action != 1:
                self.actionCount = 0
                self.action = 1
            self.facing_diraction = 3
        else:
            if self.action != 3:
                self.action = 0
                self.actionCount = 0

    def shoot(self):
        if not self.shootCD > 0:
            self.bullets.append(
                self._projectile(
                    round(self.x + self.width // 2),
                    round(self.y + self.height // 2),
                    5,
                    (230, 100, 100),
                    6,
                    self.facing_diraction,
                )
            )
            self.shootCD = 12

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        if self.invulnerableFrames == 0:
            self.health -= bullet.power
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
        # print("hit by bullet")
            
        pass

    def hit_by_enemy(self, enemy: _characterBase):
        if self.invulnerableFrames == 0:
            # -25% hp if hit with enemy
            self.health -= self.maxhealth * 0.25
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
            print(f"hit by enemy:{enemy}")
        # print(f"hit by enemy:{enemy}")
        pass


class Enemy(Character):

    ATTACK_ANIMATE_DURATION = 0.8

    def __init__(self, x, y, width, height, vel, path: tuple, img_path) -> None:
        super().__init__(x, y, width, height, vel, img_path)
        self.path = path
        self.action = 1
        self.facing_diraction = 1

    def move(self):
        if self.facing_diraction == 1:
            self.x -= self.vel
            if self.x - self.vel < self.path[0]:
                self.facing_diraction = 3
                self.actionCount = 0

        if self.facing_diraction == 3:
            self.x += self.vel
            if self.x + self.vel > self.path[1]:
                self.facing_diraction = 1
                self.actionCount = 0
        pass

    def shoot(self):
        if not self.shootCD > 0:
            self.bullets.append(
                self._projectile(
                    round(self.x + self.width // 2),
                    round(self.y + self.height // 2),
                    5,
                    (100, 230, 230),
                    6,
                    self.facing_diraction,
                )
            )
            self.shootCD = 300
        pass

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        self.health -= bullet.power
        print("hit by bullet")
        pass

    def update(self):
        self.move()
        self.shoot()