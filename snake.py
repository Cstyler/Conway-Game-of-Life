#!/usr/bin/env python
from Tkinter import Tk, Button, Frame, Canvas, Label, Menu
from numpy import zeros, int16
from threading import Timer
from random import randint, choice
from itertools import product

class Board(object):
    """Creates board with hidden cells."""
    def __init__(self, root, cell_size = 20, win_height = 20*30, win_width = 20*30, cell_distance=1):
        self.cell_size = cell_size
        self.board_height = win_height/cell_size
        self.board_width = win_width/cell_size
        self.cell_distance = cell_distance
        self.visible_cells = []
        self.canv = Canvas(root, height = win_height, width = win_width)
        self.matrix = zeros((self.board_width, self.board_height), dtype = int16)
        self.canv.bind('<Button-1>', self.draw_cell)
        self.canv.bind('<B1-Motion>', self.draw_cell)
        for x in xrange(self.board_width):
            for y in xrange(self.board_height):
                self.matrix[x][y] = self.canv.create_rectangle(x*cell_size+cell_distance, \
                y*cell_size+cell_distance, (x+1)*cell_size-cell_distance, \
                (y+1)*cell_size-cell_distance, state = 'hidden', fill = 'green', outline = 'green', tags=('%d' % x, '%d' % y))

    def draw_cell(self,event):
        """Make cells visible by clicking on left mouse button."""
        try:
            x = (event.x-self.cell_distance)/self.cell_size
            y = (event.y-self.cell_distance)/self.cell_size
            if (x, y) not in self.visible_cells:
                self.visible_cells.append((x,y))
            self.canv.itemconfig(self.matrix[x][y], state = 'normal')
        except IndexError:
            pass

class Snake(object):
    """Move snake and stop it, if game is over."""
    def __init__(self, board, repeat_time=0.1):
        self.body = board.visible_cells
        self.board = board
        self.timer = None
        self.repeat_time = repeat_time
        self.is_running = False
        self.product = list(product(xrange(0, self.board.board_width), xrange(0, self.board.board_height)))
        self.food = self.board.matrix[randint(0, self.board.board_width-1)][randint(0, self.board.board_height-1)]
        self.board.canv.itemconfig(self.food, state = 'normal', fill = 'red', outline = 'red')
    def move(self, tag):
        x, y = self.body[0]
        self.board.canv.itemconfig(self.board.matrix[x][y], state = 'hidden')
        x, y = self.body[len(self.body) - 1]
        if tag == 'u':
            y -= 1
            y %= self.board.matrix.shape[1]
            head = self.board.matrix[x][y]
        elif tag == 'd':
            y += 1
            y %= self.board.matrix.shape[1]
            head = self.board.matrix[x][y]
        elif tag == 'r':
            x += 1
            x %= self.board.matrix.shape[0]
            head = self.board.matrix[x][y]
        elif tag == 'l':
            x -= 1
            x %= self.board.matrix.shape[0]
            head = self.board.matrix[x][y]
        if (x, y) in self.body:
            self.stop_game()
            return
        self.board.canv.itemconfig(head, state = 'normal', fill = 'green', outline = 'green')
        self.body.append((x, y))
        if head == self.food:
            x, y = choice(filter(lambda x: x not in self.body, self.product))
            self.food = self.board.matrix[x][y]
            self.board.canv.itemconfig(self.food, state = 'normal', fill = 'red', outline = 'red')
        else:
            self.body = self.body[1:len(self.body)]
        self.is_running = True
        self.timer = Timer(self.repeat_time, lambda: self.move(tag))
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def set_level(self, time):
        self.repeat_time = time

    def stop_game(self):
        self.stop()
        game_over = Tk()
        game_over.geometry('+750+150')
        Label(game_over, text="Game Over!").pack()
        game_over.mainloop()

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
    win_height = cell_size*15
    win_width = cell_size*20
    root.geometry("%dx%d+500+0" % (win_width+58, win_height+5))
    frame = Frame(root, bd = 2, bg = 'black')
    board = Board(frame, cell_size, win_height, win_width, cell_distance)
    snake = Snake(board)
    menubar = Menu(root)
    levelmenu = Menu(menubar, tearoff=0)
    levelmenu.add_command(label="Easy", command=lambda: snake.set_level(0.1))
    levelmenu.add_command(label="Normal", command= lambda: snake.set_level(0.05))
    levelmenu.add_command(label="Hard", command= lambda: snake.set_level(0.025))
    menubar.add_cascade(label="Level", menu=levelmenu)
    root.config(menu=menubar)
    btn1 = Button(frame, text = 'Reboot', width = 3, command = lambda: restart(root, snake))
    root.bind('<Right>', lambda x: move(snake, 'r'))
    root.bind('<Left>', lambda x: move(snake, 'l'))
    root.bind('<Down>', lambda x: move(snake, 'd'))
    root.bind('<Up>', lambda x: move(snake, 'u'))
    btn1.pack(side = 'right')
    frame.pack()
    board.canv.pack(fill= 'both')
    root.title('Snake')
    root.mainloop()

if __name__ == '__main__':
    main()
