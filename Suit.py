# Suit
import RPGStats

class Suit:
    NONE = 0
    REFLECT = 1
    ABSORB = 2
    
    def __init__(self, parent):
        self.parent = parent
        self.health = 100
        self.chargeRage = 5000 # five secons
        self.chargeAmount = 1
        self.effect = Suit.NONE
        self.effectChance = 100
        self.stats = RPGStats.RPGStats()
        
