#!/usr/bin/env python3
from tkinter import Tk, Button, Frame, Label, Menu, NORMAL, HIDDEN, BOTH
from threading import Timer
from random import randint, choice
from itertools import product
from board import Board

class Snake(object):
    """Move snake and stop it, if game is over."""
    def __init__(self, board, repeat_time=0.1):
        self.body = board.visible_cells
        self.board = board
        self.timer = None
        self.repeat_time = repeat_time
        self.is_running = False
        self.product = list(product(range(0, self.board.board_width), range(0, self.board.board_height)))
        self.food = self.board.matrix[randint(0, self.board.board_width-1)][randint(0, self.board.board_height-1)]
        self.board.canv.itemconfig(self.food, state = NORMAL, fill = 'red', outline = 'red')
    def move(self, tag):
        x, y = self.body[0]
        self.board.canv.itemconfig(self.board.matrix[x][y], state = HIDDEN)
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
        self.board.canv.itemconfig(head, state = NORMAL, fill = 'green', outline = 'green')
        self.body.append((x, y))
        if head == self.food:
            x, y = choice(list(filter(lambda x: x not in self.body, self.product)))
            self.food = self.board.matrix[x][y]
            self.board.canv.itemconfig(self.food, state = NORMAL, fill = 'red', outline = 'red')
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
    board.canv.pack(fill= BOTH)
    root.title('Snake')
    root.mainloop()

if __name__ == '__main__':
    main()
