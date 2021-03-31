#Cooper Martin
#C463 HW3
#2/21/2021

class MagicSquare:
    def __init__(self,matrix,r,c,d):
        self.root = matrix #starting matrix
        for i in range(3): #remove row, col, and diag fields from root
            self.root.remove(self.root[len(self.root)-1])
        self.rowVals = r #row sums
        self.colVals = c #column sums
        self.diagVals = d #diagonal sums
        self.size = len(self.root) #dimension of matrix
        self.paths = [[self.root]] #list of all expanded node paths
        self.h = [[self.getSums(self.paths[0][0]),0,0]] #heuristic
        #value is a summation of difference of all rows, cols, and diags
        #first value is the h value itself
        #second value is a reference to proper index in paths array
        #third value is number of indexes processed
        self.indexes = self.getIndexes() #list of changeable indexes
        self.maxVals = self.getMaxVals() #max sums for each step, used for pruning

    def getIndexes(self):
        #return list of all indexes marked with -1
        res = [] #result
        for i in range(self.size):
            for j in range(self.size):
                if self.root[i][j] == -1:
                    res.append([i,j]) #add -1 only
        return res

    def getMaxVals(self):
        #return list of max sum achievable given number of indexes left to change
        res = [] #result
        n = 9 #max digit is 9
        for i in range(self.size):
            for j in range(self.size):
                if self.root[i][j] == -1:
                    res.append(2*n) #summed in both row and col
                    if i == j or abs(i-j) == self.size-1: #check if in diagonal position
                        if (self.size % 2 == 1 and
                            i == j and i == int(self.size/2)): #center position in both diagonals
                            res[len(res)-1] = 4*n #summed in row, col, major, and minor diag
                        else:
                            res[len(res)-1] = 3*n #summed in row, col, and one diag
        i = len(res)-2 #iterate backwards
        while i >= 0:
            res[i] = res[i] + res[i+1] #increase each position by factor of previous value
            i = i - 1
        return res

    def getSums(self,matrix):
        #calculate total summation of all rows, cols, and diags and return difference with desired sums
        vals = [[],[],[]] #lists to store rows, cols, diags respectively
        add = 0 #dumby variable used for calculations
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i][j] != -1: #do not add empty spots, they remain 0 until processed
                    add = add + matrix[i][j] #add rows
            vals[0].append(add)
            add = 0
        for i in range(self.size):
            for j in range(self.size):
                if matrix[j][i] != -1: #do not add empty spots
                    add = add + matrix[j][i] #add cols
            vals[1].append(add)
            add = 0
        for i in range(self.size):
            if matrix[i][i] != -1: #do not add empty spots
                add = add + matrix[i][i] #add major diagonal
        vals[2].append(add)
        add = 0
        for i in range(self.size):
            if matrix[i][self.size-1-i] != -1: #do not add empty spots
                add = add + matrix[i][self.size-1-i] #add minor diagonal
        vals[2].append(add)
        add = 0
        
        for i in range(self.size):
            if (self.rowVals[i]-vals[0][i] < 0 or
                self.colVals[i]-vals[1][i] < 0): #if any row/col sum is too high, result is invalid
                return -2
            add = add + (self.rowVals[i]-vals[0][i]) #add row difference
            add = add + (self.colVals[i]-vals[1][i]) #add col difference
        for i in range(2):
            if self.diagVals[i]-vals[2][i] < 0: #if any diag sum is too high, result is invalid
                return -2
            add = add + (self.diagVals[i]-vals[2][i]) #add diag difference
        return add

    def change(self,node,index,ch):
        #changes -1 index to a digit 0-9
        newNode = [] #new node to return
        for i in range(self.size):
            newNode.append([]) #make 2d array
            for j in range(self.size):
                newNode[i].append(0) #initialize with dumby values
        for i in range(self.size):
            for j in range(self.size):
                newNode[i][j] = node[i][j] #deep copy node
        newNode[index[0]][index[1]] = ch #change desired index to new value
        return newNode

    def addPath(self,path,newNode):
        #adds new path with newly expanded node into paths array
        newPath = [] #new path to return
        for i in range(len(path)):
            newPath.append(path[i]) #deep copy path
        newPath.append(newNode) #add new node to new path
        self.paths.append(newPath) #add new path to paths array

