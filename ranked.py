import arraylist
import math
import glicko
from objects import Rating
from objects import Game

def getlist(name):
    array = []
    fin = open(name,"r")
    #put it all into an array
    while True:
        text = fin.readline().strip()
        if text == "":
            break
        array.append(Rating(text.split(",") [0],text.split(",") [1],text.split(",") [2],text.split(",") [3],text.split(",") [4],text.split(",") [5],text.split(",") [6],text.split(",") [7]))
    fin.close()
    return array

def saveGame(list,fout):
    """Saves the updated game to a file

    Arguments:
        list: the list being saved
        fout: fout value of file being writen to
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
        return "ratings/mariokart.csv"
    elif(game==2):
        return "ratings/eatfatfight.csv"
    elif(game==3):
        return "ratings/brawl.csv"
    elif(game==4):
        return "ratings/swordFight.csv"
    elif(game==5):
        return "ratings/boxing.csv"
    elif(game==6):
        return "ratings/sluggers.csv"
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

    fin = open(getGame(game),"r")
    fin.close()
    if (fin == 2):
        return 2

    list = getlist(getGame(game))
    if(arraylist.hasID(list,ID)):
        return 1
    
    list.append(Rating(ID,name,1500,False,350,0,0,0))
    fin.close()
    fout = open(getGame(game),"w")
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
    fin.close()
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

def add_game(game,winner,loser,tie):
    """Adds a ranked game to the ranked database
    
    Arguents:
        game: ID of game played
        winner: ID of winner
        loser: ID of loser
        tie: boolean if it was a tie
        
    Returns:
        0: worked sucsessfully"""
    name = getGame(game).split("/")[1]
    name = f"games/{name}"
    fout = open(name,"a")
    fout.write(f"{winner},{loser},{tie}\n")
    fout.close()
    return 0

def get_matches(game):
    """Gets the matches for a game and puts them in an object arraylist
    
    Arguments:
        game: ID of game
        
    returns:
        Array list of matches"""
    name = getGame(game).split("/")[1]
    name = f"games/{name}"
    array = []
    fin = open(name,"r")
    fout = open(f"log/{name}","a")
    fout.write("\n")
    #put it all into an array
    while True:
        text = fin.readline().strip()
        if text == "":
            break
        fout.write(text+"\n")
        array.append(Game(text.split(",") [0],text.split(",") [1],text.split(",") [2]))
    fin.close()
    fout.close()
    return array


def update_ratings(game):
    """updates the ratings for the given game
    
    Arguemnts:
        game: ID of game
        
    Returns:
        0: task sucsessful"""

    
    game_list = get_matches(game)
    player_list = getlist(game)

    for i in range(len(game_list)):

        #pull the winer and lser of the current match
        winner = arraylist.index(player_list,game_list[i].winner)
        loser = arraylist.index(player_list,game_list[i].loser)

        #Calculate the two players gRD though could probably just do this for everyone elsewhere to prevent repeat
        player_list[winner].gRD = glicko.gRD(player_list[winner].RD)
        player_list[loser].gRD = glicko.gRD(player_list[loser].RD)

        #Pull Es values because we are going to be using them a few times
        Es_winner = glicko.Es(player_list[loser].gRD,player_list[winner].rating,player_list[loser].rating)
        Es_loser = glicko.Es(player_list[loser].gRD,player_list[winner].rating,player_list[loser].rating)

        #Add the values to d2 (not yet multiplied by q2)
        player_list[winner].d2sum += player_list[loser].gRD**2 * Es_winner * (1-Es_winner)
        player_list[winner].d2sum += player_list[loser].gRD**2 * Es_loser * (1-Es_loser)

        #add the values to the scoresum (also here is where draws come into accout)
        if(game_list[i].tie):
            player_list[winner].scoresum += player_list[loser].gRD * (.5-Es_winner)
            player_list[loser].scoresum += player_list[winner].gRD * (.5-Es_loser)
            player_list[winner].ties += 1
            player_list[loser].ties += 1
        else:
            player_list[winner].scoresum += player_list[loser].gRD * (1-Es_winner)
            player_list[loser].scoresum += player_list[winner].gRD * (0-Es_loser)
            player_list[winner].wins += 1
            player_list[loser].loses += 1
        

    #Update each players r and RD (Also make sure to skip users who didn't play to avoid division by 0)
    for i in range(len(player_list)):
        if(player_list[i].d2sum != 0):
            #first, multiply d2 by q2
            player_list[i].d2sum *= glicko.q()**2

            #Update their rating
            player_list[i].rating += (glicko.q()*player_list[i].scoresum/((1/player_list[i].RD**2)+(1/player_list[i].d2sum)))
            
            #Finally, update their RD
            player_list[i].RD = math.sqrt(1/((1/player_list[i].RD**2)+(1/player_list[i].d2sum)))

    #clear game log
    name = getGame(game).split("/")[1]
    fout = open(f"games/{name}","w")
    fout.close()

    fout = open(f"ratings/{name}","w")
    saveGame(player_list,fout)
    fout.close()