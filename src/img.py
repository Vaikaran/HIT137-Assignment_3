import pygame as pg
from src.resource import Res


class SpriteSheet:
    def __init__(self, image) -> None:
        self.sheet: pg.Surface = image.convert_alpha()

    def get_image(self, width, height, col=0, row=0, scale=1, colorKey=None):
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.sheet, (0, 0), (col * width, row * height, width, height))
        if scale != 1:
            image = pg.transform.scale(image, (width * scale, height * scale))
        if not colorKey:
            image.set_colorkey(colorKey)
        return image.convert_alpha()

    def get_frames(
        self, width, height, horizontal_quantities=-1, vertical_quantities=-1
    ) -> list[list]:
        frames = []
        if not horizontal_quantities >= 0:
            horizontal_quantities = self.sheet.get_width() // width
        if not vertical_quantities >= 0:
            vertical_quantities = self.sheet.get_height() // height
        for row in range(vertical_quantities):
            frames.append(
                [
                    self.get_image(width, height, col, row)
                    for col in range(horizontal_quantities)
                ]
            )
        return frames


class BGSprite(pg.sprite.Sprite):
    def __init__(self, name: str, coordinate: tuple) -> None:
        super().__init__()
        self.image = pg.image.load
