# Required Imports
import cv2 as cv
import mediapipe as mp
import time
capture = cv.VideoCapture(0)

# Create hand class object
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Drawing the hands
mpDraw = mp.solutions.drawing_utils

# Writing framerate on screen
pTime = 0
cTime = 0

while True:
    # setup basic video capture
    isTrue, frame = capture.read()

    # Convert BGR video to RGB
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process the frame and store results
    results = hands.process(frameRGB)
    # print(type(results))

    # Extract hand information from results
    # If you show your hand to the camera, it'll show the coordinat es x, y, z
    # landmarks = { x, y, z }
    # print(results.multi_hand_landmarks)

    # Draw points of hands
    # Using built-in function in mediapipe library
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draw only points
            # mpDraw.draw_landmarks(frame, handLms)

            # Draw all points and connections
            # mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

            # Working with specific points on the palm (21 points indexed 0 - 20 )
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)

                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)

                # Draw circles on specific coordinates
                # if id == 0:
                #     cv.circle(frame, (cx, cy), 12, (255, 0, 255), cv.FILLED)
                # if id == 4:
                #     cv.circle(frame, (cx, cy), 12, (255, 0, 255), cv.FILLED)

    # Write Framerate on screen
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(frame, str(int(fps)), (10, 60),
               cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)

    cv.imshow('Video', frame)
    cv.waitKey(1)


capture.release()
