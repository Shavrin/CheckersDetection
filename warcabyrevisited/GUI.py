from PIL import Image, ImageTk
from appJar import gui
# local modules
import engine
import webcam
import AI


def returnGuiObject():
    return gui("Warcaby Revisited", "850x850")


def setLabel(labelname, color, text):
    engine.app.setLabel(labelname, text)
    engine.app.setLabelBg(labelname, color)


def initialize_gui():
    ranges = {
        'green_lower': [30, 0, 100],
        'green_upper': [80, 255, 255],
        'red_lower': [170, 100, 100],
        'red_upper': [180, 255, 255],
        'blue_lower': [100, 160, 0],
        'blue_upper': [140, 255, 255],
    }
    color_range_names = ["Green H", "Green S", "Green V",
                         "Red H", "Red S", "Red V",
                         "Blue H", "Blue S", "Blue V"]
    color_ranges = ["H", "S", "V"]
    colors = ["green_upper", "green_lower",
              "red_upper", "red_lower",
              "blue_upper", "blue_lower"]

    engine.app.startTabbedFrame("engine.Application")

    engine.app.startTab("Configuration")
    engine.app.startScrollPane("Values")
    engine.app.addLabelEntry("IP")
    engine.app.setEntry("IP", "192.168.43.1")
    for val in colors:
        engine.app.startLabelFrame(val)
        for col in color_ranges:
            engine.app.addLabelScale(val + " " + col)
            engine.app.setScaleRange(val + " " + col, 0, 255)
            engine.app.showScaleValue(val + " " + col, show=True)
        engine.app.setScale(val + " " + "H", ranges[val][0])
        engine.app.setScale(val + " " + "S", ranges[val][1])
        engine.app.setScale(val + " " + "V", ranges[val][2])

        engine.app.stopLabelFrame()

    engine.app.stopScrollPane()
    engine.app.stopTab()

    engine.app.startTab("Game")

    engine.app.addButton("Capture", webcam.click_capture, row=1, column=0)
    engine.app.addButton("Check Move", AI.check_move, row=1, column=1)
    engine.app.addButton("Save move", AI.save_move, row=2, column=0)
    engine.app.addButton("Rollback", AI.rollback, row=2, column=1)
    engine.app.addLabel("Player", "", row=3, colspan=3)
    engine.app.addLabel("Status", "", row=4, colspan=3)

    engine.app.startLabelFrame("Captured Image", 0, 0)
    photo1 = ImageTk.PhotoImage(Image.open("images/initCapturedImage.jpg"))
    engine.app.addImageData("state", photo1, fmt="PhotoImage")
    engine.app.stopLabelFrame()

    engine.app.startLabelFrame("Game State", 0, 1)
    photo2 = ImageTk.PhotoImage(Image.open("images/board400.png"))
    engine.app.addImageData("renderedGame", photo2, fmt="PhotoImage")
    engine.app.stopLabelFrame()

    engine.app.stopTab()
    engine.app.stopTabbedFrame()

    engine.app.go()