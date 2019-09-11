##################################################################
#                                                                #
# Procedural Dungeon Generator                                   #
#                                                                #
# By Jay (Battery)                                               #
#                                                                #
# https://whatjaysaid.wordpress.com/                             #
# for how use it got to:                                         #
# https://whatjaysaid.wordpress.com/2016/01/15/1228              #
#                                                                #
# Feel free to use this as you wish, but please keep this header #
#                                                                #
##################################################################
import Environment
import pygame
import random
import math
import Color
import numpy

import Mind
import Player
import ParticleEngine
import Shot
from DrawINFO import DrawINFO
from Vex import Vex

myfont = None

# tile constants
EMPTY = 0
DEADEND = 1
WALL = 2
OBSTACLE = 3
TREE = 4
CASTLE = 5
CITY = 6
CITYI = 7
CITYH = 8
CITYV = 9
CITYIT = 10
CITYIL = 11
CITYIB = 12
CITYIR = 13
CITYTLB = 14
CITYTTL = 15
CITYTRT = 16
CITYTBR = 17
MOUNTAIN = 18
WOOD = 19
DOOR = 20
FLOOR = 21
CORRIDOR = 22
CAVE = 23
WATER = 24
LAVA = 25
TOXIC = 26
BUSH = 27
GRASS = 28
PLANCK = 29
ROADI = 30
ROADH = 31
ROADV = 32
ROADIT = 33
ROADIL = 34
ROADIB = 35
ROADIR = 36
ROADTLB = 37
ROADTTL = 38
ROADTRT = 39
ROADTBR = 40
ROADDD = 41
ROADDL = 42
ROADDU = 43
ROADDR = 44
CITYDD = 45
CITYDL = 46
CITYDU = 47
CITYDR = 48
CITYS = 49
TREETLC = 50
TREETRC = 51
TREEBRC = 52
TREEBLC = 53
TREEH = 54
TREEV = 55
TREEI = 56

TREES = [TREETLC, TREETRC, TREEBLC, TREEBRC, TREEH, TREEV, TREEI]
CITYWALLS = [CITYI, CITYH, CITYV, CITYIT, CITYIL, CITYIB, CITYIR, CITYTLB, CITYTTL, CITYTRT, CITYTBR \
    , CITYDD, CITYDL, CITYDU, CITYDR, CITYS]
WALLS = [WALL, MOUNTAIN, TREE, CASTLE, CITY, WOOD] + CITYWALLS + TREES
LAKES = [WATER, LAVA, TOXIC]
ROADS = [ROADI, ROADV, ROADH, ROADIT, ROADIL, ROADIB, ROADIR, ROADTLB, ROADTTL, ROADTRT, ROADTBR, ROADDD, ROADDL,
         ROADDU, ROADDR]
FLOORS = [CORRIDOR, FLOOR, PLANCK, CAVE, DOOR] + ROADS
ROUGHLINES = FLOORS[1:] + ROADS

# TILES THAT NEED 1 x 180' ROTATED IMAGE (2 IMAGES TOTAL) (ORIG + ROTATED)
# TILES THAT NEED 1 x 90' ROTATED IMAGE (2 IMAGES TOTAL) (ORIG + ROTATED) (VERTICAL / HORIZONTAL IMAGES)
ADD_1_90_TILE = [ROADH, CITYH]
# TILES THAT NEED 4 x 90' ROTATED IMAGES (4 IMAGES TOTAL) (ORIG + 3x ROTATED)
ADD_3_90_TILE = [ROADIT, ROADTLB, ROADDD, CITYIT, CITYTLB, CITYDD]

FILES = [
    'Dungeon-Empty.png',  # empty
    'Dungeon-Deadend-Pattern1.png',  # deadend
    'Dungeon-Background-Pattern1.png',  # default wall
    None,  # obstacle
    'Dungeon-Wall-Tree.png',
    'Dungeon-Wall-Castle.png',
    'Dungeon-Wall-City.png',
    'Dungeon-Wall-CityI.png',
    'Dungeon-Wall-CityH.png',
    None,
    'Dungeon-Wall-CityT.png',
    None,
    None,
    None,
    'Dungeon-Wall-CityC.png',
    None,
    None,
    None,
    'Dungeon-Wall-Mountain.png',
    'Dungeon-Wall-Wood.png',
    'Dungeon-Door-Pattern1.png',
    None,
    'Dungeon-Floor-Corridor.png',  # corridor
    'Dungeon-Floor-Cave.png',  # cave is floor
    'Dungeon-Floor-Water.png',
    'Dungeon-Floor-Lava.png',
    'Dungeon-Floor-Toxic.png',
    'Dungeon-Floor-Grass0.png',
    'Dungeon-Floor-Grass2.png',
    'Dungeon-Floor-Wood0.png',
    'Dungeon-Floor-RoadI.png',
    'Dungeon-Floor-RoadCTB.png',
    None,
    'Dungeon-Floor-RoadCT.png',
    None,
    None,
    None,
    'Dungeon-Floor-RoadTLB.png',
    None,
    None,
    None,
    'Dungeon-Floor-RoadD.png',
    None,
    None,
    None,
    'Dungeon-Wall-CityD.png',
    None,
    None,
    None,
    'Dungeon-Wall-CityS.png',
    'Dungeon-Wall-TreeTLC.png',
    'Dungeon-Wall-TreeTRC.png',
    'Dungeon-Wall-TreeBRC.png',
    'Dungeon-Wall-TreeBLC.png',
    'Dungeon-Wall-TreeH.png',
    'Dungeon-Wall-TreeV.png',
    'Dungeon-Wall-TreeI.png',
]


