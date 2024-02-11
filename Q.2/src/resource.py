import os.path as ospath
import pygame as pg
from src.img import SpriteSheet


class Res(object):
    BLACK = (0, 0, 0)
    RED = (255, 8, 8)
    PINK_RED = (230, 100, 100)
    CYAN = (100, 230, 230)
    DARK_GRAY = (30, 30, 30)
    GRAY = (100, 100, 100)
    LIGHT_GREEN = "#66CC00"
    GREEN = "#00CC00"
    BLUE = "#3399FF"

    ICON_WIDTH = 32
    ICON_HEIGHT = 32
    CHAR_WIDTH = 64
    CHAR_HEIGHT = 64
    CHAR_VELOCITY = 3
    CHAR_X = 80
    DATUM_Y = 420
    muted = False

    icons: list[list[pg.Surface]] = []
    images: dict[str, list] = {}

    def init():
        Res.icons = SpriteSheet(
            pg.image.load(Res.get("image", "icon_set.png"))
        ).get_frames(Res.ICON_WIDTH, Res.ICON_HEIGHT)

        Res.images = {
            "char": SpriteSheet(
                pg.image.load(Res.get("image", "char_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "goblin1": SpriteSheet(
                pg.image.load(Res.get("image", "goblin1_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "goblin2": SpriteSheet(
                pg.image.load(Res.get("image", "goblin2_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "demon": SpriteSheet(
                pg.image.load(Res.get("image", "demon_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "lizard": SpriteSheet(
                pg.image.load(Res.get("image", "lizard_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "rat": SpriteSheet(
                pg.image.load(Res.get("image", "rat_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
            "rat2": SpriteSheet(
                pg.image.load(Res.get("image", "rat2_universal.png"))
            ).get_frames(Res.CHAR_WIDTH, Res.CHAR_WIDTH),
        }

    def get(path: str, *paths) -> str:
        return ospath.join(ospath.dirname(__file__), "../res", path, *paths)
