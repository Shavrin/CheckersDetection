import cv2
import numpy as np
import math
import urllib.request
import socket

from appJar import gui
from PIL import Image, ImageTk

def nothing(x): pass

BLANK = True
CaptureBool = True
GLOBALstateOfTheGameList1 = [x[:] for x in [[0] * 8] * 8]
GLOBALstateOfTheGameList2 = [x[:] for x in [[0] * 8] * 8]
IsEvenCapture = False
IsPlayer1= True
hop=False
url='http://192.168.0.100:8080/shot.jpg'



def find_center_coords(contours):
    # loop over the contours
    d = []
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        d.append([cX, cY])
    return d


def draw_circle(point, image, size, color):
    cX = point[0]
    cY = point[1]
    cv2.circle(image, (cX, cY), size, color, -1)


def renderGameState(gameStateList):
    game = cv2.imread("boardForRendering.png")
    height, width, channels = game.shape
    # checker board is 8x8
    boardTileLength = width//8
    for idxY, stateRow in enumerate(gameStateList):
       for idxX, stateField in enumerate(stateRow):
            if (stateField == 0):
               continue
            if (stateField == 1):
                draw_circle((idxX * boardTileLength + boardTileLength//2, idxY * boardTileLength + boardTileLength//2), game, boardTileLength//3, (0, 255, 0))
            if (stateField == 2):
                # damka
                continue
            if(stateField == 3):
                draw_circle((idxX * boardTileLength + boardTileLength//2, idxY * boardTileLength + boardTileLength//2), game, boardTileLength//3, (0, 0, 255))
            if(stateField == 4):
                # damka
                continue
    return game

def fetchImage():
    global url
    with urllib.request.urlopen(url) as response:
        html = response.read()

    imgResponse = urllib.request.urlopen(url)
    imgNumpy = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNumpy,-1)
    size = int((img.shape[1] - img.shape[0] )/ 2)
    img = img[:,size:img.shape[0]+size]

    return img
def ex_1():
    global BLANK
    global GLOBALstateOfTheGameList2
    global GLOBALstateOfTheGameList1
    global IsEvenCapture

    # basic properties
    windowName = "Warcaby"
    kernel = np.ones((5, 5), np.uint8)

    # 0 - no checker
    # 1 - green checker
    # 2 - green queen
    # 3 - red checker
    # 4 - red queen
    # game field is 8x8
    NO_CHECKER_VALUE = 0
    GREEN_CHECKER_VALUE = 1
    GREEN_QUEEN_VALUE = 2
    RED_CHECKER_VALUE = 3
    RED_QUEEN_VALUE = 4
    stateOfTheGameList = [x[:] for x in [[NO_CHECKER_VALUE] * 8] * 8]

    # color ranges for checkers detection
    hsv_green_lower = np.array([30, 0, 100])
    hsv_green_upper = np.array([80, 255, 255])
    hsv_red_lower = np.array([170, 100, 100])
    hsv_red_upper = np.array([180, 255, 255])

    hsv_blue_lower = np.array([100, 160, 0])
    hsv_blue_upper = np.array([140, 255, 255])

    try:
        originalRGBImage = fetchImage()
    except urllib.error.URLError as err:
        app.errorBox("Error",err)
        return
    imageBW = cv2.cvtColor(originalRGBImage, cv2.COLOR_BGR2GRAY)

    # add border for checker fields detection
    imageBW = cv2.copyMakeBorder(imageBW, 2,2,2,2, cv2.BORDER_CONSTANT, value=255)
    image_HSV = cv2.cvtColor(originalRGBImage, cv2.COLOR_BGR2HSV)

    height, width, channels = originalRGBImage.shape
    # checker board is 8x8
    boardTileLength = width/8

    # get green checkers mask and do opening operation to remove noise
    greenCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_green_lower, hsv_green_upper), cv2.MORPH_OPEN, kernel)
    # get red checkers mask
    redCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_red_lower, hsv_red_upper), cv2.MORPH_OPEN, kernel)

    redCheckersMask = cv2.dilate(redCheckersMask, kernel, iterations=1)
    greenCheckersMask = cv2.dilate(greenCheckersMask, kernel, iterations=1)

    # remove unnecessary elements from image, leaving only the board
    ret, imageBW = cv2.threshold(imageBW, 200, 255, cv2.THRESH_BINARY)

    # checkers detection
    im2, greenCheckersContours, hierarchy = cv2.findContours(greenCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im2, redCheckersContours, hierarchy = cv2.findContours(redCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find middle point of all contours
    greenCheckersCoords = find_center_coords(greenCheckersContours)
    redCheckersCoords = find_center_coords(redCheckersContours)

    # tiles detection
    dilation = cv2.dilate(imageBW, kernel, iterations=2)
    resizedOriginalRGBImage = cv2.resize(originalRGBImage, (400, 400))
    cv2.imwrite('originalRGB.jpg', resizedOriginalRGBImage)
    im2, boardTilesContours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # remove biggest contour (image border)
    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in boardTilesContours]
    max_index = np.argmax(areas)
    # remove largest contour (image border)
    boardTilesContours.pop(max_index)

    fieldsCoords = find_center_coords(boardTilesContours)

    # calc distance between checkers and their fields
    # if the distance seems ok, count the X and Y index position of the checker, and then add it to the list
    print(greenCheckersCoords)
    print(redCheckersCoords)
    print(fieldsCoords)
    print(boardTileLength)
    for checkerCoord in greenCheckersCoords:
        for fieldCoord in fieldsCoords:
            if(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]) < boardTileLength/2):
                print(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]))
                X_Coord_TMP = checkerCoord[0]
                X_Index_TMP = -1
                Y_Coord_TMP = checkerCoord[1]
                Y_Index_TMP = -1
                while (X_Coord_TMP > 0):
                    X_Coord_TMP -= boardTileLength
                    X_Index_TMP += 1
                while (Y_Coord_TMP > 0):
                    Y_Coord_TMP -= boardTileLength
                    Y_Index_TMP += 1
                stateOfTheGameList[Y_Index_TMP][X_Index_TMP] = GREEN_CHECKER_VALUE

               # draw_circle(checkerCoord, originalRGBImage, 7, (255, 0, 170))
               # draw_circle(fieldCoord, originalRGBImage, 7, (255, 0, 0))

    for checkerCoord in redCheckersCoords:
        for fieldCoord in fieldsCoords:
            if(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]) < boardTileLength/2):
                print(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]))

                X_Coord_TMP = checkerCoord[0]
                X_Index_TMP = -1
                Y_Coord_TMP = checkerCoord[1]
                Y_Index_TMP = -1
                while (X_Coord_TMP > 0):
                    X_Coord_TMP -= boardTileLength
                    X_Index_TMP += 1
                while (Y_Coord_TMP > 0):
                    Y_Coord_TMP -= boardTileLength
                    Y_Index_TMP += 1
                stateOfTheGameList[Y_Index_TMP][X_Index_TMP] = RED_CHECKER_VALUE

               # draw_circle(checkerCoord, originalRGBImage, 7, (255, 0, 170))
               # draw_circle(fieldCoord, originalRGBImage, 7, (0, 0, 170))

    renderedGame = renderGameState(stateOfTheGameList)
    resizedRenderedGame = cv2.resize(renderedGame, (400, 400))
    cv2.imwrite('renderedGame.jpg', resizedRenderedGame)

    if(IsEvenCapture==False):
        GLOBALstateOfTheGameList1=stateOfTheGameList
    else:
        GLOBALstateOfTheGameList2=stateOfTheGameList
    print(GLOBALstateOfTheGameList1)
    print(GLOBALstateOfTheGameList2)

    # if BLANK == True:
    #     app.startLabelFrame("state", 0, 0)
    #     photo1 = ImageTk.PhotoImage(Image.open("originalRGB.jpg"))
    #     app.addImageData("state", photo1, fmt="PhotoImage" )
    #     app.stopLabelFrame()
    #
    #     app.startLabelFrame("renderedGame", 1, 0)
    #     photo2 = ImageTk.PhotoImage(Image.open("renderedGame.jpg"))
    #     app.addImageData("renderedGame", photo2, fmt="PhotoImage")
    #     app.stopLabelFrame()
    #     BLANK = False
    # else:
    photo1 = ImageTk.PhotoImage(Image.open("originalRGB.jpg"))
    app.reloadImageData("state", photo1, fmt="PhotoImage")
    photo2 = ImageTk.PhotoImage(Image.open("renderedGame.jpg"))
    app.reloadImageData("renderedGame", photo2, fmt="PhotoImage")

    IsEvenCapture = not IsEvenCapture
    cv2.destroyAllWindows()


