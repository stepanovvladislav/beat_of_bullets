

class Positions:
    topLeft = 0
    topCentre = 1
    topRight = 2
    centreLeft = 3
    centre = 4
    centreRight = 5
    bottomLeft = 6
    bottomCentre = 7
    bottomRight = 8



class vector2:
    """Used to determine a position, but more explicit than tuples"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, x):
        if type(x) not in (vector2, int, float):
            raise TypeError(
                "can only multiply vector2 by another vector2 or int/floats")
        if type(x) in (int, float):
            return vector2(self.x * x, self.y * x)

        else:
            return vector2(self.x * x.x, self.y * x.y)

    def __str__(self):
        return "Vector2({},{})".format(self.x, self.y)


