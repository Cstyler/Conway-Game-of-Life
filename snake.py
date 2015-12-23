#!/usr/bin/env python
from Tkinter import *
import numpy as np
import threading

class Board(object):
    def __init__(self, root, cell_size=20, win_height=20*30, win_width=20*30, cell_distance=1):
        self.cell_size = cell_size
        self.board_height = win_height/cell_size
        self.board_width = win_width/cell_size
        self.cell_distance = cell_distance
        self.visible_cells = []
        self.canv = Canvas(root, height = win_height, width = win_width)
        self.matrix = np.zeros((self.board_width, self.board_height), dtype = np.int32)
        self.canv.bind('<Button-1>', self.draw_cell)
        self.canv.bind('<B1-Motion>', self.draw_cell)
        for x in xrange(self.board_width):
            for y in xrange(self.board_height):
                self.matrix[x][y] = self.canv.create_rectangle(x*cell_size+cell_distance, \
                y*cell_size+cell_distance, (x+1)*cell_size-cell_distance, (y+1)*cell_size-cell_distance, state=HIDDEN, fill='green')
    def draw_cell(self,event):
        try:
            cell = self.matrix[(event.x-self.cell_distance)/self.cell_size][(event.y-self.cell_distance)/self.cell_size]
            if cell not in self.visible_cells:
                self.visible_cells.append(cell)
            self.canv.itemconfig(cell, state = NORMAL)
        except IndexError: pass
    def clear(self):
        for x in xrange(self.board_height):
            for y in xrange(self.board_width):
                self.canv.itemconfig(self.matrix[x][y], state = HIDDEN)
        self.visible_cells = []
    def get(self):
        return (self.visible_cells, self.canv)

class Snake(object):
    def __init__(self, board):
        self.body, self.canv = board.get()
    def move(self):
        # print self.body
        self.canv.itemconfig(self.body[0], state = HIDDEN)
        self.body = self.body[1:len(self.body)]
        self.canv.itemconfig(self.body[len(self.body)-1]+1, state = NORMAL)
        self.body.append(self.body[len(self.body)-1]+1)
        threading.Timer(0.1, self.move).start()

def main():
    root = Tk()
    cell_size = 20
    cell_distance = 1
    win_height = cell_size*30
    win_width = cell_size*30
    root.geometry("%sx%s+500+0" % (str(win_width), str(win_height)))
    board = Board(root, cell_size, win_height, win_width, cell_distance)
    snake = Snake(board)
    frame = Frame(root)
    btn1 = Button(frame, text = 'Clear', command = board.clear)
    btn2 = Button(frame, text= 'Start', command = snake.move)
    btn2.pack(side = 'top')
    btn1.pack(side = 'bottom')
    frame.pack(side = 'right')
    board.canv.pack(fill= BOTH)
    root.title('Snake')
    root.mainloop()

if __name__ == "__main__":
    main()
# frame1=Frame(root,width=100,heigh=100,bg='green',bd=50)
# frame2=Frame(root,width=150,heigh=75,bg='red',bd=50)
# button1=Button(frame1,text=u'f')
# button2=Button(frame2,text=u's')
# frame1.pack()
# frame2.pack()
# button1.pack()
# button2.pack()
# ent.bind('<Return>',caption)
# root.bind('<Control-z>',exit_)
