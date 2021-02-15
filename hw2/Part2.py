#Cooper Martin
#C463 HW2 Part 2
#2/14/2021

class N_Puzzle:
    def __init__(self,m,s=3,r=[4,2,5,1,0,6,3,8,7]):
        self.root = r #starting puzzle
        self.paths = [[self.root]] #list of all expanded node paths
        self.n = s #size of puzzle, supports 3x3 and 4x4
        if self.n == 3: #8 puzzle
            self.goal = [1,2,3,4,5,6,7,8,0]
        elif self.n == 4: #15 puzzle
            self.goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        self.mode = m #mode determines which heuristic to us
        if self.mode == 0: #Manhattan distance
            print("Algorithm 1: Total Manhattan distance")
            self.h = [[self.calcMann(self.root),0,0]] #heuristic value
            #first value is heuristic + total steps, or f(n)
            #second value is a reference to proper index in paths array
            #third value is only heuristic
        elif self.mode == 1: #out of place tiles
            print("Algorithm 2: Number of tiles out of place")
            self.h = [[self.calcDisp(self.root),0,0]]
        elif self.mode == 2: #Manhattan distance + linear conflict
            print("Algorithm 3: Manhattan distance + Linear conflict")
            self.h = [[self.calcLinear(self.root),0,0]]
        elif self.mode == 3: #regular BFS
            print("Algorithm 4: Uniform cost search, regular BFS")
            self.h = [[0,0,0]]
        self.steps = 99999999 #minimum steps to find solution

    def calcMann(self,node):
        #calculates heuristic for Manhattan distance
        matrix = [] #create a 2d representation to simplify logic
        if self.n == 3: #3x3
            matrix = [[0,0,0],[0,0,0],[0,0,0]]
        elif self.n == 4: #4x4
            matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        k = 0
        h = 0 #heuristic
        for i in range(self.n):
            for j in range(self.n):
                matrix[i][j] = node[k]
                k = k + 1
                if matrix[i][j] != 0: #calculate distance for every tile minus blank space
                    h = h + abs(i - int((matrix[i][j]-1) / self.n)) + abs(j - (matrix[i][j]-1) % self.n)
        return h #total distance

    def calcDisp(self,node):
        #calculates heuristic for out of place tiles
        h = 0 #heuristic
        for i in range(self.n*self.n-1):
            if node[i] != i+1: #tile is out of place
                h = h + 1
        return h #total out of place

    def calcLinear(self,node):
        #calculates heuristic for linear conflict
        h = self.calcMann(node) #initialize heuristic with Manhattan distance
        p = [] #create a 2d representation of all rows & cols to simplify logic
        if self.n == 3:
            p = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]
        elif self.n == 4:
            p = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
        for i in range(len(p)):
            values, conflict = [], [] #stores all values and potential conflicts respectively
            for j in range(len(p[i])):
                values.append(node[p[i][j]]) #get all values in row/col
                conflict.append(-1) #load dumby values into conflict matrix
            for j in range(len(values)):
                if p[i][j]+1 in values: #potential conflict value exists
                    conflict[values.index(p[i][j]+1)] = p[i][j]+1 #add value into proper index to maintain order
            while -1 in conflict:
                conflict.remove(conflict[conflict.index(-1)]) #remove dumby values
            for j in range(len(conflict)-1):
                if conflict[j] > conflict[j+1]: #values are out of order
                    h = h + 2 #minimum 2 moves to fix
        return h #total conflicts * 2

    def getChoices(self,node,index):
        #finds all valid choices for moving tile up, down, left, right
        res = []
        if index >= self.n: #tile can move up
            res.append(index-self.n)
        if index < self.n*(self.n-1): #tile can move down
            res.append(index+self.n)
        if index % self.n != 0: #tile can move left
            res.append(index-1)
        if index % self.n != self.n-1: #tile can move right
            res.append(index+1)
        return res #return all options

    def swap(self,node,index,ch):
        #swaps blank space with desired adjacent tile
        newNode = []
        for i in range(self.n*self.n):
            newNode.append(0) #initialize new node with dumby values
        for i in range(len(node)):
            newNode[i] = node[i] #deep copy old node into new node
        newNode[index] = newNode[ch] #blank is now adjacent tile
        newNode[ch] = 0 #old adjacent tile is now blank
        return newNode
        
    def addPath(self,path,newNode,index,ch):
        #adds new path with newly expanded node into paths array
        newPath = []
        for i in range(len(path)):
            newPath.append(path[i]) #deep copy selected path into new path
        if newNode not in newPath: #path is only created if expanded node is unique in said path
            newPath.append(newNode) #add new node to new path
            self.paths.append(newPath) #add new path to paths array

