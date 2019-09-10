'''
Dungeon Engine 2
'''
import math
import Environment
from Vex import Vex
from Line import Line

ZERO = Vex(0, 0, 0)


class PlanetRoom():
    def __init__(self, cpos, rect=[0, 0, 0, 0]):
        self.centerPos = cpos
        self.dim = rect
        self.edges = [Line(self.dim[0], self.dim[1]), Line(self.dim[1], self.dim[2]), \
                      Line(self.dim[2], self.dim[3]), Line(self.dim[3], self.dim[0])]
        self.edgesI = [(0, 1), (1, 2), (2, 3), (3, 0)]
        self.visible = True
        self.halls = []
        self.obj = []
        self.traps = []
        self.npc = []

    def __str__(self):
        return str(self.centerPos)

    def pointInPolygon(self, cp):

        j = len(self.dim) - 1
        oddNodes = False

        for i in range(len(self.dim)):
            if self.dim[i].y() < cp.y() and self.dim[j].y() >= cp.y() or \
                                    self.dim[j].y() < cp.y() and self.dim[i].y() >= cp.y():
                if self.dim[i].x() + (cp.y() - self.dim[i].y()) \
                        / (self.dim[j].y() - self.dim[i].y()) \
                        * (self.dim[j].x() - self.dim[i].x()) \
                        < cp.x():
                    oddNodes = not oddNodes
            j = i
        return oddNodes


class Hall():
    def __init__(self, roomA, roomB, width):
        self.rooms = (roomA, roomB)
        self.dim = []
        self.w = width
        self.visible = True
        self.obj = []
        self.traps = []
        self.makeUsable()

    def makeUsable(self):
        # get the angle for the hall using rooms center position
        raP = self.rooms[0].centerPos
        rbP = self.rooms[1].centerPos
        a = -raP.ang2D(rbP) + math.pi

        # calculate the hall points
        self.dim += [raP + Vex(math.sin(a) * (self.w / 2), math.cos(a) * (self.w / 2))]
        self.dim += [raP - Vex(math.sin(a) * (self.w / 2), math.cos(a) * (self.w / 2))]
        self.dim += [rbP - Vex(math.sin(a) * (self.w / 2), math.cos(a) * (self.w / 2))]
        self.dim += [rbP + Vex(math.sin(a) * (self.w / 2), math.cos(a) * (self.w / 2))]

        # get all the intersection points of rooms
        la = []
        k = len(self.rooms[0].dim) - 1
        for ri in range(len(self.rooms[0].dim)):
            r = Line(self.rooms[0].dim[k], self.rooms[0].dim[ri])
            j = len(self.dim) - 1
            for hi in range(len(self.dim)):
                fip = r.find_intersection(Line(self.dim[hi], self.dim[j]))
                if fip:
                    la += [((k, ri), (hi, j), fip)]
                j = hi
            k = ri
        lb = []
        k = len(self.rooms[1].dim) - 1
        for ri in range(len(self.rooms[1].dim)):
            r = Line(self.rooms[1].dim[k], self.rooms[1].dim[ri])
            j = len(self.dim) - 1
            for hi in range(len(self.dim)):
                fip = r.find_intersection(Line(self.dim[hi], self.dim[j]))
                if fip:
                    lb += [((k, ri), (hi, j), fip)]
                j = hi
            k = ri
        # adjust points to intersection
        print(str(raP) + "  " + str(la))
        for l in la:
            self.rooms[0].dim.insert(l[0][1], l[2])
            self.dim[l[1][1]].assign(l[2])

        for l in lb:
            self.rooms[1].dim.insert(l[0][1], l[2])
            # self.dim[l[1][1]].assign(l[2])


