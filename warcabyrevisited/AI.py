import GUI
import engine


def save_move():
    if(engine.IsEvenCapture == False):
        engine.GLOBALstateOfTheGameList1 = engine.stateOfTheGameListCapture
        engine.GLOBALstateOfThePreviousMove = engine.GLOBALstateOfTheGameList2
    else:
        engine.GLOBALstateOfTheGameList2 = engine.stateOfTheGameListCapture
        engine.GLOBALstateOfThePreviousMove = engine.GLOBALstateOfTheGameList1

    engine.IsEvenCapture = not engine.IsEvenCapture

    if(engine.firstSavesOfTheDay==0):
        engine.IsPlayer1 = not engine.IsPlayer1
    else:
        engine.firstSavesOfTheDay -= 1
        print(engine.firstSavesOfTheDay)

    GUI.setLabel("Status", "white", "")

    if (engine.firstSavesOfTheDay == 1) or (not engine.IsPlayer1):
        GUI.setLabel("Player", "red", "Czerwony")
    else:
        GUI.setLabel("Player", "green", "Zielony")


    print(engine.GLOBALstateOfTheGameList1)
    print(engine.GLOBALstateOfTheGameList2)
    return

def rollback():
    if(engine.IsEvenCapture == False):
        engine.GLOBALstateOfTheGameList1 = engine.GLOBALstateOfThePreviousMove
    else:
        engine.GLOBALstateOfTheGameList2 = engine.GLOBALstateOfThePreviousMove
    engine.IsPlayer1 = not engine.IsPlayer1
    engine.IsEvenCapture = not engine.IsEvenCapture

    if (engine.firstSavesOfTheDay == 1) or (not engine.IsPlayer1):
        GUI.setLabel("Player", "red", "Czerwony")
    else:
        GUI.setLabel("Player", "green", "Zielony")
    return

