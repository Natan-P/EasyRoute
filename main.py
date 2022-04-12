import random


def parsePath(i: str, s: int):
    c = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
    t = [baseDirs[directions.index(x)] for x in i if not (x in c)]
    n = int("".join([x for x in i if x in c]))

    p = {"n": -boardSize, "e": 1, "s": boardSize, "w": -1}

    if n is None:
        n = 1

    y = s
    for i in range(len(t)):
        y += (p.get(t[i]) * n)

    return y


def parsePos(i2: int, i1: int):
    x2, y2 = i2 % 6, i2 // 6
    x1, y1 = i1 % 6, i1 // 6

    if abs(x1 - x2) != abs(y1 - y2) and not (x1 - x2 == 0 or y1 - y2 == 0):
        raise Exception(f"Path does not follow the Chess Queen's movement ({x1}, {x2} → {y1}, {y2} is invalid)")
    xd, yd = x1 - x2, y1 - y2
    r = str(max(abs(xd), abs(yd)))
    if r == "0":
        r = ""

    if yd < 0:
        r += directions[0]
    elif yd > 0:
        r += directions[2]
    if xd < 0:
        r += directions[3]
    elif xd > 0:
        r += directions[1]

    return r


class Board:
    """
    Board class which houses all the board generation and position functions.
    """

    def __init__(self, x, y):
        self.size = x, y
        self.pos = [13]
        self.paths = list()

    def generatePath(self, b: bool, p, t):
        x, y = p % 6, p // 6  # doubles as an x/y coordinate, and as a margin to the top-left edge of the board
        bias = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5]  # RNG bias
        dirs = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        f = {"n": {"y": -1, "x": 0},  "ne": {"y": -1, "x": 1},
             "e": {"y": 0,  "x": 1},  "se": {"y": 1,  "x": 1},
             "s": {"y": 1,  "x": 0},  "sw": {"y": 1,  "x": -1},
             "w": {"y": 0,  "x": -1}, "nw": {"y": -1, "x": -1}}
        z = True
        i = t
        if b:
            i = 1
        for j in range(i):
            while z:
                rand = random.choice(bias), random.choice(dirs)
                if x - 1 <= x + rand[0] * f.get(rand[1]).get("x") < self.size[0] and \
                   y - 1 <= y + rand[0] * f.get(rand[1]).get("y") < self.size[1]:
                    self.pos.append(x + rand[0] * f.get(rand[1]).get("x") + 6 * (y + rand[0] * f.get(rand[1]).get("y")))
                    z = False
                    x = x + rand[0] * f.get(rand[1]).get("x")
                    y = y + rand[0] * f.get(rand[1]).get("y")
                    self.paths.append(parsePos(self.pos[j], self.pos[j + 1]))
            z = True


boardSize = 6
boardIndicators = [["1", "2", "3", "4", "5", "6"],
                   ["A", "B", "C", "D", "E", "F"]]  # how the board is indicated at the sides (1st E-W, 2nd N-S)
directions = ["S", "V", "J", "Z"]  # cardinal direction names of the board (direction definition going ↑→↓←)
baseDirs = ["n", "e", "s", "w"]    # cardinal directions that are used in the code
pathNums = [20, 15, 10, 5]
if __name__ == "__main__":
    path = "2SV"
    print(parsePath(path, 13))
    print(parsePos(13, parsePath(path, 13)))
    brd = Board(6, 6)
    brd.generatePath(False, 13, 4)
    print(brd.pos)
    print(brd.paths)
# newBoard(boardSize)
