# Ship
import math
import Color
import Environment

from RPGStats import RPGStats
from Vex import Vex
from Weapon import Weapon

class Ship:
    ships = []
    def __init__(self, parent, pos = [0, 0]):
        
        self.parent = parent
        self.stats = RPGStats()
        self.pos = Vex(pos[0], pos[1])
        self.rot = 0
        self.stats.lvlUP()
        
        self.weapon = Weapon(self, [0, 0, 0], [.5, .5, .5], 60, 1, 1, (255, 0, 0))
        self.points = [Vex(-.5,  .5,   0), Vex(  .5,  .5,    0), Vex( 0.0, -.5,    0), 
                            Vex(0.0,  .5, -.3), Vex( -.25,  .45, -.15), Vex( .25,  .45, -.15)]
        self.projPoints = [Vex(0, 0)]*6
        self.lines = [(0, 4), (4, 5), (5, 1), (1, 2), (2, 0), (2, 3), (3, 0), (3, 1), (2, 4), (2, 5)]

        
        self.shieldPoints = []
        self.shieldEdges = []
        self.shieldRot = [0, 0, 0]
        self.occupied = False
        
        #construct player shield
        sides = 10
        size = 2
        
        self.shieldRadius = size
        mi = 0

        for i in range(sides):
            angle_deg = (360 / sides) * i 
            angle_rad = 3.14159265359 / 180 * angle_deg
            x = 0 + size * math.cos(angle_rad)
            y = 0 + size * math.sin(angle_rad)
            self.shieldPoints += [Vex(x, y)]
        
        
        for i in range(mi, len(self.shieldPoints)):
            seg = []
            if i + 1 < len(self.shieldPoints):
                seg = (i,i + 1)
            else:
                seg = (i, mi)
                mi=i+1
            self.shieldEdges.append(seg)
        
    def getShieldRadius(self):
        return self.shieldRadius
        
    def setParent(self, par):
        self.parent = par
        
    def isOccupied(self):
        return self.occupied
    
    def setOccupied(self, val):
        self.occupied = val
        
    def totalDamage(self):
        return self.stats.getSTR()
        
    def shoot(self, pos, rot, ant):
        self.weapon.Shoot(pos, rot, ant)
        
    def syncPos(self, pos):
        self.pos = pos.copy()
        
    def updatePlayerShip(self, cam):
        env = Environment.Environment    
        self.weapon.update()
        
        proj = []
        for vec in self.points:
            if not self.isOccupied():
                v = ((vec.rotate2dXY(-self.rot)-cam.pos + self.pos).rotate2dXY(cam.rot[1])).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
            else:
                v = (vec+self.pos).setZ(vec.z()-cam.pos.z()).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
            
            f = env.fov / (v.z()+.0000001)
            if(f < env.lim):
                f = 1000
            v = v * f + env.center
            proj += [v.p2D()]
            
        for l in self.lines:
            points = [proj[l[0]], proj[l[1]]]
            if (env.inScreen(points[0]) or env.inScreen(points[1])):
                env.add_edge(Color.NEONBLUE, points)
        self.shieldRot[1] = cam.rot[1]
        
        shldH = -(self.stats.getHP()/self.stats.getHTH())/4
        proj = []
        fs = []
        for vec in self.shieldPoints:
            if not self.isOccupied():
                v = ((vec.rotate2dXY(-self.rot)-cam.pos + self.pos).rotate2dXY(cam.rot[1])).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
            else:
                v = (vec.rotate2dXY(self.shieldRot[1])+self.pos).setZ(self.pos.z() - cam.pos.z()).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
            
            f = env.fov / (v.z() + .00000001)
            if(f < env.lim):
                f = 1000
            v = v * f + env.center
            proj += [v.p2D()]
            fs += [f]
        
        for l in self.shieldEdges:
            points = [proj[l[0]], proj[l[1]]]
            fst = [fs[l[0]], fs[l[1]]]
            if (env.inScreen(points[0]) or env.inScreen(points[1])):
                env.add_edge(Color.BLUE, points, 1, 1, shldH, fst)
                    
    def updateCreatureShip(self, cam, pos, ang):
        env = Environment.Environment
        self.weapon.update()
        if cam.pos.dist2D(self.pos) < env.renderDist:
            proj = []
            for vec in self.points:
                v = ((vec.rotate2dXY(math.radians(ang))-cam.pos + pos).rotate2dXY(cam.rot[1])).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
                
                f = env.fov / (v.z() + .00000001)
                if(f < env.lim):
                    f = 1000
                v = v * f + env.center
                proj += [v.p2D()]
                
            for l in self.lines:
                points = [proj[l[0]], proj[l[1]]]
                if (env.inScreen(points[0]) or env.inScreen(points[1])):
                    env.add_edge(Color.NEONBLUE, points)
                    
            hth = -(self.stats.getHP()/self.stats.getHTH())/2
            
            proj = []
            fs = []
            for vec in self.shieldPoints:
                v = (vec.rotate2dXY( math.radians(ang))-cam.pos+pos).rotate2dXY(cam.rot[1]).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
                f = env.fov / (v.z() + .00000001)
                if(f < env.lim):
                    f = 1000
                v = v * f + env.center
                proj += [v.p2D()]
                fs += [f]
            
            for l in self.shieldEdges:
                points = [proj[l[0]], proj[l[1]]]
                fst = [fs[l[0]], fs[l[1]]]
                if (env.inScreen(points[0]) or env.inScreen(points[1])):
                    env.add_edge(Color.BLUE, points, 1, 1, hth, fst)
                        
    @staticmethod
    def remove_unoccupied(ship):
        try:
            Ship.ships.remove(ship)
        except:
            pass
        
    @staticmethod
    def add_unoccupied(ship):
        Ship.ships += [ship]
        
    @staticmethod
    def updateUnOccupied(cam):
        env = Environment.Environment
        for self in Ship.ships:
            if not self.isOccupied() and cam.pos.dist2D(self.pos) < 300:
                proj = []
                for vec in self.points:
                    v = (vec.rotate2dXY(self.rot)-cam.pos+self.pos).rotate2dXY(cam.rot[1]).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
                    
                    f = env.fov / (v.z() + .00000001)
                    if(f < env.lim):
                        f = 1000
                    v = v * f + env.center
                    proj += [v.p2D()]
                    
                for l in self.lines:
                    points = [proj[l[0]], proj[l[1]]]
                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                        env.add_edge(Color.NEONBLUE, points)
                        
                hth = -(self.stats.getHP()/self.stats.getHTH())/2
                
                proj = []
                fs = []
                for vec in self.shieldPoints:
                    v = (vec-cam.pos+self.pos).rotate2dXY(cam.rot[1]).rotate2dYZ(cam.mov[2], cam.rot[0])  # pitch
                    f = env.fov / (v.z() + .00000001)
                    if(f < env.lim):
                        f = 1000
                    v = v * f + env.center
                    proj += [v.p2D()]
                    fs += [f]
                
                for l in self.shieldEdges:
                    points = [proj[l[0]], proj[l[1]]]
                    fst = [fs[l[0]], fs[l[1]]]
                    if (env.inScreen(points[0]) or env.inScreen(points[1])):
                        env.add_edge(Color.BLUE, points, 1, 1, hth, fst)
                            