def legal_moves(x, y):
    blinds = blind_legal_moves(x, y)
    legal_moves = []

    if engine.hop == False:
        for move in blinds:
            if (engine.IsPlayer1 == True):
                if engine.IsEvenCapture==False:
                    if engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 1 and engine.GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 1 and engine.GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
            else:
                if engine.IsEvenCapture==False:
                    if engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 3 and engine.GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 3 and engine.GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

    else:  # engine.hop == True
        for move in blinds:
            if (engine.IsPlayer1 == True):
                if engine.IsEvenCapture==False:
                    if (engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 1 and engine.GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if (engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 1 and engine.GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
            else:
                if engine.IsEvenCapture==False:
                    if (engine.GLOBALstateOfTheGameList1[move[0]][move[1]] == 3 and engine.GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if (engine.GLOBALstateOfTheGameList2[move[0]][move[1]] == 3 and engine.GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

    return legal_moves


def check_move():
    amountOfChanges = 0
    for x in range(0, 8):
        if (engine.GLOBALstateOfTheGameList1[x] != engine.GLOBALstateOfTheGameList2[x]):
            for y in range(0, 8):
                if (engine.GLOBALstateOfTheGameList1[x][y] != engine.GLOBALstateOfTheGameList2[x][y]):
                    amountOfChanges=amountOfChanges+1
                    if(engine.GLOBALstateOfTheGameList1[x][y]!=0 and engine.IsEvenCapture == False):
                        PosistionOfChangedX=x
                        PosistionOfChangedY=y
                    elif (engine.GLOBALstateOfTheGameList2[x][y] != 0 and engine.IsEvenCapture == True):
                        PosistionOfChangedX = x
                        PosistionOfChangedY = y

    if(amountOfChanges<4):
        legals=legal_moves(PosistionOfChangedX,PosistionOfChangedY)
        for x in range(0, 8):
            if (engine.GLOBALstateOfTheGameList1[x] != engine.GLOBALstateOfTheGameList2[x]):
                for y in range(0, 8):
                    if (engine.GLOBALstateOfTheGameList1[x][y] != engine.GLOBALstateOfTheGameList2[x][y]):
                        if (engine.GLOBALstateOfTheGameList1[x][y] == 0 and engine.IsEvenCapture == False):
                            PosistionOfChangedX = x
                            PosistionOfChangedY = y
                        elif (engine.GLOBALstateOfTheGameList2[x][y] == 0 and engine.IsEvenCapture == True):
                            PosistionOfChangedX = x
                            PosistionOfChangedY = y
        IsCorrect=False
        for move in legals:
            if(move[0]==PosistionOfChangedX and move[1]==PosistionOfChangedY):
                IsCorrect=True

        if(amountOfChanges==3 and engine.IsPlayer1==True):
            PosistionOfGreenX=-1
            PosistionOfGreenY=-1
            for x in range(0, 8):
                if (engine.GLOBALstateOfTheGameList1[x] != engine.GLOBALstateOfTheGameList2[x]):
                    for y in range(0, 8):
                        if (engine.GLOBALstateOfTheGameList1[x][y] != engine.GLOBALstateOfTheGameList2[x][y]):
                            if(engine.IsEvenCapture == False):
                                if (engine.GLOBALstateOfTheGameList1[x][y] == 3):
                                    FirstPosistionOfRedX = x
                                    FirstPosistionOfRedY = y
                                elif (engine.GLOBALstateOfTheGameList2[x][y] == 3):
                                    SecondPosistionOfRedX = x
                                    SecondPosistionOfRedY = y
                                elif (engine.GLOBALstateOfTheGameList1[x][y] == 1):
                                    PosistionOfGreenX = x
                                    PosistionOfGreenY = y
                            else:
                                if (engine.GLOBALstateOfTheGameList2[x][y] == 3):
                                    FirstPosistionOfRedX = x
                                    FirstPosistionOfRedY = y
                                elif (engine.GLOBALstateOfTheGameList1[x][y] == 3):
                                    SecondPosistionOfRedX = x
                                    SecondPosistionOfRedY = y
                                elif (engine.GLOBALstateOfTheGameList2[x][y] == 1):
                                    PosistionOfGreenX = x
                                    PosistionOfGreenY = y

            if (FirstPosistionOfRedX + SecondPosistionOfRedX)/2 != PosistionOfGreenX or (FirstPosistionOfRedY +SecondPosistionOfRedY)/2 != PosistionOfGreenY:
                IsCorrect=False

        elif (amountOfChanges == 3 and engine.IsPlayer1 == False):
            PosistionOfRedY=-1
            PosistionOfRedX=-1
            for x in range(0, 8):
                if (engine.GLOBALstateOfTheGameList1[x] != engine.GLOBALstateOfTheGameList2[x]):
                    for y in range(0, 8):
                        if (engine.GLOBALstateOfTheGameList1[x][y] != engine.GLOBALstateOfTheGameList2[x][y]):
                            if(engine.IsEvenCapture == False):
                                if (engine.GLOBALstateOfTheGameList1[x][y] == 1):
                                    FirstPosistionOfGreenX = x
                                    FirstPosistionOfGreenY = y
                                elif (engine.GLOBALstateOfTheGameList2[x][y] == 1):
                                    SecondPosistionOfGreenX = x
                                    SecondPosistionOfGreenY = y
                                elif (engine.GLOBALstateOfTheGameList1[x][y] == 3):
                                    PosistionOfRedX = x
                                    PosistionOfRedY = y
                            else:
                                if (engine.GLOBALstateOfTheGameList2[x][y] == 1):
                                    FirstPosistionOfGreenX = x
                                    FirstPosistionOfGreenY = y
                                elif (engine.GLOBALstateOfTheGameList1[x][y] == 1):
                                    SecondPosistionOfGreenX = x
                                    SecondPosistionOfGreenY = y
                                elif (engine.GLOBALstateOfTheGameList2[x][y] == 3):
                                    PosistionOfRedX = x
                                    PosistionOfRedY = y

            if (FirstPosistionOfGreenX + SecondPosistionOfGreenX)/2 != PosistionOfRedX or (FirstPosistionOfGreenY + SecondPosistionOfGreenY)/2 != PosistionOfRedY:
                IsCorrect = False

        if IsCorrect==True:
            engine.app.setLabel("Status", "RUCH WYKONANY POPRAWNIE")
            engine.app.setLabelBg("Status", "green")
        else:
            engine.app.setLabel("Status", "RUCH WYKONANY NIEPOPRAWNIE")
            engine.app.setLabelBg("Status", "red")

    else:
        engine.setLabel("Status", "RUCH WYKONANY NIEPOPRAWNIE. ZBYT DUŻO ZMIAN POZYCJI PIONKÓW")
        engine.app.setLabelBg("Status", "red")


def blind_legal_moves(x, y):

    if engine.IsPlayer1 == True:
        blind_legal_moves = [(x-1, y-1), (x-1, y+1)]

    if engine.IsPlayer1 == False:
        blind_legal_moves = [(x + 1, y - 1), (x + 1, y + 1)]

    for i in range(0,2):
        if blind_legal_moves[i][0] < 0 or blind_legal_moves[i][1] < 0 or blind_legal_moves[i][0] > 7 or blind_legal_moves[i][1] > 7:
            blind_legal_moves.pop(i)

    return blind_legal_moves

