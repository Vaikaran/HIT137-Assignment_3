import os.path as ospath
import pygame as pg
from src.img import SpriteSheet


class Res(object):
    BLACK = (0, 0, 0)
    RED = (255, 8, 8)
    DARK_GRAY = (30, 30, 30)
    GRAY = (100, 100, 100)
    LIGHT_GREEN = "#66CC00"
    GREEN = "#00CC00"
    
    muted = False

    icons: list[list[pg.Surface]] = []

    def init():
        Res.icons = SpriteSheet(
            pg.image.load(Res.get("image", "icon_set.png"))
        ).get_frames(32, 32)

    def get(path: str, *paths) -> str:
        return ospath.join(ospath.dirname(__file__), "../res", path, *paths)
