import PySimpleGUI as menace
import BewareOfMatchBoxes as code

layout = [[menace.Text("Hello, Welcome To Menace World")]
        ]
margins=(500, 500)

GAME_BOARD_LAYOUT = [[menace.Text("Select the game mode and then start playing")],[menace.Button("Player First", key="pf")],
[menace.Button("Menace First", key="mf")]]

GAME_BOARD_LAYOUT += [[menace.Button(' ', size=(8, 4), key=str((3*j)+i+1))
                            for i in range(3)] for j in range(3)]

GAME_BOARD_LAYOUT += [[menace.Button("Reset Game", key="-RESET-", tooltip='Resets the current session.')]]

layout += GAME_BOARD_LAYOUT

ready = menace.popup_ok('Please wait')

m = code.Model(1000, 2, -1, 1)

code.train(m) 

ready = menace.popup_ok('Matchboxes are trained and ready to challenge you. Are you ready? Select the game mode')

window = menace.Window('Menace Home',layout,margins)

while True:


    m.startNewGame()
    event, values = window.Read()
    if event == 'pf':
        while not m.game.isGameOver():
            print(str(m.game))
            event, values = window.Read()
            
            window.Element(event).update("X")
            m.move(int(event))
            
            if m.game.isGameOver():
                break
            print(m.matchBox[tuple(m.game.board)])
            window.Element(str(m.intelligentMove())).update("O")
        

        winner = m.game.getWinner()
        if winner == 'Draw':
            menace.popup_ok('Draw')
        elif winner == 'X':
            menace.popup_ok('Player Won')
        elif winner == 'O':
            menace.popup_ok('Player Lost')
        else:
            menace.popup(str(winner))
        
    


    elif event == 'mf':
        while not m.game.isGameOver():
            print(m.matchBox[tuple(m.game.board)])
            window.Element(str(m.intelligentMove())).update("O")
            if m.game.isGameOver():
                    break
            event, values = window.Read()    
            
            window.Element(event).update("X")
            m.move(int(event))

        winner = m.game.getWinner()
        if winner == 'Draw':
            menace.popup_ok('Draw')
        elif winner == 'O':
            menace.popup_ok('Player Won')
        elif winner == 'X':
            menace.popup_ok('Player Lost')
        else:
            menace.popup(str(winner))
   

    elif event == '-RESET-':
        for e in range(1,10):
            window.Element(str(e)).update(" ")
        m.startNewGame()
        menace.popup_ok('Select the game mode') 
 
    elif event == menace.WIN_CLOSED:
        break

    else:
        menace.popup_ok('Select the game mode') 
            


window.Close()            
