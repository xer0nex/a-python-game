# Mind

import random
import pygame


import Color
import Ship
import Creature
import DrawINFO
import ParticleEngine
from Planets import Planets
#from Asteroid import Asteroid
import Environment
from Vex import *



class Mind:
    #states
    
    ROAM = 0
    ATTACK = 1
    FLEE = 2
    SUICIDE = 3
    BERZERK = 4
    WAIT = 5
    FALLOW = 6
    SURRENDER = 7
    ABANDON = 8
    SPEEDUP = 9
    SPEEDDOWN = 10
    STRAFLEFT = 11
    STRAFRIGHT = 12
    ROTLEFT = 13
    ROTRIGHT = 14
    FULLSTOP = 15
    FIRE = 16
    
    Minds = []
    
    def __init__(self, cam):
        pi = 3.141
        maxDist = 100
        minDist = maxDist - 50
        self.ang = random.uniform(-pi*2,pi )
        dis = random.randint(minDist, maxDist)
        self.pos = cam.pos.add( Vex(math.sin(self.ang)*dis, math.cos(self.ang)*dis, 0))
        self.pos.setZ(0)
        self.speed = -.1
        self.ship = Ship.Ship(self)
        self.inship = False
        self.inatmosphere = False
        self.state = 0
        self.mindDur = 0
        self.mindCho = 0
        self.mindTim = 0
        self.shotspd = 2
        self.shotms = 0
        self.statement = ""
        self.creature = Creature.Creature(self)
        self.target = []
        self.enterShip(self.ship)
        Mind.Minds.extend([self])
    
    def exitShip(self):
        self.inship = False
        self.ship.setOccupied(False)
    
    def enterShip(self, ship):
        self.ship = ship
        self.inship = True
        self.ship.setOccupied(True)
     
    def getPos(self):
        return self.pos
        
    @staticmethod    
    def update(cam):
        env = Environment.Environment
        env.clear_visible()
        for self in Mind.Minds:
            if self.creature.selfUpdate(cam, self.pos, self.ang):
                env.add_visible(self)
            
            self.updateAI(cam.player)
            self.ship.updateCreatureShip(cam, self.pos, self.ang)
    
    def getRadius(self):
        if self.inship:
            return self.ship.getShieldRadius()
        else:
            return self.creature.getRadius()
            
    def isAlive(self):
        out = False
        if self.inship:
            if self.ship.stats.hp>0:out = True
        else:
            if self.stats.hp > 0 : out = True
        return out
        
    @staticmethod
    def testShotHit(shot):
        x,y,z = shot.pos.Pos()
    #def testShotHit(x, y, z, dmg, ant):
        out = False
        for self in reversed(Mind.Minds):
            v = Vex(x, y, z)
            if v.dist2D(self.pos)<=2:
                tdmg = 0
                if not self.inship:
                    tdmg = int(shot.damage - self.creature.stats.getDEX()*(self.creature.stats.doLUK()*10))
                else:
                    tdmg = int(shot.damage - self.ship.stats.getDEX()*(self.ship.stats.doLUK()*10))
                out = True
                if tdmg>0:
                    DrawINFO.DrawINFO(x, y, z, tdmg, Color.RED)
                    ParticleEngine.Emitter(Vex(x, y, z), shot.angle_rad, 0)
                    self.ship.stats.hpDMG(tdmg)
                    if shot.source.isAlive():
                        if shot.source not in self.target:
                            self.target.extend([shot.source])
                else:
                    DrawINFO.DrawINFO(x, y, z, "MISS", Color.ORANGE)
                
                if self.inship:
                    if self.ship.stats.isDead():
                        if shot.source.ship.stats.updateXP(random.randint(self.ship.stats.getLVL(),2*self.ship.stats.getLVL() )):
                            DrawINFO.DrawINFO(x, y, z, "LEVEL UP", Color.RED)
                        
                        ParticleEngine.Emitter(Vex(x, y, z), shot.angle_rad, 1)
                        Mind.Minds.remove(self)
                else:
                    if self.creature.stats.isDead():
                        if shot.source.stats.updateXP(random.randint(1*self.creature.stats.getLVL(),10*self.creature.stats.getLVL() )):
                            DrawINFO.DrawINFO(x, y, z, "LEVEL UP", Color.RED)
                        
                        ParticleEngine.Emitter(Vex(x, y, z), shot.angle_rad, 1)
                        Mind.Minds.remove(self)
                
        return out
        
    def totalDamage(self):
        return self.stats.getSTR()*2
        
    def updateAI(self, player):
        # distance variable
        dis = 0
        # angle variable
        ang = 0
        
        # does the mind have a target and is it not the player
        if self.target and self.target[0] != player:
            self.state = Mind.ATTACK
            # if there are any dead targets, loop
            while self.target and not self.target[0].isAlive():
                self.target.remove(self.target[0])
            
            #sort to attack closest enemy
            self.target.sort(key = lambda m: self.pos.dist2D(m.pos), reverse = True)
            print (str(self.target))
            # if the list still isn't empty
            if self.target:
                # get the distance and angle to target
                dis = self.pos.dist2D(self.target[0].pos)
                ang = math.degrees(self.target[0].pos.ang2D(self.pos))+90.0
            
        elif self.target and self.target[0] == player:
            self.state = Mind.ATTACK
            dis = self.pos.dist2D(player.cam.pos)
            ang = math.degrees(player.cam.pos.ang2D(self.pos))+90.0
            self.statment="I'm going to get you!"
        else:
            self.state = Mind.ROAM
            self.statment = ""
        
        #if dis < 100:
            #self.state = Mind.FLEE
        #    if self.stats.getHP() > 20:
                # this signifies the attack state
                # self.state = Mind.ATTACK
        #       pass
        
        if ang < self.ang-180:ang = 360.0+ang
        if ang > self.ang+180:ang = ang - 360.0
        
