import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math

# Pycaw - https://github.com/AndreMiras/pycaw
# Open Source Volume Control library
# Required imports
# This is for Windows only (I believe?)
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Osascript - Volume Control for Mac
# Required import
import osascript

wCam, hCam = 640, 480

# Call our custom built library
detector = htm.handDetector(min_detection_confidence=0.7)
# We change detection confidence because we want it to be really sure that it is a hand.

# Initializing pycaw audio library
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))

# Testing pycaw library
# print(volume.GetVolumeRange())
# volume.SetMasterVolumeLevel(-20.0, None)

capture = cv.VideoCapture(0)
# Set width
# capture.set(3, wCam)
# Set height
# capture.set(4, hCam)

while True:
    isTrue, frame = capture.read()
    newFrame = cv.flip(frame, 1)

    # Find Hands
    newFrame = detector.findHands(newFrame)

    # Print Position
    lmList = detector.findPosition(newFrame, draw=False)
    if (len(lmList) > 0):
        # Get index and thumb tip coordinates
        # print(lmList[4], lmList[8])

        # Specific x, y coordinates
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # print(x1, y1)

        # Get center of line between two coordinates
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circle on index and thumb tip
        cv.circle(newFrame, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(newFrame, (x2, y2), 15, (255, 0, 255), cv.FILLED)

        # Draw line between them
        cv.line(newFrame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Draw circle at center
        cv.circle(newFrame, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        # Find length of line - using built-in math library
        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        # Change color when length is less
        if (length < 50):
            cv.circle(newFrame, (cx, cy), 15, (0, 255, 0), cv.FILLED)

        # Hand range (at a basic distance when sitting at desk) : 50 - 300
        # Volume range (Mac library) : 0 - 100
        # We need to match these two ranges
        vol = np.interp(length, [50, 300], [0, 100])
        print(vol)

        # Send to Mac
        volString = "set volume output volume " + str(vol)
        osascript.osascript(volString)

    cv.imshow('Video', newFrame)
    cv.waitKey(1)


capture.release()
cv.destroyAllWindows()
