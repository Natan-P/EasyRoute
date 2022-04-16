# hey, you!
# yeah, you reading this.
# good luck reading this and parsing through these variable names.
# you'll need a lot of luck.
# i've added some comments to explain what shit do but still, good luck

import random
import tkinter as tk


def parsePath(i: str, s: int):  # i would NOT advise you to even try to interpret what this is.
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


def parsePos(i2: int, i1: int):  # same comment as before
    x2, y2 = i2 % 6, i2 // 6
    x1, y1 = i1 % 6, i1 // 6
    
    if abs(x1 - x2) != abs(y1 - y2) and not (x1 - x2 == 0 or y1 - y2 == 0):
        return None
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
    
    def __init__(self, window, sizes: list, sqW=50, sqH=50, xPos=None, yPos=None):
        """
         self.size == size of the board, being [X size, Y size]
          self.pos == list of coordinates where you are supposed to land
        self.paths == list of outputted direction strings
        """
        self.squareSize = [sqW, sqH]  # initializes square size to a square
        
        self.size = sizes
        self.cnv = tk.Canvas(window, width=sqW * self.size[0], height=sqH * self.size[1])
        self.cnv.pack()
        self.pos = list()
        
        if xPos is not None:
            self.pos.append(xPos)  # initializes first X coordinate
        else:
            self.pos.append(random.randint(0, self.size[0]))  # or generates a random X start coord if none is provided
        if yPos is not None:
            self.pos[-1] += yPos * 6  # same as before but Y coord
        else:
            self.pos[-1] += random.randint(0, self.size[1]) * 6
        
        self.paths = list()
    
    def generatePath(self, times: list, startPos=None):
        """
        startPos == position to start from
           times == times to repeat, with integers in a list that define how many turns each player takes
        """
        if startPos is not None:
            x, y = startPos % 6, startPos // 6
            # doubles as an x/y coordinate, and as a margin to the top-left edge of the board
        else:
            x, y = self.pos[-1] % 6, self.pos[-1] // 6
        bias = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5]  # RNG bias
        dirs = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]  # thing for direction selection
        f = {"n": {"y": -1, "x": 0},  "ne": {"y": -1, "x": 1},
             "e": {"y": 0,  "x": 1},  "se": {"y": 1,  "x": 1},
             "s": {"y": 1,  "x": 0},  "sw": {"y": 1,  "x": -1},
             "w": {"y": 0,  "x": -1}, "nw": {"y": -1, "x": -1}}
        z = True  # defines whether to do another try of path generation or not
        
        for b in range(len(times)):
            self.paths.append(list())
            for j in range(times[b]):
                while z:
                    rand = random.choice(bias), random.choice(dirs)
                    if -1 < x + f.get(rand[1]).get("x") * rand[0] < self.size[0] and \
                            -1 < y + f.get(rand[1]).get("y") * rand[0] < self.size[1]:
                        self.pos.append(x + rand[0] * f.get(rand[1]).get("x") +
                                        6 * (y + rand[0] * f.get(rand[1]).get("y")))
                        z = False
                        x = x + rand[0] * f.get(rand[1]).get("x")
                        y = y + rand[0] * f.get(rand[1]).get("y")
                        self.paths[b].append(parsePos(self.pos[j], self.pos[j + 1]))
                z = True


win = tk.Tk()
win.title("EasyRoute")
boardSize = [6, 6]
boardIndicators = [["1", "2", "3", "4", "5", "6"],
                   ["A", "B", "C", "D", "E", "F"]]  # how the board is indicated at the sides (1st E-W, 2nd N-S)
directions = ["S", "V", "J", "Z"]  # cardinal direction names of the board (direction definition going ↑→↓←)
baseDirs = ["n", "e", "s", "w"]    # cardinal directions that are used in the code
pathNums = [20, 15, 10, 5]
if __name__ == "__main__":
    # path = "2SV"
    # print(parsePath(path, 13))
    # print(parsePos(13, parsePath(path, 13)))
    brd = Board(win, boardSize)
    # print(brd.pos)
    # print(brd.pos[-1])
    brd.generatePath(times=pathNums)
    print(brd.pos)
    print(brd.paths)
    win.mainloop()
# newBoard(boardSize)
