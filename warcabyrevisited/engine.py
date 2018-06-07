import cv2
import numpy as np
import urllib.request
from PIL import Image, ImageTk
# local modules
import webcam
import graphicsEngine
import GUI

# 0 - no checker
# 1 - green checker
# 2 - green queen
# 3 - red checker
# 4 - red queen
# game field is 8x8
global NO_CHECKER_VALUE
global GREEN_CHECKER_VALUE
global GREEN_QUEEN_VALUE
global RED_CHECKER_VALUE
global RED_QUEEN_VALUE
global stateOfTheGameListCapture
global GLOBALstateOfTheGameList1
global GLOBALstateOfTheGameList2
global GLOBALstateOfThePreviousMove
global app
global BLANK
global CaptureBool
global IsEvenCapture
global IsPlayer1
global hop
global url
global firstSavesOfTheDay

NO_CHECKER_VALUE = 0
GREEN_CHECKER_VALUE = 1
GREEN_QUEEN_VALUE = 2
RED_CHECKER_VALUE = 3
RED_QUEEN_VALUE = 4
stateOfTheGameListCapture = [x[:] for x in [[NO_CHECKER_VALUE] * 8] * 8]
GLOBALstateOfTheGameList1 = [x[:] for x in [[0] * 8] * 8]
GLOBALstateOfTheGameList2 = [x[:] for x in [[0] * 8] * 8]
GLOBALstateOfThePreviousMove = [x[:] for x in [[0] * 8] * 8]
app = GUI.returnGuiObject()
BLANK = True
CaptureBool = True
IsEvenCapture = False
IsPlayer1= True
hop=False
url='http://192.168.43.1:8080/shot.jpg'
firstSavesOfTheDay = 2


def start():
    GUI.initialize_gui()


def find_center_coords(contours):
    # loop over the contours
    d = []
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        d.append([cX, cY])
    return d


def ex_1():
    global stateOfTheGameListCapture, NO_CHECKER_VALUE, GREEN_CHECKER_VALUE, RED_CHECKER_VALUE
    # zero out previous move
    stateOfTheGameListCapture = [x[:] for x in [[NO_CHECKER_VALUE] * 8] * 8]

    # basic properties
    kernel = np.ones((5, 5), np.uint8)

    # color ranges for checkers detection - taken from sliders
    hsv_green_lower_sliders = [app.getScale("green_lower H"),   app.getScale("green_lower S"),  app.getScale("green_lower V")]
    hsv_green_upper_sliders = [app.getScale("green_upper H"),   app.getScale("green_upper S"),  app.getScale("green_upper V")]
    hsv_red_lower_sliders   = [app.getScale("red_lower H"),     app.getScale("red_lower S"),    app.getScale("red_lower V")]
    hsv_red_upper_sliders   = [app.getScale("red_upper H"),     app.getScale("red_upper S"),    app.getScale("red_upper V")]
    hsv_blue_lower_sliders  = [app.getScale("blue_lower H"),    app.getScale("blue_lower S"),   app.getScale("blue_lower V")]
    hsv_blue_upper_sliders  = [app.getScale("blue_upper H"),    app.getScale("blue_upper S"),   app.getScale("blue_upper V")]

    hsv_green_lower = np.array(hsv_green_lower_sliders)
    hsv_green_upper = np.array(hsv_green_upper_sliders)
    hsv_red_lower   = np.array(hsv_red_lower_sliders)
    hsv_red_upper   = np.array(hsv_red_upper_sliders)
    hsv_blue_lower  = np.array(hsv_blue_lower_sliders)
    hsv_blue_upper  = np.array(hsv_blue_upper_sliders)

    # try fetching image from camera
    try:
        originalRGBImage = webcam.fetchImage()
    except urllib.error.URLError as err:
        app.errorBox("Error",err)
        return

    # create hsv for markers detection
    image_HSV = cv2.cvtColor(originalRGBImage, cv2.COLOR_BGR2HSV)

    # image shape - needed if we want to crop the image
    height, width, channels = originalRGBImage.shape

    # detect markers
    # get blue marker mask
    blueMarkersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_blue_lower, hsv_blue_upper), cv2.MORPH_OPEN, kernel)
    blueMarkersMask = cv2.dilate(blueMarkersMask, kernel, iterations=1)
    # find markers contours
    im2, blueMarkersContours, hierarchy = cv2.findContours(blueMarkersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # crop image
    img_croped = []
    try:
        hierarchy = hierarchy[0]
    except:
        hierarchy = []
    min_x, min_y = width, height
    max_x = max_y = 0
    # computes the bounding box for the contours, thus we know where to crop
    for contour, hier in zip(blueMarkersContours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)
        if max_x - min_x > 0 and max_y - min_y > 0:
            img_croped = originalRGBImage[min_y+w-10:max_y-w+10, min_x+w-10:max_x-w+10]

    # compute new HSV from cropped image
    image_HSV = cv2.cvtColor(img_croped, cv2.COLOR_BGR2HSV)
    # new image shape, overwrite previous ones
    height, width, channels = img_croped.shape


    # checker board is 8x8
    boardTileLength = width/8

    # get green checkers mask and do opening operation to remove noise
    greenCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_green_lower, hsv_green_upper), cv2.MORPH_OPEN, kernel)
    # get red checkers mask
    redCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_red_lower, hsv_red_upper), cv2.MORPH_OPEN, kernel)

    redCheckersMask = cv2.erode(redCheckersMask, kernel, iterations=3)
    greenCheckersMask = cv2.erode(greenCheckersMask, kernel, iterations=3)

    # save masks
    cv2.imwrite("images/blueMask.jpg", blueMarkersMask)
    cv2.imwrite("images/redMask.jpg", redCheckersMask)
    cv2.imwrite("images/greenMask.jpg", greenCheckersMask)

    # checkers detection
    im2, greenCheckersContours, hierarchy = cv2.findContours(greenCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im2, redCheckersContours, hierarchy = cv2.findContours(redCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find middle point of all contours
    greenCheckersCoords = find_center_coords(greenCheckersContours)
    redCheckersCoords = find_center_coords(redCheckersContours)

    # save image for display
    img_croped = cv2.resize(img_croped, (400, 400))
    cv2.imwrite('images/screen1.jpg', img_croped)

    print("Green checkers coords: ")
    print(greenCheckersCoords)
    print("Red checkers coords")
    print(redCheckersCoords)
    print("Board tile len: ")
    print(boardTileLength)


    for checkerCoord in greenCheckersCoords:
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
            stateOfTheGameListCapture[Y_Index_TMP][X_Index_TMP] = GREEN_CHECKER_VALUE

    for checkerCoord in redCheckersCoords:
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
                stateOfTheGameListCapture[Y_Index_TMP][X_Index_TMP] = RED_CHECKER_VALUE

    renderedGame = graphicsEngine.renderGameState()
    resizedRenderedGame = cv2.resize(renderedGame, (400, 400))
    cv2.imwrite('images/renderedGame.jpg', resizedRenderedGame)

    photo1 = ImageTk.PhotoImage(Image.open("images/screen1.jpg"))
    app.reloadImageData("state", photo1, fmt="PhotoImage")
    photo2 = ImageTk.PhotoImage(Image.open("images/renderedGame.jpg"))
    app.reloadImageData("renderedGame", photo2, fmt="PhotoImage")

    cv2.destroyAllWindows()