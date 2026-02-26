import arraylist
import math

class Rating:
    def init(self,id,name,rating,certian,RD):
         self.id = int(id)
         self.name = str(name)
         self.rating = int(rating)
         self.certian = bool(certian)
         self.RD = float(RD)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name},{self.rating},{self.rating},{self.RD}"

def getlist(fin):
    array = []
    #put it all into an array
    while True:
        text = fin.readline().strip()
        if text == "":
            break
        array.append(Rating(text.split(",") [0],text.split(",") [1],text.split(",") [2],text.split(",") [3],text.split(",") [4]))
    return array

def saveGame(list,fout):
    """Saves the updated game to a file

    Arguments:
        list: the list being saved
        fout: fut value of file being writen to
    """
    for i in range(len(list)):
        fout.write(list[i].tostr()+"\n")

def getGame(game):
    """Gets the game as a directory
    
    Arguments:
        game: the ID of the game

    Returns:
        String value: open file of selected game\n
        2: Error: Game does not exist
    """
    if(game==1):
        return "mariokart.csv"
    elif(game==2):
        return "eatfatfight.csv"
    elif(game==3):
        return "brawl"
    else:
        return 2

def register(ID,name,game):
    """Registers you for a ranking
    
    Arguments:
        ID: ID of the person
        name: the name of the player
        game: the game they wish to join

    Returns:
        0: Now rated\n
        1: ERROR: Already registered\n
        2: ERROR: Game does not exist
    """

    fin = open("ratings/"+getGame(game),"r")
    fin.close()
    if (fin == 2):
        return 2

    list = getlist(fin)
    if(arraylist.hasID(list,ID)):
        return 1
    
    list.append(Rating(ID,name,1500,False,350))
    fin.close()
    fout = open("ratings/"+getGame(game),"w")
    saveGame(list,fout)
    fout.close()
    return 0


def get_rating(ID,game):
    """
    Gets the reting and returns the value as a string along with a potental ? if uncertian

    Arguments:
        ID: ID of person
        game: the ID of the game

    Returns:
        Positive value: Rating of player\n
        -1: Player not registered for the game\n
        -2: the game does not exist
    """
    fin = open("ratings/"+getGame(game),"r")
    fin.close()
    if (fin == 2):
        return -2
    
    list = getlist(fin)
    place = arraylist.index(list,ID)
    if(place == -1):
        return -1
    
    #check for certanty
    text = str(list[place].rating)
    if(list[place].certian):
        return text
    return text + "?"

def changeRD(game):
    """changes the RD value of all players in the specified game

    Arguments:
        game: the number of the game being changed
    """
    fin = open("ratings/"+getGame(game),"r")
    list = getlist(fin)
    for i in range(len(list)):
        c = 34.6
        RD = list[i].RD 
        num = math.sqrt(RD**2+c**2)
        if(num>350):
            num = 350
        elif(num<30):
            num = 30
        if(num<100):
            list[i].certian = True
        else:
            list[i].certian = False
        list[i].RD = num
    fout = open("ratings/"+getGame(game),"w")
    saveGame(list,fout)
    fout.close()


def reset(game):
    """Resets the wins and losses for the given game
    
    Arguements:
        game: ID of game being reset
    """
    fin = open("games/"+getGame(game),"w")
    fin.close()
    return 0