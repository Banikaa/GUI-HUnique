import os, shutil

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import numpy as np

from widgets.labels import PhotoDescriptionLabel as photo_descript_lbl
from widgets.labels import Label as lbl
from widgets.buttons import CheckBox as check_box
from widgets.buttons import Button as btn

# Class for the Creating a TAB with split screen view
# This class is responsible for the layout and functionality of the Vain Pattern Tab
# for the vain pattern segmentation model output
#
#     WHEN EXTENDING THIS, NEED TO ADD THE
    #     "detect_white_points"
    #     "set_img_to_labels"
    #     "draw_points"
    #     FUNCTIONS
# def detect_white_points(self, img_path):
#     specific for each class needs
#
class Split_tab(QWidget):

    _tab_name = ''
    _tab_description = ''
    _tab_color = 'grey'
    _is_label_hidden = False
    _graph_points = []
    _graph_points_for_original = []
    _main_window = None
    _photo_viewer_label = None
    _photo_ready = False
    _central_img_np_array = []
    _right_img_np_array = []
    _screen_widget = None
    _screen_widget_layout = None
    _model_output_widget_layout = None
    _central_widget = None
    _central_photo_label = None
    _right_widget = None
    _right_photo_label = None

    _green_btn = None
    _white_btn = None
    _draw_btn = None
    _w1 = None
    _w2 = None
    _w3 = None
    _zoom_sync_btn = None
    _reset_zoom_btn = None



    def __init__(self, main_window, tab_name, tab_description):
        super().__init__()
        self._tab_name = tab_name
        self._tab_description = tab_description
        self._main_window = main_window
        self.initUI()


    # setting up the layout and widgets for the vain pattern tab
    def initUI(self):
        self._screen_widget = QWidget()
        self._screen_widget.setObjectName(self._tab_description)
        self._screen_widget_layout = QVBoxLayout()
        self._screen_widget_layout.setContentsMargins(0, 0, 0, 0)
        self._screen_widget_layout.setSpacing(0)
        self._model_output_widget_layout = QHBoxLayout()
        # central widget setup
        self._central_photo_label = photo_descript_lbl.PhotoDescriptionLabel('central_photo_label', 'Photo', 'grey', False, True)
        self._central_widget = self._central_photo_label.get_label()
        self._central_photo_label.setScaledContents(True)
        self._central_photo_label.change_text_part_to_button('Photo View', self.focus_tab)
        self._model_output_widget_layout.addWidget(self._central_photo_label, 1)
        self._central_widget.set_parent(self)
        # right widget setup
        self._right_photo_label = photo_descript_lbl.PhotoDescriptionLabel('right_photo_label', 'Graph','grey', False, True)
        self._right_widget = self._right_photo_label.get_label()
        self._right_photo_label.change_text_part_to_button('Graph View', self.focus_tab)
        self._right_photo_label.setStyleSheet("border: 1px solid black;")
        self._model_output_widget_layout.addWidget(self._right_photo_label, 1)
        self._right_widget.set_parent(self)
        # setting up the layout of the model output tab for vain pattern segmentation
        self._screen_widget_layout.addWidget(self.tool_bar(), 1)
        self._screen_widget_layout.addLayout(self._model_output_widget_layout, 10)
        self._screen_widget.setLayout(self._screen_widget_layout)


    # called in main
    # sets the photo viewer label to the given label
    # @param view_label: string
    def set_photo_labels(self, view_label):
        self._draw_btn.setChecked(True)
        self._w1.setChecked(True)

        self.set_photo_viewer_label(view_label)
        img_fname = view_label.get_img()
        if img_fname == '':
            return
        self._photo_ready = True
        self._img_path = img_fname
        self.set_img_to_labels(img_fname)


    # returns an instance of the current tab
    def get_tab(self):
        return self._screen_widget


    # sets the photo viewer label variable to the given label
    # @param photo_viewer_label: string
    def set_photo_viewer_label(self, photo_viewer_label):
        self._photo_viewer_label = photo_viewer_label


    # getter for the photo viewer label
    def get_photo_viewer_label(self):
        return self._photo_viewer_label


    def sync_zoom(self, zoom_factor, delta_x, delta_y):
        self._right_widget.sync_zoom(zoom_factor)
        self._central_widget.sync_zoom(zoom_factor)
        self._right_widget.set_delta_pixmap(delta_x, delta_y)
        self._central_widget.set_delta_pixmap(delta_x, delta_y)


    # focuses on the correct viewer label when pressing the buttons
    # responsible for the switching between the central and right viewer labels
    # and changing the dimensions of the labels and buttons
    def focus_tab(self):
        # print('screen width: {w}'.format(w=self.screen_widget.width()))
        # print('central width: {w}'.format(w=self.central_widget.width()))
        # print('right width: {w}'.format(w=self.right_widget.width()))
        # print('--------------------------------------')

        sender_button = self.sender().objectName()
        if sender_button == 'central_photo_label':      # switch to central viewer label and back
            if not self._is_label_hidden:
                self.model_output_widget_layout.removeWidget(self._right_photo_label)
                self.right_photo_label.hide()
                self.central_photo_label.set_width(self._screen_widget.width())
                self.central_widget.set_width(self._screen_widget.width())
                if self.photo_ready:
                    self._central_photo_label.set_img_from_np_array(self._central_img_np_array)
                self._is_label_hidden = True
            else:
                self._model_output_widget_layout.removeWidget(self._right_photo_label)
                self._model_output_widget_layout.removeWidget(self._central_photo_label)
                self.set_label_half_screen_width()
                self._model_output_widget_layout.addWidget(self._central_photo_label, 1)
                self._model_output_widget_layout.addWidget(self._right_photo_label, 1)
                self._right_photo_label.show()
                self._is_label_hidden = False
                if self._photo_ready:
                    self.set_label_half_screen_width()
                    self._right_photo_label.set_img_from_np_array(self._right_img_np_array, False)
                    self._central_photo_label.set_img_from_np_array(self._central_img_np_array, False)

        elif sender_button == 'right_photo_label':      # switch to right viewer label and back
            if not self._is_label_hidden:
                self._model_output_widget_layout.removeWidget(self._central_photo_label)
                self._central_photo_label.hide()
                self._right_photo_label.set_width(self._screen_widget.width())
                self._right_widget.set_width(self._screen_widget.width())
                if self._photo_ready:
                    self._right_photo_label.set_img_from_np_array(self._right_img_np_array)
                self._is_label_hidden = True
            else:
                self._model_output_widget_layout.removeWidget(self._right_photo_label)
                self._model_output_widget_layout.removeWidget(self._central_photo_label)
                self.set_label_half_screen_width()
                self._model_output_widget_layout.addWidget(self._central_photo_label, 1)
                self._model_output_widget_layout.addWidget(self._right_photo_label, 1)
                self._central_photo_label.show()
                self._is_label_hidden = False
                self.set_label_half_screen_width()
                if self._photo_ready:
                    self.set_label_half_screen_width()
                    self._central_photo_label.set_img_from_np_array(self._central_img_np_array, False)
                    self._right_photo_label.set_img_from_np_array(self._right_img_np_array, False)

        self._central_photo_label.update()
        self._right_photo_label.update()
        self.draw_points()


    # sets the width of the labels to half of the screen width
    def set_label_half_screen_width(self):
        screen_width = self._main_window.model_output.width()-100
        screen_height = self._main_window.model_output.height()-20
        self._central_photo_label.set_width(int(screen_width / 2))
        self._right_photo_label.set_width(int(screen_width / 2))
        self._central_widget.set_width(int(screen_width / 2))
        self._central_widget.set_height(int(screen_height))
        self._central_widget.set_height(int(screen_height))
        self._right_widget.set_width(int(screen_width / 2))
        self._central_widget.set_height(self._central_photo_label.height())
        self._right_widget.set_height(self._right_photo_label.height())
        self.update()


    def set_label_screen_width(self):
        screen_width = self._screen_widget.width()-50
        self._central_photo_label.set_width(int(screen_width))
        self._right_photo_label.set_width(int(screen_width))
        self._central_widget.set_width(int(screen_width))
        self._right_widget.set_width(int(screen_width))


    # sets the image to the labels
    # TODO: change the model output to a method in main to get that

    def set_img_and_mask(self, img_mask, img_orig):
        self._photo_ready = True

        self._right_photo_label.set_width(int(self._main_window.model_output.width()/2-50))
        self._central_photo_label.set_width(int(self._main_window.model_output.width()/2-50))
        self._right_widget.set_width(int(self._main_window.model_output.width()/2-50))
        self._central_widget.set_width(int(self._main_window.model_output.width()/2-50))

        self._central_img_np_array = img_mask
        self._right_img_np_array = img_orig
        self._central_widget.set_width(int(self._main_window.output_tabs.width()-50 / 2))
        self._central_widget.set_height(self._central_photo_label.height())
        self._right_widget.set_width(int(self._main_window.output_tabs.width()-50 / 2))
        self._right_widget.set_height(self._right_photo_label.height())
        self._right_widget.set_label_img_from_np_array(img_orig)
        self._central_widget.set_label_img_from_np_array(img_mask)

        self._right_photo_label.set_width(self._right_widget.newWidth)
        self._central_photo_label.set_width(self._central_widget.newWidth)
        self.update()


    def reset(self):
        self._photo_ready = False
        self._central_img_np_array = []
        self._right_img_np_array = []
        self._central_widget.setText('')
        self._right_widget.setText('')
        self._central_widget.set_image('')
        self._right_widget.set_image('')
        self.set_label_half_screen_width()


    def delete_points(self):
        self._central_widget.delete_points()
        self._right_widget.delete_points()


    def set_photo_ready(self, ready):
        self._photo_ready = ready


