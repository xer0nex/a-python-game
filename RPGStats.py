# Attributes
# rpg stats
import random

class RPGStats:
    def __init__(self):
        self.xp = 1
        self.nxtlvlxp = 1
        self.lvl = 1
        self.hth = 50
        self.hp = self.hth
        self.str = 1
        self.con = 1
        self.blk = 1
        self.dex = 1
        self.int = 1
        self.cha = 1
        self.wis = 1
        self.wil = 1
        self.per = 1
        self.luk = 1
        self.maxluk = 100
        self.mods = []
        self.lvlUP()
        
    def nextLevel(self):
        self.nxtlvlxp += int((4 * ((self.lvl+10) ^ 3)) / 5)
        return self.nxtlvlxp
        
    def lvlUP(self):
        self.lvl += 1
        pro = 2 + int(self.lvl/5.0)
        self.setHTH(self.getHTH() + pro*pro)
        self.hp = self.getHTH()
        self.nextLevel()
        self.str += pro
        self.con += pro
        self.blk += pro
        self.dex += pro
        self.int += pro
        self.cha += pro
        self.wis += pro
        self.wil += pro
        self.per += pro
        self.luk += pro
        self.maxluk += pro
    
    def updateXP(self, xp):
        self.xp += xp
        if self.xp >= self.nxtlvlxp:
            self.lvlUP()
            return True
        return False
            
    def hpDMG(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            print ("dead")
            
            
    def isDead(self):
        if self.hp <=  0: return True
        return False
        
    def doLUK(self):
        if random.randint(0, self.maxluk) <= self.getTotalLUK(): return 1
        return random.uniform(0, .25)
    # get attribute of said object
    def getSTR(self):
        return self.str
    
    # get attribute of all equiped effective objects
    def getTotalSTR(self):
        atr = 0.0
        for s in self.mods:
            atr += s.str
        return atr + self.str
        
    # set attribute of object
    def setSTR(self, atrVal):
        self.str = atrVal
        
    # get attribute of said object
    def getCON(self):
        return self.con
    
    # get attribute of all equiped effective objects
    def getTotalCON(self):
        atr = 0.0
        for s in self.mods:
            atr += s.con
        return atr + self.con
        
    # set attribute of object
    def setCON(self, atrVal):
        self.con = atrVal
        
    # get attribute of said object
    def getBLK(self):
        return self.blk
    
    # get attribute of all equiped effective objects
    def getTotalBLK(self):
        atr = 0.0
        for s in self.mods:
            atr += s.blk
        return atr + self.blk
        
    # set attribute of object
    def setBLK(self, atrVal):
        self.blk = atrVal
        
    # get attribute of said object
    def getDEX(self):
        return self.dex
    
    # get attribute of all equiped effective objects
    def getTotalDEX(self):
        atr = 0.0
        for s in self.mods:
            atr += s.dex
        return atr + self.dex
        
    # set attribute of object
    def setDEX(self, atrVal):
        self.dex = atrVal
    
    # get attribute of said object
    def getINT(self):
        return self.int
    
    # get attribute of all equiped effective objects
    def getTotalINT(self):
        atr = 0.0
        for s in self.mods:
            atr += s.int
        return atr + self.int
        
    # set attribute of object
    def setINT(self, atrVal):
        self.int = atrVal
    
    # get attribute of said object
    def getCHA(self):
        return self.cha
    
    # get attribute of all equiped effective objects
    def getTotalCHA(self):
        atr = 0.0
        for s in self.mods:
            atr += s.cha
        return atr + self.cha
        
    # set attribute of object
    def setCHA(self, atrVal):
        self.cha = atrVal
    
    # get attribute of said object
    def getWIS(self):
        return self.wis
    
    # get attribute of all equiped effective objects
    def getTotalWIS(self):
        atr = 0.0
        for s in self.mods:
            atr += s.wis
        return atr + self.wis
        
    # set attribute of object
    def setWIS(self, atrVal):
        self.wis = atrVal
    
    # get attribute of said object
    def getWIL(self):
        return self.wil
    
    # get attribute of all equiped effective objects
    def getTotalWIL(self):
        atr = 0.0
        for s in self.mods:
            atr += s.wil
        return atr + self.wil
        
    # set attribute of object
    def setWIL(self, atrVal):
        self.wil = atrVal
    
    # get attribute of said object
    def getPER(self):
        return self.per
    
    # get attribute of all equiped effective objects
    def getTotalPER(self):
        atr = 0.0
        for s in self.mods:
            atr += s.per
        return atr + self.per
        
    # set attribute of object
    def setPER(self, atrVal):
        self.per = atrVal
    
    # get attribute of said object
    def getLUK(self):
        return self.luk
    
    # get attribute of all equiped effective objects
    def getTotalLUK(self):
        atr = 0.0
        for s in self.mods:
            atr += s.luk
        return atr + self.luk
        
    # set attribute of object
    def setLUK(self, atrVal):
        self.luk = atrVal
    
    def getMODS(self):
        return self.mods
    def addMOD(self, mod):
        self.mods.extend(mod)
    def removeMOD(self, mod):
        self.mods.remove(mod)

    def getHTH(self):
        return self.hth

    def setHTH(self, value):
        self.hth = value
    
    def getHP(self):
        if self.hp <0 :
            self.hp = 0
        return self.hp
    
    def getLVL(self):
        return self.lvl
