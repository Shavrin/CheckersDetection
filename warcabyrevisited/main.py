import cv2
import numpy as np


def nothing(x): pass


def draw_centers(contours, image):
    # loop over the contours
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (127, 127, 127), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)


def ex_1():
    windowName = "Warcaby"
    image = cv2.imread("plansza.png")
    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.namedWindow(windowName)

    while cv2.getWindowProperty(windowName, 0) >= 0:
        green = np.uint8([[[0, 255, 0]]])  #BGR
        red = np.uint8([[[0, 0, 255]]])  # BGR
        hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
        hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        # print(hsv_red)     0,255,255 HSV
        # print(hsv_green)    60,255,255 HSV

        hsv_green_lower = np.array([50,100,100])
        hsv_green_upper = np.array([70,255,255])

        hsv_red_lower = np.array([0,100,100])
        hsv_red_upper = np.array([10,255,255])

        mask = cv2.inRange(image_HSV, hsv_green_lower, hsv_green_upper)
        mask2 = cv2.inRange(image_HSV, hsv_red_lower, hsv_red_upper)

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        im2, contours2, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        draw_centers(contours, image)
        draw_centers(contours2, image)

        cv2.imshow(windowName, image)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ex_1()