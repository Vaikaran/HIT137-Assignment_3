import os.path as ospath


class Res(object):
    BLACK = (0, 0, 0)

    def get(path, *paths) -> str:
        return ospath.join(ospath.dirname(__file__), "../res", path, *paths)
