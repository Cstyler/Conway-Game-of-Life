#!/usr/bin/env python3
from board import Board
from life import neighbors
from tkinter import Tk, Button, Frame, Label, Menu
from itertools import product, chain
from random import sample

class MinesBoard(Board):
    """Show count of mines around, stop game and put flag on cell"""
    def __init__(self, root, cell_size, win_height, win_width,\
    cell_distance, color, outcolor, board_state, mines_count):
        Board.__init__(self, root, cell_size, win_height, win_width,\
        cell_distance, color, outcolor, board_state)
        self.mines = sample(list(product(range(self.board_width), range(self.board_height))), mines_count)
        for coords in chain(*map(neighbors, self.mines)):
            count = sum([neihbor in self.mines for neihbor in neighbors(coords)])
            if count:
                try:
                    self.canv.itemconfig(self.matrix[coords[0]][coords[1]], tags = count)
                except IndexError:
                    pass
        self.flags = set()

    def show_cell(self, event=0, flag=False, x=0, y=0, lst=[]):
        if not flag:
            x = (event.x-self.cell_distance)//self.cell_size
            y = (event.y-self.cell_distance)//self.cell_size
        if (x, y) in lst: return
        if(x, y) in self.mines:
            self.stop_game()
        try:
            count = self.canv.gettags(self.matrix[x][y])
        except IndexError:
            return
        if len(count)>0 and count[0]!='current':
            tx, ty = self.canv.coords(self.matrix[x][y])[0:2]
            tx += self.cell_size//2
            ty += self.cell_size//2
            self.canv.create_text(tx, ty, text = count[0])
            self.canv.itemconfig(self.matrix[x][y], fill = 'green')
        else:
            self.canv.itemconfig(self.matrix[x][y], fill = 'white')
            for neighbor_x, neighbor_y in neighbors((x, y)):
                if neighbor_x in range(self.board_width) or neighbor_y in range(self.board_height):
                    lst.append((x, y))
                    self.show_cell(self, flag=True, x=neighbor_x, y=neighbor_y, lst=lst)

    def stop_game(self, txt='Game Over!'):
        game_over = Tk()
        game_over.geometry('+750+150')
        Label(game_over, text=txt).pack()
        game_over.mainloop()

    def show_flag(self, event):
        x = (event.x-self.cell_distance)//self.cell_size
        y = (event.y-self.cell_distance)//self.cell_size
        if 'f' not in self.canv.gettags(self.matrix[x][y]):
            self.flags.add((x, y))
            self.canv.itemconfig(self.matrix[x][y], fill='red', tags = 'f')
        else:
            self.canv.itemconfig(self.matrix[x][y], fill='gray', tags=())
            if (x,y) in self.flags:
                self.flags.remove((x,y))
        if self.flags==set(self.mines):
            self.stop_game(txt='You win!')

def restart(root, mines_board):
    del mines_board
    root.destroy()
    main()

def main():
    root = Tk()
    mines_count = 10
    cell_size = 30
    cell_distance = 0
    win_height = cell_size*16
    win_width = cell_size*16
    root.geometry("%dx%d+500+0" % (win_width+5, win_height+34))
    frame = Frame(root, bd = 2, bg = 'black')
    mines_board = MinesBoard(frame, cell_size, win_height, win_width, cell_distance, color='gray',\
    outcolor='black', board_state='normal', mines_count=mines_count)
    mines_board.set_binding(('<Button-3>', mines_board.show_flag), ('<Button-1>', mines_board.show_cell))
    btn = Button(frame, text = 'Restart', command = lambda: restart(root, mines_board))
    mines_board.canv.pack(fill = 'both')
    btn.pack(side = 'bottom')
    frame.pack(side = 'bottom')
    root.title('Mines')
    root.mainloop()

if __name__ == '__main__':
    main()
