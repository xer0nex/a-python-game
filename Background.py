#background stars
import random
from Vex import *
import pygame

import Asteroid
import Environment
import math


        

class Stars:
    __stars = []
    __debre = []
    __shooting=[]
    pi = 3.14159265359 * 2
    def __init__(self, cam):
        self.lat = 0.0
        self.lon = 0.0
        self.pos = None
        self.fillDef(cam)
        self.lp = [0.0, 0.0]
    
    def fillDef(self, cam):
        env = Environment.Environment
        dis = random.randint(0, 200)
        self.lat = random.uniform(-1, 1)
        self.lon = random.uniform(-math.pi, math.pi)
        lonS = math.sin(self.lon)
        lonC = math.cos(self.lon)
        self.pos = Vex(lonS*dis, lonC*dis, random.randint(-10, 10))+cam.pos.copy().setZ(0)
        self.lat = random.uniform(-Stars.pi, Stars.pi)
        self.lon = random.uniform(-Stars.pi, Stars.pi)
        v = (self.pos - cam.pos).rotate2dXY(cam.rotSC[0])
        v.setY(v.y() + cam.mov[2])
        v.setZ(v.z() - cam.pos.z())
        
        v = v.rotate2dYZ(0, cam.rotSC[1])
        f = env.fov / (v.z()+.00000001)
        if(f < 1):
            f = 1000
        v = v * f
        v = v + env.center
        self.lp = v.p2D()
        
    def fill(self, cam):
        env = Environment.Environment
        dis = random.randint(150, 200)
        
        self.lat = random.uniform(-1, 1)
        self.lon = (cam.rot[1]+math.pi) + random.uniform(-1, 1)
        lonS = math.sin(self.lon)
        lonC = math.cos(self.lon)
        self.pos = Vex(lonS*dis, lonC*dis, random.randint(-10, 10))+cam.pos.copy().setZ(0)
        ast = Asteroid.Asteroid(random.Random(), self, 0, self.pos.copy().setZ(0))
        #ast.speed = 0
        Asteroid.Asteroid.add_temp_asteroid(ast)
        self.lat = random.uniform(-Stars.pi, Stars.pi)
        self.lon = random.uniform(-Stars.pi, Stars.pi)
        v = (self.pos - cam.pos).rotate2dXY(cam.rot[1])
        v.setY(v.Y()+cam.mov[2])
        v.setZ(v.Z()+-cam.pos.Z())

        v = v.rotate2dYZ(0, cam.rot[0])

        f = env.fov / (v.z()+.00000001)
        if(f < env.lim):
            f = 1000
        v = v * f
        v = v + env.center
        self.lp = v.p2D()
        
    @staticmethod
    def init(cam, max = 100):
        for i in range(max):
            s = Stars(cam)
            Stars.__stars.extend([s])
        for i in range(max):
            s = Stars(cam)
            Stars.__debre.extend([s])
        for i in range(5):
            s = Stars(cam)
            Stars.__shooting.extend([s])

    @staticmethod
    def update(cam):
        env = Environment.Environment
        r1 = cam.rotSC[0]
        r2 = cam.rotSC[1]
        max = 250
        for s in Stars.__shooting:
            if s.pos.dist2D(cam.pos) > max:
                s.fill(cam)
            else:
                lonS = math.sin(s.lon)
                lonC = math.cos(s.lon)
                sp = .5
                s.pos += (Vex(sp*lonC , sp*lonS , 0))
                v = (s.pos - cam.pos).rotate2dXY(r1)  # roll
                v.setY(v.Y()+cam.mov[2])
                v.setZ(v.Z()+-cam.pos.Z())

                v = v.rotate2dYZ(0, r2)

                f = env.fov / (v.z()+.00000001)
                if(f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                p = v.p2D()

                if env.inScreen(p) and env.inScreen(s.lp):
                    brt = 255#random.randint(20, 155)
                    pygame.draw.line(env.getScreen(), (brt, brt, brt), p, s.lp, 1)
                s.lp = p

        for s in Stars.__debre:
            if s.pos.dist2D(cam.pos) > max:
                s.fill(cam)
            else:
                v = (s.pos-cam.pos).rotate2dXY(r1)
                v.setY(v.Y()+cam.mov[2])
                v.setZ(v.Z()+-cam.pos.Z())
                v = v.rotate2dYZ(0, r2)

                f = env.fov / (v.z()+.00000001)
                if(f < env.lim):
                    f = 1000
                v = v * f
                v = v + env.center
                p = v.p2D()

                if env.inScreen(p) and env.inScreen(s.lp):
                    brt = random.randint(20, 155)
                    pygame.draw.line(env.getScreen(), (brt, brt, brt), p, s.lp, 1)
                s.lp = p
                    
        for s in Stars.__stars:

            v = (s.pos).rotate2dXY(r1)

            v = v.rotate2dYZ(0, r2)

            f = env.fov / (v.z()+.00000001)
            if(f < env.lim):
                f = 1000
            v = v * f
            v = v + env.center
            p = v.p2D()

            if env.inScreen(p) and env.inScreen(s.lp):
                brt = random.randint(20, 155)
                pygame.draw.line(env.getScreen(), (brt, brt, brt), p, s.lp, 1)
            s.lp = p
        
