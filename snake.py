#!/usr/bin/env python
from Tkinter import *
from numpy import zeros, int32
from threading import Timer
from random import choice

class Board(object):
    def __init__(self, root, cell_size=20, win_height=20*30, win_width=20*30, cell_distance=1):
        self.cell_size = cell_size
        self.board_height = win_height/cell_size
        self.board_width = win_width/cell_size
        self.cell_distance = cell_distance
        self.visible_cells = []
        self.canv = Canvas(root, height = win_height, width = win_width)
        self.matrix = zeros((self.board_width, self.board_height), dtype = int32)
        self.canv.bind('<Button-1>', self.draw_cell)
        self.canv.bind('<B1-Motion>', self.draw_cell)
        for x in xrange(self.board_width):
            for y in xrange(self.board_height):
                self.matrix[x][y] = self.canv.create_rectangle(x*cell_size+cell_distance, \
                y*cell_size+cell_distance, (x+1)*cell_size-cell_distance, \
                (y+1)*cell_size-cell_distance, state = HIDDEN, fill = 'green', outline = 'green')
    def draw_cell(self,event):
        try:
            cell = self.matrix[(event.x-self.cell_distance)/self.cell_size][(event.y-self.cell_distance)/self.cell_size]
            if cell not in self.visible_cells:
                self.visible_cells.append(cell)
            self.canv.itemconfig(cell, state = NORMAL)
        except IndexError:
            pass

class Snake(object):
    def __init__(self, board):
        self.body, self.canv, board_width, board_height = board.visible_cells, board.canv, board.board_width, board.board_height
        self.timer = None
        self.range = board_width * board_height
        self.is_running = False
        self.food_exist = True
        self.food = -1
    def move(self, next_coord):
        self.is_running = True
        self.canv.itemconfig(self.body[0], state = HIDDEN)
        head = self.body[len(self.body)-1] + next_coord
        if head in self.body:
            self.stop()
            game_over = Tk()
            game_over.geometry('+750+150')
            Label(game_over, text="Game Over!").pack()
            game_over.mainloop()
            return
        self.canv.itemconfig(head, state = NORMAL)
        if self.food_exist:
            self.food = choice(filter(lambda x: x not in self.body, xrange(self.range)))
            self.canv.itemconfig(self.food, state = NORMAL)
            self.food_exist = False
        self.body.append(head)
        if head == self.food:
            self.food_exist = True
        self.body = self.body[0 if head == self.food else 1:len(self.body)]
        self.timer = Timer(0.1, lambda: self.move(next_coord))
        self.timer.start()
    def stop(self):
        self.timer.cancel()

def restart(root, snake):
    if snake.is_running:
        snake.stop()
    root.destroy()
    main()

def move(snake, next_coord):
    if snake.is_running:
        snake.stop()
    snake.move(next_coord)

def main():
    root = Tk()
    cell_size = 20
    cell_distance = 1
    win_height = cell_size*30
    win_width = cell_size*30
    root.geometry("%sx%s+500+0" % (str(win_width-3), str(win_height+5)))
    frame = Frame(root, bd = 2, bg = 'black')
    board = Board(frame, cell_size, win_height, win_width, cell_distance)
    snake = Snake(board)
    btn1 = Button(frame, text = 'Reboot', width = 3, command = lambda: restart(root, snake))
    root.bind('<Right>', lambda x: move(snake, win_height/cell_size))
    root.bind('<Left>', lambda x: move(snake, -win_height/cell_size))
    root.bind('<Down>', lambda x: move(snake, 1))
    root.bind('<Up>', lambda x: move(snake, -1))
    btn1.pack(side = 'right')
    frame.pack()
    board.canv.pack(fill= BOTH)
    root.title('Snake')
    root.mainloop()

if __name__ == '__main__':
    main()
