import random
import math
import PySimpleGUI as training
import logging
import time

logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s", filemode="w")
                     
############## UI Layout Design for the Menace starts ##################################################

layout = [[training.Text("Hello, Welcome To Menace World")]]
margins=(500, 500)

GAME_BOARD_LAYOUT = [[training.Button('Start Training',size=(10,2),key='train')]]
GAME_BOARD_LAYOUT += [[training.Button(' ', size=(8, 4), key=str((3*j)+i+1))
                            for i in range(3)] for j in range(3)]

GAME_BOARD_LAYOUT += [[training.Text("Menace Wins")],[training.Button('',size=(8,2),key='won')]]
GAME_BOARD_LAYOUT += [[training.Text("Menace Loses")],[training.Button('',size=(8,2),key='lost')]]
GAME_BOARD_LAYOUT += [[training.Text("Draws")],[training.Button('',size=(8,2),key='draw')]]

layout += GAME_BOARD_LAYOUT

window = training.Window('Menace Home',layout,margins)



############## UI Layout Design for the Menace ends ##################################################


class Game:

    # 0 -> Position Empty; 1 -> X; 10-> O
    def __init__(self):
        self.board = [0] * 9
        self.turn = 1
    
    def getRowSum(self, n):
        n = (n - 1) * 3 
        sm = 0
        for i in range(n, n+3):
            sm += self.board[i]
        return sm
    
    def getColSum(self, n):
        n -= 1
        sm = 0
        while n < 9:
            sm += self.board[n]
            n += 3
        return sm

    def getDiagSumTB(self):
        board = self.board
        return board[0] + board[4] + board[8]

    def getDiagSumBT(self):
        board = self.board
        return board[2] + board[4] + board[6]
            
################################ Game Over method ###############################
    def isGameOver(self):

        for i in range(1, 4):
            x = self.getRowSum(i)
            y = self.getColSum(i)
            if x == 3 or x == 30 or y == 3 or y == 30:
                return True

        diagTB = self.getDiagSumTB()
        diagBT = self.getDiagSumBT()

        if diagTB == 3 or diagTB == 30 or diagBT == 3 or diagBT == 30:
            return True
        
        allFilled = True
        for i in range(9):
            if self.board[i] == 0:
                allFilled = False
    
        return allFilled
######################################################################################

################################ Method to get the winner (returns X or O) ################################  
    def getWinner(self):
        if self.isGameOver():
            for i in range(1, 4):
                x = self.getRowSum(i)
                y = self.getColSum(i)
                if x == 3 or y == 3:
                    return 'X'
                elif x == 30 or y == 30:
                    return 'O'
            if self.getDiagSumBT() == 3 or self.getDiagSumTB() == 3:
                return 'X'
            if self.getDiagSumBT() == 30 or self.getDiagSumTB() == 30:
                return 'O'
            return 'Draw'
        else:
            return 'Not Over Yet'
################################################################################################

############## Move method ##############
    def move(self, n):
        if n > 0 and n < 10 and self.board[n - 1] == 0:
            n -= 1
            if self.turn == 1:
                self.board[n] = 1
                self.turn = 10
            else:
                self.board[n] = 10
                self.turn = 1
#############################################################

############## To String the Game (For Console)##############
    def __str__(self):
        s = ''
        n = 0
        board = self.board
        for i in range(3):
            for j in range(3):
                if board[n] == 1:
                    s += 'X'
                elif board[n] == 10:
                    s += 'O'
                else:
                    s += ' '
                if j != 2:
                    s += '|'
                n += 1
            if i != 2:
                s += '\n-----\n'
        return s+'\n'
#################################################################################


############################ Designing a menace Model############################
class Model:
    def __init__(self, alpha, beta, gamma, delta):
        self.game = Game()
        self.matchBox = dict()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.trainWins=0
        self.trainLoses=0
        self.trainDraws=0
        self.initializeMatchBox()

    def initializeMatchBox(self):
        q = [[[0, 0, 0, 0, 0, 0, 0, 0, 0], 1]]
        while len(q) != 0:
            u, turn = q.pop()
            if tuple(u) not in self.matchBox:
                self.matchBox[tuple(u)] = dict()
            vAll = self.getNextStates(u, turn)
            for v in vAll:
                boardCopy = u[:]
                boardCopy[v] = turn
                q.append([boardCopy, 1 if turn == 10 else 10])
                self.matchBox[tuple(u)][v] = self.alpha
            


############## Method to find out all possible next states for each state of the game ##############
   
    def getNextStates(self, board = None, turn = None):
        if board == None:
            board = self.game.board
        if turn == None:
            turn = self.game.turn
        nextStates = []
        for i in range(9):
            if board[i] == 0:
                nextStates.append(i)
        return nextStates

############## Start new Game ##############
    def startNewGame(self):
        self.game = Game()

    
    def move(self, n):
        self.game.move(n)

############################ Intelligent Move Method after the Menace is completely trained############################
    
    def intelligentMove(self):
        currentState = tuple(self.game.board)
        nextStates = self.getNextStates()
        nextStateWeights = [self.matchBox[currentState][i] for i in nextStates]
        move = None
        mx = -math.inf
        for i in nextStates:
            if mx <  self.matchBox[currentState][i]:
                mx = self.matchBox[currentState][i]
                move = i
        print(move)
        self.move(move + 1)
        return move + 1


