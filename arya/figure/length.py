

class Length():
    def __init__(self, fixed, strech=0, shrink=0):
        self._fixed = fixed
        self._strech = strech
        self._shrink = shrink

    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass


class Box():
    def __init__(self, width, height):
        self._width = width
        self._height = height


