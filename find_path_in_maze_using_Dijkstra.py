import time
from threading import Event
from tkinter import messagebox, Tk
import pygame
import sys
import random


class Box:
    def __init__(self, i, j):
        self.x = i  # position of the Box
        self.y = j  # position of the Box
        self.start = False  # True if the Box is a Start
        self.wall = False  # True if the Box is a Wall
        self.target = False  # True if the Box is a Target or Exit from Maze
        self.queued = False  # True if the Box is in a Queue
        self.visited = False  # True if the Box is already visited
        self.neighbours = []  # Searching for Box neighbours
        self.prior = None  # Prior to Box

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * grid_width, self.y * grid_height, grid_width - 2, grid_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def main(my_choice):
    begin_search = False
    target_box_set = False
    searching = True

    # Set Walls
    for i in range(columns):
        for j in range(rows):
            if my_choice == 0:
                if map[j][i] == 1:
                    grid[i][j].wall = True
            else:
                grid[i][j].wall = random.choice([True, False])
                if grid[i][j].wall is True:
                    grid[i][j].wall = random.choice([True, False])

    # Set Start, Start shouldn't be a Wall
    start_box = grid[0][0]
    if start_box.wall is True:
        for ii, state in enumerate(grid[0]):
            if state.wall is False:
                start_box = grid[0][ii]
                start_box.start = True
                start_box.visited = True
                queue.append(start_box)
                break
    else:
        start_box.start = True
        start_box.visited = True
        queue.append(start_box)

    # Set Target, Target shouldn't be a Wall
    i = random.randint(columns // 2, columns - 1)
    j = random.randint(rows // 2, rows - 1)
    target_box = grid[i][j]
    target_box.target = True
    target_box_set = True
    if target_box.wall is True:
        target_box.wall = False

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start Searching
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Attention!", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (255, 255, 0))
                    # Event().wait(0.0001)
                if box.visited:
                    box.draw(window, (0, 255, 0))
                if box in path:
                    box.draw(window, (0, 0, 255))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (255, 255, 255))

        pygame.display.flip()


if __name__ == '__main__':

    map = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    window_width = 800
    window_height = 800

    window = pygame.display.set_mode((window_width, window_height))

    my_choice = 0 # if You want to use predetermined map choose 0, # if You want to use random map choose 1

    if my_choice == 0:
        columns = len(map[0])
        rows = len(map)
    else:
        columns = 70
        rows = 70

    grid_width = window_width // columns
    grid_height = window_height // rows

    grid = []
    queue = []
    path = []
    draw_path = True

    # Create Grids
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)

    # Set Neighbours
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours()

    main(my_choice)
