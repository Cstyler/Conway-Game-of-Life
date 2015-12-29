#!/usr/bin/env python3
from board import Board
from tkinter import Tk, Button, Frame, Menu
from itertools import product, chain
from threading import Timer
from parser import parser

def neighbors(point):
    """Calc neighbors of point (x, y)"""
    x, y = point
    for i, j  in product(range(-1,2), repeat = 2):
        if any((i, j)) and not (x + i < 0 or y + j < 0):
            yield (x + i, y + j)

class Life:
    """Make next generation, repeat it and stop"""
    def __init__(self, body, repeat_time=0.1):
        self.body = body
        self.repeat_time = repeat_time
        self.timer = None
    def refresh(self):
        newbody = []
        for x in chain(*map(neighbors, self.body)):
            count = sum([neihbor in self.body for neihbor in neighbors(x)])
            if (count == 2 and x in self.body and x not in newbody) or (count == 3 and x not in newbody):
                newbody.append(x)
        self.body = newbody

    def set_timer(self, time):
        self.repeat_time = time

    def repaint(self, board):
        self.refresh()
        board.repaint(self.body)
        self.timer = Timer(self.repeat_time, lambda: self.repaint(board))
        self.timer.start()

    def stop(self):
        self.timer.cancel()

def restart(board, life):
    board.clear()
    life.body = board.visible_cells
    life.stop()

def main():
    root = Tk()
    cell_size = 10
    cell_distance = 0
    win_height = cell_size*90
    win_width = cell_size*180
    root.geometry("%dx%d+500+0" % (win_width+5, win_height+34))
    frame = Frame(root, bd = 2, bg = 'black')
    board = Board(frame, cell_size, win_height, win_width, cell_distance)
    board.set_binding(('<Button-1>', board.draw_cell), ('<B1-Motion>', board.draw_cell))
    coords = parser()
    board.draw_by_coords(coords)
    menubar = Menu(root)
    levelmenu = Menu(menubar, tearoff=0)
    levelmenu.add_command(label="0.5 sec", command=lambda: life.set_timer(0.5))
    levelmenu.add_command(label="0.1 sec", command= lambda: life.set_timer(0.1))
    levelmenu.add_command(label="0.01 sec", command= lambda: life.set_timer(0.01))
    menubar.add_cascade(label="Timer", menu=levelmenu)
    root.config(menu=menubar)
    life = Life(board.visible_cells)
    btn1 = Button(frame, text = 'Start', command = lambda: life.repaint(board))
    btn2 = Button(frame, text = 'Restart', command = lambda: restart(board, life))
    board.canv.pack(fill = 'both')
    btn1.pack(side = 'left')
    btn2.pack(side = 'right')
    frame.pack(side = 'bottom')
    root.title('Life')
    root.mainloop()

if __name__ == '__main__':
    main()
