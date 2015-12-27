#!/usr/bin/env python3
from tkinter import Canvas, NORMAL, HIDDEN
from numpy import zeros, int16

class Board(object):
    """Creates board with hidden cells."""
    def __init__(self, root, cell_size = 20, win_height = 20*30, win_width = 20*30, cell_distance=1):
        self.cell_size = cell_size
        self.board_height = win_height//cell_size
        self.board_width = win_width//cell_size
        self.cell_distance = cell_distance
        self.visible_cells = []
        self.canv = Canvas(root, height = win_height, width = win_width)
        self.matrix = zeros((self.board_width, self.board_height), dtype = int16)
        self.canv.bind('<Button-1>', self.draw_cell)
        self.canv.bind('<B1-Motion>', self.draw_cell)
        for x in range(self.board_width):
            for y in range(self.board_height):
                self.matrix[x][y] = self.canv.create_rectangle(x*cell_size+cell_distance,\
                y*cell_size+cell_distance, (x+1)*cell_size-cell_distance,\
                (y+1)*cell_size-cell_distance, state = HIDDEN, fill = 'green', outline = 'green', tags=('%d' % x, '%d' % y))

    def draw_cell(self,event):
        """Make cells visible by clicking on left mouse button."""
        try:
            x = (event.x-self.cell_distance)//self.cell_size
            y = (event.y-self.cell_distance)//self.cell_size
            if (x, y) not in self.visible_cells:
                self.visible_cells.append((x,y))
            self.canv.itemconfig(self.matrix[x][y], state = NORMAL)
        except IndexError:
            pass

    def repaint(self, body):
        newvis = []
        for coords in body:
            x, y = coords
            try:
                if coords not in self.visible_cells:
                    newvis.append(coords)
                    self.canv.itemconfig(self.matrix[x][y], state = NORMAL)
            except IndexError:
                pass

        for coords in self.visible_cells:
            x, y = coords
            try:
                if coords in body:
                    newvis.append((x, y))
                else:
                    self.canv.itemconfig(self.matrix[x][y], state = HIDDEN)
            except IndexError:
                pass
        self.visible_cells = newvis

    def clear(self):
        for i in range(1, self.board_width*self.board_height+1):
            self.canv.itemconfig(i, state = HIDDEN)
        self.visible_cells = []
