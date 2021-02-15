#Cooper Martin
#C463 HW2 Part 1
#2/14/2021

class Cannibals:
    def __init__(self,root=(3,3,1)):
        #state representation is of starting side of river only
        self.root = root #starting positions
        self.paths = [[self.root]] #list of all expanded node paths
        self.goal = (0,0,0) #goal state, starting side is empty
        self.maxM = root[0] #number of missionaries
        self.maxC = root[1] #number of cannibals

    def addPath(self,path,node):
        #adds new path with newly expanded node into paths array
        newPath = []
        for i in range(len(path)):
            newPath.append(path[i]) #deep copy selected path into new path
        newPath.append(node) #add new node to new path
        self.paths.append(newPath) #add new path to paths array

    def isValid(self,node,i):
        #determines if new node is valid
        if (node not in self.paths[i] and node[0] >= 0 and
            node[0] <= self.maxM and node[1] >= 0 and
            node[1] <= self.maxC and node[2] >= 0 and
            node[2] <= 1 and (node[0] >= node[1] and
            (self.maxM - node[0] >= self.maxC - node[1] or
            self.maxM - node[0] == 0) or node[0] == 0 and
            (self.maxM >= self.maxC - node[1]))):
            #checks if: node is unique, number of missionaries is between 0 and maximum,
            #number of cannibals is between 0 and maximum, boat is between 0 and 1,
            #number of missionaries on either side 
            #number of missionaries on either side is either 0, maximum, or same as cannibals
            return True
        return False

def BFS(x):
    #BFS algorithm, or uniform cost search. searches every path one level at a time
    while len(x.paths) > 0: #continue search as long as more unique paths exist
        size = len(x.paths) #number of nodes at current level
        for i in range(size):
            node = x.paths[i][len(x.paths[i])-1] #node to expand
            if (node[0] == 0 and node[1] == 0): #solution has been found
                return x.paths[i] #return solution path
            boat, sign = 0, 0 #initialize with dumby values
            if node[2] == 1: #boat is moving from start side to finish side
                boat = 0 #new value
                sign = -1 #decrement
            elif node[2] == 0: #boat is moving from finish side to start side
                boat = 1 #new value
                sign = 1 #increment
            if x.isValid((node[0],node[1]+sign,boat),i): #send 1 cannibal
                x.addPath(x.paths[i],(node[0],node[1]+sign,boat))
            if x.isValid((node[0]+sign,node[1],boat),i): #send 1 missionary
                x.addPath(x.paths[i],(node[0]+sign,node[1],boat))
            if x.isValid((node[0]+sign,node[1]+sign,boat),i): #send 1 of each
                x.addPath(x.paths[i],(node[0]+sign,node[1]+sign,boat))
            if x.isValid((node[0],node[1]+2*sign,boat),i): #send 2 cannibals
                x.addPath(x.paths[i],(node[0],node[1]+2*sign,boat))
            if x.isValid((node[0]+2*sign,node[1],boat),i): #send 2 missionaries
                x.addPath(x.paths[i],(node[0]+2*sign,node[1],boat))
        for i in range(size):
            x.paths.remove(x.paths[0]) #remove expanded paths
    return [x.root] #if path is somehow not found, return root state

def printPath(path):
    #outputs solution trace and total steps taken
    out = [case.maxM,case.maxC,1]
    print("\n-------\n\nM,C,B,_______M,C,B,")
    for i in range(len(path)):
        for j in range(len(path[i])):
            print(path[i][j],end=",")
        print("_______",end="")
        for j in range(len(path[i])):
            print(out[j]-path[i][j],end=",")
        print()
    print("\n-------\n")
    print("Total steps:",len(path)-1)

#main function       
case = Cannibals((5,4,1))
path = BFS(case)
printPath(path)