#---------------------------------------------------------------
#---------------------TOOL BAR SETUP---------------------------
#---------------------------------------------------------------
    def tool_bar(self):
        tool_bar = QToolBar()
        tool_bar.setMovable(False)

        self._green_btn = check_box.CheckBox('green_btn', 'Green', 'green')
        self._green_btn.clicked.connect(self.green_points)
        self._white_btn = check_box.CheckBox('white_btn', 'White', 'white')
        self._white_btn.clicked.connect(self.white_points)
        self._w1 = check_box.CheckBox('w1', 'w 1px', 'w1')
        self._w1.clicked.connect(self.w1_clicked)
        self._w2 = check_box.CheckBox('w2', 'w 2px', 'w2')
        self._w2.clicked.connect(self.w2_clicked)
        self._w3 = check_box.CheckBox('w3', 'w 3px', 'w3')
        self._w3.clicked.connect(self.w3_clicked)

        self._zoom_sync_btn = check_box.CheckBox('zoom_sync_btn', 'Sync Zoom', 'zoom_sync')
        self._zoom_sync_btn.clicked.connect(self.enable_sync)

        self._draw_btn = check_box.CheckBox('draw_btn', 'Draw', 'draw')
        self._draw_btn.clicked.connect(self.reset_zoom)

        tool_bar.addWidget(self._green_btn)
        tool_bar.addWidget(self._white_btn)
        tool_bar.addWidget(self._draw_btn)
        tool_bar.addWidget(self._w1)
        tool_bar.addWidget(self._w2)
        tool_bar.addWidget(self._w3)
        tool_bar.addWidget(self._zoom_sync_btn)
        tool_bar.addWidget(self._reset_zoom_btn)

        return tool_bar


    def draw_btn_clicked(self):
        if self._draw_btn.isChecked():
            self.draw_points()
        else:
            self._green_btn.setChecked(False)
            self._white_btn.setChecked(False)
            self.delete_points()


    def w1_clicked(self):
        self._w1.setChecked(True)
        self._w2.setChecked(False)
        self._w3.setChecked(False)
        self._central_widget.set_pen_point_width(1)
        self._right_widget.set_pen_point_width(1)


    def w2_clicked(self):
        self._w2.setChecked(True)
        self._w1.setChecked(False)
        self._w3.setChecked(False)
        self._central_widget.set_pen_point_width(2)
        self._right_widget.set_pen_point_width(2)


    def w3_clicked(self):
        self._w3.setChecked(True)
        self._w1.setChecked(False)
        self._w2.setChecked(False)
        self._central_widget.set_pen_point_width(3)
        self._right_widget.set_pen_point_width(3)


    def white_points(self):
        self._green_btn.setChecked(False)
        self._draw_btn.setChecked(True)
        self.draw_btn_clicked()
        self._central_widget.set_point_color('white')
        self._right_widget.set_point_color('white')


    def green_points(self):
        self._white_btn.setChecked(False)
        self._draw_btn.setChecked(True)
        self.draw_btn_clicked()
        self._central_widget.set_point_color('green')
        self._right_widget.set_point_color('green')


    def enable_sync(self):
        if self._zoom_sync_btn.isChecked():
            self._right_widget.set_sync_bool(True)
            self._central_widget.set_sync_bool(True)
        else:
            self._right_widget.set_sync_bool(False)
            self._central_widget.set_sync_bool(False)


    def reset_zoom(self):
        self._reset_zoom_btn.setChecked(False)
        self._right_widget.sync_zoom(1)
        self._central_widget.sync_zoom(1)
        self._right_widget.set_delta_pixmap(0, 0)
        self._central_widget.set_delta_pixmap(0, 0)