class DungeonRoom:
    """ 
    a simple container for dungeon rooms
    since you may want to return to constructing a room, edit it, etc. it helps to have some way to save them
    without having to search through the whole game grid
         
    Args:
        x and y coodinates for the room
        width and height for the room
     
    Attributes:
        x, y: the starting coordinates in the 2d array
        width: the ammount of cells the room spans 
        height: the ammount of cells the room spans 
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = "room"


class DungeonGenerator:
    """
    A renderer/framework/engine independent functions for generating random dungeons,
    including rooms, corridors, connects and path finding
     
    The dungeon is built around a 2D list, the resulting dungeon is a 2D tile map, where each x,y point
    holds a constant. The grid can then be iterated through using the contained constant to determine
    the tile to render and the x,y index can be multiplied by x,y size of the tile. The class it's self
    can be iterated through. For example:
         
        tileSize = 2
        for x, y, tile in dungeonGenerator:
            if tile = FLOOR:
                render(floorTile)
                floorTile.xPosition = x * tileSize
                floorTile.yPosition = y * tileSize
            and so forth...
     
    Alternatively:
         
        for x in range(dungeonGenerator.width):
            for y in range(dungeonGenerator.height):
                if dungeonGenerator.grid[x][y] = FLOOR:
                    render(floorTile)
                    floorTile.xPosition = x * tileSize
                    floorTile.yPosition = y * tileSize
                and so forth...
             
     
    Throughout x,y refer to indicies in the tile map, nx,ny are used to refer to neighbours of x,y
     
    Args:
        height and width of the dungeon to be generated
         
    Attributes:

        width: size of the dungeon in the x dimension

        height: size of the dungeon in the y dimension

        grid: a 2D list (grid[x][y]) for storing tile constants (read tile map)

        rooms: **list of all the dungeonRoom objects in the dungeon, empty until placeRandomRooms() is called

        doors: **list of all grid coordinates of the corridor to room connections, elements are tuples (x,y),
        empty until connectAllRooms() is called

        corridors: **list of all the corridor tiles in the grid, elements are tuples (x,y), empty until
        GenerateCorridors() is called

        deadends: list of all corridor tiles only connected to one other tile, elements are tuples (x,y),
        empty until findDeadends() is called

        graph: dictionary where keys are the coordinates of all floor/corridor tiles and values are a list
        of floor/corridor directly connected, ie (x, y): [(x+1, y), (x-1, y), (x, y+1), (x, y-1)], empty until
        constructGraph() is called
         
        ** once created these will not be re-instanced, therefore any user made changes to grid will also
        need to update these lists for them to remain valid
    """

    DUNGEON_SCALE = 2.5
    DUNGEON_IMAGES = []
    DUNGEON_TILE_SIZE = 64 * DUNGEON_SCALE

    def __init__(self, rnd, height, width):
        self.rnd = rnd
        self.height = abs(height)
        self.width = abs(width)
        #[[[None] for x in range(0, width)] for y in range(0, height)]
        self.grid = [[EMPTY for i in range(0,self.height)] for j in range(0,self.width)]
        self.rooms = []
        self.doors = []
        self.corridors = []
        self.deadends = []
        self.segs = []
        self.bg_color = (0, 0, 0)
        self.graph = {}
        self.active_tiles = []
        self.displayEmpty = False
        self.layer_empty = False
        self.draw_lines = False

    def __iter__(self):
        for xi in range(self.width):
            for yi in range(self.height):
                yield xi, yi, self.grid[xi][yi]

    @staticmethod
    def init():
        DG = DungeonGenerator
        # for f in FILES:
        #     if f is None:
        #         DG.DUNGEON_IMAGES += [None]
        #     else:
        #         DG.DUNGEON_IMAGES += [pygame.image.load("images/" + f).convert_alpha()]
        #
        # for i in ADD_1_90_TILE:
        #     DG.DUNGEON_IMAGES[i + 1] = pygame.transform.rotate(DG.DUNGEON_IMAGES[i], 90)
        #
        # for i in ADD_3_90_TILE:
        #     for k in range(1, 4):
        #         DG.DUNGEON_IMAGES[i + k] = pygame.transform.rotate(DG.DUNGEON_IMAGES[i], 360 - 90 * k)
        #
        # for i in range(len(DG.DUNGEON_IMAGES)):
        #     if DG.DUNGEON_IMAGES[i] is not None:
        #         DG.DUNGEON_IMAGES[i] = pygame.transform.scale(DG.DUNGEON_IMAGES[i],
        #                                                       (int(DG.DUNGEON_TILE_SIZE), int(DG.DUNGEON_TILE_SIZE)))

    # HELPER FUNCTIONS #####

    def find_neighbours(self, x, y):
        """
        finds all cells that touch a cell in a 2D grid
         
        Args:
            x and y: integer, indicies for the cell to search around
             
        Returns:
            returns a generator object with the x,y indicies of cell neighbours
        """

        xi = (0, -1, 1) if 0 < x < self.width - 1 else ((0, -1) if x > 0 else (0, 1))
        yi = (0, -1, 1) if 0 < y < self.height - 1 else ((0, -1) if y > 0 else (0, 1))
        for a in xi:
            for b in yi:
                if a == b == 0:
                    continue
                yield (x + a, y + b)

    def find_neighbours_direct(self, x, y):
        """
        finds all neighbours of a cell that directly touch it (up, down, left, right) in a 2D grid
         
        Args:
            x and y: integer, indicies for the cell to search around
             
        Returns:
            returns a generator object with the x,y indicies of cell neighbours
        """
        xi = (0, -1, 1) if 0 < x < self.width - 1 else ((0, -1) if x > 0 else (0, 1))
        yi = (0, -1, 1) if 0 < y < self.height - 1 else ((0, -1) if y > 0 else (0, 1))
        for a in xi:
            for b in yi:
                if abs(a) == abs(b):
                    continue
                yield (x + a, y + b)

    def can_carve(self, x, y, xd, yd):
        """
        checks to see if a path can move in certain direction, used by getPossibleMoves()
         
        Args:
            x and y: integer, indicies in the 2D grid of the starting cell
            xd and xy: integer, direction trying to move in where
            (-1,0) = left, (1,0) = right, (0,1) = up, (0,-1) = down
             
        Returns:
            True if it is safe to move that way
        """

        xi = (-1, 0, 1) if not xd else (1 * xd, 2 * xd)
        yi = (-1, 0, 1) if not yd else (1 * yd, 2 * yd)
        for a in xi:
            for b in yi:
                if self.grid[a + x][b + y]:
                    return False
        return True

    def get_possible_moves(self, x, y):
        """
        searches for potential directions that a corridor can expand in
        used by generatePath()
         
        Args:
            x and y: integer, indicies of the tile on grid to find potential moves (up, down, left, right) for
             
        Returns:
            a list of potential x,y coords that the path could move it, each entry stored as a tuple
        """

        available_squares = []
        for nx, ny in self.find_neighbours_direct(x, y):
            if nx < 1 or ny < 1 or nx > self.width - 2 or ny > self.height - 2:
                continue
            xd = nx - x
            yd = ny - y
            if self.can_carve(x, y, xd, yd):
                available_squares.append((nx, ny))
        return available_squares

    def quad_fits(self, sx, sy, rx, ry, margin):
        """
        looks to see if a quad shape will fit in the grid without colliding with any other tiles
        used by placeRoom() and placeRandomRooms()
         
        Args:
            sx and sy: integer, the bottom left coords of the quad to check
            rx and ry: integer, the width and height of the quad, where rx > sx and ry > sy
            margin: integer, the space in grid cells (ie, 0 = no cells, 1 = 1 cell, 2 = 2 cells) to be away
            from other tiles on the grid
             
        returns:
            True if the quad fits
        """

        sx -= margin
        sy -= margin
        rx += margin * 2
        ry += margin * 2
        if sx + rx < self.width and sy + ry < self.height and sx >= 0 and sy >= 0:
            for x in range(int(rx)):
                for y in range(int(ry)):
                    if self.grid[sx + x][sy + y]:
                        return False
            return True
        return False

    def quad_fits2(self, sx, sy, rx, ry, margin, exclude):
        """
        looks to see if a quad shape will fit in the grid without colliding with any other tiles
        used by placeRoom() and placeRandomRooms()

        Args:
            sx and sy: integer, the bottom left coords of the quad to check
            rx and ry: integer, the width and height of the quad, where rx > sx and ry > sy
            margin: integer, the space in grid cells (ie, 0 = no cells, 1 = 1 cell, 2 = 2 cells) to be away
            from other tiles on the grid

        returns:
            True if the quad fits
        """

        sx -= margin
        sy -= margin
        rx += margin * 2
        ry += margin * 2
        if -1 < (sx + rx) < self.width and -1 < (sy + ry) < self.height:
            for x in range(rx):
                for y in range(ry):
                    if self.grid[sx + x][sy + y] in exclude:
                        return False
            return True
        return False

    def floodFill(self, x, y, fillWith, tilesToFill=[], grid=None):
        """
        Fills tiles connected to the starting tile
        passing the same fillWith value as the starting tile value will produce no results since they're already filled
         
        Args:
            x and y: integers, the grid coords to star the flood fill, all filled tiles will be connected to this tile
            fillWith: integer, the constant of the tile to fill with
            tilesToFill: list of integers, allows you to control what tile get filled, all if left out
            grid: list[[]], a 2D array to flood fill, by default this is dungeonGenerator.grid, however if you do not want to overwrite this you can provide your own 2D array (such as a deep copy of dungeonGenerator.grid)
             
        Returns:
            none
        """

        if not grid: grid = self.grid
        toFill = set()
        toFill.add((x, y))
        count = 0
        while toFill:
            x, y = toFill.pop()
            if tilesToFill and grid[x][y] not in tilesToFill: continue
            if not grid[x][y]: continue
            grid[x][y] = fillWith
            for nx, ny in self.find_neighbours_direct(x, y):
                if grid[nx][ny] != fillWith:
                    toFill.add((nx, ny))
            count += 1
            if count > self.width * self.height:
                print('overrun')
                break

    ##### LEVEL SEARCH FUNCTIONS #####

    def findEmptySpace(self, distance):
        """
        Finds the first empty space encountered in the 2D grid that it not surrounding by anything within the given distance
         
        Args:
            distance: integer, the distance from the current x,y point being checked to see if is empty
             
        Returns:
            the x,y indicies of the free space or None, None if no space was found
        """

        for x in range(distance, self.width - distance):
            for y in range(distance, self.height - distance):
                touching = 0
                for xi in range(-distance, distance):
                    for yi in range(-distance, distance):
                        if self.grid[x + xi][y + yi]: touching += 1
                if not touching:
                    return x, y
        return None, None

    def findUnconnectedAreas(self):
        """
        Checks through the grid to find islands/unconnected rooms
        Note, this can be slow for large grids and memory intensive since it needs to create a deep copy of the grid
        in order to use joinUnconnectedAreas() this needs to be called first and the returned list passed to joinUnconnectedAreas()
         
        Args:
            none
             
        Returns:
            A list of unconnected cells, where each group of cells is in its own list and each cell indice is stored as a tuple, ie [[(x1,y1), (x2,y2), (x3,y3)], [(xi1,yi1), (xi2,yi2), (xi3,yi3)]] 
        """

        unconnectedAreas = []
        areaCount = 0
        gridCopy = [[EMPTY for i in range(self.height)] for j in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]:
                    gridCopy[x][y] = 'x'
        for x in range(self.width):
            for y in range(self.height):
                if gridCopy[x][y] == 'x':
                    unconnectedAreas.append([])
                    areaCount += 1
                    self.floodFill(x, y, areaCount, None, gridCopy)
        for x in range(self.width):
            for y in range(self.height):
                if gridCopy[x][y]:
                    i = gridCopy[x][y]
                    unconnectedAreas[i - 1].append((x, y))
        return unconnectedAreas

    def findDeadends(self):
        """
        looks through all the corridors generated by generatePath() and joinUnconnectedAreas() to identify dead ends
        populates self.deadends and is used by pruneDeadends()
         
        Args:
            none
        Returns:
            none
        """

        self.deadends = []
        for x, y in self.corridors:
            touching = 0
            for nx, ny in self.find_neighbours_direct(x, y):
                if self.grid[nx][ny]: touching += 1
            if touching == 1: self.deadends.append((x, y))

    ##### GENERATION FUNCTIONS ##### 

    def placeRoom(self, startX, startY, roomWidth, roomHeight, ignoreOverlap=False):
        """
        place a defined quad within the grid and add it to self.rooms
         
        Args:
            x and y: integer, starting corner of the room, grid indicies
            roomWdith and roomHeight: integer, height and width of the room where roomWidth > x and roomHeight > y
            ignoreOverlap: boolean, if true the room will be placed irregardless of if it overlaps with any other tile in the grid
                note, if true then it is up to you to ensure the room is within the bounds of the grid
         
        Returns:
            True if the room was placed
        """

        if self.quad_fits(startX, startY, roomWidth, roomHeight, 0) or ignoreOverlap:
            for x in range(roomWidth):
                for y in range(roomHeight):
                    self.grid[startX + x][startY + y] = FLOOR
            self.rooms.append(DungeonRoom(startX, startY, roomWidth, roomHeight))
            return True

    def placeRandomRooms(self, minRoomSize, maxRoomSize, roomStep=1, margin=1, attempts=500, overlap=False, floor=FLOOR,
                         exclude=[]):
        """ 
        randomly places quads in the grid
        takes a brute force approach: randomly a generate quad in a random place -> check if fits -> reject if not
        Populates self.rooms
         
        Args:
            minRoomSize: integer, smallest size of the quad
            maxRoomSize: integer, largest the quad can be
            roomStep: integer, the amount the room size can grow by, so to get rooms of odd or even numbered sizes set roomSize to 2 and the minSize to odd/even number accordingly
            margin: integer, space in grid cells the room needs to be away from other tiles
            attempts: the amount of tries to place rooms, larger values will give denser room placements, but slower generation times
             
        Returns:
            none
        """

        for attempt in range(attempts):
            roomWidth = self.rnd.randrange(minRoomSize, maxRoomSize, roomStep)
            roomHeight = self.rnd.randrange(minRoomSize, maxRoomSize, roomStep)
            startX = self.rnd.randint(0, self.width)
            startY = self.rnd.randint(0, self.height)
            if not overlap:
                if self.quad_fits(startX, startY, roomWidth, roomHeight, margin):
                    for x in range(roomWidth):
                        for y in range(roomHeight):
                            self.grid[startX + x][startY + y] = floor
                    self.rooms.append(DungeonRoom(startX, startY, roomWidth, roomHeight))
            else:
                if self.quad_fits2(startX, startY, roomWidth, roomHeight, margin, exclude):
                    for x in range(roomWidth):
                        for y in range(roomHeight):
                            self.grid[startX + x][startY + y] = floor
                    self.rooms.append(DungeonRoom(startX, startY, roomWidth, roomHeight))

    def generateCaves(self, p=45, smoothing=4):
        """
        Generates more organic shapes using cellular automata
         
        Args:
            p: the probability that a cell will become a cave section, values between 30 and 45 work well
            smoothing: amount of noise reduction, lower values produce more jagged caves, little effect past 4
             
        Returns:
            None
        """

        for x in range(self.width):
            for y in range(self.height):
                if self.rnd.randint(0, 100) < p:
                    self.grid[x][y] = CAVE
        for i in range(smoothing):
            for x in range(self.width):
                for y in range(self.height):
                    if x == 0 or x == self.width or y == 0 or y == self.height:
                        self.grid[x][y] = EMPTY
                    touchingEmptySpace = 0
                    for nx, ny in self.find_neighbours(x, y):
                        if self.grid[nx][ny] == CAVE:
                            touchingEmptySpace += 1
                    if touchingEmptySpace >= 5:
                        self.grid[x][y] = CAVE
                    elif touchingEmptySpace <= 2:
                        self.grid[x][y] = EMPTY

    def generateCorridors(self, mode='r', x=None, y=None):
        """
        generates a maze of corridors on the growing tree algorithm, 
        where corridors do not overlap with over tiles, are 1 tile away from anything else and there are no diagonals
        Populates self.corridors
         
        Args:
            mode: char, either 'r', 'f', 'm' or 'l'
                  this controls how the next tile to attempt to move to is determined and affects how the generated corridors look
                  'r' - random selection, produces short straigh sections with spine like off-shoots, lots of deadends
                  'f' - first cell in the list to check, long straight secions and few diagnol snaking sections
                  'm' - similar to first but more likely to snake
                  'l' - snaking and winding corridor sections
            x and y: integer, grid indicies, starting point for the corridor generation,
                     if none is provided a random one will be chosen
             
            Returns:
                none
        """

        cells = []
        if not x and not y:
            x = self.rnd.randint(1, self.width - 2)
            y = self.rnd.randint(1, self.height - 2)
            while not self.can_carve(x, y, 0, 0):
                x = self.rnd.randint(1, self.width - 2)
                y = self.rnd.randint(1, self.height - 2)
        self.grid[x][y] = CORRIDOR
        self.corridors.append((x, y))
        cells.append((x, y))
        while cells:
            if mode == 'l':
                x, y = cells[-1]
            elif mode == 'r':
                x, y = self.rnd.choice(cells)
            elif mode == 'f':
                x, y = cells[0]
            elif mode == 'm':
                x, y = cells[len(cells) // 2]
            possMoves = self.get_possible_moves(x, y)
            if possMoves:
                xi, yi = self.rnd.choice(possMoves)
                self.grid[xi][yi] = CORRIDOR
                self.corridors.append((xi, yi))
                cells.append((xi, yi))
            else:
                cells.remove((x, y))

    def pruneDeadends(self, amount):
        """
        Removes deadends from the corridors/maze
        each iteration will remove all identified dead ends
        it will update self.deadEnds after
         
        Args:
            amount: number of iterations to remove dead ends
             
        Returns:
            none
        """
        for i in range(amount):
            self.findDeadends()
            for x, y in self.deadends:
                self.grid[x][y] = EMPTY
                self.corridors.remove((x, y))
        self.findDeadends()

    def placeWalls(self, type=WALL):
        """
        Places wall tiles around all floor, door and corridor tiles
        As some functions (like floodFill() and anything that uses it) dont
        distinguish between tile types it is best called later/last
         
        Args:
            none
             
        Returns:
            none
        """

        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y]:
                    for nx, ny in self.find_neighbours(x, y):
                        if self.grid[nx][ny] and self.grid[nx][ny] is not type:
                            self.grid[x][y] = type
                            break

    def connectAllRooms(self, extraDoorChance=0, doors=True):
        """
        Joins rooms to the corridors
        This not gauranteed to join everything, 
        depending on how rooms are placed and corridors generated it is possible to have unreachable rooms
        in that case joinUnconnectedAreas() can join them
        Populates self.doors
         
        Args:
            extraDoorChance: integer, where 0 >= extraDoorChance <= 100, the chance a room will have more than one connection to the corridors
        if extraDoorChance >= 100: extraDoorChance = 99
         
        Returns:
            list of dungeonRoom's that are not connected, this will not include islands, so 2 rooms connected to each other, but not the rest will not be included
        """

        unconnectedRooms = []
        for room in self.rooms:
            connections = []
            for i in range(room.width):
                if self.grid[room.x + i][room.y - 2]:
                    connections.append((room.x + i, room.y - 1))
                if room.y + room.height + 1 < self.height and self.grid[room.x + i][room.y + room.height + 1]:
                    connections.append((room.x + i, room.y + room.height))
            for i in range(room.height):
                if self.grid[room.x - 2][room.y + i]:
                    connections.append((room.x - 1, room.y + i))
                if room.x + room.width + 1 < self.width and self.grid[room.x + room.width + 1][room.y + i]:
                    connections.append((room.x + room.width, room.y + i))
            if connections and doors:
                chance = -1
                while chance <= extraDoorChance:
                    pickAgain = True
                    while pickAgain:
                        x, y = self.rnd.choice(connections)
                        pickAgain = False
                        for xi, yi in self.find_neighbours(x, y):
                            if self.grid[xi][yi] == DOOR:
                                pickAgain = True
                                break
                    chance = self.rnd.randint(0, 100)
                    self.grid[x][y] = DOOR
                    self.doors.append((x, y))
            else:
                unconnectedRooms.append(room)
        return unconnectedRooms

    def joinUnconnectedAreas(self, unconnectedAreas, style=CORRIDOR):
        """
        Forcibly connect areas not joined together
        This will work nearly every time (I've seen one test case where an area was still unjoined)
        But it will not always produce pretty results - connecting paths may cause diagonal touching
         
        Args:
            unconnectedAreas: the list returned by findUnconnectedAreas() - ie [[(x1,y1), (x2,y2), (x3,y3)], [(xi1,yi1), (xi2,yi2), (xi3,yi3)]]
         
        Returns:
            none
        """
        # connections = []
        while len(unconnectedAreas) >= 2:
            bestDistance = self.width + self.height
            c = [None, None]
            toConnect = unconnectedAreas.pop()
            for area in unconnectedAreas:
                for x, y in area:
                    for xi, yi in toConnect:
                        distance = abs(x - xi) + abs(y - yi)
                        if distance < bestDistance and (x == xi or y == yi):
                            bestDistance = distance
                            c[0] = (x, y)
                            c[1] = (xi, yi)

            if c[0] is None:
                break
            c.sort()

            x, y = c[0]
            for x in range(c[0][0] + 1, c[1][0]):
                if self.grid[x][y] == EMPTY:
                    self.grid[x][y] = style
            for y in range(c[0][1] + 1, c[1][1]):
                if self.grid[x][y] == EMPTY:
                    self.grid[x][y] = style
            self.corridors.append((x, y))

    ##### PATH FINDING FUNCTIONS #####                

    def constructNavGraph(self):
        """
        builds the navigation grapth for path finding
        must be called before findPath()
        Populates self.graph
         
        Args:
            none
             
        Returns:
            none
        """
        for x, y in self.corridors:
            if self.grid[x][y] < WALL: break
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] not in [WALL, EMPTY, OBSTACLE]:
                    self.graph[(x, y)] = []
                    for nx, ny in self.find_neighbours_direct(x, y):
                        if self.grid[nx][ny] not in [WALL, EMPTY, OBSTACLE]:
                            self.graph[(x, y)].append((nx, ny))

    def findPath(self, startX, startY, endX, endY):
        """
        finds a path between 2 points on the grid
        While not part of generating a dungeon/level it was included as I initially thought that
        since the generator had lots of knowledge about the maze it could use that for fast path finding
        however, the overhead of any heuristic was always greater than time saved. But I kept this as its useful
         
        Args:
            startX, startY: integers, grid indicies to find a path from
            endY, endY: integers, grid indicies to find a path to
         
        Returns:
            a list of grid cells (x,y) leading from the end point to the start point
            such that [(endX, endY) .... (startY, endY)] to support popping of the end as the agent moves
        """

        cells = []
        cameFrom = {}
        cells.append((startX, startY))
        cameFrom[(startX, startY)] = None
        while cells:
            # manhattan distance sort, commented out at slow, but there should you want it
            # cells.sort(key=lambda x: abs(endX-x[0]) + abs(endY - x[1]))
            current = cells[0]
            del cells[0]
            if current == (endX, endY):
                break
            for nx, ny in self.graph[current]:
                if (nx, ny) not in cameFrom:
                    cells.append((nx, ny))
                    cameFrom[(nx, ny)] = current
        if (endX, endY) in cameFrom:
            path = []
            current = (endX, endY)
            path.append(current)
            while current != (startX, startY):
                current = cameFrom[current]
                path.append(current)
            return path

    def doWalls(self, tileSize, max, var):

        self.segs = [[[None] for x in range(self.width)] for y in range(self.height)]
        max_segs = max

        for xi in range(len(self.grid)):
            for yi in range(len(self.grid[xi])):
                if self.grid[xi][yi] in WALLS:

                    x = xi * tileSize
                    y = yi * tileSize

                    # right top - bottom
                    if xi + 1 < len(self.grid):
                        if self.grid[xi + 1][yi] not in WALLS and self.grid[xi + 1][yi] != EMPTY:
                            num_segs = 1
                            if self.grid[xi + 1][yi] in ROUGHLINES:
                                num_segs = random.randint(2, max_segs)
                            seg = []
                            seg += [(int(x + tileSize), int(y))]
                            for r in range(1, num_segs):
                                sx = int(x + tileSize - random.randint(-var, var))
                                sy = int(y + (tileSize / (num_segs)) * r)
                                seg += [(sx, sy)]
                            seg += [(int(x + tileSize), int(y + tileSize))]
                            if self.segs[xi][yi] != [None]:
                                self.segs[xi][yi] += [seg]
                            else:
                                self.segs[xi][yi] = [seg]

                    # bottom right - left
                    if yi + 1 < len(self.grid[xi]):
                        if self.grid[xi][yi + 1] not in WALLS and self.grid[xi][yi + 1] != EMPTY:
                            num_segs = 1
                            if self.grid[xi][yi + 1] in ROUGHLINES:
                                num_segs = random.randint(2, max_segs)
                            seg = []
                            seg += [(int(x + tileSize), int(y + tileSize))]
                            for r in range(1, num_segs):
                                mx = int(x + tileSize - (tileSize / (num_segs)) * r)
                                seg += [(mx, int(y + tileSize - random.randint(-var, var)))]
                            seg += [(int(x), int(y + tileSize))]
                            if self.segs[xi][yi] != [None]:
                                self.segs[xi][yi] += [seg]
                            else:
                                self.segs[xi][yi] = [seg]

                    # left bottom-top
                    if xi - 1 > -1:
                        if self.grid[xi - 1][yi] not in WALLS and self.grid[xi - 1][yi] != EMPTY:
                            num_segs = 1
                            if self.grid[xi - 1][yi]  in ROUGHLINES:
                                num_segs = random.randint(2, max_segs)
                            seg = []
                            seg += [(int(x), int(y + tileSize))]
                            for r in range(1, num_segs):
                                seg += [(int(x - random.randint(-var, var)),
                                         int(y + tileSize - (tileSize / (num_segs)) * r))]
                            seg += [(int(x), int(y))]
                            if self.segs[xi][yi] != [None]:
                                self.segs[xi][yi] += [seg]
                            else:
                                self.segs[xi][yi] = [seg]

                    # top left - right
                    if yi - 1 > -1:
                        if self.grid[xi][yi - 1] not in WALLS and self.grid[xi][yi - 1] != EMPTY:
                            num_segs = 1
                            if self.grid[xi][yi - 1] in ROUGHLINES:
                                num_segs = random.randint(2, max_segs)
                            seg = []
                            seg += [(int(x), int(y))]
                            for r in range(1, num_segs):
                                seg += [(int(x + (tileSize / (num_segs)) * r), int(y - random.randint(-var, var)))]
                            seg += [(int(x + tileSize), int(y))]
                            if self.segs[xi][yi] != [None]:
                                self.segs[xi][yi] += [seg]
                            else:
                                self.segs[xi][yi] = [seg]



    def square(self, x, y, width, height, wall=WALL, fill=False, floor=FLOOR):
        # print(str(x)+'  '+str(y)+'  '+str(width)+'  '+str(height))
        self.rooms.append(DungeonRoom(x, y, width, height))

        for xi in range(x, x + width + 1):
            self.grid[xi][y] = wall
            self.grid[xi][y + height] = wall
        for yi in range(y, y + height):
            self.grid[x][yi] = wall
            self.grid[x + width][yi] = wall

        # pick random side for door
        rd = self.rnd.randint(0, 4)
        if rd == 0:
            xi = self.rnd.randint(x + 1, x + width - 1)
            self.grid[xi][y] = DOOR
        elif rd == 1:
            xi = self.rnd.randint(x + 1, x + width - 1)
            self.grid[xi][y + height] = DOOR
        elif rd == 2:
            yi = self.rnd.randint(y + 1, y + height - 1)
            self.grid[x][yi] = DOOR
        else:
            yi = self.rnd.randint(y + 1, y + height - 1)
            self.grid[x + width][yi] = DOOR

        if fill:
            for xi in range(x + 1, x + width):
                for yi in range(y + 1, y + height):
                    self.grid[xi][yi] = floor

    def printGrid(self):
        print()
        for xi in range(len(self.grid)):
            ro = ''
            for yi in range(len(self.grid[xi])):
                ro += '{:2d}'.format(self.grid[yi][xi]) + ''
            print(str(ro))

    def place_round_room(self, startX, startY, size, width=0, floor=FLOOR, ignoreOverlap=True):
        roomWidth = size
        roomHeight = size
        cent = Vex(startX + size / 2, startY + size / 2)
        if self.quad_fits(startX, startY, roomWidth, roomHeight, 0) or ignoreOverlap:
            for x in range(roomWidth):
                for y in range(roomHeight):
                    cp = Vex(startX + x, startY + y)
                    d = cent.dist2D(cp)
                    if width <= 0:
                        if d < size / 2:
                            if -1 < (startX + x) < self.width and -1 < (startY + y) < self.height:
                                self.grid[startX + x][startY + y] = floor
                    else:
                        if size / 2 - width < d < size / 2:
                            if -1 < (startX + x) < self.width and -1 < (startY + y) < self.height:
                                self.grid[startX + x][startY + y] = floor
            self.rooms.append(DungeonRoom(startX, startY, roomWidth, roomHeight))
            return True
        pass

    @staticmethod
    def gen_city(seed, width, height):
        print('seed:'+str(seed))
        # seed = 2497015709609
        dm = DungeonGenerator(random.Random(seed), width, height)
        dm.bg_color = (132, 126, 135)
        dm.displayEmpty = False
        dm.layer_empty = True
        rms = dm.rnd.randint(3*width, 7*width)
        # rms = dm.rnd.randint(200,300)
        rps = dm.rnd.randint(1, 1)
        dm.placeRandomRooms(3, 6, 1, 2, rms, True)

        dm.generateCorridors('f')
        dm.connectAllRooms(0, False)
        dm.pruneDeadends(50)

        # join unconnected areas
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        self = dm

        for xi in range(width):
            for yi in range(height):
                if dm.grid[xi][yi] == CORRIDOR:
                    dm.grid[xi][yi] = ROADI

        # PLACE ROADS HORIZONTAL AND VERTICAL
        for xi in range(dm.width):
            for yi in range(dm.height):
                if dm.grid[xi][yi] in FLOORS:
                    xin, yin = False, False
                    if xi - 1 > -1 and xi + 1 < dm.width:
                        if dm.grid[xi - 1][yi] in FLOORS and dm.grid[xi + 1][yi] in FLOORS:
                            dm.grid[xi][yi] = ROADH
                    if yi - 1 > -1 and yi + 1 < dm.height:
                        if dm.grid[xi][yi - 1] in FLOORS and dm.grid[xi][yi + 1] in FLOORS:
                            dm.grid[xi][yi] = ROADV

        mk_grass = []
        for xi in range(width):
            for yi in range(height):
                if dm.grid[xi][yi] in FLOORS:
                    ngt = dm.get_neighbors_t(xi,yi)
                    ngx = dm.get_neighbors_x(xi,yi)
                    if all_in_list(FLOORS,ngt) and all_in_list(FLOORS,ngx):
                        mk_grass += [(xi, yi)]
        for mg in mk_grass:
            dm.grid[mg[0]][mg[1]] = GRASS

        for yi in range(0, height, 6):
            err = dm.rnd.randint(2, 6)
            for xi in range(0, width):
                if xi%err == 0:
                    off =  dm.rnd.randint(0,err*2)-err
                if dm.grid[xi][clamp(yi+off,0,height-1)] == GRASS:
                    dm.grid[xi][clamp(yi+off,0,height-1)] = ROADH

        for xi in range(0, width, 6):
            err = dm.rnd.randint(2, 6)
            for yi in range(0, height):
                if yi%err == 0:
                    off = dm.rnd.randint(0, err * 2) - err
                if dm.grid[clamp(xi+off,0,height-1)][yi] == GRASS:
                    dm.grid[clamp(xi+off,0,height-1)][yi] = ROADV

        mk_grass = []
        for xi in range(width):
            for yi in range(height):
                if dm.grid[xi][yi] in FLOORS:
                    ngt = dm.get_neighbors_t(xi,yi)
                    ngx = dm.get_neighbors_x(xi,yi)
                    if all_in_list(FLOORS,ngt) and all_in_list(FLOORS,ngx):
                        mk_grass += [(xi, yi)]
        for mg in mk_grass:
            dm.grid[mg[0]][mg[1]] = GRASS

        dm.connect_corner_tiles(FLOORS, ROADS, (ROADTRT, ROADTTL, ROADTLB, ROADTBR, ROADI))
        dm.connect_intersection_tiles(FLOORS, ROADS, (ROADIB, ROADIL, ROADIT, ROADIR))
        dm.connect_corner_tiles(FLOORS, ROADS, (ROADTRT, ROADTTL, ROADTLB, ROADTBR, ROADI))

        dm.placeWalls(CITY)

        dm.enclose(CITY)

        dm.do_city_walls()

        dm.replace(CITY, GRASS)
        
        dm.connect_corner_tiles(CITYWALLS, CITYWALLS, (CITYTRT, CITYTTL, CITYTLB, CITYTBR, CITYI))
        dm.connect_intersection_tiles(CITYWALLS, CITYWALLS, (CITYIB, CITYIL, CITYIT, CITYIR))
        dm.connect_corner_tiles(CITYWALLS, CITYWALLS, (CITYTRT, CITYTTL, CITYTLB, CITYTBR, CITYI))

        dm.do_deadends(ROADS, ROADS, (ROADDD,ROADDL,ROADDU,ROADDR))
        dm.do_deadends(CITYWALLS, CITYWALLS, (CITYDD, CITYDL,CITYDU,CITYDR))

        for xi in range(width):
            for yi in range(height):
                if dm.grid[xi][yi] == ROADI:
                    ngt = dm.get_neighbors_t(xi,yi)
                    ngx = dm.get_neighbors_x(xi,yi)
                    if all_in_list(ROADS,ngt) and all_in_list(ROADS,ngx):
                        dm.grid[xi][yi] = GRASS
                if dm.grid[xi][yi] in CITYWALLS:
                    ngt = dm.get_neighbors_t(xi,yi)
                    if ngt[0] not in CITYWALLS and ngt[1] not in CITYWALLS and \
                            ngt[2] not in CITYWALLS and ngt[3] not in CITYWALLS:
                        dm.grid[xi][yi] = GRASS

        dm.test_side_tiles((CITYH,CITYV),CITYWALLS,[None,GRASS,EMPTY]+FLOORS,(CITYV,CITYH))
        dm.test_side_tiles((ROADH,ROADV),ROADS,[GRASS]+CITYWALLS,(ROADV,ROADH))

        # i WANT LAYERED FLARE NOT REPLACEMENT OF TILES
        #dm.replace_rng_tile([GRASS], (TREE, GRASS, BUSH, MOUNTAIN), (3, 3, 3, 3))

        dm.active_tiles = [EMPTY]
        dm.active_tiles += [CITY]
        dm.active_tiles += CITYWALLS
        dm.active_tiles += ROADS
        dm.active_tiles += [GRASS]
        dm.active_tiles += [DOOR]
        return dm

    def connect_corner_tiles(self, triggers, listof, output):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in triggers:
                    ngh = self.get_neighbors_t(xi, yi)
                    if ngh[1] in listof and ngh[2] in listof and ngh[0] not in listof and ngh[3] not in listof:
                        self.grid[xi][yi] = output[0]  # good
                    if ngh[2] in listof and ngh[0] in listof and ngh[1] not in listof and ngh[3] not in listof:
                        self.grid[xi][yi] = output[1]
                    if ngh[0] in listof and ngh[3] in listof and ngh[1] not in listof and ngh[2] not in listof:
                        self.grid[xi][yi] = output[2]  # good
                    if ngh[3] in listof and ngh[1] in listof and ngh[0] not in listof and ngh[2] not in listof:
                        self.grid[xi][yi] = output[3]
                    cr = 0
                    for r in ngh:
                        if r in listof:
                            cr += 1
                        else:
                            break
                    if cr > 3:
                        self.grid[xi][yi] = output[4]

    def connect_intersection_tiles(self, triggers, listof, s_output):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in triggers:
                    ngh = self.get_neighbors_t(xi, yi)
                    if ngh[1] in listof and ngh[2] in listof and ngh[0] in listof and ngh[3] not in listof:
                        self.grid[xi][yi] = s_output[0]  # good
                    if ngh[2] in listof and ngh[0] in listof and ngh[3] in listof and ngh[1] not in listof:
                        self.grid[xi][yi] = s_output[1]
                    if ngh[0] in listof and ngh[3] in listof and ngh[1] in listof and ngh[2] not in listof:
                        self.grid[xi][yi] = s_output[2]  # good
                    if ngh[3] in listof and ngh[1] in listof and ngh[2] in listof and ngh[0] not in listof:
                        self.grid[xi][yi] = s_output[3]

    def test_intersection_tiles(self,triggers,f_list,f_output):
        # not working correctly
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in triggers:
                    ngh = self.get_neighbors_t(xi, yi)
                    if self.grid[xi][yi] == triggers[0]:
                        if ngh[3] in f_list and ngh[0] not in f_list and ngh[1] not in f_list:
                            self.grid[xi][yi] = f_output[0]
                    if self.grid[xi][yi] == triggers[1]:
                        if ngh[0] in f_list and ngh[2] not in f_list and ngh[3] not in f_list:
                            self.grid[xi][yi] = f_output[1]  # good
                    if self.grid[xi][yi] == triggers[2]:
                        if ngh[2] in f_list and ngh[0] not in f_list and ngh[1] not in f_list:
                            self.grid[xi][yi] = f_output[2]
                    if self.grid[xi][yi] == triggers[3]:
                        if ngh[1] in f_list and ngh[2] not in f_list and ngh[3] not in f_list:
                            self.grid[xi][yi] = f_output[3]  # good

    def test_side_tiles(self, triggers, sa_list, sb_list, f_output):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in triggers:
                    ngh = self.get_neighbors_t(xi, yi)
                    if self.grid[xi][yi] == triggers[0]:
                        if ngh[0] not in sa_list or ngh[1] not in sa_list or \
                                        ngh[2] not in sb_list or ngh[3] not in sb_list:
                            self.grid[xi][yi] = f_output[0]
                        else:
                            self.grid[xi][yi] = f_output[1]

                    elif self.grid[xi][yi] == triggers[1]:
                        if ngh[2] not in sa_list or ngh[3] not in sa_list or \
                                        ngh[0] not in sb_list or ngh[1] not in sb_list:
                            self.grid[xi][yi] = f_output[1]
                        else:
                            self.grid[xi][yi] = f_output[0]

    def do_deadends(self, triggers, listof, output):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in triggers:
                    ngh = self.get_neighbors_t(xi, yi)
                    if ngh[1] in listof and ngh[2] not in listof and ngh[0] not in listof and ngh[3] not in listof:
                        self.grid[xi][yi] = output[3]  # good
                    if ngh[2] in listof and ngh[0] not in listof and ngh[3] not in listof and ngh[1] not in listof:
                        self.grid[xi][yi] = output[2]
                    if ngh[0] in listof and ngh[3] not in listof and ngh[1] not in listof and ngh[2] not in listof:
                        self.grid[xi][yi] = output[1]  # good
                    if ngh[3] in listof and ngh[1] not in listof and ngh[2] not in listof and ngh[0] not in listof:
                        self.grid[xi][yi] = output[0]

    def do_city_walls(self):
        dm = self
        for xi in range(dm.width):
            for yi in range(dm.height):
                if dm.grid[xi][yi] in WALLS:
                    ngt = dm.get_neighbors_t(xi, yi)
                    if ngt[0] == EMPTY or ngt[0] is None and ngt[1] in FLOORS or ngt[1] == GRASS and ngt[2] in WALLS and \
                                    ngt[3] in WALLS:
                        dm.grid[xi][yi] = CITYV
                    if ngt[2] == EMPTY or ngt[2] is None and ngt[3] in FLOORS or ngt[3] == GRASS and ngt[0] in WALLS and \
                                    ngt[1] in WALLS:
                        dm.grid[xi][yi] = CITYH
                    if ngt[1] == EMPTY or ngt[1] is None and ngt[0] in FLOORS or ngt[0] == GRASS and ngt[2] in WALLS and \
                                    ngt[3] in WALLS:
                        dm.grid[xi][yi] = CITYV
                    if ngt[3] == EMPTY or ngt[3] is None and ngt[2] in FLOORS or ngt[2] == GRASS and ngt[0] in WALLS and \
                                    ngt[1] in WALLS:
                        dm.grid[xi][yi] = CITYH

                    if dm.grid[xi][yi] == CITY:
                        ngx = dm.get_neighbors_x(xi, yi)
                        if (EMPTY in ngx or None in ngx) and (
                                        ngt[0] in WALLS or ngt[2] in WALLS or ngt[1] in WALLS or ngt[3] in WALLS):
                            dm.grid[xi][yi] = CITYH

    def do_city_wall_corners(self):
        dm = self
        for xi in range(dm.width):
            for yi in range(dm.height):
                if dm.grid[xi][yi] in CITYWALLS:
                    ngh = dm.get_neighbors_t(xi, yi)
                    if ngh[3] in CITYWALLS and ngh[1] in CITYWALLS:
                        print(ngh)
                        if ngh[3] in [10, 16] and ngh[1] in [7, 17]:
                            dm.grid[xi][yi] = CITYWTL
                            continue
                        elif ngh[3] in [8, 18] and ngh[1] in [9, 16]:
                            dm.grid[xi][yi] = CITYWTLI
                            continue
                    if ngh[2] in CITYWALLS and ngh[1] in CITYWALLS:
                        if ngh[2] in [10, 16] and ngh[1] in [9, 16]:
                            dm.grid[xi][yi] = CITYWBL
                            continue
                        elif ngh[2] in [8, 16] and ngh[1] in [7, 17]:
                            dm.grid[xi][yi] = CITYWBLI
                            continue
                    if ngh[0] in CITYWALLS and ngh[3] in CITYWALLS:
                        if ngh[0] in [7, 17] and ngh[3] in [8, 18]:
                            dm.grid[xi][yi] = CITYWTR
                            continue
                        elif ngh[0] in [9, 16] and ngh[3] in [10, 16]:
                            dm.grid[xi][yi] = CITYWTRI
                            continue
                    if ngh[0] in CITYWALLS and ngh[2] in CITYWALLS:
                        if ngh[0] in [9, 16] and ngh[2] in [8, 16]:
                            dm.grid[xi][yi] = CITYWBR
                            continue
                        elif ngh[0] in [7, 17] and ngh[2] in [10, 16]:
                            dm.grid[xi][yi] = CITYWBRI
                            continue

    def replace(self, existing, new):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] == existing:
                    if yi > 0 or xi > 0 or yi < self.height - 1 or xi < self.width - 1:
                        self.grid[xi][yi] = new

    @staticmethod
    def gen_castle(seed, width, height):
        dm = DungeonGenerator(random.Random(seed), width, height)
        dm.bg_color = (132, 126, 135)
        rad = 15
        dm.placeRoom(int(rad / 2), int(rad / 2), 3, height - (rad + 2))
        dm.placeRoom(int(rad / 2), int(rad / 2), width - (rad + 2), 3)
        dm.placeRoom(int(rad / 2), int(height - (rad / 2 + 3)), width - (rad + 2), 3)
        dm.placeRoom(int(width - (rad / 2 + 3)), int(rad / 2), 3, height - (rad + 2))

        style = dm.rnd.randint(0, 3)
        if style == 0:
            dm.place_round_room(1, 1, rad, 3)
            dm.place_round_room(1, height - (rad + 2), rad)
            dm.place_round_room(width - (rad + 2), 1, rad, 1)
            dm.place_round_room(width - (rad + 2), height - (rad + 2), rad)
        elif style == 1:
            num = dm.rnd.randint(1, 6)
            for i in range(num):
                rad = dm.rnd.randint(6, 15)
                sx = dm.rnd.randint(rad, width - rad)
                sy = dm.rnd.randint(rad, width - rad)
                dm.place_round_room(sx, sy, rad)
        elif style == 3:
            dm.placeRandomRooms(5, 15, 1, 1, 3000)
            dm.place_round_room(width / 2, height / 2, width / 2 - 5)

        dm.placeRandomRooms(5, 15, 1, 1, 3000)
        dm.generateCorridors('f')
        dm.connectAllRooms(0)
        dm.pruneDeadends(50)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)

        # dm.printGrid()
        dm.placeWalls(CASTLE)
        # dm.enclose2(1, FLOOR)
        dm.enclose(CASTLE)
        dm.active_tiles = [EMPTY]
        dm.active_tiles += [CASTLE]
        dm.active_tiles += [FLOOR]
        dm.active_tiles += [CORRIDOR]
        dm.active_tiles += [DOOR]
        dm.active_tiles += [LAVA]
        return dm

    @staticmethod
    def gen_mountains(seed, width, height):

        dm = DungeonGenerator(random.Random(seed), width, height)
        dm.bg_color = (132, 126, 135)
        dm.generateCaves(40, 4)
        # clear away small islands
        unconnected = dm.findUnconnectedAreas()
        for area in unconnected:
            if len(area) < 35:
                for x, y in area:
                    dm.grid[x][y] = EMPTY
        # generate rooms and corridors
        # dm.placeRandomRooms(3, 5, 1, 1, 2000)
        x, y = dm.findEmptySpace(3)
        while x:
            dm.generateCorridors('l', x, y)
            x, y = dm.findEmptySpace(3)
        # join it all together
        dm.connectAllRooms(0)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        dm.pruneDeadends(40)
        dm.placeWalls(MOUNTAIN)
        # dm.printGrid()
        # ensure that there is no escape from array without exit
        dm.enclose(MOUNTAIN)
        dm.active_tiles = [EMPTY]
        dm.active_tiles += [MOUNTAIN]
        dm.active_tiles += [CAVE]
        dm.active_tiles += [CORRIDOR]

        return dm

    @staticmethod
    def gen_caves(seed, width, height):

        dm = DungeonGenerator(random.Random(seed), width, height)
        dm.bg_color = (217, 160, 102)
        dm.generateCaves(40, 4)
        # clear away small islands
        unconnected = dm.findUnconnectedAreas()
        for area in unconnected:
            if len(area) < 35:
                for x, y in area:
                    dm.grid[x][y] = EMPTY
        # generate rooms and corridors
        # dm.placeRandomRooms(3, 5, 1, 1, 2000)
        x, y = dm.findEmptySpace(3)
        while x:
            dm.generateCorridors('l', x, y)
            x, y = dm.findEmptySpace(3)
        # join it all together
        dm.connectAllRooms(0)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        dm.pruneDeadends(40)
        dm.placeWalls()
        # dm.printGrid()
        # ensure that there is no escape from array without exit
        dm.enclose(WALL)
        dm.active_tiles = [EMPTY]
        dm.active_tiles += [WALL]
        dm.active_tiles += [CAVE]
        dm.active_tiles += [CORRIDOR]
        return dm

    @staticmethod
    def genCaveRoom(seed, width, height):

        dm = DungeonGenerator(random.Random(seed), width, height)

        dm.generateCaves(40, 4)
        # clear away small islands
        unconnected = dm.findUnconnectedAreas()
        for area in unconnected:
            if len(area) < 35:
                for x, y in area:
                    dm.grid[x][y] = EMPTY
        # generate rooms and corridors
        dm.placeRandomRooms(3, 5, 1, 1, 2000)
        x, y = dm.findEmptySpace(3)
        while x:
            dm.generateCorridors('l', x, y)
            x, y = dm.findEmptySpace(3)
        # join it all together
        dm.connectAllRooms(0)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        dm.pruneDeadends(40)
        dm.placeWalls()
        # dm.printGrid()
        # ensure that there is no escape from array without exit
        dm.enclose(WALL)
        dm.active_tiles = [EMPTY]
        dm.active_tiles += [WALL]
        dm.active_tiles += [EMPTY]
        return dm

    @staticmethod
    def genSpiderRooms(seed, width, height):
        dm = DungeonGenerator(random.Random(seed), width, height)
        dm.generateCorridors()
        dm.pruneDeadends(20)

        dm.placeWalls()
        x, y = dm.corridors[1]
        dm.floodFill(x, y, CORRIDOR)

        dm.placeRandomRooms(4, 9, 1, 1, 3000)
        dm.connectAllRooms(30)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        # dm.printGrid()
        return dm.doWalls()

    @staticmethod
    def genPlanetDungeon(seed, width, height):
        gc = Vex(width / 2.0, height / 2.0)
        dm = DungeonGenerator(random.Random(seed), width, height)
        rad = (width / 2.0) - 5

        dm.placeRoom(int(width / 2) - 5, int(height / 2) - 5, 10, 10, True)
        dm.placeRandomRooms(5, 15, 1, 1, 3000)
        # determine the 4 quadrants of a circle and organize
        #        for i in range(20):
        #            sx = rnd.randint(0, width)
        #            sy = rnd.randint(0, height)
        #            sv = Vex(sx, sy)
        #            rw = rnd.randint(2, 5)
        #            rh = rnd.randint(2, 5)
        #            rv = Vex(sx+rw, sy+rh)
        #            if sv.dist2D(gc) < rad and rv.dist2D(gc) < rad:
        #                dm.placeRoom(sx, sy, rw, rh, True)

        dm.generateCorridors('r')
        dm.connectAllRooms(0)
        dm.pruneDeadends(20)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        for x in range(len(dm.grid)):
            for y in range(len(dm.grid[x])):
                v = Vex(x, y)
                if v.dist2D(gc) > rad:
                    dm.grid[x][y] = 0
        # dm.printGrid()

        return dm

    @staticmethod
    def genRooms(seed, width, height):
        dm = DungeonGenerator(random.Random(seed), width, height)

        dm.placeRandomRooms(5, 15, 1, 1, 3000)
        dm.generateCorridors('l')
        dm.connectAllRooms(0)
        dm.pruneDeadends(50)

        # join unconnected areas
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        # dm.printGrid()
        return dm

    @staticmethod
    def gen_forest(rnd, width, height):
        dm = DungeonGenerator(random.Random(rnd), width, height)
        dm.bg_color = (75, 155, 47)
        dm.layer_empty = True
        dm.displayEmpty = True
        random.seed(rnd)
        for xi in range(width):
            for yi in range(height):
                dm.grid[xi][yi] = FLOOR

        dm.replace_rng_tile([FLOOR], [TREEI, BUSH, MOUNTAIN], [5, 10, 5])

        q = dm.rnd.randint(1, 5)
        for i in range(q):
            rw = dm.rnd.randint(3, 7)
            rh = dm.rnd.randint(3, 7)
            sx = dm.rnd.randint(2, (dm.width - 2) - rw)
            sy = dm.rnd.randint(2, (dm.height - 2) - rh)
            dm.square(sx, sy, rw, rh, WOOD, True, PLANCK)
        dm.enclose(TREE)
        for xi in range(width):
            dm.grid[xi][0] = TREEH
            dm.grid[xi][height-1]=TREEH
        for yi in range(height):
            dm.grid[0][yi] = TREEV
            dm.grid[width-1][yi]=TREEV
        dm.grid[0][0] = TREETLC
        dm.grid[width-1][0]=TREETRC
        dm.grid[width-1][height-1]=TREEBRC
        dm.grid[0][height-1]=TREEBLC

        dm.replace(FLOOR,EMPTY)
        dm.active_tiles = [EMPTY, TREE, PLANCK, BUSH, WOOD, GRASS, FLOOR, MOUNTAIN] + TREES
        return dm

    @staticmethod
    def gen_forest_lake(rnd, width, height):
        dm = DungeonGenerator(random.Random(rnd), width, height)

        dm.bg_color = (75, 105, 47)
        random.seed(rnd)

        dm.generateCaves(40, 25)
        # clear away small islands
        # unconnected = dm.findUnconnectedAreas()
        # for area in unconnected:
        #     if len(area) < 35:
        #         for x, y in area:
        #             dm.grid[x][y] = EMPTY

        for xi in range(0, dm.width):
            for yi in range(0, dm.height):
                if dm.grid[xi][yi] != CAVE:
                    dm.grid[xi][yi] = FLOOR
                else:
                    dm.grid[xi][yi] = WATER

        for xi in range(dm.width):
            for yi in range(dm.height):
                n = random.randint(0, 1000) / 10
                if n < 5:
                    if dm.exclude_neighbors(xi, yi, LAKES):
                        dm.grid[xi][yi] = TREE
                n = random.randint(0, 1000) / 10
                if n < 100:
                    if dm.exclude_neighbors(xi, yi, LAKES):
                        dm.grid[xi][yi] = GRASS
                n = random.randint(0, 1000) / 10
                if n < 10:
                    if dm.exclude_neighbors(xi, yi, LAKES):
                        dm.grid[xi][yi] = BUSH

        dm.enclose2(1, FLOOR)
        dm.enclose(TREE)
        dm.active_tiles = [EMPTY]
        dm.active_tiles += [TREE]
        dm.active_tiles += [BUSH]
        dm.active_tiles += [WATER]
        dm.active_tiles += [GRASS]
        dm.active_tiles += [FLOOR]
        return dm

    def replace_rng_tile(self, source, outs, percents):
        for xi in range(self.width):
            for yi in range(self.height):
                if self.grid[xi][yi] in source:
                    for i in range(len(outs)):
                        n = random.randint(0, 1000) / 10
                        if n < percents[i]:
                            self.grid[xi][yi] = outs[i]

    def exclude_neighbors(self, x, y, list):
        if 0 <= x - 1:
            if self.grid[x - 1][y] in list:
                return False
        if x + 1 < self.width:
            if self.grid[x + 1][y] in list:
                return False
        if 0 <= y - 1:
            if self.grid[x][y - 1] in list:
                return False
        if y + 1 < self.height:
            if self.grid[x][y + 1] in list:
                return False
        return True

    def get_neighbors_t(self, x, y):
        ls = []
        if 0 <= x - 1:
            ls += [self.grid[x - 1][y]]
        else:
            ls += [None]
        if x + 1 < self.width:
            ls += [self.grid[x + 1][y]]
        else:
            ls += [None]
        if 0 <= y - 1:
            ls += [self.grid[x][y - 1]]
        else:
            ls += [None]
        if y + 1 < self.height:
            ls += [self.grid[x][y + 1]]
        else:
            ls += [None]
        return ls

    def get_neighbors_x(self, x, y):
        ls = []
        if 0 <= x - 1 and 0 <= y - 1:  # top left
            ls += [self.grid[x - 1][y - 1]]
        else:
            ls += [None]
        if x + 1 < self.width and 0 <= y - 1:  # top right
            ls += [self.grid[x + 1][y - 1]]
        else:
            ls += [None]
        if 0 <= x - 1 and y + 1 < self.height:  # bottom left
            ls += [self.grid[x - 1][y + 1]]
        else:
            ls += [None]
        if x + 1 < self.width and y + 1 < self.height:  # bottom right
            ls += [self.grid[x + 1][y + 1]]
        else:
            ls += [None]
        return ls

    def enclose(self, structure):
        for xi in range(self.width):
            if self.grid[xi][0] != EMPTY:
                self.grid[xi][0] = structure
            if self.grid[xi][self.width - 1] != EMPTY:
                self.grid[xi][self.width - 1] = structure
        for yi in range(self.height):
            if self.grid[0][yi] != EMPTY:
                self.grid[0][yi] = structure
            if self.grid[self.height - 1][yi] != EMPTY:
                self.grid[self.height - 1][yi] = structure

    def enclose2(self, offset, structure):
        for xi in range(self.width):
            if self.grid[xi][offset] != EMPTY:
                self.grid[xi][offset] = structure
            if self.grid[xi][(self.width - 1) - (offset)] != EMPTY:
                self.grid[xi][(self.width - 1) - (offset)] = structure
        for yi in range(self.height):
            if self.grid[offset][yi] != EMPTY:
                self.grid[offset][yi] = structure
            if self.grid[(self.height - 1) - (offset)][yi] != EMPTY:
                self.grid[(self.height - 1) - (offset)][yi] = structure
                # for yi in range(len(self.grid[xi])):

    def pygame_init(self):
        Environment.Environment()
        pygame.init()

    def run(self, cam):
        DG = DungeonGenerator
        fog_surf = pygame.Surface((self.width + 2, self.height + 2)).convert_alpha()
        player = cam.player
        # player is in dungeon
        cam.player.in_dungeon = True
        entered_dungeon = True

        view_size = int((10 + DG.DUNGEON_SCALE * DG.DUNGEON_SCALE) / DG.DUNGEON_SCALE)

        hts = int(DG.DUNGEON_TILE_SIZE / 2)
        env = Environment.Environment

        tiles = []

        for row in range(0, len(self.grid)):
            for col in range(0, len(self.grid[row])):
                x = (row * DG.DUNGEON_TILE_SIZE - cam.dmpos.x())
                y = (col * DG.DUNGEON_TILE_SIZE - cam.dmpos.y())

                if entered_dungeon:
                    if self.grid[row][col] in FLOORS:
                        entered_dungeon = False
                        cam.pos.set2D(x + DG.DUNGEON_TILE_SIZE / 2, y + DG.DUNGEON_TILE_SIZE / 2)
                        cam.dmpos.set2D(x + DG.DUNGEON_TILE_SIZE / 2, y + DG.DUNGEON_TILE_SIZE / 2)
                        break
            else:
                continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)

        # set the dungeons font
        myfont = pygame.font.SysFont("consolas", 15)

        # prep the terminator
        exit_dungeon = False

        # ignite the clock and set fps
        clock = pygame.time.Clock()
        f_p_s = 60

        max_wall_segments = 10
        variance = 10
        self.doWalls(DG.DUNGEON_TILE_SIZE, max_wall_segments, variance * DG.DUNGEON_SCALE)
        delta_time2 = 1
        wt = 0

        while not exit_dungeon:

            env.clear_visible_objects()
            env.clear_edges()

            pygame.display.set_caption(('FPS: ' + str("%.2f" % (1000.0 / delta_time2))))
            delta_time = delta_time2 / 1000.0
            env.getScreen().fill(self.bg_color)

            Environment.interact = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_dungeon = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_dungeon = True
                cam.events(event)

            key = pygame.key.get_pressed()
            cam.update(delta_time, key)

            cdx = int(cam.dmpos.x() / DG.DUNGEON_TILE_SIZE)
            cdy = int(cam.dmpos.y() / DG.DUNGEON_TILE_SIZE)

            if -1 < cdy < len(self.grid[0]) and -1 < cdx < len(self.grid):
                if self.grid[cdx][cdy] in WALLS:
                    cam.pos.assign(cam.lpos)
                    cam.dmpos.assign(cam.ldmpos)

            tiles.clear()
            tiles = []

            for ix in range(cdx - view_size, cdx + view_size):
                for iy in range(cdy - view_size, cdy + view_size):
                    if -1 < ix < self.width and -1 < iy < self.height:
                        tiles += [Tile(ix, iy, self.grid[ix][iy])]


            tiles.sort(key=lambda x: x.tile, reverse=True)

            for t in tiles:
                row = t.x
                col = t.y
                tile = t.tile
                # for row in range(0, len(self.grid)):
                #   for col in range(0, len(self.grid[row])):
                x = (row * DG.DUNGEON_TILE_SIZE - cam.dmpos.x())
                y = (col * DG.DUNGEON_TILE_SIZE - cam.dmpos.y())

                if tile in LAKES:
                    # rect = image[tile].get_bounding_rect()
                    fog_surf.set_at((t.x + 1, t.y + 1), (99, 155, 255))
                elif tile in WALLS:
                    fog_surf.set_at((t.x + 1, t.y + 1), (255, 255, 255))
                elif tile in ROADS:
                    fog_surf.set_at((t.x + 1, t.y + 1), (155, 155, 155))
                elif tile == GRASS:
                    fog_surf.set_at((t.x + 1, t.y + 1), (85, 255, 85))

                if -DG.DUNGEON_TILE_SIZE <= x + env.center_x <= env.screen_width + DG.DUNGEON_TILE_SIZE and \
                                        -DG.DUNGEON_TILE_SIZE <= y + env.center_x <= env.screen_width + DG.DUNGEON_TILE_SIZE:

                    # x, y = (Vex(x + DG.DUNGEON_TILE_SIZE / 2,
                    #             y + DG.DUNGEON_TILE_SIZE / 2) + env.center).p2D()  # .rotate2dXY(cam.rotSC[0])

                    # if DG.DUNGEON_IMAGES[tile] is not None:
                        # rect = image[EMPTY].get_bounding_rect()
                    if tile in LAKES:
                        # rect = image[tile].get_bounding_rect()
                        fog_surf.set_at((t.x + 1, t.y + 1), (99, 155, 255))
                    elif tile in WALLS:
                        fog_surf.set_at((t.x + 1, t.y + 1), (255, 255, 255))
                    elif tile in ROADS:
                        fog_surf.set_at((t.x + 1, t.y + 1), (155, 155, 155))
                    elif tile == GRASS:
                        fog_surf.set_at((t.x + 1, t.y + 1), (85, 255, 85))
                        # if tile != EMPTY and self.layer_empty:
                        #     env.screen.blit(DG.DUNGEON_IMAGES[EMPTY], (x - hts, y - hts))
                        # if tile == EMPTY and self.displayEmpty:
                        #     env.screen.blit(DG.DUNGEON_IMAGES[tile], (x - hts, y - hts))
                        # elif tile != EMPTY:
                        #     env.screen.blit(DG.DUNGEON_IMAGES[tile], (x - hts, y - hts))

                    if self.draw_lines or not self.draw_lines:
                        # fog_surf.set_at((t.x + 1, t.y + 1), (85, 0, 225))
                        if self.segs[row][col] != [None]:

                            for ss in self.segs[row][col]:
                                segs = []
                                for s in ss:
                                    sx, sy = (Vex(s[0] - cam.dmpos.x(),
                                                  s[1] - cam.dmpos.y()) + env.center).p2D()  # .rotate2dXY(cam.rotSC[0])
                                    segs += [(sx, sy)]
                                    # segs += [(s[0] - cam.pos.x(), s[1] - cam.pos.y())]
                                pygame.draw.lines(env.screen, (255, 255, 255), False, segs, 1)

            # ParticleEngine.Emitter.update(cam)
            Shot.Shot.update_in_dungeon(cam)
            env.player.update(cam)
            # Mind.update(cam)
            DrawINFO.update(cam)
            # draw_bar(300, 0, Color.BLUE, player.creature.stats.xp, player.creature.stats.nxtlvlxp, "XP",myfont)
            draw_bar(300, 0, Color.BLUE, 100 - player.creature.weapon.getTemp(), 100, "Energy", myfont)
            draw_bar(300, 1, Color.RED, player.creature.stats.getHP(), player.creature.stats.getHTH(), "Health", myfont)

            draw_bar(300, 3, Color.RED, float('{0:.2f}'.format(1000.0 / delta_time2)), 60, "FPS", myfont)
            draw_bar(300, 4, Color.RED, cdx, cdy,
                     "POS = " + str(max(0, cdx - 1)) + '   ' + str(min(cdy + 1, self.height - 1)) + \
                     '                          ' + str(self.grid[cdx][cdy]) + '  ' + str(FILES[self.grid[cdx][cdy]]),
                     myfont)
            # fog of war map, upper right
            fog_map = pygame.transform.scale2x(fog_surf)  # , (int(tile_size * 2), int(tile_size * 2)))
            env.screen.blit(fog_map, (0, env.screen_height - fog_map.get_height()), None, pygame.BLEND_RGBA_MAX)
            pygame.draw.rect(env.screen, Color.RED,
                             (2 + cdx * 2, 2 + (env.screen_height - fog_map.get_height()) + cdy * 2, 2, 2))
            env.draw()

            pygame.display.flip()
            delta_time2 = clock.tick(f_p_s)

        cam.player.in_dungeon = False

    @staticmethod
    def invoke(seed, cam, style):
        myfont = pygame.font.SysFont("consolas", 15)

        p = cam.player
        # p.set_cam_pos(0, -10, -5)
        # p.cam.top = True
        rn = random.Random(seed)
        size = rn.randint(10, 35) * 2 + 1
        dm = None
        if style == 0:  # castle
            dm = DungeonGenerator.gen_castle(seed, size, size)
        elif style == 1:  # forest
            dm = DungeonGenerator.gen_forest(seed, size, size)
        elif style == 2:  # cave
            dm = DungeonGenerator.gen_caves(seed, size, size)
        elif style == 3:  # lake
            dm = DungeonGenerator.gen_forest_lake(seed, size, size)
        elif style == 4:  # city
            dm = DungeonGenerator.gen_city(seed, size, size)
        elif style == 5:  # mountain
            dm = DungeonGenerator.gen_mountains(seed, size, size)
        elif style == 6:  # farm
            pass

        if dm is not None:
            dm.run(cam)
        else:
            print("Dungeon not ready yet.")


class Tile(object):
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.tile = tile


def all_same(items):
    return all(x == items[0] for x in items)

def all_in_list(items, list):
    return all( x in items for x in list)

def main():
    print('Start dungeon gen')
    # CHECK 34 & 36
    dim = random.randint(20,91)
    #dm = DungeonGenerator.gen_forest(random.randint(1,9999999999999), dim, dim)
    #dm = DungeonGenerator.gen_city(34, 91, 91)
    #dm = DungeonGenerator.gen_caves(34,35,35)
    dm = DungeonGenerator.gen_forest_lake(dim,dim,dim)

    print(dm.printGrid())

    dm.pygame_init()

    DungeonGenerator.init()

    print('run')
    p = Player.Player()
    p.set_cam_pos(0, -10, -5)
    p.cam.top = True
    Environment.Environment.player = p
    p.exitShip()
    dm.run(p.cam)


def rot_center(image, angle):
    rot_image = pygame.transform.rotozoom(image, angle, 1)

    return rot_image


def rot_center2(image, angle):
    rect = image.get_rect()
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image


def draw_bar(bar_w, pos, color, value, high, desc, myfont=None):
    env = Environment.Environment
    pygame.draw.rect(env.getScreen(), Color.BLACK, (0, 5 + 15 * pos, bar_w, 10))
    pygame.draw.rect(env.getScreen(), color, (0, 5 + 15 * pos, bar_w, 10), 1)
    val = (bar_w - 1) / (high + .000001) * value
    if val < 0:
        val = 0
    if val > 298:
        val = 298
    pygame.draw.rect(env.getScreen(), color, (1, 6 + 15 * pos, val, 8))

    myfont.set_bold(True)
    font_text = myfont.render(str(value) + "/" + str(high), 1, (255, 255, 0))
    env.screen.blit(font_text, (bar_w, 1 + 15 * pos))
    env.screen.blit(myfont.render(desc, 1, (255, 255, 255)), (0, 1 + 15 * pos))
    myfont.set_bold(False)


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def clamp(val,low,high):
    return max(low, min(val,high))

if __name__ == "__main__":
    main()
