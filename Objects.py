"""
    --Objects-- 
    This class with house information for both static and interactable objects
    
"""

from DungeonEngine import DungeonGenerator
from Vex import Vex
from MyMaths import rand2D
import Environment
import pygame
import random
import math


class Objects:
    objects = []
    src_images = {}
    rot_images = {}

    def __init__(self, parent, seed, pos=Vex(0, 0),
                 hp=-1, ang=0, color=(0, 255, 255), image=None, interactable=False, trigger=None):
        self.parent = parent
        self.points = [Vex(-.5, -.5), Vex(.5, -.5), Vex(.5, .5), Vex(-.5, .5)]
        self.pos = pos
        self.ang = ang
        self.statement = ''
        self.scale = 1
        self.interactable = interactable
        self.hp = hp
        self.trigger = trigger
        self.radius = .5
        self.height = 16
        rn = int((seed * 100) % 6)
        self.img_name = 'Default'
        if rn == 0:
            self.img_name = 'Castle'
        elif rn == 1:
            self.img_name = 'Forest'
        elif rn == 2:
            self.img_name = 'Cave'
        elif rn == 3:
            self.img_name = 'Lake'
        elif rn == 4:
            self.img_name = 'City'
        elif rn == 5:
            self.img_name = 'Mountain'
        elif rn == 6:
            self.img_name = 'Farm'


        self.img = rn
        self.color = color

    def selfUpdate(self, cam):
        env = Environment.Environment
        # self.weapon.update()
        inscreen = False
        projectedPoints = []
        dis = cam.pos.dist2D(self.pos)
        if dis < 1 and env.interact:
            print("Enter " + self.img_name)
            print(self.parent.seed)
            # enter dungeon with 0,0,0
            cam.dpos.assign(cam.pos)
            cam.pos.set2D(0,0)
            cam.dmpos.set2D(0,0)
            nseed = rand2D(self.pos.x(), self.pos.y(), self.parent.seed)
            print(str(cam.pos)+'   '+str(cam.dmpos))
            DungeonGenerator.invoke(nseed, cam, self.img)
            cam.pos.assign(cam.dpos)
            cam.dpos.set2D(0,0)

            pass
            """ enter thing """
        if dis < 50 and self.pos.dist2D(self.parent.pos) < self.parent.rad - 8:
            for i, p in enumerate(self.points):
                v = ((p * self.scale).rotate2dXY(math.radians(self.ang))
                     + self.pos - cam.pos).rotate2dXY(cam.rot[1]).rotate2dYZ(cam.mov[2], cam.rot[0])
                f = env.fov / (v.z() + .000000001)
                if (f < env.lim):
                    f = 1000
                p = (v * f + env.center).p2D()
                projectedPoints += [p]
                if env.inScreen(p):
                    inscreen = True

            if inscreen:
                env.add_visible_object(self)
                env.add_edge(self.color, projectedPoints, 1, 2)
                env.add_image(Objects.rot_images[self.img],
                              ((self.pos.projectedPos(cam))[1] - Vex(16, self.height)))
                # env.screen.blit(self.img,((self.pos.projectedPos(cam))[1]-Vex(16, 64)).p2D())
        return inscreen

    @staticmethod
    def Update(cam):
        env = Environment.Environment
        for self in reversed(Objects.objects):
            if self.health > 0:
                if self.selfUpdate(cam):
                    env.add_visible_object(self)
            else:
                Objects.objects.remove(self)

    @staticmethod
    def init():
        for rn in range(6):
            img_name = Objects.get_image_name(rn)
            Objects.src_images[img_name] = pygame.image.load("images/"+img_name + '.png').convert_alpha()

    @staticmethod
    def get_image_name(num):
        if num == 0:
            img_name = 'Castle'
        elif num == 1:
            img_name = 'Forest'
        elif num == 2:
            img_name = 'Cave'
        elif num == 3:
            img_name = 'Lake'
        elif num == 4:
            img_name = 'City'
        elif num == 5:
            img_name = 'Mountain'
        else:
            imge_name = 'Default'
        return img_name

    @staticmethod
    def update_image_rotation(cam):
        Objects.rot_images = {}
        for rn in range(0,6):
            img_name = Objects.get_image_name(rn)
            Objects.rot_images[rn] = rot_center(Objects.src_images[img_name],math.degrees(0))

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
