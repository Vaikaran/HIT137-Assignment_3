import pygame as pg
from pygame import Surface
from pygame.key import ScancodeWrapper
from src.resource import Res
from src.img import SpriteSheet
from src import game
from src.encounter import Encounter


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

    # default projectile params
    PROJECTILE_RADIUS = 5
    PROJECTILE_VELOCITY = 6
    PROJECTILE_POWER = 20
    PROJECTILE_COLOR = Res.CYAN
    PROJECTILE_COOLDOWN = 200

    def __init__(self, x, y, width, height, vel, img_frames) -> None:
        self.initialData = (x, y, width, height, vel, img_frames)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.frames = img_frames
        self.bullets: list[Character._projectile] = []
        self.hitbox = (self.x + 12, self.y + 4, 40, 60)
        self.actionCount = 0
        # facing direction based on sprite image: 0-up, 1-left, 2-down, 3-right
        self.facing_diraction = 3
        # action of character: 0-standing, 1-walking, 2-attacking, 3-dying, 4-dead
        self.action = 0
        self.shootCD = _characterBase.PROJECTILE_COOLDOWN
        self.currentCD = self.shootCD
        self.pRadius = _characterBase.PROJECTILE_RADIUS
        self.pColor = _characterBase.PROJECTILE_COLOR
        self.pVelocity = _characterBase.PROJECTILE_VELOCITY
        self.pPower = _characterBase.PROJECTILE_POWER
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
        if self.currentCD > 0:
            self.currentCD -= 1
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

    DEFAULT_SHOOT_CD = 15
    DEFAULT_JUMP_COUNT = 15

    def __init__(self, x, y, width, height, vel, img_frames) -> None:
        super().__init__(x, y, width, height, vel, img_frames)
        self.boundary = (width / 2, game.SCREEN_WIDTH * 3 / 5 - width / 2)
        self.level = 1
        self.update_level_power()
        self.isJump = False
        self.jumpCount = self.DEFAULT_JUMP_COUNT
        self.pColor = Res.PINK_RED
        self.score = 0
        self.encounter = Encounter()
        self.hitSound = pg.mixer.Sound(Res.get("sound", "collision.ogg"))
        self.shootSound = pg.mixer.Sound(Res.get("sound", "projectile1.ogg"))
        self.jumpSound = pg.mixer.Sound(Res.get("sound", "jump.ogg"))
        self.levelUpSound = pg.mixer.Sound(Res.get("sound", "up.ogg"))

    def update_level_power(self):
        self.shootCD = self.DEFAULT_SHOOT_CD - self.level * 2
        self.vel = Res.CHAR_VELOCITY + self.level
        self.pPower = _characterBase.PROJECTILE_POWER + 5 * (self.level - 1)
        self.pRadius = _characterBase.PROJECTILE_RADIUS + 2 * (self.level - 1)

    def handle_keys(self, instance, keys: ScancodeWrapper):
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
                # todo: scroll left on some fight
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
            boundaryR = self.boundary[1]
            if not self.encounter.scrollable(-self.vel):
                boundaryR = game.SCREEN_WIDTH - self.width
            if self.x >= boundaryR:
                if self.encounter.scrollable(-self.vel):
                    instance.scroll(-self.vel)
                    self.encounter.scroll(-self.vel)
            else:
                self.x += self.vel
            if self.action != 1:
                self.actionCount = 0
                self.action = 1
            self.facing_diraction = 3
        else:
            if self.action != 3:
                self.action = 0
                self.actionCount = 0

    def shoot(self):
        if not (self.dying or self.isDead) and not self.currentCD > 0:
            self.bullets.append(
                self._projectile(
                    round(self.x + self.width // 2),
                    round(self.y + self.height // 2),
                    self.pRadius,
                    self.pColor,
                    self.pVelocity,
                    self.facing_diraction,
                    self.pPower,
                )
            )
            self.currentCD = self.shootCD
            if not Res.muted:
                self.shootSound.play()

    def hit_by_bullet(self, enemy: _characterBase, bullet: _characterBase._projectile):
        if self.invulnerableFrames == 0:
            self.health -= bullet.power
            if self.health < 0:
                self.health = 0
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
            if not Res.muted:
                self.hitSound.play()

        pass

    def hit_by_enemy(self, enemy: _characterBase):
        if not (self.dying or self.isDead) and self.invulnerableFrames == 0:
            # -25% hp if hit with enemy
            self.health -= self.maxhealth * 0.25
            if self.health < 0:
                self.health = 0
            self.invulnerableFrames = int(game.FPS * self.INVULNERABLE_DURATION)
            if not Res.muted:
                self.hitSound.play()
        pass

    def update(self):
        super().update()
        # update jump
        if self.isJump:
            if self.jumpCount >= -self.DEFAULT_JUMP_COUNT:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= abs(self.jumpCount) ** 1.3 * 0.8 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = self.DEFAULT_JUMP_COUNT
            pass
        # update level
        level = 1
        if self.score >= 500:
            level = 3
        elif self.score >= 200:
            level = 2
        else:
            level = 1
        # level up
        if self.level < level:
            self.level = level
            self.update_level_power()
            if not Res.muted:
                self.levelUpSound.play()


class Enemy(Character):

    ATTACK_ANIMATE_DURATION = 0.8
    DEFAULT_POINT = 50

    def __init__(
        self, x, y, width, height, vel, img_frames, position, path: tuple, params: dict
    ) -> None:
        super().__init__(x, y, width, height, vel, img_frames)
        self.position = position
        self.path = path
        self.point = Enemy.DEFAULT_POINT
        self.action = 1
        self.facing_diraction = 1
        self.hitSound = pg.mixer.Sound(Res.get("sound", "hit.ogg"))
        self.shootSound = pg.mixer.Sound(Res.get("sound", "projectile2.ogg"))
        self.update_params(params)

    def update_params(self, params: dict):
        if "health" in params:
            self.maxhealth = params["health"]
            self.health = self.maxhealth
        if "velocity" in params:
            self.vel = params["velocity"]
        if "point" in params:
            self.point = params["point"]
        if "shootCD" in params:
            self.shootCD = params["shootCD"]
            self.currentCD = self.shootCD
        if "pRadius" in params:
            self.pRadius = params["pRadius"]
        if "pColor" in params:
            self.pColor = params["pColor"]
        if "pVelocity" in params:
            self.pVelocity = params["pVelocity"]
        if "pPower" in params:
            self.pPower = params["pPower"]
        pass

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
        # skip if not on screen
        if self.x <= 0 or self.x >= game.SCREEN_WIDTH - self.width:
            return
        if not self.currentCD > 0:
            self.bullets.append(
                self._projectile(
                    round(self.x + self.width // 2),
                    round(self.y + self.height // 2),
                    self.pRadius,
                    self.pColor,
                    self.pVelocity,
                    self.facing_diraction,
                    self.pPower,
                )
            )
            self.currentCD = self.shootCD
            if not Res.muted:
                self.shootSound.play()
        pass

    def hit_by_bullet(self, enemy: Player, bullet: _characterBase._projectile):
        if not (self.dying or self.isDead):
            self.health -= bullet.power
            if self.health <= 0:
                enemy.score += self.point
                if not Res.muted:
                    self.hitSound.play()
            else:
                enemy.score += 1
        pass

    def scroll(self, offset):
        self.x += offset

    def update(self):
        self.move()
        self.shoot()
        super().update()
