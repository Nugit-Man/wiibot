import arraylist
import ranked

class Person:
    def init(self,id,name,marioKart,eatFatFight,brawl):
         self.id = int(id)
         self.name = str(name)
         self.marioKart = bool(marioKart)
         self.eatFatFight = bool(eatFatFight)
         self.brawl = bool(brawl)
    def tostr (self):
        #only used to write to file
        return f"{self.id},{self.name},{self.marioKart},{self.eatFatFight},{self.brawl}"

def register(ID,name):
    """Registers a player for ranked games
    
    Arguments:
        ID: The ID of the user
        name: the name of the user

    Returns:
        0: Seccsessful register\n
        1: Error: Already registered
    """
    list = arraylist.get()
    if(arraylist.hasID(list,ID)):
        return 1
    list.append(Person(str(ID),name,"false","false","false"))
    arraylist.save(list)
    return 0

def unrated(ID,name,game):
    """give someone an inital rating of 1500 in a game of thier choice
    
    Arguments:
        ID: ID of the person
        name: the name of the player
        game: the game they wish to join (0 for all)

    Returns:
        0: rated properly\n
        1: ERROR: is not registered\n
        2: ERROR: already rated in that game
    """
    list = arraylist.get()
    place = arraylist.index(list,ID)
    if(place == -1):
        return 1
    if(game != 0):

        if(game==1):
            if(list[place].marioKart):
                return 2
            list[place].marioKart = True
        elif(game==2):
            if(list[place].eatFatFight):
                return 2
            list[place].eatFatFight = True
        elif(game==3):
            if(list[place].brawl):
                return 2
            list[place].brawl = True

        return ranked.register(ID,name,game)
    
    #register for all the games, checking to see if any work to return the correct value
    sucsess = 0
    for i in range(1,4):
        out = ranked.register(ID,name,i)
        if(i == 0):
            sucsess += 1
        if(i == 1):
            return 1
    if(sucsess == 0):
        return 2
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
        -2: Game does not exist
    """
    return ranked.get(ID,game)

def is_registered(ID):
    """Checks if the user is registered
    
    Arguments:
        ID: The ID of the person you are searching for
    
    Returns:
        Boolean of if they are registered or not
    """
    list = arraylist.get()
    return arraylist.hasID(list,ID)

def new_day():
    """Used to change the RD of all players when a new play period is active

    Returns:
        0: Worked sucsessfully
    """
    for i in range(1,4):
        ranked.changeRD(i)
        ranked.reset(i)

def add_game(game,winner,loser,tie):
    """Adds a rated game to the game database
    
    Arguments:
        game: ID of game played
        winner: ID of winner
        loser: ID of loser
        tie: boolean if it was a tie or not
    """
    fout = open("games/"+ranked.getGame(game),"a")
    if(tie):
        fout.print(winner+","+loser+",true")
    else:
        fout.print(winner+","+loser+",false")
    fout.close()
    return 0

def game_list():
    """Gets the game list

    Returns:
        A string of games seperated by a line break    
    """
    return "Mario Kart Wii" \
    "Eat Fat Fight" \
    "Super Smash Bros Brawl"

