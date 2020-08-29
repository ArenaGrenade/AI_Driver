# import pyautogui
import cv2
import numpy as np
import time
from DirectInput import PressKey, ReleaseKey, UP
from mss import mss

if __name__ == '__main__':
    prev_time = time.time()
    print("A small wait for you to transfer window control the the testing application")

    capture_dim = {'left': 0, 'top': 32, 'width': 796, 'height': 600}
    sct = mss()

    frame = 0

    time.sleep(2)
    print("Starting Now....")

    # Main Loop
    while True:
        screen_capture = np.array(sct.grab(capture_dim))
        cv2.imshow("Original Screen Capture", screen_capture)
        frame += 1

        if (time.time() - prev_time) >= 1:
            prev_time = time.time()
            print("Last second had {} fps".format(frame))
            frame = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
