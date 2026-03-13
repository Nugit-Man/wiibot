class Rating:
    def init(self,id,name,rating,certian,RD,wins,loses):
         self.id = int(id)
         self.name = str(name)
         self.rating = int(rating)
         self.certian = bool(certian)
         self.RD = float(RD)
         self.wins = int(wins)
         self.loses = int(loses)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name},{self.rating},{self.rating},{self.RD},{self.wins},{self.loses}"

class Person:
    def init(self,id,name,marioKart,eatFatFight,brawl,swordFight):
         self.id = int(id)
         self.name = str(name)
         self.marioKart = bool(marioKart)
         self.eatFatFight = bool(eatFatFight)
         self.brawl = bool(brawl)
         self.swordFight = bool(swordFight)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name},{self.marioKart},{self.eatFatFight},{self.brawl},{self.swordFight}"
