import cv2
import pytesseract
import numpy as np
import imutils


class Processor:
    def __init__(self, screen):
        self.color_image = screen
        self.greyscale_image = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    def get_speed(self):
        (odys, odye, odxs, odxe) = (520, 570, 675, 755)
        # (odys, odye, odxs, odxe) = (520, 570, 725, 755)

        speed_image = self.greyscale_image[odys:odye, odxs:odxe]
        speed_image = cv2.GaussianBlur(speed_image, (3, 3), 0)
        speed_image = cv2.threshold(speed_image, 150, 255, cv2.THRESH_BINARY)[1]
        # speed_image = cv2.Canny(speed_image, 30, 200)

        DIGITS_LOOKUP = {
            (1, 1, 1, 0, 1, 1, 1): 0,
            (0, 0, 1, 0, 0, 1, 0): 1,
            (1, 0, 1, 1, 1, 1, 0): 2,
            (1, 0, 1, 1, 0, 1, 1): 3,
            (0, 1, 1, 1, 0, 1, 0): 4,
            (1, 1, 0, 1, 0, 1, 1): 5,
            (1, 1, 0, 1, 1, 1, 1): 6,
            (1, 0, 1, 0, 0, 1, 0): 7,
            (1, 1, 1, 1, 1, 1, 1): 8,
            (1, 1, 1, 1, 0, 1, 1): 9
        }

        cnts = cv2.findContours(speed_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        digitCnts = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= 5 and 23 <= h <= 30:
                digitCnts.append(c)

        for dg in digitCnts:
            (x, y, w, h) = cv2.boundingRect(dg)
            # cv2.rectangle(self.color_image[odys:odye, odxs:odxe], (x, y), (x + w, y + h), (0, 0, 255), 2)

        digitCnts = self.sort_contours(digitCnts, method='left-to-right')
        digits = []

        roi = []
        for bbox in digitCnts:
            (x, y, w, h) = bbox
            roi = speed_image[y:y + h, x:x + w]

            (roiH, roiW) = roi.shape
            (dW, dH) = (int(roiW * 0.18), int(roiH * 0.12))
            dHC = int(roiH * 0.05)
            dWC = int(roiW * 0.2)

            segments = [
                ((x, y), (x + w, y + dH)),  # 0 top
                ((x + dWC, y), (x + dW + dWC, y + (h // 2))),  # 1 top-left
                ((x + w - dW - dWC, y), (x + w, y + h // 2)),  # 2 top-right
                ((x, y + (h // 2) - dHC), (x + w, y + (h // 2) + dHC)),  # 3 center
                ((x, y + h // 2), (x + dW, y + h)),  # 4 bottom-left
                ((x + w - dW - dWC, y + h // 2), (x + w - dWC, y + h)),  # 5 bottom-right
                ((x, y + h - dH), (x + w, y + h))  # 6 bottom
            ]
            '''Next two for testing purposes
            ((xA, yA), (xB, yB)) = segments[2]
            cv2.rectangle(self.color_image[odys:odye, odxs:odxe], (xA, yA), (xB, yB), (255, 0, 0), 1)
            segROI = roi[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)'''
            on = [0] * len(segments)
            for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
                cv2.rectangle(self.color_image[odys:odye, odxs:odxe], (xA, yA), (xB, yB), (255, 0, 0), -1)

                segROI = roi[yA:yB, xA:xB]
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)

                if area != 0 and total / float(area) > 0.5:
                    on[i] = 1
            digit = DIGITS_LOOKUP.get(tuple(on))
            digits.append(digit)
            cv2.rectangle(self.color_image[odys:odye, odxs:odxe], (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(self.color_image[odys:odye, odxs:odxe], str(digit), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 2)

        return self.color_image[odys:odye, odxs:odxe], 0
        # return roi, 0

    def sort_contours(self, contours, method='left'):
        bboxes = [cv2.boundingRect(cnt) for cnt in contours]
        return sorted(bboxes, key=lambda x: x[0] + x[1])

