import random
from os import walk

import cv2
import time
import pyglet

from screeninfo import get_monitors
from cvzone.HandTrackingModule import HandDetector


class Label:
    def __init__(self, x, y, w, h, v, s):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.s = s

    def draw(self, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, (0, 0, 0), self.s)

    def resize(self, w, h, img):
        cv2.putText(img, self.v, (self.x + w, self.y + h), cv2.FONT_HERSHEY_PLAIN, self.s, (0, 0, 0), self.s)

    def color(self, rgb, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, rgb, self.s)

    def text(self, value, img):
        cv2.putText(img, value, (self.x + 25, self.y + 40), cv2.FONT_HERSHEY_PLAIN, self.s, (0, 0, 0), self.s)

    def shrink(self, value, limit, img):
        cv2.putText(img, (self.v[:limit + 1][-1] + value), (self.x + 25, self.y + 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 0, 0), 2)


def main():
    pTime = 0
    cTime = 0

    primary_monitor = {}
    for m in get_monitors():
        print("Connected monitors {}".format(m))
        if m.is_primary:
            primary_monitor = m
            break

    cap = cv2.VideoCapture(1)
    cap.set(3, primary_monitor.width)
    cap.set(4, primary_monitor.height)
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    tipIds = [4, 8, 12, 16, 20]

    sounds = next(walk("media"), (None, None, []))[2]
    for sound in sounds:
        print("Available sounds:")
        print("File: {}".format(sound))

    overlayList = []

    timer_total = 0

    while cap.isOpened():

        success, img = cap.read()
        img = cv2.flip(img, 1)
        # detection hand
        hand, img = detector.findHands(img, flipType=False)

        if len(hand) == 1:
            landmarks = hand[0]["lmList"]

            if len(landmarks) != 0:
                fingers = []

                # Thumb
                if landmarks[tipIds[0]][1] > landmarks[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = fingers.count(1)
                print(totalFingers)

                cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)

                # Tested but too fast
                # sound = pyglet.resource.media("media/" + sounds[sound_index - 1], streaming=False)
                # sound.play()

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

        elif len(hand) >= 2:

            landmarks1 = hand[0]["lmList"]
            landmarks2 = hand[1]["lmList"]

            if len(landmarks1) != 0 and len(landmarks2) != 0:
                fingers1 = []

                # Thumb first hand
                if landmarks1[tipIds[0]][1] > landmarks1[tipIds[0] - 1][1]:
                    fingers1.append(1)
                else:
                    fingers1.append(0)

                # 4 Fingers first hand
                for tId in range(1, 5):
                    if landmarks1[tipIds[tId]][2] < landmarks1[tipIds[tId] - 2][2]:
                        fingers1.append(1)
                    else:
                        fingers1.append(0)

                totalFingers1 = fingers1.count(1)

                fingers2 = []

                # Thumb first hand
                if landmarks2[tipIds[0]][1] > landmarks2[tipIds[0] - 1][1]:
                    fingers2.append(1)
                else:
                    fingers2.append(0)

                # 4 Fingers first hand
                for tId in range(1, 5):
                    if landmarks2[tipIds[tId]][2] < landmarks2[tipIds[tId] - 2][2]:
                        fingers2.append(1)
                    else:
                        fingers2.append(0)

                totalFingers2 = fingers2.count(1)

                totalFingers = totalFingers1 + totalFingers2

                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)

                # Tested but too fast
                # sound = pyglet.resource.media(os.path.dirname(__file__) + "/media/" + sounds[sound_index - 1], streaming=False)
                # sound.play()

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

        cv2.imshow("Image", img)

        key = cv2.waitKey(1)
        if key == ord('q'):  # to stop the program
            exit(-1)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
