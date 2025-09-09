import cv2
import numpy as np
import torch


class TatooInference:
    def __init__(self, model_path='./tatoo.pth'):
        pass

    def build_model(self, model_path='/home/hunique/Desktop/GUI/gui_application_test/program/models/Inference_tatoos/tatoo.pth'):
        pass


    @torch.no_grad()
    def inference(self,
                  img,):  # input: is numpy array of shape (H, W, C) [0,255]

        mask = cv2.imread('/Users/banika/Desktop/GUI_primary/gui_application_test/program copy 5.09 before infrared vein/restult-3.png')
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        return mask

