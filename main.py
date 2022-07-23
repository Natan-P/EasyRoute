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
import tkinter.messagebox as msgbox


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


def parsePos(i1: int, i2: int, dirs: tuple = None, num: bool = True):  # inverse of the previous function
    if dirs is None:
        dirs = directions
    x1, y1 = i1 % boardSize[0], i1 // boardSize[0]  # figure out x and y coordinates of the start and end
    x2, y2 = i2 % boardSize[0], i2 // boardSize[0]

    if abs(x1 - x2) != abs(y1 - y2) and not (x1 - x2 == 0 or y1 - y2 == 0):  # check if this move is possible
        raise Exception(f"something went wrong ({i1} -> {i2}; {x1}, {y1} -> {x2}, {y2})")
    xd, yd = x2 - x1, y2 - y1
    d = str()
    if num:
        d = str(max(abs(xd), abs(yd)))
        if d == "0":
            d = ""
    
    if yd < 0:
        d += dirs[0]
    elif yd > 0:
        d += dirs[2]
    if xd < 0:
        d += dirs[3]
    elif xd > 0:
        d += dirs[1]
    
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

        self.cnv = tk.Canvas(self.mainframe, width=sqW * self.size[0] + 1, height=sqH * self.size[1] + 1,
                             background="#ffffff", bd=0, highlightthickness=0)
        self.cnv.grid(column=0, row=0)

        self.buttonframe = ttk.Frame(self.mainframe)
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

        self.outputBox = tk.Text(self.buttonframe, state="disabled")
        self.outputBox.grid(column=0, row=2, columnspan=2)

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

    def initCanvas(self, canvas: tk.Canvas, draw: bool = True, size: list = None, sq: list = None, lines: list = None):
        if sq is None:
            sq = self.squareSize
        if size is None:
            size = self.size
        if lines is None:
            lines = self.linesToDraw
        canvas.config(width=sq[0] * size[0] + 1, height=sq[1] * size[1] + 1)
        canvas.delete("all")
        for j in range(size[0]):  # board has sizes[0] vertical squares + right border
            for z in range(size[1]):  # board has sizes[1] horizontal squares + bottom border
                canvas.create_rectangle(sq[0] * j, sq[1] * z,
                                        sq[0] * (j + 1), sq[1] * (z + 1), outline="#999", tags="grid")

        # in about 2 weeks or less i shall hate myself a lot for hard-coding all the color values but oh well

        if draw:
            self.centeredCircle(canvas, lines[0][0] % size[0],
                                lines[0][0] // size[0], fill="blue")
            print(self.pos)
            print(self.paths)
            for i, j in zip(lines, range(len(lines))):
                self.drawPathLine(i[0], i[1], i[2], index=j)

    def generatePath(self, times: list, startPos: int = None):
        """
        startPos == position to start from
           times == times to repeat, with integers in a list that define how many turns each player takes
        """

        self.linesToDraw = list()

        if startPos is not None:
            x, y = startPos % self.size[0], startPos // self.size[0]
            # doubles as an x/y coordinate, and as a margin to the top-left edge of the board

        else:
            x, y = self.pos[-1] % self.size[0], self.pos[-1] // self.size[0]
        bias = [1, 1, 2, 2, 2, 3, 3, 4, 4, 5]  # RNG bias
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

    def drawPathLine(self, p1: int, p2: int, flag=False, clr="black", canvas: tk.Canvas = None, index="unindexed"):
        """
          p1 == position 1 (starting point)
          p2 == position 2 (ending point)
        flag == whether to draw a (rudimentary) flag at the end or not
        """

        if canvas is None:
            canvas = self.cnv

        h = 3

        s1, s2 = self.squareSize[0]/h, self.squareSize[1]/h

        f = {"n": {"y": 0, "x": -s1}, "ne": {"y": -s2, "x": -s1},
             "e": {"y": -s2, "x": 0}, "se": {"y": -s2, "x": s1},
             "s": {"y": 0, "x": s1}, "sw": {"y": s2, "x": s1},
             "w": {"y": s2, "x": 0}, "nw": {"y": s2, "x": -s1}}

        s = self.size[0]  # shorthand, no other purpose

        x1, y1, = \
            p1 % s * self.squareSize[0] + .5 * self.squareSize[0], \
            p1 // s * self.squareSize[1] + .5 * self.squareSize[1]
        x2, y2 = \
            p2 % s * self.squareSize[0] + .5 * self.squareSize[0], \
            p2 // s * self.squareSize[1] + .5 * self.squareSize[1]
        xm, ym = \
            (x1 + x2) / 2 + f.get(parsePos(p1, p2, dirs=baseDirs, num=False)).get("x"), \
            (y1 + y2) / 2 + f.get(parsePos(p1, p2, dirs=baseDirs, num=False)).get("y")

        canvas.create_line([x1, y1, xm, ym, x2, y2], smooth=True, fill=clr, arrow="last",
                           tags=("line", "arrow", clr, str(index)))
        if flag:
            self.flag(canvas, x2, y2, fill="cyan")

    def onNewGame(self, times: list, rand: tk.BooleanVar):
        xPos, yPos = None, None
        if not rand.get():
            exitstatus = False  # what to do after cancelling
            def newGameCommand(e, scaleVar: tk.IntVar, x, y):
                scaleVar.set(round(float(e)))
                canvas.delete("circle")
                self.centeredCircle(canvas, x.get() - 1, y.get() - 1, fill="blue")
            def done():
                nonlocal exitstatus
                prompt.destroy()
                exitstatus = True
            def cancel():
                prompt.destroy()
            prompt = tk.Toplevel()
            frm = ttk.Frame(prompt, padding=3)
            frm.grid(column=0, row=0)

            topScaleVar = tk.IntVar(value=1)
            botScaleVar = tk.IntVar(value=1)

            canvas = tk.Canvas(frm, bd=0, highlightthickness=0)
            canvas.grid(column=1, row=2)
            self.initCanvas(canvas, draw=False)

            newGameCommand(1, tk.IntVar(), topScaleVar, botScaleVar)

            ttk.Label(frm, text="Enter a start position for your game.").grid(column=0, row=0, columnspan=2)
            topScale = ttk.Scale(frm, orient="horizontal", length=self.squareSize[0]*self.size[0],
                                 from_=1, to=self.size[0], variable=topScaleVar,
                                 command=lambda x: newGameCommand(x, topScaleVar, topScaleVar, botScaleVar))
            topScale.grid(column=1, row=1)
            botScale = ttk.Scale(frm, orient="vertical", length=self.squareSize[1]*self.size[1],
                                 from_=1, to=self.size[1], variable=botScaleVar,
                                 command=lambda y: newGameCommand(y, botScaleVar, topScaleVar, botScaleVar))
            botScale.grid(column=0, row=2)

            btnframe = ttk.Frame(frm, padding=(0, 3, 0, 0))
            btnframe.grid(column=0, row=3, columnspan=2, sticky="se")
            ttk.Button(btnframe, command=lambda: done(), text="Done").grid(column=0, row=0)
            ttk.Button(btnframe, command=lambda: cancel(), text="Cancel").grid(column=1, row=0)

            prompt.wait_window(prompt)

            if not exitstatus:
                return
            xPos, yPos = topScaleVar.get()-1, botScaleVar.get()-1

            self.cnv.delete("line||flag||circle")
        self.pos = list()

        if xPos is not None:  # literally just reused code, read comments from line 116
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
        def do():
            try:
                if inp[0].get() == "":
                    inp[0].set(str(max(int(inp_[0])-1, 2)))
                    inp_[0] = inp[0].get()
                    return
                if inp[1].get() == "":
                    inp[1].set(str(max(int(inp_[1])-1, 2)))
                    inp_[1] = inp[1].get()
                    return
                if int(inp[0].get()) > 20 or int(inp[1].get()) > 20:
                    raise ValueError
            except ValueError:
                win.bell()
                inp[0].set(inp_[0])
                inp[1].set(inp_[1])
                return
            self.size[0], self.size[1] = int(inp[0].get()), int(inp[1].get())
            inp_[0], inp_[1] = inp[0].get(), inp[1].get()
            self.initCanvas(cnv, draw=False)
        exitstatus = False

        def done():
            nonlocal exitstatus
            prompt.destroy()
            exitstatus = True

        def cancel():
            prompt.destroy()

        oldSize = [int(self.size[0]), int(self.size[1])]
        prompt = tk.Toplevel()
        frm = ttk.Frame(prompt, padding=3)
        frm.grid(column=0, row=0)
        ttk.Label(frm, text="Enter size of playing field (min 2x2, max 20x20)", padding=(0, 0, 0, 3))\
            .grid(column=0, row=0, columnspan=2)
        inp = [tk.StringVar(value=self.size[0]), tk.StringVar(value=self.size[1])]
        inp_ = [str(self.size[0]), str(self.size[1])]  # backup for validation
        inp[0].trace("w", lambda a, b, c: do())
        inp[1].trace("w", lambda a, b, c: do())

        frmL = ttk.Frame(frm, padding=(0, 0, 3, 0))
        frmR = ttk.Frame(frm)
        frmL.grid(column=0, row=1)
        frmR.grid(column=1, row=1)

        ttk.Label(frmL, text="Width: ").grid(column=0, row=0)
        ttk.Spinbox(frmL, from_=2, to=20, increment=1, textvariable=inp[0]).grid(column=1, row=0)
        ttk.Label(frmR, text="Height: ").grid(column=0, row=0)
        ttk.Spinbox(frmR, from_=2, to=20, increment=1, textvariable=inp[1]).grid(column=1, row=0)

        cnv = tk.Canvas(frm, bd=0, highlightthickness=0)
        cnv.grid(column=0, row=2, columnspan=3)

        btnframe = ttk.Frame(frm, padding=3)
        btnframe.grid(column=0, row=3, columnspan=2, sticky="se")
        ttk.Button(btnframe, text="Done", command=lambda: done()).grid(column=0, row=0)
        ttk.Button(btnframe, text="Cancel", command=lambda: cancel()).grid(column=1, row=0)

        frm.grid_columnconfigure(2, weight=1)
        do()
        prompt.wait_window(prompt)

        if not exitstatus:
            return

        if oldSize == self.size:
            return
        if msgbox.askokcancel("Use configuration?", "Do you want to use this board configuration?\n\
        Your current game will be discarded."):
            self.newButton.invoke()
        else:
            self.size = oldSize

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
boardSize = [6, 6]
boardIndicators = [["1", "2", "3", "4", "5", "6"],
                   ["A", "B", "C", "D", "E", "F"]]  # how the board is indicated at the sides (1st E-W, 2nd N-S)
directions = ("S", "V", "J", "Z")  # cardinal direction names of the board (direction definition going ↑→↓←)
baseDirs = ("n", "e", "s", "w")  # cardinal directions that are used in the code, do not change
# note that the hardcoded directions will always be lowercase and output will always be uppercase in the code
# the output shown to the user will be formatted later
pathNums = [20, 15, 10, 5]

if __name__ == "__main__":
    brd = Board(win, boardSize, sqW=50, sqH=50)
    win.mainloop()
# newBoard(boardSize)
