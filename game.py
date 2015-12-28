#!/usr/bin/env python3
from board import Board
from tkinter import Tk, Button, Frame, Label, Menu
from itertools import product, chain

class MinesBoard(Board):
    """docstring for MinesBoard"""
    def __init__(self, root, cell_size, win_height, win_width,\
    cell_distance, color, outcolor, board_state, mines_count):
        Board.__init__(self, root, cell_size, win_height, win_width,\
        cell_distance, color, outcolor, board_state)
        self.mines_count = mines_count
    def show_cell(self, event):
        pass

def f():
    pass

def main():
    root = Tk()
    mines_count = 10
    cell_size = 30
    cell_distance = 0
    win_height = cell_size*16
    win_width = cell_size*16
    root.geometry("%dx%d+500+0" % (win_width+5, win_height+34))
    frame = Frame(root, bd = 2, bg = 'black')
    mines_board = MinesBoard(frame, cell_size, win_height, win_width, cell_distance, color='white',\
    outcolor='black', board_state='normal', mines_count=mines_count)
    mines_board.set_binding(mines_board.show_cell)
    btn1 = Button(frame, text = 'Start', command = lambda: f)
    btn2 = Button(frame, text = 'Restart', command = lambda: f)
    mines_board.canv.pack(fill = 'both')
    btn1.pack(side = 'left')
    btn2.pack(side = 'right')
    frame.pack(side = 'bottom')
    root.title('Mines')
    root.mainloop()

if __name__ == '__main__':
    main()
