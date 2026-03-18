class Rating:
    def __init__(self,id,name,rating,certian,RD,wins,loses,ties):
         self.id = int(id)
         self.name = str(name)
         self.rating = int(rating)
         self.certian = bool(certian)
         self.RD = float(RD)
         self.wins = int(wins)
         self.loses = int(loses)
         self.ties = int(ties)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name},{self.rating},{self.rating},{self.RD},{self.wins},{self.loses},{self.ties}"

class Person:
    def __init__(self,id,name):
         self.id = int(id)
         self.name = str(name)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name}"
