import os, shutil

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import numpy as np


from tabs.Split_tab import Split_tab as Split_Tab

# TODO: implement the changing of label sizes when resizing the window after setting image
# TODO: debug the finger tab label resizing issues




# Class for the Vain Pattern Tab
# This class is responsible for the layout and functionality of the Vain Pattern Tab
# for the vain pattern segmentation model output
class VainPatternTab(Split_Tab):
    _graph_points = []
    _graph_points_for_original = []

    def detect_white_points(self, image):
        _, binary = cv2.threshold(image.astype(np.uint8), 2, 255, cv2.THRESH_BINARY)
        white_points_indices = np.column_stack(np.where(binary != 0))
        white_points = [(point[1], point[0]) for point in white_points_indices]
        return white_points


    def draw_points(self):
        self.central_widget.draw_graph(self.graph_points)
        self.right_widget.draw_graph(self.graph_points_for_original)

    def set_img_to_labels(self, img_orig, img_mask):
        self.set_img_and_mask(cv2.cvtColor(img_mask, cv2.COLOR_GRAY2RGB), img_orig)
        self._graph_points = self.detect_white_points(img_mask)

        if img_mask.shape == img_orig.shape:
            self._graph_points_for_original = self._graph_points
        else:
            width_ratio = img_orig.shape[1] / img_mask.shape[1]
            height_ratio = img_orig.shape[0] / img_mask.shape[0]
            self._graph_points_for_original = []
            for point in self._graph_points:
                self._graph_points_for_original.append([int(point[0] * width_ratio), int(point[1] * height_ratio)])

        self.central_widget.draw_graph(self.graph_points)
        self.right_widget.draw_graph(self.graph_points_for_original)