#        testedA = Asteroid.testRadiusCollision(self, self.pos, self.getRadius())
#        if testedA:
#            self.pos.assign(testedA.setZ(self.pos.z()))
#                    
        # action
        diffA = ang - self.ang
        if self.state == Mind.ATTACK:
            
            if diffA > 1:
                self.ang += 2.0 + random.uniform(0,.1)
            elif diffA < -1 :
                self.ang -= 2.0 - random.uniform(0, .1)
            
            if dis > 10 :
                # get the x, y movement
                rads = math.radians(-self.ang)
                x = math.sin(rads)*self.speed
                y = math.cos(rads)*self.speed
                tv = Vex(x, y)
#                testedA = Asteroid.testRadiusCollision(self, self.pos+tv, self.getRadius())
#                if testedA:
#                    self.pos.assign(testedA.setZ(self.pos.z()))
#                    
                tested = Planets.testRadiusCollision(self, self.pos+tv, self.getRadius())
                if not tested:
                    self.pos.selfAdd2D(x, y)
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))
            elif dis < 9 :
                # get the x, y movement
                rads = math.radians(self.ang)
                x = math.sin(rads)*self.speed
                y = math.cos(rads)*self.speed
                
                tv = Vex(x, y)
#                testedA = Asteroid.testRadiusCollision(self, self.pos+tv, self.getRadius())
#                if testedA:
#                    self.pos.assign(testedA.setZ(self.pos.z()))
#                    
                tested = Planets.testRadiusCollision(self, self.pos+tv, self.getRadius())
                if not tested:
                    self.pos.selfAdd2D(x, y)
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))
            if self.ang < ang+3 and self.ang > ang - 3:
                self.state = Mind.FIRE
                
        if self.state == Mind.FLEE:
            self.statement = "Run away!"
            if diffA > 1:
                self.ang += 2.0 + random.uniform(0,.1)
            elif diffA < -1 :
                self.ang -= 2.0 - random.uniform(0, .1)
            # get the x, y movement
            rads = math.radians(self.ang)
            x = math.sin(rads)*self.speed
            y = math.cos(rads)*self.speed
            tv = Vex(x, y)
#            testedA = Asteroid.testRadiusCollision(self, self.pos+tv, self.getRadius())
#            if testedA:
#                self.pos.assign(testedA.setZ(self.pos.z()))
                    
            tested = Planets.testRadiusCollision(self, self.pos+tv, self.getRadius())
            if not tested:
                self.pos.selfAdd2D(x, y)
            else:
                self.pos.assign(tested.setZ(self.pos.z()))
                
        if self.state == Mind.FIRE:
            self.statement = "Pew pew pew!"
            self.shoot()
        
        if self.state == Mind.ROAM:
            self.statement = ""
            if self.mindCho == 0:
                self.mindTim = pygame.time.get_ticks()
                self.mindDur = random.randint(500,1500)
                self.mindCho = random.randint(0,2)
            elif self.mindCho == 1:
                self.ang += 1
            elif self.mindCho == 2:
                self.ang -= 1
                
            if pygame.time.get_ticks()-self.mindTim > self.mindDur:
                self.mindCho = 0
            
            # get the x, y movement
            rads = math.radians(-self.ang)
            x = math.sin(rads)*self.speed
            y = math.cos(rads)*self.speed
            tv = Vex(x, y)
#            testedA = Asteroid.testRadiusCollision(self, self.pos+tv, self.getRadius())
#            if testedA:
#                self.pos.assign(testedA.setZ(self.pos.z()))
#                
            tested = Planets.testRadiusCollision(self, self.pos+tv, self.getRadius())
            if not tested:
                self.pos.selfAdd2D(x, y)
            else:
                self.pos.assign(tested.setZ(self.pos.z()))
        
    def shoot(self):
        if self.inship:
            self.ship.shoot(self.pos,math.radians(-self.ang),self)
            
   
