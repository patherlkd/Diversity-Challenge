import RPi.GPIO as GPIO

class player:
    'Class for player'
    
    def __init__(self,name,number,teamname,GPIOpin):
        self.name = name
        self.number = number
        self.teamname = teamname
        self.GPIOpin = GPIOpin
        
        self.score = 0
    
    def addTen(self):
        self.score += 10
    
    def addFive(self):
        self.score += 5
    
    def minusFive(self):
        self.score -= 5
    
    def getPlayerName(self):
        return self.name
    
    def getPlayerNumber(self):
        return self.number
    
    def getTeamName(self):
        return self.teamname
    
    def getPlayerGPIOpin(self):
        return self.GPIOpin
    
    def getScore(self):
        return self.score
    
    def hasBuzzed(self):
        if GPIO.input(self.GPIOpin) == 0:
            return True
        else:
            return False
            
class team:
    'class for a collection of players'
    
    def __init__(self,size,teamname,playernames,GPIOpins):
            self.size = size
            self.teamname = teamname
            self.playernames = playernames
            self.GPIOpins = GPIOpins
            
            self.captainname = playernames[0]
            self.players = [ player(playernames[i],i,teamname,GPIOpins[i]) for i in range(self.size) ]
            
    def setGPIOs(self):
        for i in range(self.size):
            GPIO.setup(self.GPIOpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def getTeamName(self):
        return self.teamname
    
    def getSize(self):
        return self.size
    
    def getPlayers(self):
        return self.players
    
    def getTotalScore(self):
        sum = 0
        for p in self.players:
            sum += p.getScore()
        return sum
        
        
            