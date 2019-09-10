# Player
import pygame
import math

import Color
import Ship
import Creature
import DrawINFO
import Environment

from Vex import Vex
from RPGStats import RPGStats
from ParticleEngine import Emitter
from Planets import Planets


# from Asteroid import Asteroid


class Player:
    sensorPoints = []
    sensorEdges = []
    player = None

    def __init__(self, pos=[0, 0, 0], rot=[0.0, 0.0, 0.0]):
        # give player a creature to control
        self.creature = Creature.Creature(self)

        # let Creature class know what creature is the player creature
        Creature.Creature.PlayerCreature = self.creature

        # give the player a ship - for testing
        self.ship = Ship.Ship(self)

        # Give the player an OP weapon - for testing
        self.ship.weapon.setFireRate(20)
        self.ship.weapon.setCoolrate(20)

        # Player is not really in ship yet
        self.inship = False

        # set the position of the player. this should not be used.

        # var to tell if player is in the atmosphere of some planet
        self.inatmosphere = False

        # var to tell if player is in a dungeon
        self.in_dungeon = False

        # give the player a camera
        self.cam = Camera(self)

        # let the Player class know the player instance
        Player.setPlayer(self)

        # give the player stats
        self.stats = RPGStats()

        # the player will be level 1
        self.stats.lvlUP()

        # player enters ship, set vars to make this happen - for testing
        self.enterShip(self.ship)

    # get the radius of influence of the player, related to object occupancy
    def getRadius(self):
        if self.inship:
            return self.ship.getShieldRadius()
        else:
            return self.creature.getRadius()

    # get the total damage
    def totalDamage(self):
        return self.stats.getSTR() * 2

    # get camera assosciated to the player
    def get_cam(self):
        return self.cam

    # is the player or occupied ship have health
    def isAlive(self):
        out = False
        if self.inship:
            if self.ship.stats.hp > 0: out = True
        else:
            if self.stats.hp > 0: out = True
        return out

    # set vars to reflect an exit of ship
    def exitShip(self):
        self.inship = False
        self.ship.pos = self.cam.pos.copy()
        self.ship.pos.setZ(0)
        self.ship.rot = -self.cam.rot[1]
        self.ship.setOccupied(False)
        Ship.Ship.add_unoccupied(self.ship)
        self.ship.setParent(None)
        self.ship = None

    # set vars to reflect an entrance of ship
    def enterShip(self, ship):
        Ship.Ship.remove_unoccupied(ship)
        self.ship = ship
        ship.setParent(self)
        self.inship = True
        self.cam.pos = ship.pos.copy().setZ(self.cam.pos.z())
        self.cam.rot[1] = -ship.rot
        ship.pos = Vex(0, 0, 0)
        ship.setOccupied(True)

    # return the position of the player
    def getPos(self):
        return self.cam.pos

    # set the player as thing?????  why would this ever get called?
    @staticmethod
    def setPlayer(thing):
        Player.player = thing

    # does a shot hit the player   
    @staticmethod
    def testShotHit(sh):
        # dont let the player shoot themselves
        if sh.source != Player.player:
            # exchange for faster access
            dmg = sh.damage
            # exchange for faster access
            player = Player.player
            v = sh.pos.copy()
            if v.dist2D(player.cam.pos) <= 2:
                tdmg = player.doDMG(dmg)
                if tdmg > 0:
                    DrawINFO.DrawINFO(player.cam.pos.X(), player.cam.pos.Y(), 0, tdmg)
                else:
                    DrawINFO.DrawINFO(player.cam.pos.X(), player.cam.pos.Y(), 0, "MISS", Color.GREEN)
                return True
        return False

    def doDMG(self, dmg):
        dmg = int(dmg - self.stats.getDEX() * (self.stats.doLUK() * 10))
        if dmg > 0:
            if self.inship:
                self.ship.stats.hpDMG(dmg)
            else:
                self.creature.stats.hpDMG(dmg)
        return dmg

    def getLVL(self):
        return self.stats.getLVL()

    def set_cam_pos(self, x, y, z):
        self.cam.pos.set(x, y, z)

    def shoot(self):
        cp = self.cam.pos
        if self.inship:
            self.ship.shoot(cp, self.cam.rot[1], self)
        else:
            self.creature.weapon.Shoot(cp, self.cam.rot[1], self)

    def update(self, cam):
        if Camera.mbd:
            Player.player.shoot()

        self.creature.selfUpdatePlayer(cam)
        if self.ship: self.ship.updatePlayerShip(cam)


