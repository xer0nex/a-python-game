# weapon
import RPGStats
import pygame
from Shot import Shot

class Weapon:
    
    def __init__(self, parent, rotation=[0, 0, 0], scale=[1, 1, 1], speed=10, damage=1,
                 shape=1, color=[255, 0, 0], offset = 2, dst=50):
        self.parent = parent
        self.stats = RPGStats.RPGStats()
        self.rotation = rotation
        self.scale = scale
        self.speed = speed
        self.damage = damage
        self.shape = shape
        self.color = color
        self.offset = -offset
        self.enable = True
        self.dst = dst
        
        self.temp = 0.0
        self.heatup = 5
        self.cooldown = 2
        self.coolrate = 500
        self.time = 0
        self.fireRate = 500
        self.timer = 0
        
    def Shoot(self, pos, rot, ant):
    #def __  ( pos=[0, 0, 0],            rot=     ,       scale,  angle_rad=0, speed=1, damage=0, shape=0, color=[255, 0, 0]):
        if self.updateTimer() and self.updateTemp():
            Shot(ant, [pos.X(), pos.Y(), 0], self.getRotation(), self.getScale(), rot, 
            self.getSpeed(), self.totalDamage(), self.getShape(), self.getColor(), self.getOffset(), self.dst)
    
    def updateTimer(self):
        ticks = pygame.time.get_ticks()
        if ticks-self.timer >= self.getFireRate():
            self.timer = ticks
            return True
        return False
        
    def updateTemp(self):
        out = False
        if self.temp < 100.0-self.heatup+1:
            out = True
            self.time = pygame.time.get_ticks()
            self.temp += self.heatup
        return out
        
    def update(self):
        if self.temp <= 0:
            self.temp = 0
            return
        if pygame.time.get_ticks()-self.time >= self.coolrate:
            self.temp -= self.cooldown
            self.time = pygame.time.get_ticks()
            
    def totalDamage(self):
        return (self.getDamage() + self.getParent().totalDamage())*2
    
    def getParent(self):
        return self.parent

    def setParent(self, value):
        self.parent = value

    def getRotation(self):
        return self.rotation

    def setRotation(self, value):
        self.rotation = value

    def getScale(self):
        return self.scale

    def setScale(self, value):
        self.scale = value

    def getSpeed(self):
        return self.speed

    def setSpeed(self, value):
        self.speed = value

    def getDamage(self):
        return self.damage

    def setDamage(self, value):
        self.damage = value

    def getShape(self):
        return self.shape

    def setShape(self, value):
        self.shape = value

    def getColor(self):
        return self.color

    def setColor(self, value):
        self.color = value

    def getOffset(self):
        return self.offset

    def setOffset(self, value):
        self.offset = value

    def getEnable(self):
        return self.enable

    def setEnable(self, value):
        self.enable = value

    def getTemp(self):
        return self.temp

    def setTemp(self, value):
        self.temp = value

    def getHeatup(self):
        return self.heatup

    def setHeatup(self, value):
        self.heatup = value

    def getCoolrate(self):
        return self.coolrate

    def setCoolrate(self, value):
        self.coolrate = value

    def getFireRate(self):
        return self.fireRate

    def setFireRate(self, value):
        self.fireRate = value
