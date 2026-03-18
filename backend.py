import arraylist
import ranked
from objects import Person

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
    list.append(Person(str(ID),name))
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
        if(arraylist.hasID(ranked.getlist(ranked.getGame(game),"r"),ID)):
            return 2

        return ranked.register(ID,name,game)
    
    #register for all the games, checking to see if any work to return the correct value
    sucsess = 0
    for i in range(1,7):
        out = ranked.register(ID,name,i)
        if(out == 0):
            sucsess += 1
        if(out == 1):
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
    for i in range(1,6):
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
    "Super Smash Bros Brawl"\
    "Wii sports Swordfighting"\
    "Wii sports Boxing"\
    "Mario Super Sluggers"

def is_admin(ID):
    """Checks if the user is a admin
    
    Arguments:
        ID of user being checked
    
    Returns:
        Boolean if that user is an admin or not
    """
    fin = open("admin.txt","r")
    while True:
        text = fin.readline().strip()
        if(text == ""):
            fin.close()
            return False
        if(int(text) == ID):
            return True
        
def add_admin(ID):
    """Adds a user to the admin list
    
    Arguments:
        ID: the ID of the user being added
        
    Returns:
        0: User added sucsessfully
        1: WARNING: User already admin"""
    if(is_admin(ID)):
        return 1
    fout = open("admins.txt","a")
    fout.print(str(ID)+"\n")
    fout.close()
    return 0

def add_game(game,winner,loser,tie):
    """Adds a ranked game to the ranked database
    
    Arguents:
        game: ID of game played
        winner: ID of winner
        loser: ID of loser
        tie: boolean if it was a tie
        
    Returns:
        0: worked sucsessfully"""
    ranked.add_game(game,winner,loser,tie)
    return 0

def end_day():
    """Ends the day's rating period and updates everyones ratings
    
    Returns:
        0: Worked sucsessfully
    """

def get_name(ID):
    """Gets the name of a user based of their ID
    
    Arguemtns:
        ID: id of user
        
    Returns:
        name: name of user
        0: user is not registered"""
    
    list = arraylist.get()
    if(is_registered(ID)):
        for i in range(len(list)):
            if(list[i].id == ID):
                return list[i].name
    return "0"