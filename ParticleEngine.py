#Emitter and Partical

import pygame
import random
import Environment
from math import cos, sin, pi
from MyMaths import rotate2d
from Vex import Vex


class Particle():
    def __init__(self, parent, angle, speed, type=0, Color=[255, 255, 255]):
        self.par = parent
        self.pos = parent.pos.copy()
        self.lpo = parent.pos.copy()
        self.ang = angle
        self.spd = speed
        self.typ = type
        self.col = Color
        self.dur = parent.getDuration()
        self.cur = pygame.time.get_ticks()

    def update(self,  cam):
        env = Environment.Environment
        self.lpo = self.pos.copy()
        self.pos.pos[0] -= sin(self.ang)*self.spd*cam.delta
        self.pos.pos[1] -= cos(self.ang)*self.spd*cam.delta
        pp = []
        x, y, z = 0, 0, 0
        if self.typ == 3:
            j, k, l = (self.par.pos).rotate2dXY(cam.rot[1]).Pos()
            l -= cam.pos.z()
            k, l = rotate2d((k + cam.mov[2], l), cam.rot[0])
            g = env.fov / (l+.00000001)
            if(g>1):
                j, k = j * g, k*g
            else:
                j, k = j*1000, k*1000
            pp = [env.cx() + int(j), env.cy() + int(k)]
            x, y, z = (self.pos).rotate2dXY(cam.rot[1]).Pos()
            z = -cam.pos.z()
        else:
            x, y, z = (self.pos-cam.pos).rotate2dXY(cam.rot[1]).Pos()
        
        y, z = rotate2d((y + cam.mov[2], z), cam.rot[0])  # pitch
        f = env.fov / (z+.00000001)
        if(f > 1):
            x, y = x * f, y * f
        else:
            x, y = x*1000, y*1000
            
        p = [env.cx() + int(x), env.cy() + int(y)]
        
        if self.typ == 3:
            if env.inScreen(p) and env.inScreen(pp):
                pygame.draw.line(env.getScreen(), self.col, p, pp, 1)
        else:
            if env.inScreen(p):
                pygame.draw.line(env.getScreen(), self.col, p, p, 1)


class Emitter(object):
    emitters = []
    def __init__(self, pos, ang, debType = 0,  max=25, shape=[Vex(0, 0)], shape_rnd=False,rate=1):
        if debType==3:
            self.pos = Vex(0, 0, 0)
        else:
            self.pos = pos.copy()
        self.type = debType
        self.dur = 2000
        self.cur = pygame.time.get_ticks()
        self.shape = shape
        self.shape_rnd = shape_rnd
        self.scale = Vex(1, 1)
        
        if debType == 0:
            max = 25
            self.particles = [Particle(self,pi+ang+random.uniform(-.5, .5), random.uniform(.1, .2)*rate, debType) for x in range(max)]
        elif debType == 1:
            # max = 50
            self.dur = 5000
            self.particles = [Particle(self,pi+ang+random.uniform(-pi, pi), random.uniform(.1, .5)*rate, debType, (255, 0, 0)) for x in range(max)]
        elif debType == 2:
            max = 25
            self.dur = 1000
            self.particles = [Particle(self,pi+ang+random.uniform(-.5, .5), random.uniform(.01, .2)*rate, debType, (0, 200, 0)) for x in range(max)]
        elif debType == 3:
            max = 10
            self.dur = 200
            self.particles = [Particle(self,pi+ang+random.uniform(-.5, .5), random.uniform(.01, .2)*rate, debType, (255, 0, 0)) for x in range(max)]
        
        Emitter.emitters += [self]
        
        
    def getDuration(self):
        out = random.randint(500, 2000)
        if self.type == 0:
            pass
        elif self.type == 1:
            out = random.randint(3000, 5000)
        elif self.type == 2:
            out = random.randint(100, self.dur)
        elif self.type == 3:
            out = random.randint(10, 200)
        return out
        
    def updateEmitter(self,  cam):
        
        if self.particles:
            for p in reversed(self.particles):
                if pygame.time.get_ticks()-p.cur < p.dur:
                    p.update(cam)
                else:
                    self.particles.remove(p)
        else:
            Emitter.emitters.remove(self)

    @staticmethod
    def update(cam):
        for e in reversed(Emitter.emitters):
            e.updateEmitter(cam)

    
