"""
    Sanctuary - The area within the planet that has randomly generated content.
"""
import random

import Objects
from MyMaths import rand2D
from Vex import Vex

# import Environment

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


def shift(direction, number, matrix):
    ln = len(matrix)
    arrayShifted = [[[None] for x in range(0, ln)] for y in range(0, ln)]
    if direction == UP:
        for row in range(0, ln):
            arrayShifted[row] = matrix[(row + number) % ln]
    elif direction == DOWN:
        for row in range(0, ln):
            arrayShifted[row] = matrix[(row - number) % ln]
    elif direction == LEFT:
        for row in range(0, ln):
            for col in range(0, ln):
                arrayShifted[row][col] = matrix[row][(col + number) % ln]
    elif direction == RIGHT:
        for row in range(0, ln):
            for col in range(0, ln):
                arrayShifted[row][col] = matrix[row][(col - number) % ln]

    return arrayShifted


# orig = [[1,2,3],[4,5,6],[7,8,9]]
# print (shift(LEFT,1,orig))


class Sanctuary():
    def __init__(self, parent, seed, width=50, height=50, scale=1):
        self.parent = parent
        self.percent = .5
        self.objectGrid = [[[None] for x in range(0, width)] for y in range(0, height)]
        self.objects = []
        self.seed = seed
        self.width = width
        self.height = height
        self.scale = scale
        self.localPos = [0, 0]

    def init(self, cam):
        x = (cam.pos.x())
        y = (cam.pos.y())
        rnd = random.seed(self.seed)
        self.localPos = [int(x), int(y)]
        self.objectGrid = [[[None] for x in range(0, self.width)] for y in range(0, self.height)]
        self.objects = []
        px = -(x - int(x))
        py = -(y - int(y))
        hh = int(self.height / 2)
        hw = int(self.width / 2)
        for row in range(0, self.height):
            for col in range(0, self.width):
                o = None
                val = (((rand2D((x) + col - hw, (y) + row - hh, self.seed) + 1) / 2) * 100)
                if val < self.percent:
                    val = rand2D(int(x), int(y) , self.seed)
                    o = Objects.Objects(self.parent, val, Vex((x + px + col - hh), (y + py + row - hw)))
                    self.objects += [o]
                self.objectGrid[row][col] = o

        Objects.Objects.update_image_rotation(cam)
        for o in self.objects:
            o.selfUpdate(cam)

    def update(self, cam):
        # update should only do parts of a grid that have moved on.
        x = (cam.pos.x())
        y = (cam.pos.y())
        intX = int(x)
        intY = int(y)
        px = -(x - intX)
        py = -(y - intY)

        hh = int(self.height / 2)
        hw = int(self.width / 2)

        if intX > self.localPos[0]:

            self.objectGrid = shift(LEFT, 1, self.objectGrid)

            col = self.width
            for row in range(0, self.height):
                if self.objectGrid[row][col - 1] != [None] and self.objectGrid[row][col - 1] != None:
                    self.objects.remove(self.objectGrid[row][col - 1])
                val = (((rand2D((x) + col - hw, (y) + row - hh, self.seed) + 1) / 2) * 100)
                o = None
                if val < self.percent:
                    val = rand2D(int(x)+col, int(y)+row, self.seed)
                    o = Objects.Objects(self.parent, val, Vex((x + px + (col - 1) - hw), (y + py + row - hh)))
                    self.objects += [o]
                self.objectGrid[row][col - 1] = o

        if intX < self.localPos[0]:
            self.objectGrid = shift(RIGHT, 1, self.objectGrid)

            col = 0
            for row in range(0, self.height):
                if self.objectGrid[row][col] != [None] and self.objectGrid[row][col] != None:
                    self.objects.remove(self.objectGrid[row][col])
                val = (((rand2D((x) + col - hw, (y) + row - hh, self.seed) + 1) / 2) * 100)
                o = None
                if val < self.percent:
                    val = rand2D(int(x) + col, int(y) + row, self.seed)
                    o = Objects.Objects(self.parent, val, Vex((x + px + col - hw), (y + py + row - hh)))
                    self.objects += [o]
                self.objectGrid[row][col] = o

        if intY > self.localPos[1]:
            self.objectGrid = shift(UP, 1, self.objectGrid)

            row = self.height
            for col in range(0, self.width):
                if self.objectGrid[row - 1][col] != [None] and self.objectGrid[row - 1][col] != None:
                    self.objects.remove(self.objectGrid[row - 1][col])
                val = (((rand2D((x) + col - hw, (y) + row - hh, self.seed) + 1) / 2) * 100)
                o = None
                if val < self.percent:
                    val = rand2D(int(x) + col, int(y) + row, self.seed)
                    o = Objects.Objects(self.parent, val, Vex((x + px + col - hw), (y + py + (row - 1) - hh)))
                    self.objects += [o]
                self.objectGrid[row - 1][col] = o

        if intY < self.localPos[1]:
            self.objectGrid = shift(DOWN, 1, self.objectGrid)

            row = 0
            for col in range(0, self.width):
                if self.objectGrid[row][col] != [None] and self.objectGrid[row][col] != None:
                    self.objects.remove(self.objectGrid[row][col])
                val = (((rand2D((x) + col - hw, (y) + row - hh, self.seed) + 1) / 2) * 100)
                o = None
                if val < self.percent:
                    val = rand2D(int(x) + col, int(y) + row, self.seed)
                    o = Objects.Objects(self.parent, val, Vex((x + px + col - hw), (y + py + row - hh)))
                    self.objects += [o]
                self.objectGrid[row][col] = o

        self.localPos = [intX, intY]

        #Objects.Objects.update_image_rotation(cam)
        for o in self.objects:
            o.selfUpdate(cam)