def blind_legal_moves(x, y):
    """
    Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
    If that location is empty, then blind_legal_moves() return an empty list.
    """
    global IsPlayer1

    if IsPlayer1 == True:
        blind_legal_moves = [(x-1, y-1), (x-1, y+1)]

    if IsPlayer1 == False:
        blind_legal_moves = [(x + 1, y - 1), (x + 1, y + 1)]

    for i in range(0,2):
        if blind_legal_moves[i][0] < 0 or blind_legal_moves[i][1] < 0 or blind_legal_moves[i][0] > 7 or blind_legal_moves[i][1] > 7:
            blind_legal_moves.pop(i)

    return blind_legal_moves


def legal_moves(x, y):
    """
    Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
    If that location is empty, then legal_moves() returns an empty list.
    """
    global IsPlayer1
    global hop
    global IsEvenCapture

    blinds = blind_legal_moves(x, y)
    legal_moves = []

    if hop == False:
        for move in blinds:
            if (IsPlayer1 == True):
                if IsEvenCapture==False:
                    if GLOBALstateOfTheGameList1[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (GLOBALstateOfTheGameList1[move[0]][move[1]] == 1 and GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if GLOBALstateOfTheGameList2[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (GLOBALstateOfTheGameList2[move[0]][move[1]] == 1 and GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
            else:
                if IsEvenCapture==False:
                    if GLOBALstateOfTheGameList1[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (GLOBALstateOfTheGameList1[move[0]][move[1]] == 3 and GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if GLOBALstateOfTheGameList2[move[0]][move[1]] == 0:
                        legal_moves.append(move)
                    elif (GLOBALstateOfTheGameList2[move[0]][move[1]] == 3 and GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

    else:  # hop == True
        for move in blinds:
            if (IsPlayer1 == True):
                if IsEvenCapture==False:
                    if (GLOBALstateOfTheGameList1[move[0]][move[1]] == 1 and GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if (GLOBALstateOfTheGameList2[move[0]][move[1]] == 1 and GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
            else:
                if IsEvenCapture==False:
                    if (GLOBALstateOfTheGameList1[move[0]][move[1]] == 3 and GLOBALstateOfTheGameList1[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

                else:
                    if (GLOBALstateOfTheGameList2[move[0]][move[1]] == 3 and GLOBALstateOfTheGameList2[move[0] + (move[0]-x)][move[1] + (move[1]-y)] == 0):
                        if (move[0] + (move[0] - x)) >= 0 or (move[1] + (move[1] - y)) >= 0 or (move[0] + (move[0] - x)) <= 7 or (move[1] + (move[1] - y)) <= 7:
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

    return legal_moves


def check_move():
    global IsPlayer1
    global hop
    global IsEvenCapture

    amountOfChanges = 0
    for x in range(0, 8):
        if (GLOBALstateOfTheGameList1[x] != GLOBALstateOfTheGameList2[x]):
            for y in range(0, 8):
                if (GLOBALstateOfTheGameList1[x][y] != GLOBALstateOfTheGameList2[x][y]):
                    amountOfChanges=amountOfChanges+1
                    if(GLOBALstateOfTheGameList1[x][y]!=0 and IsEvenCapture == False):
                        PosistionOfChangedX=x
                        PosistionOfChangedY=y
                    elif (GLOBALstateOfTheGameList2[x][y] != 0 and IsEvenCapture == True):
                        PosistionOfChangedX = x
                        PosistionOfChangedY = y

    if(amountOfChanges<4):
        legals=legal_moves(PosistionOfChangedX,PosistionOfChangedY)
        for x in range(0, 8):
            if (GLOBALstateOfTheGameList1[x] != GLOBALstateOfTheGameList2[x]):
                for y in range(0, 8):
                    if (GLOBALstateOfTheGameList1[x][y] != GLOBALstateOfTheGameList2[x][y]):
                        if (GLOBALstateOfTheGameList1[x][y] == 0 and IsEvenCapture == False):
                            PosistionOfChangedX = x
                            PosistionOfChangedY = y
                        elif (GLOBALstateOfTheGameList2[x][y] == 0 and IsEvenCapture == True):
                            PosistionOfChangedX = x
                            PosistionOfChangedY = y
        IsCorrect=False
        for move in legals:
            if(move[0]==PosistionOfChangedX and move[1]==PosistionOfChangedY):
                IsCorrect=True

        if(amountOfChanges==3 and IsPlayer1==True):
            PosistionOfGreenX=-1
            PosistionOfGreenY=-1
            for x in range(0, 8):
                if (GLOBALstateOfTheGameList1[x] != GLOBALstateOfTheGameList2[x]):
                    for y in range(0, 8):
                        if (GLOBALstateOfTheGameList1[x][y] != GLOBALstateOfTheGameList2[x][y]):
                            if(IsEvenCapture == False):
                                if (GLOBALstateOfTheGameList1[x][y] == 3):
                                    FirstPosistionOfRedX = x
                                    FirstPosistionOfRedY = y
                                elif (GLOBALstateOfTheGameList2[x][y] == 3):
                                    SecondPosistionOfRedX = x
                                    SecondPosistionOfRedY = y
                                elif (GLOBALstateOfTheGameList1[x][y] == 1):
                                    PosistionOfGreenX = x
                                    PosistionOfGreenY = y
                            else:
                                if (GLOBALstateOfTheGameList2[x][y] == 3):
                                    FirstPosistionOfRedX = x
                                    FirstPosistionOfRedY = y
                                elif (GLOBALstateOfTheGameList1[x][y] == 3):
                                    SecondPosistionOfRedX = x
                                    SecondPosistionOfRedY = y
                                elif (GLOBALstateOfTheGameList2[x][y] == 1):
                                    PosistionOfGreenX = x
                                    PosistionOfGreenY = y

            if (FirstPosistionOfRedX + SecondPosistionOfRedX)/2 != PosistionOfGreenX or (FirstPosistionOfRedY +SecondPosistionOfRedY)/2 != PosistionOfGreenY:
                IsCorrect=False

        elif (amountOfChanges == 3 and IsPlayer1 == False):
            PosistionOfRedY=-1
            PosistionOfRedX=-1
            for x in range(0, 8):
                if (GLOBALstateOfTheGameList1[x] != GLOBALstateOfTheGameList2[x]):
                    for y in range(0, 8):
                        if (GLOBALstateOfTheGameList1[x][y] != GLOBALstateOfTheGameList2[x][y]):
                            if(IsEvenCapture == False):
                                if (GLOBALstateOfTheGameList1[x][y] == 1):
                                    FirstPosistionOfGreenX = x
                                    FirstPosistionOfGreenY = y
                                elif (GLOBALstateOfTheGameList2[x][y] == 1):
                                    SecondPosistionOfGreenX = x
                                    SecondPosistionOfGreenY = y
                                elif (GLOBALstateOfTheGameList1[x][y] == 3):
                                    PosistionOfRedX = x
                                    PosistionOfRedY = y
                            else:
                                if (GLOBALstateOfTheGameList2[x][y] == 1):
                                    FirstPosistionOfGreenX = x
                                    FirstPosistionOfGreenY = y
                                elif (GLOBALstateOfTheGameList1[x][y] == 1):
                                    SecondPosistionOfGreenX = x
                                    SecondPosistionOfGreenY = y
                                elif (GLOBALstateOfTheGameList2[x][y] == 3):
                                    PosistionOfRedX = x
                                    PosistionOfRedY = y

            if (FirstPosistionOfGreenX + SecondPosistionOfGreenX)/2 != PosistionOfRedX or (FirstPosistionOfGreenY + SecondPosistionOfGreenY)/2 != PosistionOfRedY:
                IsCorrect = False

        if IsCorrect==True:
            print("RUCH WYKONANY POPRAWNIE")
        else:
            print("RUCH WYKONANY NIEPOPRAWNIE")

    else:
        print("RUCH WYKONANY NIEPOPRAWNIE. ZBYT DUŻO ZMIAN POZYCJI PIONKÓW")

def click(event):
    global url
    if event == "Capture":
        tempUrl = app.getEntry("IP")

        try:
            socket.inet_aton(tempUrl)
        except socket.error:
            app.errorBox("Error!","Invalid IP Address..")
            return
        url = 'http://' + tempUrl + ':8080/shot.jpg'
        ex_1()
    return

if __name__ == "__main__":
    ranges = {
        'green_lower' :[30, 0, 100],
        'green_upper': [80, 255, 255],
        'red_lower' : [170, 100, 100],
        'red_upper': [180, 255, 255],
        'blue_lower' : [100, 160, 0],
        'blue_upper' : [140, 255, 255],
    }
    color_range_names = ["Green H", "Green S", "Green V",
                         "Red H", "Red S", "Red V",
                         "Blue H","Blue S","Blue V"]
    color_ranges = ["H","S","V"]
    colors = ["green_upper","green_lower",
              "red_upper","red_lower",
              "blue_upper","blue_lower"]

    app = gui("Warcaby Revisited", "550x850")
    app.startTabbedFrame("Application")

    app.startTab("Configuration")
    #app.startScrollPane("Values")
    for val in colors:
        app.startLabelFrame(val)
        for col in color_ranges:
            app.addLabelScale(val + " " + col)
            app.setScaleRange(val + " " + col, 0, 255)
            app.showScaleValue(val + " " + col, show=True)
        app.setScale(val + " " + "H", ranges[val][0])
        app.setScale(val + " " + "S", ranges[val][1])
        app.setScale(val + " " + "V", ranges[val][2])


        #app.setScale(val,)
        app.stopLabelFrame()

    #app.stopScrollPane()
    app.stopTab()

    app.startTab("Game")

    app.addButton("Capture", click, row=0, column=1)
    app.addButton("Check Move", check_move, row=1, column=1)
    app.addLabelEntry("IP")

    app.startLabelFrame("Captured Image", 0, 0)
    photo1 = ImageTk.PhotoImage(Image.open("initCapturedImage.jpg"))
    app.addImageData("state", photo1, fmt="PhotoImage")
    app.stopLabelFrame()

    app.startLabelFrame("Game State", 1, 0)
    photo2 = ImageTk.PhotoImage(Image.open("board400.png"))
    app.addImageData("renderedGame", photo2, fmt="PhotoImage")
    app.stopLabelFrame()
    #BLANK = False


    app.stopTab()
    app.stopTabbedFrame()

    app.go()