############## Rotations method To handle the symmetry of the game board ############################
def getRotations(board, move):
    rotations = [[0,1,2,3,4,5,6,7,8],
    [0,3,6,1,4,7,2,5,8],
    [6,3,0,7,4,1,8,5,2],
    [6,7,8,3,4,5,0,1,2],
    [8,7,6,5,4,3,2,1,0],
    [8,5,2,7,4,1,6,3,0],
    [2,5,8,1,4,7,0,3,6],
    [2,1,0,5,4,3,8,7,6]]

    ret = []

    for rotation in rotations:
        x = [0] * 9
        newMove = None
        for r in range(len(rotation)):
            x[r] = board[rotation[r]]
            if rotation[r] == move:
                newMove = r
        ret.append((tuple(x), newMove))

    return ret

 
############## METHOD TO TRAIN THE MENACE MODEL AGAINST HUMAN STRATEGY ##############            
def train(model, n = 10):
    print('Training started')

    for i in range(n):
        time.sleep(0.1)
        model.startNewGame()
        
        for e in range(1,10):
            window.Element(str(e)).update(" ")
        window.Refresh()    
        
        modelMoveHistory = []
        turn = 'X'

        if i % 2 == 0:
            playerChoices = model.getNextStates()
            playerMove = random.choice(playerChoices) + 1
            
            model.move(playerMove)
            if i>n-3:
                logging.debug('Last Training Game moves %s', playerMove)
            time.sleep(0.1)    
            window.Element(str(playerMove)).update(turn)
            window.Refresh()
            time.sleep(0.1)
            turn = 'X' if turn == 'O' else 'O'
        

        while not model.game.isGameOver():

            modelChoices = model.getNextStates()
            modelChoiceWeights = [model.matchBox[tuple(model.game.board)][i] for i in modelChoices]
            modelMove = random.choices(modelChoices, weights = modelChoiceWeights)[0] + 1
            modelMoveHistory.append((tuple(model.game.board), modelMove - 1))
            model.move(modelMove)
            if i>n-3:
                logging.debug('MatchBox: ' + str(m.matchBox[tuple(m.game.board)]))
                logging.debug('Last Training Game moves %s',modelMove)
            
            window.Element(str(modelMove)).update(turn)
            window.Refresh()
            
            time.sleep(0.1)
            turn = 'X' if turn == 'O' else 'O'



            if model.game.isGameOver():
                break

            playerChoices = model.getNextStates()
            playerChoiceWeights = [model.matchBox[tuple(model.game.board)][i] for i in playerChoices]
            
            ####### Chooses the best move in 90% probability and other moves in remaining 10% ####
            maxPlayerWeight = max(playerChoiceWeights) 
            playerChoiceWeights = [.9 if i == maxPlayerWeight else .1/(len(playerChoices)-1) for i in playerChoiceWeights]
            playerMove = random.choices(playerChoices, weights = playerChoiceWeights)[0] + 1
            #playerMove = random.choice(playerChoices)

            model.move(playerMove)
            
            if i > n-3:
                logging.debug( 'Last Training Game moves %s' ,playerMove)
            window.Element(str(playerMove)).update(turn)
            window.Refresh()
            time.sleep(0.1)
            turn = 'X' if turn == 'O' else 'O'
            

        winner = model.game.getWinner()
        

        logging.debug('Training round %s : %s is the winner - Menace Wins : %s  Menace Loses : %s Draws :%s',i, winner, str(model.trainWins),str(model.trainLoses),str(model.trainDraws))
          

        if i % 2 == 0:
            if winner == 'O':
                model.trainWins+=1
            elif winner == 'Draw':
                model.trainDraws+=1
            else:
                model.trainLoses+=1
                
            for state, move in modelMoveHistory:
                rotations = getRotations(state, move)
                for rotatedState, rotatedMove in rotations:
                    
                    if winner == 'O':
                        model.matchBox[rotatedState][rotatedMove] += model.beta
                        window.Element('won').update(model.trainWins)
                        window.Refresh()
                        
                    elif winner == 'Draw':
                        model.matchBox[rotatedState][rotatedMove] += model.delta
                        window.Element('draw').update(model.trainDraws)
                        window.Refresh()
                        
                    else:
                        model.matchBox[rotatedState][rotatedMove] += model.gamma
                        model.matchBox[rotatedState][rotatedMove] = max(model.alpha, model.matchBox[rotatedState][rotatedMove])
                        window.Element('lost').update(model.trainLoses)
                        window.Refresh()
                        # 

        else:
            if winner == 'X':
               model.trainWins+=1
            elif winner == 'Draw':
                model.trainDraws+=1
            else:
                model.trainLoses+=1    
                      

            for state, move in modelMoveHistory:
                rotations = getRotations(state, move)
                for rotatedState, rotatedMove in rotations:
                
                    if winner == 'X':
                        model.matchBox[rotatedState][rotatedMove] += model.beta
                        window.Element('won').update(model.trainWins)
                        window.Refresh()
                        
                    elif winner == 'Draw':
                        model.matchBox[rotatedState][rotatedMove] += model.delta
                        window.Element('draw').update(model.trainDraws)
                        window.Refresh()
                        
                    else:
                        model.matchBox[rotatedState][rotatedMove] += model.gamma
                        model.matchBox[rotatedState][rotatedMove] = max(model.alpha, model.matchBox[rotatedState][rotatedMove])  
                        window.Element('lost').update(model.trainLoses)  
                        window.Refresh()      
                        
    print('Training Ended')


m = Model(1000, 2, -1, 1)
def startTraining():
    while True :  
        event, values = window.Read()

        
        if event == 'train':
            train(m, 100) 
            trained = True   
            
        elif event == training.WIN_CLOSED:
            break

    window.Close()                                                                                                                                
                   



       
