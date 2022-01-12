# Required Imports
import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.static_image_mode, self.max_num_hands,  self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(frame, (cx, cy), 12, (255, 0, 255), cv.FILLED)

        return lmList


def main():
    capture = cv.VideoCapture(0)
    pTime = 0
    cTime = 0

    # Create class object
    detector = handDetector()

    while True:
        isTrue, frame = capture.read()

        # Use class method
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False)
        if (len(lmList) != 0):
            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10, 60),
                   cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)

        cv.imshow('Video', frame)
        cv.waitKey(1)


if __name__ == "__main":
    main()
else:
    print("Imported")