class Camera:
    maxTilt = math.pi / 2 - .3
    mbd = False
    camera = None

    # initialize camera
    def __init__(self, player):
        self.pos = Vex(0.0, 0.0)
        self.dmpos = Vex(0.0,0.0)
        self.dpos = Vex(0.0,0.0)
        self.lpos = self.pos.copy()
        self.ldmpos = self.dmpos.copy()
        self.rot = [0.0, 0.0, 0.0]
        self.rotSC = [0.0, 0.0]
        self.mov = [0.0, 0.0, 0.0]
        self.sway = 0
        self.sway2 = 0
        self.player = player
        self.minHeight = 1.45
        self.maxHeightS = 60.0
        self.maxHeightC = 30.0
        self.delta = 0
        self.top = False

        self.mouseRel = False
        pygame.mouse.set_visible(0)
        pygame.event.set_grab(1)

        self.joy = Controller()
        self.joy.init(self)
        Camera.camera = self

        self.cvp_triggered = False  # camera view point triggered
        self.vehicle_triggered = False

    # handle events that effect camera
    def events(self, event):
        env = Environment.Environment
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_j:
                if self.player.inship:
                    self.player.exitShip()
                else:
                    for ship in Ship.Ship.ships:
                        if ship.pos.dist2D(self.pos) < ship.getShieldRadius():
                            self.player.enterShip(ship)

            if event.key == pygame.K_SPACE:
                self.mouseRel = not self.mouseRel
                if self.mouseRel:
                    pygame.mouse.set_visible(1)
                    pygame.event.set_grab(0)
                else:
                    pygame.mouse.set_visible(0)
                    pygame.event.set_grab(1)

        if self.mouseRel:
            return

        if env.useController:
            self.joy.joystick(event)

        self.rot[2] *= .98
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_rel()
            self.rot[1] -= (x / 150)  # rol
            self.rot[2] += y / 150  # pitch

        if event.type == pygame.MOUSEBUTTONDOWN or self.joy.button_data.get(5):
            Camera.mbd = True
        if event.type == pygame.MOUSEBUTTONUP or self.joy.button_up_data.get(5):
            self.joy.button_up_data[5] = False
            Camera.mbd = False



        # controller exit or enter vehicle
        if self.joy.button_data.get(3) and not self.vehicle_triggered:
            self.vehicle_triggered = True
            if self.player.inship:
                self.player.exitShip()
            else:
                for ship in Ship.Ship.ships:
                    if ship.pos.dist2D(self.pos) < ship.getShieldRadius():
                        self.player.enterShip(ship)
                    env.interact = True
        # single press mechanism
        if not self.joy.button_data.get(3) and self.vehicle_triggered:
            self.vehicle_triggered = False




    # update camera from keys and other
    def update(self, dt, key):
        if self.mouseRel:
            return

        if self.top:
            self.rot[0] = 0
            self.sway2 = self.rot[0] * 2.5
        else:
            self.rot[0] = -Camera.maxTilt
            self.sway2 = self.rot[0] * 2.5


        enableJ = False
        self.rot[1] -= self.joy.angleRS / 40
        height = 0
        if Player.player.inship:
            h = -self.maxHeightS - (
            (((self.maxHeightS - self.minHeight) / self.maxTilt) * self.rot[0]) + self.minHeight)
        elif not self.player.in_dungeon:
            h = -self.maxHeightC - (
            (((self.maxHeightC - self.minHeight) / self.maxTilt) * self.rot[0]) + self.minHeight)
        else:
            h = -15

        height = h

        self.pos.setZ(height)



        self.sway *= .89
        self.mov[2] = -self.sway + self.sway2

        self.delta = dt

        s = dt * 2
        if self.player.inship:
            s = dt * 15
        elif self.player.in_dungeon:
            s = dt * 2


        if key[pygame.K_u] or self.joy.button_data.get(13):
            if Player.player.inship:
                Player.player.ship.weapon.temp = 0
            else:
                Player.player.creature.weapon.temp = 0

            #        if key[pygame.K_r]:
            #            self.minHeight -= s
            #        if key[pygame.K_f]:
            #            self.minHeight += s

        jump = 0

        if ((key[pygame.K_k] and key[pygame.K_w]) or self.joy.button_data.get(4)):
            enableJ = True
            if self.player.inship and not Planets.inAtmosphere(self.player.cam.pos):
                jump = 10
            else:
                jump = .0525



        # forward /backward
        ms = math.sin(self.rot[1])
        mc = math.cos(self.rot[1])

        #        testedA = Asteroid.testRadiusCollision(Player.player, self.pos, Player.player.getRadius())
        #        if testedA:
        #            self.pos.assign(testedA.setZ(self.pos.z()))
        #
        if not self.player.in_dungeon:
            if key:
                x, y = (s + jump) * ms, (s + jump) * mc
            if self.joy.angleLS[1] != 0.0:
                xj, yj = (s + jump) * ms * self.joy.angleLS[1], (s + jump) * mc * self.joy.angleLS[1]
            if self.rot[2] != 0.0:
                xj, yj = (s + jump) * ms * self.rot[2], (s + jump) * mc * self.rot[2]
            tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(0, 0), Player.player.getRadius())
            if tested:
                self.pos.assign(tested.setZ(self.pos.z()))
            else:
                self.lpos.assign(self.pos)
            if self.joy.angleLS[1] != 0.0:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(xj, yj), Player.player.getRadius())
                if not tested:
                    enableJ = True
                    self.pos.setX(self.pos.X() + xj)
                    self.pos.setY(self.pos.Y() + yj)
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))

            if key[pygame.K_w]:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(-x, -y), Player.player.getRadius())
                # testedA = Asteroid.testRadiusCollision(Player.player, self.pos+Vex(-x, -y), Player.player.getRadius())
                if not tested:
                    # if not testedA:
                    enableJ = True
                    self.pos.setX(self.pos.X() - x)
                    self.pos.setY(self.pos.Y() - y)
                #                else:
                #                    self.pos.assign(testedA.setZ(self.pos.z()))
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))

            if key[pygame.K_s]:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(x, y), Player.player.getRadius())
                # testedA = Asteroid.testRadiusCollision(Player.player, self.pos+Vex(x, y), Player.player.getRadius())
                if not tested:
                    # if not testedA:
                    self.pos.setX(self.pos.X() + x)
                    self.pos.setY(self.pos.Y() + y)
                #                else:
                #                    self.pos.assign(testedA.setZ(self.pos.z()))
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))

            # straff left /right keyboard
            x, y = (s * ms), (s * mc)
            # straff left / right controller
            xc, yc = (s * ms * self.joy.angleLS[0]), (s * mc * self.joy.angleLS[0])
            if self.joy.angleLS[0] != 0.0:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(yc, -xc), Player.player.getRadius())
                # testedA = Asteroid.testRadiusCollision(Player.player, self.pos+Vex(-y, x), Player.player.getRadius())
                if not tested:
                    # if not testedA:
                    self.pos.setX(self.pos.X() + yc)
                    self.pos.setY(self.pos.Y() - xc)
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))

            if key[pygame.K_a]:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(-y, x), Player.player.getRadius())
                # testedA = Asteroid.testRadiusCollision(Player.player, self.pos+Vex(-y, x), Player.player.getRadius())
                if not tested:
                    # if not testedA:
                    self.pos.setX(self.pos.X() - y)
                    self.pos.setY(self.pos.Y() + x)
                #                else:
                #                    self.pos.assign(testedA.setZ(self.pos.z()))
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))

            if key[pygame.K_d]:
                tested = Planets.testRadiusCollision(Player.player, self.pos, Vex(y, -x), Player.player.getRadius())
                # testedA = Asteroid.testRadiusCollision(Player.player, self.pos+Vex(y, -x), Player.player.getRadius())

                if not tested:
                    # if not testedA:
                    self.pos.setX(self.pos.X() + y)
                    self.pos.setY(self.pos.Y() - x)
                #                else:
                #                    self.pos.assign(testedA.setZ(self.pos.z()))
                else:
                    self.pos.assign(tested.setZ(self.pos.z()))
        elif self.player.in_dungeon:
            scl = 30
            if key:
                x, y = (s + jump) * ms, (s + jump) * mc
                dx, dy = (s + jump)*scl * ms, (s + jump)*scl * mc
            if self.joy.angleLS[1] != 0.0:
                xj, yj = (s + jump) * ms * self.joy.angleLS[1], (s + jump) * mc * self.joy.angleLS[1]
                dxj, dyj = (s + jump)*scl * ms * self.joy.angleLS[1], (s + jump)*scl * mc * self.joy.angleLS[1]
            if  self.rot[2] != 0.0:
                xj, yj = (s + jump) * ms * self.rot[2], (s + jump) * mc * self.rot[2]
                dxj, dyj = (s + jump) * scl * ms * self.rot[2], (s + jump) * scl * mc * self.rot[2]
            self.lpos.assign(self.pos)
            self.ldmpos.assign(self.dmpos)
            if self.joy.angleLS[1] != 0.0 or self.rot[2] != 0.0:
                enableJ = False
                self.pos.setX(self.pos.X() + xj)
                self.pos.setY(self.pos.Y() + yj)
                self.dmpos.setX(self.dmpos.X() + dxj)
                self.dmpos.setY(self.dmpos.Y() + dyj)

            if key[pygame.K_w]:
                enableJ = False
                self.pos.setX(self.pos.X() - x)
                self.pos.setY(self.pos.Y() - y)
                self.dmpos.setX(self.dmpos.X() - dx)
                self.dmpos.setY(self.dmpos.Y() - dy)

            if key[pygame.K_s]:
                self.pos.setX(self.pos.X() + x)
                self.pos.setY(self.pos.Y() + y)
                self.dmpos.setX(self.dmpos.X() + dx)
                self.dmpos.setY(self.dmpos.Y() + dy)

            # straff left /right keyboard
            if key:
                x, y = (s * ms), (s * mc)
                dx, dy = (s * scl * ms), (s * scl * mc)
            # straff left / right controller
            if self.joy.angleLS[0] != 0.0:
                xc, yc = (s * ms * self.joy.angleLS[0]), (s * mc * self.joy.angleLS[0])
                dxc, dyc = (s * scl * ms * self.joy.angleLS[0]), (s * scl * mc * self.joy.angleLS[0])

            if self.joy.angleLS[0] != 0.0:
                self.pos.setX(self.pos.X() + yc)
                self.pos.setY(self.pos.Y() - xc)
                self.dmpos.setX(self.dmpos.X() + dyc)
                self.dmpos.setY(self.dmpos.Y() - dxc)

            if key[pygame.K_a]:
                self.pos.setX(self.pos.X() - y)
                self.pos.setY(self.pos.Y() + x)
                self.dmpos.setX(self.dmpos.X() - dy)
                self.dmpos.setY(self.dmpos.Y() + dx)

            if key[pygame.K_d]:
                self.pos.setX(self.pos.X() + y)
                self.pos.setY(self.pos.Y() - x)
                self.dmpos.setX(self.dmpos.X() + dy)
                self.dmpos.setY(self.dmpos.Y() - dx)

        if jump > 0 and enableJ:
            if Player.player.inship:
                Emitter(self.pos.copy().setZ(0), self.rot[1], 3)
            self.sway += jump / 15

        self.rotSC = [[ms, mc], [math.sin(self.rot[0]), math.cos(self.rot[0])]]