def A_Star(x):
    #A* algorithm, finds shortest path based on admissible heuristic
    if x.mode == 3: #save time by using smaller function for BFS as heuristic is not used
        return BFS(x)
    while len(x.h) > 0: #continue search as long as more unique paths exist
        i = x.h[0][1] #index for current path to expand
        node = x.paths[i][len(x.paths[i])-1] #node to expand
        size = len(x.paths[i]) #length of current path
        if (node == x.goal): #solution has been found
            return x.paths[i] #return solution path
        index = node.index(0) #index of blank space
        choices = x.getChoices(node,index) #valid tiles adjacent to blank
        newNodes, h, bad = [], [], [] #stores new choice nodes, h values, and non unique indexes respectively
        for j in range(len(choices)):
            newNodes.append(x.swap(node,index,choices[j])) #add new node
            if newNodes[j] not in x.paths[i]: #new node is unique in path
                if x.mode == 0: #calculate based on heuristic function
                    h.append(x.calcMann(newNodes[j]))
                elif x.mode == 1:
                    h.append(x.calcDisp(newNodes[j]))
                elif x.mode == 2:
                    h.append(x.calcLinear(newNodes[j]))
                elif x.mode == 3:
                    h.append(0)
            else: #new node is not unique and needs to be removed
                bad.append(j-len(bad))
        for j in range(len(bad)):
            newNodes.remove(newNodes[bad[j]]) #remove non unique node
            choices.remove(choices[bad[j]]) #remove non unique choice
        for j in range(len(choices)):
            x.h.append([h[j]+size,len(x.paths),h[j]]) #store f(n), paths index, and h(n) respectively
            x.addPath(x.paths[i],newNodes[j],index,choices[j]) #add new path to paths array
        x.h.remove(x.h[0]) #remove expanded path
        x.h.sort(key=lambda y:y[0]) #sort by f(n)
    return [x.root] #if path is somehow not found, return root state
        
def BFS(x):
    #BFS algorithm, or uniform cost search. searches every path one level at a time
    while len(x.paths) > 0: #continue search as long as more unique paths exist
        size = len(x.paths) #number of nodes at current level
        for i in range(size):
            node = x.paths[i][len(x.paths[i])-1] #node to expand
            if (node == x.goal): #solution has been found
                return x.paths[i] #return solution path
            index = node.index(0) #index of blank space
            choices = x.getChoices(node,index) #valid tiles adjacent to blank
            for j in range(len(choices)):
                newNode = x.swap(node,index,choices[j]) #create new node for each valid choice
                x.addPath(x.paths[i],newNode,index,choices[j]) #add new path to paths array
        for i in range(size):
            x.paths.remove(x.paths[0]) #remove expanded paths
    return [x.root] #if path is somehow not found, return root state

def printPath(path):
    #outputs solution trace and total steps taken
    print("\n-------\n")
    for i in range(len(path)):
        for j in range(len(path[i])):
            print(path[i][j],end=",")
            if j % case.n == case.n - 1:
                print()
        print("\n-------\n")
    print("Total steps:",len(path)-1)
    print("\n-------\n")

#main function
case = N_Puzzle(0)
path1 = A_Star(case)
printPath(path1)
input()

case = N_Puzzle(1)
path2 = A_Star(case)
printPath(path2)
input()

case = N_Puzzle(2)
path3 = A_Star(case)
printPath(path3)
input()

case = N_Puzzle(3)
path4 = A_Star(case)
printPath(path4)

#Various test cases used
#[1,2,5,3,0,6,7,4,8]
#[8,4,5,3,0,1,7,2,6]
#[2,3,5,1,8,4,0,7,6]
#[4,2,5,1,0,6,3,8,7]
#[7,1,3,6,4,5,0,2,8]
#[1,2,3,4,5,6,7,8,9,10,0,15,13,14,12,11]
#[2,6,1,4,0,7,3,8,5,9,10,15,13,14,12,11]
