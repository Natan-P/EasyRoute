# hey, you!
# yeah, you reading this.
# good luck reading this and parsing through these variable names. trust me, i also hate one-letter var names now.
# you'll need a lot of luck.
# i've added some comments to explain what shit do but still, good luck

"""
Basic explanation of the system:
This program mostly uses a single integer, 0-based coordinate system.
This means that there is no X or Y, just a single number.
The coordinates would go as follows, if we had a 3x3 grid:
-------------
| 0 | 1 | 2 |
-------------
| 3 | 4 | 5 |
-------------
| 6 | 7 | 8 |
-------------
There is no real, good reason for this, it is just what I implemented in the beginning, and now half my code is
hard-coded with this system and I will not go around the hassle of re-implementing it with an X/Y coordinate system.
Good luck!
"""

# TODO: refactor into multiple files, refactor one-letter variable names into something readable

import random
import tkinter as tk
import tkinter.ttk as ttk


def parsePath(i: str, s: int):  # edit: returned to the code and realized it is unreadable, added comments
    c = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
    d = [baseDirs[directions.index(x)] for x in i if not (x in c)]  # direction specified in cardinal directions
    n = int("".join([x for x in i if x in c]))  # number of steps to do in a direction
    
    p = {"n": -boardSize[0], "e": 1, "s": boardSize[0], "w": -1}
    
    if n is None:  # if no step is defined, do one step
        n = 1

    y = s
    for i in range(len(d)):  # put it all into my stupid one-integer system for coordinates
        y += (p.get(d[i]) * n)
    
    return y


def parsePos(i1: int, i2: int):  # same comment as before; inverse of the previous function
    x1, y1 = i1 % boardSize[0], i1 // boardSize[1]  # figure out x and y coords of the start and end
    x2, y2 = i2 % boardSize[0], i2 // boardSize[1]

    if abs(x1 - x2) != abs(y1 - y2) and not (x1 - x2 == 0 or y1 - y2 == 0):  # check if this move is possible
        raise Exception(f"sumthin went wrong ({i1} -> {i2}; {x1}, {y1} -> {x2}, {y2})")
    xd, yd = x2 - x1, y2 - y1
    d = str(max(abs(xd), abs(yd)))
    if d == "0":
        d = ""
    
    if yd < 0:
        d += directions[0]
    elif yd > 0:
        d += directions[2]
    if xd < 0:
        d += directions[3]
    elif xd > 0:
        d += directions[1]
    
    return d


