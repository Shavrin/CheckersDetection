import socket
import urllib.request
import cv2
import numpy as np
# local modules
import engine


def click_capture(event):
    global url
    if event == "Capture":
        tempUrl = engine.app.getEntry("IP")

        try:
            socket.inet_aton(tempUrl)
        except socket.error:
            engine.app.errorBox("Error!","Invalid IP Address..")
            return
        url = 'http://' + tempUrl + ':8080/shot.jpg'
        engine.ex_1()
    return

def fetchImage():
    with urllib.request.urlopen(url) as response:
        html = response.read()

    imgResponse = urllib.request.urlopen(url)
    imgNumpy = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNumpy,-1)
    size = int((img.shape[1] - img.shape[0] )/ 2)
    img = img[:,size:img.shape[0]+size]

    return img