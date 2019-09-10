
import math
import random
from MyMaths import rand2D
from Planets import Planets
import Environment
import ParticleEngine
from Vex import Vex

class Sun:
    maxRange = 7000
    maxSize = 50
    minSize = 50
    maxRad = 400
    minRad = 200
    maxPlanets = 25
    minPlanets = 0
    counter = 0
    
    def __init__(self, pos=[0, 0], seed = 0):
        Planets.pl = []
        self.seed = seed
        self.rnd = random.Random(self.seed)
        self.pos = Vex(self.rnd.randint(-2000, 2000), self.rnd.randint(-2000, 2000))
        self.rot = [0, 0, 0]
        self.points = []
        self.surfProjPoints = []
        self.edges = []
        self.corePoints = []
        self.coreProjPoints = []
        self.coreEdges = []
        self.corHealth = 10000
        
        self.rad = self.rnd.randint(Sun.minRad, Sun.maxRad)
        self.xoffset = self.rnd.randint(1, 99999999999)
        self.yoffset = self.rnd.randint(1, 99999999999)
        self.pickRndSurfacePoints = self.rnd.randint(Sun.minSize, Sun.maxSize)
        self.numPlanets = self.rnd.randint(Sun.minPlanets, Sun.maxPlanets)
        self.planets = []
        self.doCore()
        for i in range(self.numPlanets):
            ang_rad = math.radians(self.rnd.randint(0, 360))
            dist_sun = self.rnd.randint(self.maxRad*2+25, Sun.maxRange)
            px = math.sin(ang_rad)*dist_sun
            py = math.cos(ang_rad)*dist_sun
            p = Planets(self.rnd.randint(1,123456789012345678901234567890), (px+self.pos.x(), py+self.pos.y()))
            for pl in Planets.pl:
                while pl.pos.dist2D(p.pos)<=pl.atmos+p.atmos and p != pl:
                    ang_rad = math.radians(self.rnd.randint(0, 360))
                    dist_sun = self.rnd.randint(self.maxRad*2+25, Sun.maxRange)
                    px = math.sin(ang_rad)*dist_sun
                    py = math.cos(ang_rad)*dist_sun
                    p.pos.set2D(px+self.pos.x(), py+self.pos.y())
            self.planets += [p]
        
        step = math.radians(360.0 / self.pickRndSurfacePoints)
        for surfacePoint in range(self.pickRndSurfacePoints):
            sx = math.sin(step * surfacePoint)
            sy = math.cos(step * surfacePoint)
            x = sx * (self.rad)
            y = sy * (self.rad)
            h = rand2D(x, y)
            self.points += [Vex(sx * (self.rad+h), sy * (self.rad+h))]
            self.surfProjPoints += [0, 0]
        
        for i in range(len(self.points)):
            if i + 1 < len(self.points):
                self.edges.append([i, i + 1])
            else:
                self.edges.append([i, 0])

    def update2(self, cam):
        env = Environment.Environment
        for p in self.planets:
            p.update(cam)
        ptpdst = cam.pos.dist2D(self.pos) #player to sun distance
        
        if ptpdst < env.renderDist+self.rad:
            cam.player.doDMG(((env.renderDist+self.rad)-ptpdst)/100)
            
            for i, c in enumerate(self.corePoints):
                v = (c+self.pos-cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch
                f = env.fov / (v.z()+.000000001)
                if(f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                v.setZ(f)
                self.coreProjPoints[i] = v
            
            hth = -(self.corHealth/200)
            for line in self.coreEdges:
                points = []
                fs = [self.coreProjPoints[line[0]].z(), self.coreProjPoints[line[1]].z()]
                points = [self.coreProjPoints[line[0]].p2D(), self.coreProjPoints[line[1]].p2D()]
                if ptpdst < env.renderDist+self.rad: 
                    esc = env.screenClip(points)
                    if esc[0]:
                        points = esc[1]
                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                        env.add_edge((255, 0, 0), points, 1, 1, hth, fs)
            
            onscreen = False
            for i, p in enumerate(self.points):
                cl = 1.5-rand2D(p.x(), p.y())/10
                scl = Vex(cl, cl)
                v = (p*scl+self.pos-cam.pos).rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])  # pitch
                    
                f = env.fov / (v.z()+.000000001)
                if(f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                self.surfProjPoints[i] = v.p2D()
                if env.inScreen(self.surfProjPoints[i]):
                    onscreen = True
            if onscreen:env.add_edge((170, 23, 23), self.surfProjPoints, 1, 2)

        if ptpdst >= env.renderDist+self.rad:
            p1 = self.pos.projectedPos( cam)
            if p1[0]:
                points = [(p1[1].x()-self.rad*p1[1].z(), p1[1].y()), (p1[1].x()+self.rad*p1[1].z(), p1[1].y())]
                esc = env.screenClip(points)
                if esc[0]:
                    points = esc[1]
                if (env.inScreen(points[0]) or env.inScreen(points[1])):
                    env.add_edge((170, 23, 23), points, 8)
            

                
    def doCore(self):
        pickRndCorePoints = 8
        step = (360.0 / pickRndCorePoints)
        mi = 0
        for corePoint in range(pickRndCorePoints):
            sx = math.sin(math.radians(step * corePoint))
            sy = math.cos(math.radians(step * corePoint))
            x = sx * (Sun.minRad)
            y = sy * (Sun.minRad)
            self.corePoints += [Vex(x, y)]
            self.coreProjPoints += [(0, 0)]

        for i in range(mi, len(self.coreProjPoints)):
            if i + 1 < len(self.coreProjPoints):
                self.coreEdges.append((i, i + 1))
            else:
                self.coreEdges.append((i, mi))
                mi = i+1

    @staticmethod
    def testShotHit(shot):
        p = Environment.Environment.sun
        x, y, z = shot.pos.Pos()
        sp = Vex(x, y)
        dmg = shot.damage/100.0
        d = p.pos.dist2D(sp)
        if d <= Sun.minRad:
            ParticleEngine.Emitter(Vex(x, y), shot.angle_rad, 2)
            p.corHealth-=dmg*10
            if p.corHealth <= 0:
                # destroy sun, destroy planets, generate random asteroids
                pass
            return True
        return False
   