def A_Star(x):
    #A* algorithm, finds shortest path based on admissible heuristic
    while len(x.h) > 0: #continue search as long as more unique paths exist
        i = x.h[0][1] #index for current path to expand
        node = x.paths[i][len(x.paths[i])-1] #node to expand
        size = len(x.paths[i]) #length of current pat
        cnt = x.h[0][2] #count of total indexes changed
        if x.h[0][0] == 0 and cnt >= len(x.indexes): #solution has been found
            return x.paths[i][len(x.paths[i])-1] #return solution matrix
        if cnt >= len(x.indexes) or x.h[0][0] > x.maxVals[cnt]: #cnt out of range
            #or heuristic is too high, cannot find solution with indexes left available
            x.h.remove(x.h[0]) #remove this bad node
            continue #loop again
        index = x.indexes[cnt] #index to be processed
        choices = [0,1,2,3,4,5,6,7,8,9] #valid digits to change to
        newNodes, h = [], [] #stored new choice nodes and h values respectively
        for j in range(len(choices)):
            newNodes.append(x.change(node,index,choices[j])) #add new node
            h.append(x.getSums(newNodes[j])) #add new heuristic
            if h[len(h)-1] < 0: #returned heuristic was invalid
                newNodes.remove(newNodes[len(newNodes)-1]) #remove bad node
                h.remove(h[len(h)-1]) #remove bad heuristic
                break #break since choices are in numerical order, all other choices also invalid
        for j in range(len(h)):
            x.h.append([h[j],len(x.paths),cnt+1]) #store h(n), paths index, and steps respectively
            x.addPath(x.paths[i],newNodes[j]) #add new path to paths array
        x.h.remove(x.h[0]) #remove expanded path
        x.h.sort(key=lambda y:y[0]) #sort by h(n)
    return -1  #if solution is not found, return -1

def parseFile(name):
    #parse input file
    f = open(name,"r")
    size = eval(f.readline()) #matrix dimensions
    matrix = []
    for i in range(size):
        matrix.append([]) #2d array
        line = f.readline().split() #split row values into line
        for j in range(size):
            matrix[i].append(int(line[j])) #add row values individually
    for i in range(3): #end of matrix holds desired sums for rows, cols, diags respectively
        matrix.append([]) #2d array
        line = f.readline().split() #split sums into line
        for j in range(len(line)):
            matrix[i+size].append(int(line[j])) #add sums individually
    return matrix

def printSoln(path):
    #outputs solution matrix
    if path == -1:
        print("False")
        return
    print("True")
    for i in range(len(path)):
        for j in range(len(path[i])):
            print(path[i][j],end=" ")
            if j % case.size == case.size - 1:
                print()

data = parseFile("sample1.txt")
case = MagicSquare(data,data[len(data)-3],data[len(data)-2],data[len(data)-1])
path = A_Star(case)
printSoln(path)
input()

data = parseFile("sample2.txt")
case = MagicSquare(data,data[len(data)-3],data[len(data)-2],data[len(data)-1])
path = A_Star(case)
printSoln(path)
input()

data = parseFile("sample2_fail.txt")
case = MagicSquare(data,data[len(data)-3],data[len(data)-2],data[len(data)-1])
path = A_Star(case)
printSoln(path)
input()

data = parseFile("sample3.txt")
case = MagicSquare(data,data[len(data)-3],data[len(data)-2],data[len(data)-1])
path = A_Star(case)
printSoln(path)
input()

data = parseFile("sample3_fail.txt")
case = MagicSquare(data,data[len(data)-3],data[len(data)-2],data[len(data)-1])
path = A_Star(case)
printSoln(path)
input()
