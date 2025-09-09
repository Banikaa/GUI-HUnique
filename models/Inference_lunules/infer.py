import os

import cv2
import numpy as np
from PIL import Image

class LunuleInference:
    def __init__(self, model_path='./lunule.pth'):
        self.ct = 0
        self.t_return_photo = '/Users/banika/Desktop/inference_gui_test/masks/Andrei-00002-Ex4-10.png'


    def build_model(self, model_path):
        print('model built')
        pass



    def inference(self, img):
        mask = cv2.imread(
            '/Users/banika/Desktop/GUI_primary/gui_application_test/program copy 5.09 before infrared vein/restult-3.png')
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        return mask