class PlanetDungeonEngine():
    def __init__(self, parent):
        self.parent = parent
        self.rnd = parent.rnd
        self.maxRad = parent.rad - 10
        self.minRad = parent.coreRad + 10
        self.entryPs = parent.entryPs
        self.rooms = []
        self.doors = []
        self.corridors = []
        self.deadends = []

    def placeRandomRooms(self, minRoomSize, maxRoomSize, roomStep=1, attempts=100):

        for attempt in range(attempts):
            roomWidth = self.rnd.randrange(minRoomSize, maxRoomSize, roomStep)
            roomHeight = self.rnd.randrange(minRoomSize, maxRoomSize, roomStep)
            rw = roomWidth / 2
            rh = roomHeight / 2
            tl = Vex(-rw, -rh)
            tr = Vex(rw, -rh)
            br = Vex(rw, rh)
            bl = Vex(-rw, rh)

            a = math.radians(self.rnd.randint(0, 360))
            d = self.rnd.randint(int(self.minRad + roomHeight / 2), int(self.maxRad - roomHeight / 2))
            startX = math.sin(a) * d
            startY = math.cos(a) * d
            rp = Vex(startX, startY)
            tl = tl.rotate2dXY(-a) + rp
            tr = tr.rotate2dXY(-a) + rp
            br = br.rotate2dXY(-a) + rp
            bl = bl.rotate2dXY(-a) + rp

            if self.roomFits(rp, (tl, tr, br, bl)):
                self.rooms.append(PlanetRoom(rp, [tl, tr, br, bl]))

    def placeRoom(self, width, height, a, d):
        rw = width / 2
        rh = height / 2
        tl = Vex(-rw, -rh)
        tr = Vex(rw, -rh)
        br = Vex(rw, rh)
        bl = Vex(-rw, rh)

        a = math.radians(a)
        startX = math.sin(a) * d
        startY = math.cos(a) * d
        rp = Vex(startX, startY)
        tl = tl.rotate2dXY(-a) + rp
        tr = tr.rotate2dXY(-a) + rp
        br = br.rotate2dXY(-a) + rp
        bl = bl.rotate2dXY(-a) + rp

        if self.roomFits(rp, (tl, tr, br, bl)):
            self.rooms.append(PlanetRoom(rp, [tl, tr, br, bl]))

    def roomFits(self, rc, dim=(0, 0, 0, 0)):
        out = True
        ls = []
        ls += [Line(dim[0], dim[1])]
        ls += [Line(dim[1], dim[2])]
        ls += [Line(dim[2], dim[3])]
        ls += [Line(dim[3], dim[0])]

        for r in self.rooms:
            if r.pointInPolygon(rc):
                return False
            for p in dim:
                if r.pointInPolygon(p):
                    return False
            rl = []
            rl += [Line(r.dim[0], r.dim[1])]
            rl += [Line(r.dim[1], r.dim[2])]
            rl += [Line(r.dim[2], r.dim[3])]
            rl += [Line(r.dim[3], r.dim[0])]

            for l in ls:
                for rm in rl:
                    if l.find_intersection(rm):
                        return False
        return out

    def connectAllRooms(self):

        for a in range(360):
            ray = Line(ZERO, Vex(math.sin(a) * self.maxRad, math.cos(a) * self.maxRad))
            vertConRooms = []
            for r in self.rooms:
                for e in r.edges:
                    if ray.find_intersection(e):
                        vertConRooms += [r]
                        break
            if len(vertConRooms) > 1:
                vertConRooms.sort(key=lambda x: x.centerPos.sqrLength())
                j = 0
                for i in range(1, len(vertConRooms)):
                    if (vertConRooms[j].centerPos.dist2D(vertConRooms[i].centerPos)) < 35:
                        add = True
                        for h in self.corridors:
                            if (h.rooms[0] == vertConRooms[j] and h.rooms[1] == vertConRooms[i]) or \
                                    (h.rooms[1] == vertConRooms[j] and h.rooms[0] == vertConRooms[i]):
                                add = False
                        if add:
                            self.corridors.append(Hall(vertConRooms[j], vertConRooms[i], 3))
                    j = i

    def update(self, cam, pos):
        env = Environment.Environment
        for r in self.rooms:
            if cam.pos.dist2D(r.centerPos + self.parent.pos) < 100:
                proj = []
                for vec in r.dim:
                    v = ((vec + self.parent.pos - cam.pos).rotate2dXY(cam.rotSC[0])).rotate2dYZ(cam.mov[2],
                                                                                                cam.rotSC[1])  # pitch
                    f = env.fov / (v.z() + .00000001)
                    if (f < env.lim):
                        f = 1000
                    v = v * f
                    v = v + env.center
                    proj += [v.p2D()]
                env.add_edge((255, 255, 255), proj, 1, 2)
        for r in self.corridors:
            proj = []
            for vec in r.dim:
                v = ((vec + self.parent.pos - cam.pos).rotate2dXY(cam.rotSC[0])).rotate2dYZ(cam.mov[2],
                                                                                            cam.rotSC[1])  # pitch
                f = env.fov / (v.z() + .00000001)
                if (f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                proj += [v.p2D()]
            env.add_edge((255, 255, 255), proj, 1, 2)

    @staticmethod
    def genPlanetDungeon(parent):
        dm = PlanetDungeonEngine(parent)
        dm.placeRoom(30, 30, 0, 0)
        dm.placeRandomRooms(10, int((parent.rad - 10) / 2))
        dm.connectAllRooms()
        return dm