class Board:
    """
    Class which houses all the board generation and position functions.
    """

    def __init__(self, window, sizes: list, sqW=50, sqH=50, xPos=None, yPos=None):
        """
         self.size == size of the board, being [X size, Y size]
          self.pos == list of coordinates where you are supposed to land
        self.paths == list of outputted direction strings
        """
        self.squareSize = [sqW, sqH]  # initializes square size to a square
        self.size = sizes

        self.linesToDraw = list()

        self.mainframe = ttk.Frame(window, padding=(3, 3, 3, 3))
        self.mainframe.grid(column=0, row=0)

        self.cnv = tk.Canvas(self.mainframe, width=sqW * self.size[0] + 1, height=sqH * self.size[1] + 1)
        self.cnv.grid(column=0, row=0)

        self.buttonframe = ttk.Frame(window)
        self.buttonframe.grid(column=1, row=0)
        self.randVal = tk.BooleanVar(value=True)
        self.newButton = ttk.Button(self.buttonframe, text="New Game",
                                    command=lambda: self.onNewGame(times=pathNums, rand=self.randVal))
        self.newButton.grid(column=0, row=0)
        self.randomCheck = tk.BooleanVar()
        self.newRandomCheck = ttk.Checkbutton(self.buttonframe, text="Randomize Start Position?", variable=self.randVal)
        self.newRandomCheck.grid(column=1, row=0)
        self.resizeButton = ttk.Button(self.buttonframe, text="Resize Map",
                                       command=lambda: self.onResize())
        self.resizeButton.grid(column=0, row=1)
        self.pos = list()

        if xPos is not None:
            self.pos.append(xPos)  # initializes first X coordinate

        else:
            self.pos.append(random.randint(0, self.size[0]-1))
        if yPos is not None:
            self.pos[-1] += yPos * sizes[0]  # same as before but Y coord

        else:
            self.pos[-1] += random.randint(0, self.size[1]-1) * sizes[0]

        self.paths = list()
        self.generatePath(times=pathNums)

    def initCanvas(self, canvas: tk.Canvas, draw: bool = True, size: list = None, sq: list = None):
        if sq is None:
            sq = self.squareSize
        if size is None:
            size = self.size
        canvas.config(width=sq[0] * size[0] + 1, height=sq[1] * size[1] + 1)
        canvas.delete("all")
        for j in range(size[0]):  # board has sizes[0] vertical squares + right border
            for z in range(size[1]):  # board has sizes[1] horizontal squares + bottom border
                canvas.create_rectangle(sq[0] * j + 2, sq[1] * z + 2,
                                        sq[0] * (j + 1) + 2, sq[1] * (z + 1) + 2, tags="grid")
        if draw:
            self.centeredCircle(canvas, self.linesToDraw[0][0] % size[0],
                                self.linesToDraw[0][0] // size[1], fill="blue")
            self.drawPath()

    def generatePath(self, times: list, startPos: int = None):
        """
        startPos == position to start from
           times == times to repeat, with integers in a list that define how many turns each player takes
        """

        self.linesToDraw = list()

        if startPos is not None:
            x, y = startPos % self.size[0], startPos // self.size[1]
            # doubles as an x/y coordinate, and as a margin to the top-left edge of the board

        else:
            x, y = self.pos[-1] % self.size[0], self.pos[-1] // self.size[1]
        bias = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5]  # RNG bias
        dirs = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]  # thing for direction selection
        f = {"n": {"y": -1, "x": 0}, "ne": {"y": -1, "x": 1},
             "e": {"y": 0, "x": 1}, "se": {"y": 1, "x": 1},
             "s": {"y": 1, "x": 0}, "sw": {"y": 1, "x": -1},
             "w": {"y": 0, "x": -1}, "nw": {"y": -1, "x": -1}}
        z = True  # defines whether to do another try of path generation or not
        flag = False  # draw a flag on this line (set to true if it's the last step of the sequence)

        for b in range(len(times)):
            self.paths.append(list())
            for j in range(times[b]):
                while z:
                    rand = random.choice(bias), random.choice(dirs)
                    if -1 < x + f.get(rand[1]).get("x") * rand[0] < self.size[0] and \
                            -1 < y + f.get(rand[1]).get("y") * rand[0] < self.size[1]:
                        endPos = x + rand[0] * f.get(rand[1]).get("x") + \
                                 self.size[0] * (y + rand[0] * f.get(rand[1]).get("y"))
                        self.pos.append(endPos)
                        self.paths[b].append(parsePos(self.pos[j + b * times[b]], self.pos[j + b * times[b] + 1]))
                        if j == times[b] - 1:
                            flag = True
                        self.linesToDraw.append((x + y * self.size[0], endPos, flag))
                        flag = False
                        z = False
                        x = x + rand[0] * f.get(rand[1]).get("x")
                        y = y + rand[0] * f.get(rand[1]).get("y")
                z = True
        self.initCanvas(self.cnv)

    def drawPath(self):
        for i in self.linesToDraw:
            assert type(i) == tuple
            self.drawPathLine(i[0], i[1], i[2])

    def drawPathLine(self, p1: int, p2: int, flag=False, clr="black"):
        """
          p1 == position 1 (starting point)
          p2 == position 2 (ending point)
        flag == whether to draw a (rudimentary) flag at the end or not
        """
        f, j = self.size[0], self.size[1]  # shorthands, no other purpose

        x1, y1, = \
            p1 % f * self.squareSize[0] + .5 * self.squareSize[0], \
            p1 // j * self.squareSize[1] + .5 * self.squareSize[1]
        x2, y2 = \
            p2 % f * self.squareSize[0] + .5 * self.squareSize[0], \
            p2 // j * self.squareSize[1] + .5 * self.squareSize[1]
        self.cnv.create_line(x1, y1, x2, y2, fill=clr, arrow="last", tags=("line", "arrow", clr))
        if flag:
            self.flag(self.cnv, x2, y2, fill="cyan")

    def onNewGame(self, times: list, rand: tk.BooleanVar):
        def newGameCommand(e, scaleVar: tk.IntVar, x, y):
            scaleVar.set(round(float(e)))
            canvas.delete("circle")
            self.centeredCircle(canvas, x.get()-1, y.get()-1, fill="blue")

        xPos, yPos = None, None

        if not rand.get():
            prompt = tk.Toplevel()
            frm = ttk.Frame(prompt)
            frm.grid(column=0, row=0)

            topScaleVar = tk.IntVar(value=1)
            botScaleVar = tk.IntVar(value=1)
            dummy = tk.IntVar()  # god help me, what made me think this is okay
                                 # oh wait, it works, everything is okay and i do not care

            canvas = tk.Canvas(frm)
            canvas.grid(column=1, row=1)
            self.initCanvas(canvas, draw=False)

            newGameCommand(1, dummy, topScaleVar, botScaleVar)

            topScale = ttk.Scale(frm, orient="horizontal", length=self.squareSize[0]*self.size[0],
                                 from_=1, to=self.size[0], variable=topScaleVar,
                                 command=lambda x: newGameCommand(x, topScaleVar, topScaleVar, botScaleVar))
            topScale.grid(column=1, row=0)
            botScale = ttk.Scale(frm, orient="vertical", length=self.squareSize[1]*self.size[1],
                                 from_=1, to=self.size[1], variable=botScaleVar,
                                 command=lambda y: newGameCommand(y, botScaleVar, topScaleVar, botScaleVar))
            botScale.grid(column=0, row=1)

            btn = ttk.Button(frm, command=lambda: prompt.destroy(), text="Done", width=5)
            btn.grid(column=0, row=0)

            prompt.wait_window(prompt)

            xPos, yPos = topScaleVar.get()-1, botScaleVar.get()-1

            self.cnv.delete("line||flag||circle")
        self.pos = list()

        if xPos is not None:  # literally just reused code, read comments from line 84
            self.pos.append(xPos)
        else:
            self.pos.append(random.randint(0, self.size[0]-1))
        if yPos is not None:
            self.pos[-1] += yPos * self.size[0]
        else:
            self.pos[-1] += random.randint(0, self.size[1]-1) * self.size[0]

        self.paths = list()
        self.generatePath(times=times)

    def onResize(self):
        def resizeDo(this, x):
            pass
        prompt = tk.Toplevel()
        frm = ttk.Frame(prompt, padding=3)
        frm.grid()
        lbl = ttk.Label(frm, text="Input the size of a square (px)")
        lbl.grid(column=0, row=0, columnspan=2)
        inp = tk.IntVar(value=50)
        box = ttk.Spinbox(frm, from_=10, to=100, increment=5, textvariable=inp)
        scl = ttk.Scale(frm, from_=10, to=100, variable=inp, length=200)
        box.grid(column=0, row=1)
        scl.grid(column=1, row=1)

    #   ### Drawing Utils ###

    def centeredCircle(self, canvas: tk.Canvas, x, y, r: int = 5, color: str = "black", fill: str = ""):
        return canvas.create_oval(x * self.squareSize[0] + .5 * self.squareSize[0] - r,
                                  y * self.squareSize[1] + .5 * self.squareSize[1] - r,
                                  x * self.squareSize[0] + .5 * self.squareSize[0] + r,
                                  y * self.squareSize[1] + .5 * self.squareSize[1] + r,
                                  tags="circle", outline=color, fill=fill)

    def flag(self, canvas: tk.Canvas, x, y, color: str = "black", fill: str = ""):
        canvas.create_polygon([x-5, y+10, x-5, y-10, x+5, y-5, x-5, y], tags="flag", outline=color, fill=fill)


win = tk.Tk()
win.title("EasyRoute")
boardSize = [7, 6]
boardIndicators = [["1", "2", "3", "4", "5", "6"],
                   ["A", "B", "C", "D", "E", "F"]]  # how the board is indicated at the sides (1st E-W, 2nd N-S)
directions = ("S", "V", "J", "Z")  # cardinal direction names of the board (direction definition going ↑→↓←)
baseDirs = ("n", "e", "s", "w")  # cardinal directions that are used in the code
# note that the hardcoded directions will always be lowercase and output will always be uppercase in the code
# the output shown to the user will be formatted later
pathNums = [20, 15, 10, 5]
if __name__ == "__main__":
    # path = "2SV"
    # print(parsePath(path, 13))
    # print(parsePos(13, parsePath(path, 13)))
    brd = Board(win, boardSize, sqW=50, sqH=50)
    print(brd.pos)
    print(brd.paths)
    win.mainloop()
# newBoard(boardSize)
