import cv2


class Processor:
    def __init__(self, screen):
        self.color_image = screen
        self.greyscale_image = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
