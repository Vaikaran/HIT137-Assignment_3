import pygame as pg

# init pygame
pg.init()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

from pygame import Surface
from src.resource import Res
from src.character import Player
from src.character import Enemy


class Window:
    def __init__(self, caption: str):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(caption)

        self.bg_img0 = pg.image.load(Res.get("image", "Mountains1.png"))
        self.bg_img1 = pg.image.load(Res.get("image", "Mountains2.png"))
        self.bg_img2 = pg.image.load(Res.get("image", "Mountains3.png"))
        # scale to screen square size
        self.bg_img = pg.transform.scale(self.bg_img2, (SCREEN_WIDTH, SCREEN_WIDTH))
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
        # game status: 0-main menu, 1-in game, 2-gameover/finished
        self._gameStatus = 0
        # init sound/music
        self.music = pg.mixer.music.load(Res.get("sound", "bg2.ogg"))
        self.gameoverSound = pg.mixer.Sound(Res.get("sound", "gameover.ogg"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.5)

        # init font
        self.headerFont = pg.font.SysFont("comicsans", 52, True)
        self.hintFont = pg.font.SysFont("comicsans", 26)
        self.statusFont = pg.font.SysFont("comicsans", 22)
        self.descFont = pg.font.SysFont("arial", 20)
        # print(pg.font.get_fonts())

        self.player: Player = None

    @property
    def gameStatus(self):
        return self._gameStatus

    @gameStatus.setter
    def gameStatus(self, status):
        if status == 2 and self._gameStatus != status:
            if self.player.isDead:
                self.gameoverSound.play()
        self._gameStatus = status

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
                    self.gameend()
                    pass
            pg.display.update()
        pass

    def main_menu(self):
        # draw title
        title = self.headerFont.render(
            f"{pg.display.get_caption()[0]}", 1, Res.LIGHT_GREEN
        )
        self.window.screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 120))
        # draw hint
        hint = self.hintFont.render("Press anykey to start", 1, Res.GREEN)
        self.window.screen.blit(
            hint,
            (SCREEN_WIDTH / 2 - hint.get_width() / 2, 120 + title.get_height() + 40),
        )
        # draw descriptions
        descText = "Press anykey to start \nPress A,D or ARROW keys to move \nPress SPACE to jump, \nPress J or ENTER to shoot\nPress F1 to mute/unmute"
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
        if not self.player:
            img = Res.get("image", "char_universal.png")
            self.player = Player(
                Res.CHAR_X,
                Res.DATUM_Y,
                Res.CHAR_WIDTH,
                Res.CHAR_HEIGHT,
                Res.CHAR_VELOCITY,
                Res.images["char"],
            )
        # update score
        statusText = f"Score: {self.player.score:<{len(str(self.player.score))+7}}Level:{self.player.level}"
        statusSurf = self.statusFont.render(statusText, 1, Res.BLACK)
        self.window.screen.blit(statusSurf, (40, 14))
        # gameover if player dead
        if self.player.isDead:
            self.gameStatus = 2
        # end if finished
        if self.player.encounter.finished():
            self.gameStatus = 2
        # update player
        self.player.update()
        # draw characters
        self.player.draw(self.window.screen)

    def gameend(self):
        # draw title
        if self.player.isDead:
            title = self.headerFont.render("Gameover", 1, Res.RED)
        else:
            title = self.headerFont.render("Congratulations", 1, Res.BLUE)
        self.window.screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 120))
        score = self.hintFont.render(
            f"Your score: {self.player.score}", 1, Res.LIGHT_GREEN
        )

        self.window.screen.blit(
            score,
            (SCREEN_WIDTH / 2 - score.get_width() / 2, 120 + title.get_height() + 40),
        )
        hint = self.hintFont.render("Press R to restart the game", 1, Res.GREEN)
        self.window.screen.blit(
            hint,
            (
                SCREEN_WIDTH / 2 - hint.get_width() / 2,
                120 + title.get_height() + 40 + score.get_height() + 20,
            ),
        )
        self.window.screen.blit(
            self.hintFont.render("Press ESC to return to the menu", 1, Res.GREEN),
            (
                SCREEN_WIDTH / 2 - hint.get_width() / 2,
                120
                + title.get_height()
                + 40
                + score.get_height()
                + 20
                + hint.get_height()
                + 15,
            ),
        )
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._run = False
                return
            if event.type == pg.KEYUP:
                if event.key == pg.K_F1:
                    if Res.muted:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    Res.muted = not Res.muted
                    return
                if self.gameStatus == 2:
                    self.player.reset()
                    # restart game
                    if event.key == pg.K_r:
                        self.gameStatus = 1
                        # todo reset bg, and enemies
                    else:
                        # back to menu
                        self.gameStatus = 0
                    return
                if self.gameStatus == 0:
                    # press anykey to start game
                    self.gameStatus = 1
                    pass

    pass

    def handle_keys(self):
        keys = pg.key.get_pressed()
        match self.gameStatus:
            case 1:
                if self.player:
                    self.player.handle_keys(self, keys)
                return
        pass

    def scroll(self, vel):
        self.window.scroll_bg(vel)
        pass
