import os, shutil

from PyQt5.QtWidgets import *


import cv2
import numpy as np

from tabs.Split_tab import Split_tab as Split_Tab



# TODO: implement the changing of label sizes when resizing the window after setting image
# TODO: debug the finger tab label resizing issues



# Class for the Vain Pattern Tab
# This class is responsible for the layout and functionality of the Vain Pattern Tab
# for the vain pattern segmentation model output

class LunuleSegTab(QWidget):
    _tab_name = ''
    _tab_description = ''
    _tab_color = 'grey'
    _main_window = None
    _finger_coord = {}
    _finger_tabs = []


    def __init__(self, main_window, tab_name, tab_description):
        super().__init__()
        self._tab_name = tab_name
        self._tab_description = tab_description
        self._main_window = main_window

        self._screen_widget = QTabWidget()
        self._screen_widget.setObjectName(tab_description)
        finger_1 = LunuleSegWidget(self._main_window, 'Finger 1', 'Finger 1')
        finger_2 = LunuleSegWidget(self._main_window, 'Finger 2', 'Finger 2')
        finger_3 = LunuleSegWidget(self._main_window, 'Finger 3', 'Finger 3')
        finger_4 = LunuleSegWidget(self._main_window, 'Finger 4', 'Finger 4')
        finger_5 = LunuleSegWidget(self._main_window, 'Finger 5', 'Finger 5')

        self._finger_tabs = [finger_1, finger_2, finger_3, finger_4, finger_5]

        finger_1_tab = finger_1.get_tab()
        finger_2_tab = finger_2.get_tab()
        finger_3_tab = finger_3.get_tab()
        finger_4_tab = finger_4.get_tab()
        finger_5_tab = finger_5.get_tab()

        self._screen_widget.addTab(finger_1_tab, 'Finger 1')
        self._screen_widget.addTab(finger_2_tab, 'Finger 2')
        self._screen_widget.addTab(finger_3_tab, 'Finger 3')
        self._screen_widget.addTab(finger_4_tab, 'Finger 4')
        self._screen_widget.addTab(finger_5_tab, 'Finger 5')
        self.tab_changed()
        self.update()
        self._screen_widget.currentChanged.connect(self.tab_changed)

    def reset(self):
        for finger in self._finger_tabs:
            finger.delete_points()
            finger.set_img_and_mask(np.zeros((100,100,3)), np.zeros((100,100,3)))

    def tab_changed(self):
        if self._finger_coord not in [{}, {1:None, 2:None, 3:None, 4: None, 5: None}]:
            finger_num = self._screen_widget.currentIndex()
            finger_num += 1
            if self._finger_coord[finger_num] is not None:
                self._main_window.reset_left_photo_label('lunule')
                ratio = self._main_window.get_left_photo_label('lunule').get_label_ratio()
                self._main_window.lunule_label.add_bounding_box(self._finger_coord[finger_num][0] * ratio,
                                                            self._finger_coord[finger_num][1] * ratio,
                                                            self._finger_coord[finger_num][2] * ratio,
                                                            self._finger_coord[finger_num][3] * ratio,
                                                            'red',
                                                            str("F" + str(finger_num)))
            self._main_window.update_left_photo_label('lunule')

    def get_lunule_index(self):
        return self._screen_widget.currentIndex() + 1


    # TODO add this
    def input_lunule_dict(self, lunule_mask, finger_img, finger_coord):
        self._finger_coord = finger_coord
        self._main_window.reset_left_photo_label('lunule')
        for i in range(1,6):
            if lunule_mask[i] is not None:
                self._finger_tabs[i-1].setEnabled(True)
                self._finger_tabs[i-1].set_img_to_labels(lunule_mask[i], finger_img[i])
            else:
                self._finger_tabs[i-1].setEnabled(False)
                self._finger_tabs[i-1].set_img_and_mask(np.zeros((100,100,3)), np.zeros((100,100,3)))
                self._finger_tabs[i-1].delete_points()

    def set_single_lunule(self, lunule_mask, finger_img, finger_num):
        # self._main_window.lunule_label.remove_bounding_box()
        # ratio = self._main_window.lunule_label.ratio
        # self._main_window.lunule_label.add_bounding_box(self._finger_coord[finger_num][0] * ratio,
        #                                                self._finger_coord[finger_num][1] * ratio,
        #                                                self._finger_coord[finger_num][2] * ratio,
        #                                                self._finger_coord[finger_num][3] * ratio,
        #                                                'red',
        #                                                str("F" + str(finger_num)))
        # self._main_window.lunule_label.update()
        self._finger_tabs[finger_num-1].setEnabled(True)
        self._finger_tabs[finger_num-1].set_img_to_labels(lunule_mask, finger_img)


    def get_tab(self):
        return self._screen_widget



class LunuleSegWidget(Split_Tab):
    _graph_points = []


    def detect_white_points(self, image):
        # image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        border_points = []
        _, binary = cv2.threshold(image, 2, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            border_points.append(contour.squeeze())
        return border_points


    def draw_points(self):
        self.central_widget.draw_points(self.graph_points)
        self.right_widget.draw_points(self.graph_points)


    def set_img_to_labels(self, img_mask, img_orig):
        mask_to_rgb = np.stack((img_mask,) * 3, axis = -1)
        self.set_img_and_mask(mask_to_rgb, img_orig)
        self._graph_points = []
        self._graph_points = self.detect_white_points(img_mask)
        self.central_widget.draw_points(self._graph_points)
        self.right_widget.draw_points(self._graph_points)


