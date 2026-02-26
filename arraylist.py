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


def get():
    """Get the registered player list
    
    Returns:
        An arraylist of registered players
    """
    fin = open("register.csv","r")
    array = []
    #put it all into an array
    while True:
        text = fin.readline().strip()
        if text == "":
            break
        array.append(Person(text.split(",") [0],text.split(",") [1],text.split(",") [2],text.split(",") [3],text.split(",") [4]))
    fin.close()
    return array

def save(array):
    """Saves the registered player list
    
    Arguments:
        array: the arraylist of people
    """
    fout= open("register.csv","w")
    for i in range(len(array)):
        fout.write(array[i].tostr()+"\n")
    fout.close()

def hasID(array, ID):
    """Checks if a specific ID is in the arraylist
    
    Arguments:
        array: the array that wishes to be searched
        ID: the target ID to be found

    Returns:
        A Boolean if it was found or not
    """
    for i in range(len(array)):
        if(array[i].id == ID): return True
    return False

def index(array, ID):
    """Gets the index of where the ID is in the arraylist
    
    Arguments:
        array: arraylist being indexed
        ID: the id being searched for

    Returns:
        index value of arraylist or -1 if not found
    """
    for i in range(len(array)):
        if(array[i].id == ID): return i
    return -1