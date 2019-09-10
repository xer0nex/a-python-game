import math

import Color
import ParticleEngine
import Environment
import random


from Asteroid import Asteroid
from Vex import Vex
from MyMaths import rand2D
from Sanctuary import Sanctuary

# from DungeonEngine2 import PlanetDungeonEngine

from Line import Line

ZERO = Vex(0, 0, 0)


class Planets:
    maxSize = 50
    minSize = 50
    maxRad = 150
    minRad = 100
    con = 1
    pl = []

    def __init__(self, seed, pos=[0, 0]):
        self.seed = seed
        self.rnd = random.Random(seed)
        self.pos = Vex(pos[0], pos[1])
        self.rot = [0, 0, 0]
        self.surfPoints = []
        self.sancPoints = []
        self.surfProjPoints = []
        self.sancProjPoints = []
        self.edges = []
        self.sancEdges = []
        self.atmos = 0
        self.atmosPoints = []
        self.atmosProjPoints = []
        self.asteroids = []
        self.hasAsteroids = False
        self.rad = self.rnd.randint(self.minRad, self.maxRad)
        self.xoffset = self.rnd.randint(1, 99999999999)
        self.yoffset = self.rnd.randint(1, 99999999999)
        self.corHealth = 1000
        self.corePoints = []
        self.coreProjPoints = []
        self.coreRad = 10
        self.coreEdges = []
        self.surfColor = [self.rnd.randint(0, 255), self.rnd.randint(0, 255), self.rnd.randint(0, 255)]
        self.atmosColor = [self.rnd.randint(0, 255), self.rnd.randint(0, 255), self.rnd.randint(0, 255)]
        self.doCore()
        self.sanctuary = Sanctuary(self, self.rnd.randint(1,999999999999999), 50, 50)
        self.inSanctuary = False
        self.entryPs = self.doSurface()
        self.doAtmosphere()
        self.hasAsteroids = False
        self.viewAsteroids = True
        if self.rnd.randint(0, 10) > -1:
            self.hasAsteroids = True
            self.doAsteroids()
        #        else:
        #            #if self.rnd.randint(0, 5)==0:
        #            self.hasDungeon = True
        #            #self.dm = dungeonGenerator.genPlanetDungeon(self.rnd, 51, 51)
        #            self.dm = PlanetDungeonEngine.genPlanetDungeon(self)
        Planets.pl.extend([self])

    def update(self, cam):

        env = Environment.Environment
        ptpdst = cam.pos.dist2D(self.pos)  # player to planet distance
        viewAsteroids = True

        # maybe do a list of creatures within the planet?  cause items will not work?
        if ptpdst < self.atmos:
            # v = rand2D(cam.pos.x(), cam.pos.y(), self.seed)
            viewAsteroids = False
            if not self.inSanctuary:
                self.sanctuary.init(cam)
                self.inSanctuary = True
            else:
                self.sanctuary.update(cam)
            #        else:
            #            self.hasAsteroids = False

        if ptpdst < env.renderDist:
            if self.hasAsteroids and viewAsteroids:
                Asteroid.asteroids = self.asteroids
                for a in self.asteroids:
                    a.update(cam)

                #            ''' Do Core '''
                #            for i, c in enumerate(self.corePoints):
                #                v = (c+self.pos-cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch
                #                f = env.fov / (v.z()+.000000001)
                #                if(f < env.lim):
                #                    f = 1000
                #                v = v * f
                #                v = v + env.center
                #                v.setZ(f)
                #                self.coreProjPoints[i] = v
                #
                #            hth = -(self.corHealth/100)
                #            for line in self.coreEdges:
                #                points = []
                #                fs = [self.coreProjPoints[line[0]].z(), self.coreProjPoints[line[1]].z()]
                #                points = [self.coreProjPoints[line[0]].p2D(), self.coreProjPoints[line[1]].p2D()]
                #                if ptpdst < env.renderDist:
                #                    esc = env.screenClip(points)
                #                    if esc[0]:
                #                        points = esc[1]
                #                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                #                        env.add_edge(Color.RED, points, 1, 1, hth, fs)

            ''' Do Atmosphere'''
            for i, p in enumerate(self.atmosPoints):
                v = (p + self.pos - cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch

                f = env.fov / (v.z() + .000000001)
                if (f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                self.atmosProjPoints[i] = v.p2D()

            env.add_edge(self.atmosColor, self.atmosProjPoints, 1, 2)

            '''Do sanctuary'''
            for i, p in enumerate(self.sancPoints):
                v = (p + self.pos - cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch

                f = env.fov / (v.z() + .000000001)
                if (f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                self.sancProjPoints[i] = v.p2D()

            for pointz in self.edges:

                points = [self.sancProjPoints[pointz[0][1]], self.sancProjPoints[pointz[0][0]]]
                if ptpdst < env.renderDist:
                    esc = env.screenClip(points)
                    if esc[0]:
                        points = esc[1]
                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                        if pointz[1] == 0:
                            env.add_edge((255, 255, 255), points, 1, 0)
                        else:
                            env.add_edge(Color.YELLOW, points, 1, 0)
            ''' Do surface '''
            for i, p in enumerate(self.surfPoints):
                v = (p + self.pos - cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch

                f = env.fov / (v.z() + .000000001)
                if (f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                self.surfProjPoints[i] = v.p2D()

            for pointz in self.edges:

                points = [self.surfProjPoints[pointz[0][0]], self.surfProjPoints[pointz[0][1]]]
                if ptpdst < env.renderDist:
                    esc = env.screenClip(points)
                    if esc[0]:
                        points = esc[1]
                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                        if pointz[1] == 0:
                            env.add_edge(self.surfColor, points, 1, 0)
                        else:
                            env.add_edge(Color.YELLOW, points, 1, 0)

            ''' Do Entry Points '''
            for segs in self.entryPs:
                border = [self.surfProjPoints[segs[0]], self.sancProjPoints[segs[0]]]
                env.add_edge(self.surfColor, border, 1, 0)
                border = [self.sancProjPoints[segs[1]], self.surfProjPoints[segs[1]]]
                env.add_edge(self.surfColor, border, 1, 0)

        ''' Do minimal render '''
        if ptpdst >= env.renderDist:
            p1 = self.pos.projectedPos(cam)
            if p1[0]:
                points = [(p1[1].x() - self.rad * p1[1].z(), p1[1].y()), (p1[1].x() + self.rad * p1[1].z(), p1[1].y())]
                esc = env.screenClip(points)
                if esc[0]:
                    points = esc[1]
                if (env.inScreen(points[0]) or env.inScreen(points[1])):
                    env.add_edge(self.surfColor, points, 1, 0)

    @staticmethod
    def testShotHit(shot):
        x, y, z = shot.pos.Pos()
        lx, ly, lz = shot.lpos.Pos()
        sp = Vex(x, y)
        lsp = Vex(lx, ly)
        dmg = shot.damage / 100.0
        for p in Planets.pl:
            d = p.pos.dist2D(sp)
            if d < p.atmos:
                shln = Line(lsp - p.pos, sp - p.pos)
                for lines2 in p.edges:
                    if lines2[1] != 1:
                        lines = Line(p.surfPoints[lines2[0][0]], p.surfPoints[lines2[0][1]])
                        li = shln.find_intersection(lines)
                        if li:
                            minR = 5
                            ParticleEngine.Emitter(li + p.pos, shot.angle_rad, 2)
                            if lines.seg[0].length() > p.rad - minR:
                                a1 = math.atan2(lines.seg[0].Y(), lines.seg[0].X())
                                d1 = ZERO.dist2D(lines.seg[0]) - dmg
                                lines.seg[0].set2D(math.cos(a1) * d1, math.sin(a1) * d1)

                            if lines.seg[1].length() > p.rad - minR:
                                a2 = math.atan2(lines.seg[1].Y(), lines.seg[1].X())
                                d2 = ZERO.dist2D(lines.seg[1]) - dmg
                                lines.seg[1].set2D(math.cos(a2) * d2, math.sin(a2) * d2)
                            return True
            if d <= p.coreRad:
                ParticleEngine.Emitter(Vex(x, y), shot.angle_rad, 2)
                p.corHealth -= dmg * 10
                if p.corHealth <= 0:
                    # do explody stuff
                    pass
                return True
        return False

    @staticmethod
    def testRadiusCollision(ent, cp, np, rad):
        ent.inatmosphere = False
        for p in Planets.pl:
            d = (cp + np).dist2D(p.pos)
            if d <= p.atmos:
                edit = False
                if d > p.coreRad - 6:
                    ent.inatmosphere = True
                    v = (cp + np)
                    out = Vex(0, 0)
                    delta = v - p.pos  # new position relative to planet position
                    delta0 = cp - p.pos

                    for lines2 in p.edges:
                        lines = (Line(p.surfPoints[lines2[0][0]], p.surfPoints[lines2[0][1]]), lines2[1])
                        if lines[1] == 0 or (lines[1] == 1 and ent.inship):
                            ds = lines[0].ClosestPointOnLine(delta0)
                            cpol = delta.dist2D(ds)
                            if cpol <= rad:
                                # print (lines[0])
                                a = -(lines[0].angle()) + math.pi
                                v = Vex(math.sin(a) * rad, math.cos(a) * rad) + ds + p.pos
                                ParticleEngine.Emitter(v, a, 3)
                                ParticleEngine.Emitter(ds + p.pos, a, 2)
                                out.assign(v)
                                edit = True
                                break
                    if not edit:
                        for segs in p.entryPs:
                            ln = []
                            ln += [Line(p.surfPoints[segs[0]], p.sancPoints[segs[0]])]
                            ln += [Line(p.sancPoints[segs[1]], p.surfPoints[segs[1]])]
                            for i in range(0, 2):
                                lines = ln[i]
                                ds = lines.ClosestPointOnLine(delta)
                                cpol = delta.dist2D(ds)
                                if cpol <= rad:
                                    a = -(lines.angle()) + math.pi
                                    v = Vex(math.sin(a) * rad, math.cos(a) * rad) + ds + p.pos
                                    ParticleEngine.Emitter(ds + p.pos, a, 2)
                                    out.assign(v)
                                    edit = True
                # if d < p.rad:
                #     if not edit:
                #         for lines2 in p.edges:
                #             lines = (Line(p.sancPoints[lines2[0][1]], p.sancPoints[lines2[0][0]]), lines2[1])
                #             if lines[1] == 0 or (lines[1] == 1 and ent.inship):
                #                 ds = lines[0].ClosestPointOnLine(delta)
                #                 cpol = delta.dist2D(ds)
                #                 if cpol <= rad:
                #                     a = -(lines[0].angle()) + math.pi
                #                     v = Vex(math.sin(a) * rad, math.cos(a) * rad) + ds + p.pos
                #                     ParticleEngine.Emitter(ds + p.pos, a, 2)
                #                     out.assign(v)
                #                     edit = True

                if edit:
                    return out
        return None

    @staticmethod
    def inAtmosphere(pos):
        for p in Planets.pl:
            if pos.dist2D(p.pos) <= p.atmos:
                return True
        return False

    def getPos(self):
        return self.pos

    def getSurface(self):
        return self.surfPoints

    def doCore(self):
        pickRndCorePoints = 8
        step = (360.0 / pickRndCorePoints)
        mi = 0
        for corePoint in range(pickRndCorePoints):
            sx = math.sin(math.radians(step * corePoint))
            sy = math.cos(math.radians(step * corePoint))
            x = sx * (self.coreRad)
            y = sy * (self.coreRad)
            self.corePoints += [Vex(x, y)]
            self.coreProjPoints += [(0, 0)]

        for i in range(mi, len(self.coreProjPoints)):
            if i + 1 < len(self.coreProjPoints):
                self.coreEdges.append((i, i + 1))
            else:
                self.coreEdges.append((i, mi))
                mi = i + 1

    def doAtmosphere(self):
        pickRndSurfacePoints = self.minSize
        step = (360.0 / pickRndSurfacePoints)
        # mi = 0
        stp = 1
        for surfacePoint in range(pickRndSurfacePoints):
            sx = math.sin(math.radians(step * surfacePoint))
            sy = math.cos(math.radians(step * surfacePoint))
            x = sx * (self.atmos / Planets.con) * stp
            y = sy * (self.atmos / Planets.con) * stp
            x = sx * (self.atmos)
            y = sy * (self.atmos)
            self.atmosPoints += [Vex(x, y)]
            self.atmosProjPoints += [(0, 0)]

    def doSurface(self):
        pickRndSurfacePoints = self.rnd.randint(self.minSize, self.maxSize)
        step = (360.0 / pickRndSurfacePoints)
        mi = 0
        stp = 1
        maxH = 0

        for surfacePoint in range(pickRndSurfacePoints):
            sx = math.sin(math.radians(step * surfacePoint))
            sy = math.cos(math.radians(step * surfacePoint))
            x = sx * (self.rad / Planets.con) * stp
            y = sy * (self.rad / Planets.con) * stp
            # h = (Noise.Perlin3D(x, y, 0, 16, 1, 0, 4))*2
            h = rand2D(x, y) * 2

            x = sx * (self.rad + h)
            y = sy * (self.rad + h)
            sax = sx * (self.rad - 6)
            say = sy * (self.rad - 6)
            if maxH < h: maxH = h
            self.surfPoints += [Vex(x, y)]
            self.sancPoints += [Vex(sax, say)]
            self.surfProjPoints += [(0, 0)]
            self.sancProjPoints += [(0, 0)]

        self.atmos = maxH + self.rad / 5 + self.rad

        entryPs = []
        ents = self.rnd.randint(1, 4)
        leng = len(self.surfProjPoints)
        for i in range(mi, leng):
            r2 = 0
            r1 = i % int((leng) / (ents + 1))
            if r1 == 0: r2 = 1
            if i + 1 < len(self.surfProjPoints):
                seg = (i, i + 1)
            else:
                seg = (i, mi)
                mi = i + 1
            if r2 == 1:
                entryPs += [seg]
            self.edges.append((seg, r2))

        return entryPs

    def doAsteroids(self):
        dir = False
        mnt = self.rnd.randint(1, 50)
        if mnt % 2 == 1: dir = True
        for x in range(mnt):
            md = self.atmos + 10
            wide = self.rnd.randint(5, 25)
            o_ang = math.radians(self.rnd.randint(0, 360))
            ap = Vex(math.sin(o_ang) * (md + wide), math.cos(o_ang) * (md + wide))
            self.asteroids += [Asteroid(self.rnd, self, (md + wide), ap + self.pos, dir)]
