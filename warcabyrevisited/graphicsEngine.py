import cv2
import engine

def draw_circle(point, image, size, color):
    cX = point[0]
    cY = point[1]
    cv2.circle(image, (cX, cY), size, color, -1)


def renderGameState():
    game = cv2.imread("images/boardForRendering.png")
    height, width, channels = game.shape
    # checker board is 8x8
    boardTileLength = width//8
    for idxY, stateRow in enumerate(engine.stateOfTheGameListCapture):
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