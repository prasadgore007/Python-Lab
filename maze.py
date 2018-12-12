import random
import tkinter as tk
from tkinter import *
import sys


class App(tk.Frame):
    def __init__(self, width=21, height=21, size=10):
        tk.Frame.__init__(self)
        self.maze = Maze(width, height)
        self.size = size
        self.steps = 0
        self.grid()
        self.create_widgets()
        self.draw_maze()
        self.create_events()
        
    def create_widgets(self):
        width = self.maze.width * self.size
        height = self.maze.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid()
        self.status = tk.Label(self)
        self.status.grid()

    def draw_maze(self):
        for i, row in enumerate(self.maze.maze):
            for j, col in enumerate(row):
                x0 = j * self.size
                y0 = i * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                color = self.get_color(x=j, y=i)
                id = self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=color)
                if self.maze.start_cell == (j, i):
                    self.cell = id

        self.canvas.tag_raise(self.cell) 
        self.status.config(text='Movidas mínimas: %d' % self.maze.steps)

    def create_events(self):
        self.canvas.bind_all('<KeyPress-Up>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Down>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Left>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Right>', self.move_cell)

    def move_cell(self, event):
        if event.keysym == 'Up':
            if self.check_move(0, -1):
                self.canvas.move(self.cell, 0, -self.size)
                self.steps += 1
        if event.keysym == 'Down':
            if self.check_move(0, 1):
                self.canvas.move(self.cell, 0, self.size)
                self.steps += 1
                self.get_color(0, self.size)
        if event.keysym == 'Left':
            if self.check_move(-1, 0):
                self.canvas.move(self.cell, -self.size, 0)
                self.steps += 1
                self.get_color( -self.size,0)
        if event.keysym == 'Right':
            if self.check_move(1, 0):
                self.canvas.move(self.cell, self.size, 0)
                self.steps += 1
                self.get_color(self.size,0)

        args = (self.steps, self.maze.steps)
        self.status.config(text='Moves: %d/%d' % args)
        self.check_status()

    def check_move(self, x, y):
        x0, y0 = self.get_cell_coords()
        x1 = x0 + x
        y1 = y0 + y
        return self.maze.maze[y1][x1] == 0

    def get_cell_coords(self):
        position = self.canvas.coords(self.cell)
        x = int(position[0] / self.size)
        y = int(position[1] / self.size)
        return (x, y)

    def check_status(self):
        if self.maze.exit_cell == self.get_cell_coords():
            args = (self.steps, self.maze.steps)
            self.status.config(text='won in %d/%d movidas!' % args)

    def get_color(self, x, y):
        if self.maze.start_cell == (x, y):
            return 'blue'
        if self.maze.exit_cell == (x, y):
            return 'green'
        if self.maze.maze[y][x] == 1:
            return 'black'
        

class Maze(object):

    def __init__(self, width=21, height=21, exit_cell=(1, 1)):
        self.width = width
        self.height = height
        self.exit_cell = exit_cell
        self.create()

    def create(self):
        self.maze = [[1] * (self.width+1) for _ in range(self.height+1)]
        self.start_cell = None
        self.steps = None
        self.recursion_depth = 0
        self._visited_cells = []
        self._visit_cell(self.exit_cell)

    def _visit_cell(self, cell, depth=0):
        x, y = cell
        self.maze[y][x] = 0                                    
        self._visited_cells.append(cell)
        neighbors = self._get_neighbors(cell)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not neighbor in self._visited_cells:
                self._remove_wall(cell, neighbor)
                self._visit_cell(neighbor, depth+1)
        self._update_start_cell(cell, depth)

    def _get_neighbors(self, cell):
       
        x, y = cell
        neighbors = []

        # Left
        if x - 2 > 0:
            neighbors.append((x-2, y))
        # Right
        if x + 2 < self.width:
            neighbors.append((x+2, y))
        # Up
        if y - 2 > 0:
            neighbors.append((x, y-2))
        # Down
        if y + 2 < self.height:
            neighbors.append((x, y+2))

        return neighbors

    def _remove_wall(self, cell, neighbor):
        x0, y0 = cell
        x1, y1 = neighbor
        # Vertical
        if x0 == x1:
            x = x0
            y = (y0 + y1) / 2
          
        # Horizontal
        if y0 == y1:
            x = (x0 + x1) / 2
            y = y0
        self.maze[int(y)][int(x)] = 0 # remove wall

    def _update_start_cell(self, cell, depth):
        if depth > self.recursion_depth:
            self.recursion_depth = depth
            self.start_cell = cell
            self.steps = depth * 2 # wall + cell

sys.setrecursionlimit(1000)

e=App(40,40,10)
e.mainloop()
