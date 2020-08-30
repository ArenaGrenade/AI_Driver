import cv2
import numpy as np
import time
from DirectInput import PressKey, ReleaseKey, UP
from image_processor import *
from mss import mss
import pytesseract

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    prev_time = time.time()
    print("A small wait for you to transfer window control the the testing application")

    capture_dim = {'left': 0, 'top': 32, 'width': 796, 'height': 600}
    sct = mss()

    frame = 0

    time.sleep(2)
    print("Starting Now....")

    test_img = np.zeros(shape=(200, 300, 3)).astype('uint8')
    cv2.imshow('Speed Frame', test_img)
    cv2.moveWindow('Speed Frame', 100, 700)
    cv2.waitKey(1)

    # Main Loop
    while True:
        screen_capture = np.array(sct.grab(capture_dim))
        # cv2.imshow("Original Screen Capture", screen_capture)
        frame += 1

        image_processor = Processor(screen_capture)

        if (time.time() - prev_time) >= 1:
            prev_time = time.time()
            # print("Last second had {} fps".format(frame))
            cv2.putText(
                screen_capture,
                "{} fps".format(frame),
                (796, 600),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 2)
            frame = 0

        im, txt = image_processor.get_speed()
        cv2.imshow("Speed Frame", im)
        # print(txt)

        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            cv2.destroyAllWindows()
            break
        elif keypress == ord('s'):
            cv2.imwrite("./screenshot_test.jpg", screen_capture)
            print("Saved Image")
