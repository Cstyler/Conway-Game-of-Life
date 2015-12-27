#!/usr/bin/env python3
from board import Board
from tkinter import Tk, Button, Frame, Label, Menu, NORMAL, HIDDEN
from itertools import product, chain
from threading import Timer

def neighbors(point):
    x, y = point
    for i, j  in product(range(-1,2), repeat = 2):
        if any((i, j)):
            if not (x + i < 0 or y + j < 0):
                yield (x + i, y + j)

class Life:
    def __init__(self, body, repeat_time = 0.1):
        self.body = body
        self.timer = None
    def refresh(self):
        newbody = []
        for x in chain(*map(neighbors, self.body)):
            count = sum([neihbor in self.body for neihbor in neighbors(x)])
            if (count == 2 and x in self.body and x not in newbody) or (count == 3 and x not in newbody):
                newbody.append(x)
        self.body = newbody

    def repaint(self, board):
        self.refresh()
        board.repaint(self.body)
        self.timer = Timer(0.1, lambda: self.repaint(board))
        self.timer.start()
    def stop(self):
        self.timer.cancel()

def Restart(board, life):
    board.clear()
    life.body = board.visible_cells
    life.stop()

def main():
    root = Tk()
    cell_size = 10
    cell_distance = 0
    win_height = cell_size*50
    win_width = cell_size*120
    root.geometry("%dx%d+500+0" % (win_width+5, win_height+34))
    frame = Frame(root, bd = 2, bg = 'black')
    board = Board(frame, cell_size, win_height, win_width, cell_distance)
    life = Life(board.visible_cells, 0.1)
    btn1 = Button(frame, text = 'Start', command = lambda: life.repaint(board))
    btn2 = Button(frame, text = 'Restart', command = lambda: Restart(board, life))
    board.canv.pack(fill = 'both')
    btn1.pack(side = 'left')
    btn2.pack(side = 'right')
    frame.pack(side = 'bottom')
    root.title('Life')
    root.mainloop()

if __name__ == '__main__':
    main()
