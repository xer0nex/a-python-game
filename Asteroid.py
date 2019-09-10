'''
    Asteroid
'''
import math
import MyMaths
from Vex import Vex
import Environment
from Line import Line
import ParticleEngine


ZERO = Vex(0, 0, 0)

class Asteroid:
    asteroids = []
    tempAsteroids = []
    #                   self.rnd, self, (md+wide), ap+self.pos,dir 
    def __init__(self, rnd, par, rad, pos=Vex(0, 0, 0), dir=False, minSize=2, maxSize=4):
        self.rnd = rnd
        self.parent = par
        self.pos = pos
        self.scale = Vex(.5, .5)
        self.rot = math.radians(self.rnd.randint(0, 360))
        self.ang = math.radians(self.rnd.randint(0, 360))
        self.rotsp = self.rnd.uniform(-.1, .1)
        self.speed = self.rnd.uniform(.1, 3)
        if dir:  self.speed = -self.speed
        self.edges = []
        rc = self.rnd.randint(25, 255)
        self.color = (rc, rc, rc)
        self.corHealth = 150
        mi = 0
        self.points = []
        self.projectedPoints = []
        size = self.rnd.randint(8, 16)
        step = 360.0/size
        
        for i in range(0, size):
            sx = math.sin(math.radians(step * i))
            sy = math.cos(math.radians(step * i))
            d = MyMaths.rand2Dinst(sx, sy, self.rnd)/2+2
            tv = Vex(sx*d, sy*d)
            self.points += [tv]
            self.projectedPoints += [0, 0]
        
        for i in range(mi, len(self.points)):
            if i + 1 < len(self.points):
                self.edges.append((i, i + 1))
            else:
                self.edges.append((i, mi))
                mi = i+1
    
    @staticmethod
    def add_asteroid(ast):
        Asteroid.asteroids += [ast]
    
    @staticmethod
    def add_temp_asteroid(ast):
        Asteroid.tempAsteroids += [ast]
        
    @staticmethod
    def remove_asteroid(ast):
        try:
            Asteroid.asteroids.remove(ast)
        except:
            pass
        try:
            Asteroid.temAsteroids.remove(ast)
        except:
            pass
    
    def update(self, cam):
        env = Environment.Environment
        r1 = cam.rotSC[0]
        r2 = cam.rotSC[1]
     
        if cam.pos.dist2D(self.pos)<env.renderDist-250:
            d = self.pos.dist2D(self.parent.pos)
            delt = self.parent.pos - self.pos
            a1 = math.degrees(math.atan2(delt.y(), delt.x()))
            ra = math.radians(-a1+90+(self.speed*cam.delta))
            dp = Vex(math.sin(ra)*d, math.cos(ra)*d)
            np = self.parent.pos-dp
            self.pos.assign(np)
            
           
            for i, p in enumerate(self.points):
                p.assign(p.rotate2dXY(self.rotsp))
                v = (p*self.scale+self.pos-cam.pos).rotate2dXY(r1).rotate2dYZ(cam.mov[2], r2)  # pitch
                    
                f = env.fov / (v.z()+.000000001)
                if(f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                self.projectedPoints[i] = v.p2D()
  
            env.add_edge(self.color, self.projectedPoints, 1, 2)
    
    @staticmethod
    def updateTempAsteroids(cam):
        
        env = Environment.Environment
        r1 = cam.rotSC[0]
        r2 = cam.rotSC[1]
        for self in reversed(Asteroid.tempAsteroids):

            if cam.pos.dist2D(self.pos)<env.renderDist-250:
                self.pos.assign(Vex(math.sin(self.ang)*(self.speed*cam.delta), math.cos(self.ang)*(self.speed*cam.delta))+self.pos)
                for i, p in enumerate(self.points):
                    p.assign(p.rotate2dXY(self.rotsp))
                    v = (p*self.scale+self.pos-cam.pos).rotate2dXY(r1).rotate2dYZ(cam.mov[2], r2)  # pitch
                        
                    f = env.fov / (v.z()+.000000001)
                    if(f < env.lim):
                        f = 1000
                    v = v * f
                    v = v + env.center
                    self.projectedPoints[i] = v.p2D()
      
                env.add_edge(self.color, self.projectedPoints, 1, 2)
            else:
                Asteroid.tempAsteroids.remove(self)
            
    @staticmethod
    def testShotHit(shot):
        x, y, z = shot.pos.Pos()
        lx, ly, lz = shot.lpos.Pos()
        sp = Vex(x, y)
#        lsp = Vex(lx, ly)
        dmg = shot.damage
        for p in Asteroid.asteroids:
            d = p.pos.dist2D(sp)
            if d<2:
                ParticleEngine.Emitter(p.pos, shot.angle_rad, 2,50,Vex(0, 0),False,25)
                p.corHealth -= dmg
                if p.corHealth <= 0:
                    ParticleEngine.Emitter(p.pos, shot.angle_rad, 1,50,Vex(0, 0),False,50)
                    p.corHealth = 150
                    d = p.pos.dist2D(p.parent.pos)
                    delt = p.parent.pos - p.pos
                    a1 = math.degrees(math.atan2(delt.y(), delt.x()))
                    ra = math.radians(-a1+90+p.speed+180)
                    dp = Vex(math.sin(ra)*d, math.cos(ra)*d)
                    np = p.parent.pos-dp
                    p.pos.assign(np)
                return True
                    
        for p in Asteroid.tempAsteroids:
            d = p.pos.dist2D(sp)
            if d<2:
                ParticleEngine.Emitter(p.pos, shot.angle_rad, 2)
                p.corHealth -= dmg
                if p.corHealth <= 0:
                    ParticleEngine.Emitter(p.pos, shot.angle_rad, 1,10,Vex(0, 0),False,1)
                    Asteroid.tempAsteroids.remove(p)
                return True
        return False
    

    @staticmethod
    def testRadiusCollision(ent, np, rad):
        v = np.copy()
        out = Vex(0, 0)
        edit = False
        for p in Asteroid.asteroids:
            d = v.dist2D(p.pos)
            if d <= 20:
                for lines2 in p.edges:
                    lines = (Line(p.points[lines2[0]]*p.scale, p.points[lines2[1]]*p.scale))
                   
                    delta = v-p.pos # new position relative to asteroid position
                    ds = lines.ClosestPointOnLine(delta) 
                    cpol = delta.dist2D(ds)
                    if cpol<=rad:
                        rad+=p.speed
                        a = -(lines.angle())+math.pi
                        v = Vex(math.sin(a)*rad,  math.cos(a)*rad)+ds+p.pos
                        out.assign (v)
                        edit = True
        if edit:
            return out
        else:
            return None
