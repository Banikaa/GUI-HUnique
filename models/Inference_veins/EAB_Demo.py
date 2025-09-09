import cv2
import numpy as np


def initialize_model(data_type="RGB"):
    pass




def process_image(image, model):
    mask = cv2.imread(
        '/Users/banika/Desktop/GUI_primary/gui_application_test/program copy 5.09 before infrared vein/restult-3.png')
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    return mask