class Controller():
    parent = None
    controller = None
    axis_data = {}
    button_data = {}
    button_up_data = {}
    hat_data = {}
    angleLS = [0.0, 0.0]
    angleRS = 0.0

    def init(self, parent):
        Controller.parent = parent
        pygame.joystick.init()
        try:
            Controller.controller = pygame.joystick.Joystick(0)
            Controller.controller.init()
            self.test_empty()
        except:
            Environment.Environment.useController = False

        return self

    def joystick(self, event):
        if not self.button_up_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_up_data[i] = False

        if event.type == pygame.JOYAXISMOTION:
            self.axis_data[event.axis] = round(event.value, 1)
            self.angleLS = [self.axis_data.get(0, 0.0), self.axis_data.get(1, 0.0)]
            self.angleRS = self.axis_data.get(2, 0.0)
            if self.angleRS == .1 or self.angleRS == -.1: self.angleRS = 0.0
            if self.angleLS[0] == .1 or self.angleLS[0] == -.1: self.angleLS[0] = 0.0
            if self.angleLS[1] == .1 or self.angleLS[1] == -.1: self.angleLS[1] = 0.0
        elif event.type == pygame.JOYBUTTONDOWN:
            self.button_data[event.button] = True
            self.button_up_data[event.button] = False
        elif event.type == pygame.JOYBUTTONUP:
            self.button_up_data[event.button] = True
            self.button_data[event.button] = False


        elif event.type == pygame.JOYHATMOTION:
            self.hat_data[event.hat] = event.value

        # print(self.button_data)

        # print (self.axis_data)
        #        if 1 in self.axis_data and 0 in self.axis_data:
        # print (str(self.axis_data.get(1, 0.0)))

        # , self.axis_data.get(0, 0.0)]
        #        if 2 in self.axis_data and 3 in self.axis_data:
        #            self.angleRS = math.atan2(self.axis_data.get(3, 0.0), self.axis_data.get(2, 0.0))
        # print (str(self.angleLS) + str(self.angleRS))

    def test_empty(self):
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.button_up_data:
            self.button_up_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_up_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
