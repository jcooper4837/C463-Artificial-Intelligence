#Cooper Martin
#C463 HW4 Part 1
#3/20/2021

import random
import time

class TSP:
    def __init__(self,d,c,t):
        self.matrix = d #city cost matrix
        self.cities = c #number of citites
        self.target = t #target cost
        self.popSize = 100 #size of each population. can be changed
        self.popul = [] #array holding each population member
        self.fitness = [] #array holding each member's fitness (quality)
        self.best = 999999999 #best cost found
        self.rate = 0.1 #rate of mutations. can be changed
        self.fitRate = 8 #rate that influences fitness calculations. can be changed
        self.path = [] #array to hold the final path

    def GA(self):
        #genetic algorithm. takes random populations and breeds members based on fitness to find the best path
        indexes = []
        for i in range(self.cities):
            indexes.append(i) #get all possible indexes
        for i in range(self.popSize):
            random.shuffle(indexes) #initialize with shuffled order of indexes
            temp = [0] #city 0 is always first
            for j in range(len(indexes)):
                if indexes[j] != 0: #do not add city 0 again
                    temp.append(indexes[j])
            self.popul.append(temp) #add new route to population
            self.fitness.append(-1) #initialize fitness with dummy value
        while True: #main ga loop
            self.getFitness() #get fitness values for entire population
            if self.best == self.target: #break if target is found, else loop indefinitely
                return
            self.getNextGen() #get the next generation of routes
            
    def getFitness(self):
        #calculates fitness scores based on how close each route is to the target
        for i in range(self.popSize):
            sum1 = 0
            for j in range(self.cities): #total up costs between each city in route including back to city 0 at the end
                sum1 = sum1 + self.matrix[self.popul[i][j]][self.popul[i][(j+1)%self.cities]]
            if sum1 < self.best: #new best route has been found
                self.best = sum1
                print("New best cost:",self.best)
                print("Current best path:\n",self.popul[i])
                if self.best <= self.target: #target has been reached. ga is completed
                    self.path = self.popul[i] #update path
                    print("Target reached:",self.target)
                    return
            self.fitness[i] = 1 / (pow(sum1-self.target,self.fitRate)+1) #fitness function. fitness rate used to better prioritize closer routes
        for i in range(self.popSize):
            sum2 = 0
            for i in range(self.popSize): #total up all fitness scores
                sum2 = sum2 + self.fitness[i]
            for i in range(self.popSize): #normalize fitness scores so that summing each will add up to 100%
                self.fitness[i] = self.fitness[i] / sum2
        
    def getNextGen(self):
        #creates new members for new generation via crossover and mutation
        newPop = []
        for i in range(self.popSize):
            routeA = self.getRoute() #select 2 random members in population based on fitness score
            routeB = self.getRoute()
            newRoute = self.getCrossover(routeA,routeB) #merge 2 routes together via crossover
            newRoute = self.getMutation(newRoute) #generate random 2 swap based on mutation rate
            newPop.append(newRoute) #add new route to new population
        self.popul = newPop #overwrite old population with next generation

    def getRoute(self):
        #randomly selects a route factoring in probability given fitness scores
        index = -1
        ch = random.random() #random number between 0 and 1
        while ch > 0:
            index = index+1 #increment index
            ch = ch - self.fitness[index] #reduce ch by fitness score. bigger fitness scores break this loop more often this way
        return self.popul[index] #member chosen

    def getCrossover(self,a,b):
        #combines 2 members into 1 with shared random attributes
        cutoff = random.randint(1,len(a)) #randomly select how many genes from parent a are passed on
        newRoute = a[:cutoff]
        for i in range(len(b)):
            if b[i] not in newRoute: #add leftover genes from parent b that were not taken from parent a in same order as found in parent b
                newRoute.append(b[i])
        return newRoute #crossover complete

    def getMutation(self,newRoute):
        #randomly swaps 2 cities based on mutation rate
        for i in range(self.cities):
            ch = random.random() #random float 0-1
            if ch < self.rate: #only mutate if ch is lower than rate
                indexA = random.randint(1,len(newRoute)-1) #randomly select 2 indexes that are not city 0
                indexB = random.randint(1,len(newRoute)-1)
                if indexA == indexB: #cannot swap city with itself
                    indexB = (indexB+1)%self.cities #swap next city over in this case
                    if indexB == 0: #cannot swap with city 0, increment to index 1
                        indexB = 1
                temp = newRoute[indexA] #perform 2 swap
                newRoute[indexA] = newRoute[indexB]
                newRoute[indexB] = temp
        return newRoute #mutations complete

def parseFile(name,cities):
    f = open(name,"r")
    size = int(cities*(cities-1)/2) #number of entries in file
    matrix = [] #matrix to store city costs
    for i in range(cities):
        matrix.append([])
        for j in range(cities):
            matrix[i].append(-1) #initialize with dummy values
    for i in range(cities):
        line = f.readline().split() #read entire line at once
        for j in range(0,len(line)):
            matrix[i][j+i+1] = int(line[j]) #upper right and lower left of matrix are identically mirrored for ease in calculations
            matrix[j+i+1][i] = int(line[j])
    return matrix

def main():
    cities = 16 #number of citites
    target = 1222 #target cost to seek
    data = parseFile("tsp16.txt",cities) #get city data from file
    case = TSP(data,cities,target)
    begin = time.perf_counter() #begin timing right before genetic algorithm starts
    case.GA()
    end = time.perf_counter() #end time when ga is finished
    print("Final path:\n",case.path)
    print("Time spent searching: {:0.3f}".format(end-begin),"seconds")

main()
