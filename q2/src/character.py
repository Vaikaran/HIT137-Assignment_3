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
        self.initialData = (x, y, width, height, vel, img_path)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.frames = SpriteSheet(pg.image.load(img_path)).get_frames(width, height)
        self.bullets: list[Character._projectile] = []
        self.hitbox = (self.x + 12, self.y + 4, 40, 60)
        self.actionCount = 0
        # facing direction based on sprite image: 0-up, 1-left, 2-down, 3-right
        self.facing_diraction = 3
        # action of character: 0-standing, 1-walking, 2-attacking, 3-dying, 4-dead
        self.action = 0
        self.shootCD = 300
        self.maxhealth = 100
        self.health = self.maxhealth
        self.invulnerableFrames = 0

    @property
    def dying(self):
        return self.action == 3

    @property
    def isDead(self):
        return self.action > 3


class Character(_characterBase):

    def draw(self, win: Surface):
        # draw projectiles
        for index, bullet in enumerate(self.bullets):
            if bullet.x < game.SCREEN_WIDTH and bullet.x > 0:
                bullet.x += bullet.vel
                bullet.draw(win)
            else:
                self.bullets.pop(index)

        # draw health bar
        # skip draw health bar if dead
        if not self.isDead:
            pg.draw.rect(
                win, Res.DARK_GRAY, (self.hitbox[0], self.hitbox[1] - 20, 50, 8), 0, 2
            )
            pg.draw.rect(
                win,
                Res.RED,
                (
                    self.hitbox[0],
                    self.hitbox[1] - 20,
                    50 - (50 / self.maxhealth) * (self.maxhealth - self.health),
                    8,
                ),
                0,
                2,
            )
        skipDrawing = False
        # blink while invulnerable
        if self.invulnerableFrames > 0:
            if self.invulnerableFrames % 11 < 6:
                # skip drawing character in current frame
                skipDrawing = True
                pass

        # standing
        if self.action == 0:
            self.actionCount = 0
            not skipDrawing and win.blit(
                self.frames[8 + self.facing_diraction][0], (self.x, self.y)
            )
        # walk
        elif self.action == 1:
            self.actionCount %= game.FPS * self.WALK_ANIMATE_DURATION
            not skipDrawing and win.blit(
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
            not skipDrawing and win.blit(
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
        elif self.action == 3:
            if self.actionCount >= game.FPS * self.DYING_ANIMATE_DURATION:
                self.action = 4
                pass
            if self.dying:
                not skipDrawing and win.blit(
                    self.frames[20][
                        int(
                            self.actionCount
                            // (
                                game.FPS
                                * self.DYING_ANIMATE_DURATION
                                / self.DYING_IMG_NUM
                            )
                        )
                    ],
                    (self.x, self.y),
                )
        self.actionCount += 1

    def collision_check(self, enemies: list[_characterBase]):
        if self.dying or self.isDead:
            return
        for enemy in enemies:
            if enemy.dying or enemy.isDead:
                continue
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

    # calling super is manditory otherwise some actions might not work correctly
    def update(self):

        # check health status
        if self.action > 3:
            return
        if self.health <= 0:
            self.die()
        # update shooting cooldown
        if self.shootCD > 0:
            self.shootCD -= 1
        # update hitbox
        self.hitbox = (self.x + 12, self.y + 4, 40, 60)
        # update invulnerable status
        if self.invulnerableFrames > 0:
            self.invulnerableFrames -= 1
        pass

    def die(self):
        # update action status
        if self.action < 3:
            self.action = 3
            self.actionCount = 0

    def reset(self):
        self.__init__(*self.initialData)


class Player(Character):
    ATTACK_ANIMATE_DURATION = 0.4
    # invulnerable duration after being damaged
    INVULNERABLE_DURATION = 1

    def __init__(self, x, y, width, height, vel, img_path) -> None:
        super().__init__(x, y, width, height, vel, img_path)
        self.boundary = (width / 2, game.SCREEN_WIDTH * 3 / 4 - width / 2)
        self.isJump = False
        self.jumpCount = 15
        self.shootCD = 0
        self.score = 0

        self.hitSound = pg.mixer.Sound(Res.get("sound", "collision.ogg"))
        self.shootSound = pg.mixer.Sound(Res.get("sound", "projectile1.ogg"))
        self.jumpSound = pg.mixer.Sound(Res.get("sound", "jump.ogg"))

    def handle_keys(self, game, keys: ScancodeWrapper):
        # skip actions after die
        if self.dying or self.isDead:
            return
        # jump
        if keys[pg.K_SPACE]:
            if not self.isJump:
                if not Res.muted:
                    self.jumpSound.play()
            self.isJump = True
        # shoot
        if keys[pg.K_j] or keys[pg.K_RETURN]:
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
                # scroll right only
                # game.scroll(self.vel)

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
                game.scroll(-self.vel)
            if self.action != 1:
                self.actionCount = 0
                self.action = 1
            self.facing_diraction = 3
        else:
            if self.action != 3:
                self.action = 0
                self.actionCount = 0

    def shoot(self):
        if not (self.dying or self.isDead) and not self.shootCD > 0:
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
            if not Res.muted:
                self.shootSound.play()

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        if self.invulnerableFrames == 0:
            self.health -= bullet.power
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
            if not Res.muted:
                self.hitSound.play()

        pass

    def hit_by_enemy(self, enemy: _characterBase):
        if not (self.dying or self.isDead) and self.invulnerableFrames == 0:
            # -25% hp if hit with enemy
            self.health -= self.maxhealth * 0.25
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
            if not Res.muted:
                self.hitSound.play()
        pass

    def update(self):
        super().update()
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


class Enemy(Character):

    ATTACK_ANIMATE_DURATION = 0.8

    def __init__(self, x, y, width, height, vel, path: tuple, img_path) -> None:
        super().__init__(x, y, width, height, vel, img_path)
        self.path = path
        self.action = 1
        self.facing_diraction = 1
        self.hitSound = pg.mixer.Sound(Res.get("sound", "hit.ogg"))
        self.shootSound = pg.mixer.Sound(Res.get("sound", "projectile2.ogg"))

    def move(self):
        if self.dying or self.isDead:
            return
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
        if self.dying or self.isDead:
            return
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
            if not Res.muted:
                self.shootSound.play()
        pass

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        if not (self.dying or self.isDead):
            self.health -= bullet.power
            if self.health <= 0:
                if not Res.muted:
                    self.hitSound.play()
        pass

    def scroll(self, offset):
        self.x += offset

    def update(self):
        self.move()
        self.shoot()
        super().update()
        # delete enemy if it is behind left of the screen
        if self.x + self.width < -game.SCREEN_WIDTH // 3:
            self.die()
