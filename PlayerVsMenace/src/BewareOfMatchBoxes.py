import random
import math

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

    def move(self, n):
        if n > 0 and n < 10 and self.board[n - 1] == 0:
            n -= 1
            if self.turn == 1:
                self.board[n] = 1
                self.turn = 10
            else:
                self.board[n] = 10
                self.turn = 1

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


class Model:
    def __init__(self, alpha, beta, gamma, delta):
        self.game = Game()
        self.matchBox = dict()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
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

    def startNewGame(self):
        self.game = Game()

    def move(self, n):
        self.game.move(n)

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
            
def train(model, n = 200000):
    print('Training started')
    for i in range(n):
        
        model.startNewGame()

        modelMoveHistory = []


        if i % 2 == 0:

            playerChoices = model.getNextStates()

            playerMove = random.choice(playerChoices)

            model.move(playerMove)
        
        while not model.game.isGameOver():

            modelChoices = model.getNextStates()
            modelChoiceWeights = [model.matchBox[tuple(model.game.board)][i] for i in modelChoices]

            # mx = -math.inf
            # modelMove = None
            # for i in range(len(modelChoices)):
            #     if mx < modelChoiceWeights[i]:
            #         mx = modelChoiceWeights[i]
            #         modelMove = modelChoices[i] + 1
            
            modelMove = random.choices(modelChoices, weights = modelChoiceWeights)[0] + 1

            modelMoveHistory.append((tuple(model.game.board), modelMove - 1))

            model.move(modelMove)

            #print(str(model.game))

            if model.game.isGameOver():
                break

            playerChoices = model.getNextStates()
            playerChoiceWeights = [model.matchBox[tuple(model.game.board)][i] for i in playerChoices]
            # maxPlayerWeight = max(playerChoiceWeights)
            # playerChoiceWeights = [.9 if i == maxPlayerWeight else .1/(len(playerChoices)-1) for i in playerChoiceWeights]
            #playerMove = random.choice(playerChoices)
            playerMove = random.choices(playerChoices, weights = playerChoiceWeights)[0] + 1
            #playerMove = random.choice(playerChoices)

            model.move(playerMove)

            #print(str(model.game))

        winner = model.game.getWinner()

        if i % 2 == 0:

            for state, move in modelMoveHistory:
                #print(state, move)

                rotations = getRotations(state, move)

                for rotatedState, rotatedMove in rotations:
                    
                    if winner == 'O':
                        model.matchBox[rotatedState][rotatedMove] += model.beta
                    elif winner == 'Draw':
                        model.matchBox[rotatedState][rotatedMove] += model.delta
                    else:
                        model.matchBox[rotatedState][rotatedMove] += model.gamma
                        model.matchBox[rotatedState][rotatedMove] = max(model.alpha, model.matchBox[rotatedState][rotatedMove])

        else:

            for state, move in modelMoveHistory:
                #print(state, move)

                rotations = getRotations(state, move)

                for rotatedState, rotatedMove in rotations:
                
                    if winner == 'X':
                        model.matchBox[rotatedState][rotatedMove] += model.beta
                    elif winner == 'Draw':
                        model.matchBox[rotatedState][rotatedMove] += model.delta
                    else:
                        model.matchBox[rotatedState][rotatedMove] += model.gamma
                        model.matchBox[rotatedState][rotatedMove] = max(model.alpha, model.matchBox[rotatedState][rotatedMove])                
        
# m = Model(1000, 2, -1, 1)

# train(m)

# while True:
#     print('----Tic Tac Toe----')

#     print('(1) Player starts first\n(2) Menace starts first\n(3) Quit')

#     n = int(input())

#     m.startNewGame()

#     if n == 1:
    
#         while not m.game.isGameOver():

#             print(m.matchBox[tuple(m.game.board)])

#             print(str(m.game))
            
#             playerMove = int(input())

#             m.move(playerMove)

#             if (m.game.isGameOver()):
#                 break
            
#             print(m.matchBox[tuple(m.game.board)])

#             m.intelligentMove()

#         winner = m.game.getWinner()

#         if winner == 'Draw':
#             print('Draw')
#         elif winner == 'X':
#             print('Player Won')
#         elif winner == 'O':
#             print('Player Lost')
#         else:
#             print(winner)

#     elif n == 2:

#         while not m.game.isGameOver():

#             m.intelligentMove()

#             print(str(m.game))

#             if (m.game.isGameOver()):
#                 break
            
#             playerMove = int(input())

#             m.move(playerMove)

#         winner = m.game.getWinner()

#         if winner == 'Draw':
#             print('Draw')
#         elif winner == 'O':
#             print('Player Won')
#         elif winner == 'X':
#             print('Player Lost')
#         else:
#             print(winner)

#     else:
#         break