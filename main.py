def newBoard(size):
    global board
    board = list()

def generatePath(paths):
    pass

def parsePath(i, s):
    p = {"n": -boardSize, "nw": -boardSize+1,
         "w": -1, "sw": boardSize-1,
         "s": boardSize, "se": boardSize+1,
         "e": 1, "ne": -boardSize-1}
    c = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
    t = "".join([x for x in i if not(x in c)])
    n = "".join([x for x in i if x in c])
    if n == "":
        n = 1
    else:
        n = int(n)
    return s + (p.get(t) * n)


boardSize = 6
boardIndicators = [["1", "2", "3", "4", "5", "6"],
                   ["A", "B", "C", "D", "E", "F"]]  # how the board is indicated at the sides (1st E-W, 2nd N-S)
directions = ["N", "W", "S", "E"]  # cardinal direction names of the board (direction definition going ↑→↓←)
pathNums = [20, 15, 10, 5]
if __name__ == "__main__":
    path = "sw"
    print(parsePath(path, 5))
#newBoard(boardSize)
