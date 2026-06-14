class Rating:
    def __init__(self,id,rating,certian,RD,wins,loses,ties):
         self.id = int(id)
         self.rating = float(rating)
         self.certian = bool(certian)
         self.RD = float(RD)
         self.wins = int(wins)
         self.loses = int(loses)
         self.ties = int(ties)
         self.gRD = 0
         self.scoresum = 0
         self.d2sum = 0
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.rating},{self.certian},{self.RD},{self.wins},{self.loses},{self.ties}"

class Person:
    def __init__(self,id):
         self.id = int(id)
    def tostr (self):
        #only used to write to file
        return f"{self.id}"
    
class Game:
    def __init__(self,winner,loser,tie):
        self.winner = int(winner)
        self.loser = int(loser)
        self.tie = bool(tie)