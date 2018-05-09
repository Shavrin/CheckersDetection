import cv2
import numpy as np
import math


def nothing(x): pass


def find_center_coords(contours):
    # loop over the contours
    d = []
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        d.append([cX, cY])
    return d


def draw_centers(point, image, color):
    cX = point[0]
    cY = point[1]

    # draw the contour and center of the shape on the image
    # cv2.drawContours(image, [c], -1, (127, 127, 127), 2)
    cv2.circle(image, (cX, cY), 7, color, -1)

def ex_1():
    # basic properties
    windowName = "Warcaby"
    kernel = np.ones((5, 5), np.uint8)

    # color ranges for checkers detection
    hsv_green_lower = np.array([30, 0, 100])
    hsv_green_upper = np.array([80, 255, 255])
    hsv_red_lower = np.array([170, 100, 100])
    hsv_red_upper = np.array([180, 255, 255])

    # basic methods
    cv2.namedWindow(windowName)

    # load images
    originalRGBImage = cv2.imread("p1.jpg")
    corners = np.array([
        [40, 38],
        [1721, 30],
        [38, 1829],
        [1957, 1703]], dtype="float32")
    dst = np.array([
        [0,0],
        [1900,0],
        [0,1900],
        [1900,1900]], dtype="float32")
    M = cv2.getPerspectiveTransform(corners, dst)
    originalRGBImage = cv2.warpPerspective(originalRGBImage, M, (1900, 1900))
    originalRGBImage = cv2.resize(originalRGBImage,(1000,1000), interpolation = cv2.INTER_CUBIC)
    cv2.imshow(windowName, originalRGBImage)

    imageBW = cv2.imread("p1.jpg", cv2.IMREAD_GRAYSCALE)
    corners = np.array([
        [40, 38],
        [1721, 30],
        [38, 1829],
        [1957, 1703]], dtype="float32")
    dst = np.array([
        [0, 0],
        [1900, 0],
        [0, 1900],
        [1900, 1900]], dtype="float32")
    M = cv2.getPerspectiveTransform(corners, dst)

    imageBW = cv2.warpPerspective(imageBW, M, (1900, 1900))
    imageBW = cv2.resize(imageBW,(1000,1000), interpolation = cv2.INTER_CUBIC)

    cv2.imshow(windowName, imageBW)

    # add border for checker fields detection
    imageBW = cv2.copyMakeBorder(imageBW, 2,2,2,2, cv2.BORDER_CONSTANT, value=255)

    image_HSV = cv2.cvtColor(originalRGBImage, cv2.COLOR_BGR2HSV)

    height, width, channels = originalRGBImage.shape
    # checker board is 8x8
    boardTileLength = width/8
    # magic
    while cv2.getWindowProperty(windowName, 0) >= 0:
        # get green checkers mask and do opening operation to remove noise
        greenCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_green_lower, hsv_green_upper), cv2.MORPH_OPEN, kernel)
        # get red checkers mask
        redCheckersMask = cv2.morphologyEx(cv2.inRange(image_HSV, hsv_red_lower, hsv_red_upper), cv2.MORPH_OPEN, kernel)

        redCheckersMask=cv2.dilate(redCheckersMask, kernel, iterations=1)
        greenCheckersMask = cv2.dilate(greenCheckersMask, kernel, iterations=1)

        # remove unnecessary elements from image, leaving only the board
        ret, imageBW = cv2.threshold(imageBW, 200, 255, cv2.THRESH_BINARY)

        # checkers detection
        im2, greenCheckersContours, hierarchy = cv2.findContours(greenCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        im2, redCheckersContours, hierarchy = cv2.findContours(redCheckersMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        greenCheckersCoords = find_center_coords(greenCheckersContours)
        redCheckersCoords = find_center_coords(redCheckersContours)

        # tiles detection
        dilation = cv2.dilate(imageBW, kernel, iterations=2)
        im2, boardTilesContours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # remove biggest contour (image border)
        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in boardTilesContours]
        max_index = np.argmax(areas)
        # remove largest contour (image border)
        boardTilesContours.pop(max_index)

        fieldsCoords = find_center_coords(boardTilesContours)

        # calc distance between checkers and their fields
        print(greenCheckersCoords)
        print(redCheckersCoords)
        print(fieldsCoords)
        print(boardTileLength)
        for checkerCoord in greenCheckersCoords:
            for fieldCoord in fieldsCoords:
                if(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]) < boardTileLength/2):
                    print(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]))
                    draw_centers(checkerCoord, originalRGBImage, (255, 0, 170))
                    draw_centers(fieldCoord, originalRGBImage, (255, 0, 0))

        for checkerCoord in redCheckersCoords:
            for fieldCoord in fieldsCoords:
                if(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]) < boardTileLength/2):
                    print(math.hypot(checkerCoord[0] - fieldCoord[0], checkerCoord[1] - fieldCoord[1]))
                    draw_centers(checkerCoord, originalRGBImage, (255, 0, 170))
                    draw_centers(fieldCoord, originalRGBImage, (0, 0, 170))

        cv2.imshow(windowName, originalRGBImage)
        cv2.imshow("Erozja", dilation)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ex_1()