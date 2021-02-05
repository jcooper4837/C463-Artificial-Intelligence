#Cooper Martin
#C463 HW1
#2/4/2021

import random

class Concentration:
    def __init__(self, st):
        self.board = ['X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X'] #board with cards flipped, visible to agent
        self.actual = self.randomizeCards() #actual card values, not visible to agent
        self.choices = [0,1,2,3,4,5,6,7,
                        8,9,10,11,12,13,14,15,
                        16,17,18,19,20,21,22,23,
                        24,25,26,27,28,29,30,31] #cards agent can choose from
        self.hasState = st #boolean to distinguish agent with and without memory
        self.memory = ['X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X',
                      'X','X','X','X','X','X','X','X'] #values that agent can remember from previous flips
        self.memorized = False #boolean to represent if entire board is memorized
        self.steps = 0 #number of turns played in game
        self.complete = False #game is finished
        if st:
            print("\nConcentration Game using smart agent start\n")
        else:
            print("\nConcentration Game using dumb agent start\n")
        
    def action(self):
        #calls appropriate function based on type of agent
        if self.hasState:
            self.smartAction()
        else:
            self.dumbAction()
            
    def dumbAction(self):
        #action taken if agent has no memory state
        print("--------------------\nBegin turn",self.steps+1)
        random.shuffle(self.choices) #values are unknown, so choice of cards are randomized
        cards = [self.choices[0],self.choices[1]] #draw 2 random cards from the board
        print("Flipping cards",cards[0]+1,"and",cards[1]+1)
        self.board[cards[0]] = self.actual[cards[0]] #cards are flipped, values are now visible
        self.board[cards[1]] = self.actual[cards[1]]
        print("1st Card Value:",self.board[cards[0]])
        print("2nd Card Value:",self.board[cards[1]])
        print("Current Board:\n",self.board)
        
        if self.board[cards[0]] != self.board[cards[1]]:
            #if cards are not equal value, flip cards back over
            self.board[cards[0]] = 'X'
            self.board[cards[1]] = 'X'
            print("No match! Flipping cards back over")
        else:
            #match is found, remove chosen cards from choices array
            self.choices.remove(cards[0])
            self.choices.remove(cards[1])
            print("Match found! Cards remain flipped")
            
        self.steps = self.steps + 1 #increment turn counter
        print("End turn",self.steps)

        if len(self.choices) == 0:
            #if no more cards to choose from, game is finished
            self.complete = True
            print("--------------------\nGame complete!\nTotal Turns:",self.steps)
            print("Final board:\n",self.board)
        
    def smartAction(self):
        #action taken if agent does have memory state
        print("--------------------\nBegin turn",self.steps+1)
        if not self.memorized:
            #path taken if there are still cards with value unknown to the agent
            random.shuffle(self.choices) #randomize choices of cards with unknown values
            cards = [self.choices[0],-1] #draw 1 card
            print("Flipping card",cards[0]+1)
            self.board[cards[0]] = self.actual[cards[0]] #card is flipped, value is now visible
            print("1st Card Value:",self.board[cards[0]])
            
            if self.board[cards[0]] in self.memory:
                #if value on card has been seen before, flip that card again to find match
                cards[1] = self.memory.index(self.board[cards[0]]) #find other matching card in memory and flip that card
                self.choices.remove(cards[0]) #remove known card from choices array. other card was already known, so only 1 removal needed
                print("Value",self.board[cards[0]],"found in memory!")
            else:
                #value on card has never been seen, choose second card randomly from unknown choices
                cards[1] = self.choices[1]
                self.choices.remove(cards[0]) #remove known cards from choices array
                self.choices.remove(cards[1])
                print("Value",self.board[cards[0]],"is not in memory")

            print("Flipping card",cards[1]+1)
            self.board[cards[1]] = self.actual[cards[1]] #card is flipped, value is now known
            print("2nd Card Value:",self.board[cards[1]])
            self.memory[cards[0]] = self.actual[cards[0]] #record values into state memory
            self.memory[cards[1]] = self.actual[cards[1]]
            print("Current Board:\n",self.board)
            print("Current Memory:\n",self.memory)
            
            if self.board[cards[0]] != self.board[cards[1]]:
                #if cards are not equal value, flip cards back over
                self.board[cards[0]] = 'X'
                self.board[cards[1]] = 'X'
                print("No match! Flipping cards back over")
            else:
                print("Match found! Cards remain flipped")
                
            if len(self.choices) == 0:
                #all card values are now known. for remaining matches, iterate through all unflipped cards and add to choices array
                for i in range(32):
                    if self.board[i] == 'X':
                        self.choices.append(i)
                        
                self.memorized = True #entire board has been memorized
                print("Board has been fully memorized")
                if len(self.choices) == 0:
                    #if no more cards to choose from, game is finished
                    #this if is unlikely to ever be visited, requires all matches before full memorization
                    self.complete = True
                    print("--------------------\nGame complete!\nTotal Turns:",self.steps+1)
                    print("Final board:\n",self.board)
                
            print("End turn",self.steps+1)
        else:
            #path taken when entire board is known, including unflipped cards
            print(self.choices)
            cards = [self.choices[0],self.memory.index(self.memory[self.choices[0]],self.choices[0]+1)] #flip first choice
                #flip other card by finding the second occurence of a card that holds the same value as the first card
            print("Flipping cards",cards[0]+1,"and",cards[1]+1)
            self.board[cards[0]] = self.actual[cards[0]] #cards are flipped, values are now visible and are a match
            self.board[cards[1]] = self.actual[cards[1]]
            print("1st Card Value:",self.board[cards[0]])
            print("2nd Card Value:",self.board[cards[1]])
            print("Current Board:\n",self.board)
            self.choices.remove(cards[0]) #remove matched cards from choice array
            self.choices.remove(cards[1])
            print("End turn",self.steps+1)
            
            if len(self.choices) == 0:
                #if no more cards to choose from, game is finished
                self.complete = True
                print("--------------------\nGame complete!\nTotal Turns:",self.steps+1)
                print("Final board:\n",self.board)
                
        self.steps = self.steps + 1 #increment turn counter
        
    def randomizeCards(self):
        #returns a shuffled board with all possible values inserted
        array = ['0','0','1','1','2','2','3','3',
                 '4','4','5','5','6','6','7','7',
                 '8','8','9','9','A','A','B','B',
                 'C','C','D','D','E','E','F','F'] #16 pairs of values
        random.shuffle(array)
        return array

#main function
dumbGame = Concentration(False) #initialize dumb agent, has no memory state
while not dumbGame.complete:
    dumbGame.action() #perform action until game is complete
print("\n\n\n")
smartGame = Concentration(True) #initialize smart agent, does have memory state
while not smartGame.complete:
    smartGame.action() #perform action until game is complete
