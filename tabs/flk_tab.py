import os, shutil, time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from widgets.labels import PhotoDescriptionLabel as photo_descript_lbl
from widgets.labels import Label as lbl
from widgets.buttons import CheckBox as check_box



class FlkTab(QLabel):

    _name = None
    _photo_ready = False
    _screen_widget = None
    _grid_layout = None
    _main_window = None
    _img_np_array = None
    _model_output = None
    _photo_viewer_label = None
    _hand_side = 'left'
    _hand_position = 'dorsal'
    _label_height = 400
    _label_width = 300

    _fingers = []
    _knuckles_m = []
    _knuckles_M = []
    _knuckles_b = []

    _angle_dict = None
    _model_output_dict = None

    _finger_btn = None
    _knuckle_m_btn = None
    _knuckle_M_btn = None
    _knuckle_b_btn = None
    _all_included = None
    _add_bndboxes = None
    _small_labels = None
    _medium_labels = None
    _large_labels = None
    _input_conf_threshold = None
    _conf_button = None
    _togle_left_right = None


    def __init__(self, main_window, name):

        super(FlkTab, self).__init__()
        self.setObjectName(name)
        self._name = name
        self._main_window = main_window
        self._screen_widget = QWidget()
        self._screen_widget.setObjectName(name)

        # setting up the main tab layout
        screen_widget_layout = QVBoxLayout()
        screen_widget_layout.setContentsMargins(0, 0, 0, 0)
        screen_widget_layout.setSpacing(0)
        screen_widget_layout.setStretch(0, 1)
        screen_widget_layout.setStretch(1, 9)
        screen_widget_layout.addWidget(self.tool_bar(), stretch=1)

        image_grid = QWidget()
        self._grid_layout = QGridLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)

        self.set_initial_state_labels()

        image_grid.setLayout(self._grid_layout)
        scroll_area.setWidget(image_grid)
        screen_widget_layout.addWidget(scroll_area, stretch=9)
        self._screen_widget.setLayout(screen_widget_layout)

    def set_photo_ready(self, photo_ready):
        self._photo_ready = photo_ready


    # setting up the labels in the tab that will contain each feature subimage after localization
    def set_initial_state_labels(self):
        finger_1 = photo_descript_lbl.PhotoDescriptionLabel(
            'finger_1', 'Finger 1', 'red', False, stretch=True)
        finger_2 = photo_descript_lbl.PhotoDescriptionLabel(
            'finger_2', 'Finger 2', 'red', True, stretch=True)
        finger_3 = photo_descript_lbl.PhotoDescriptionLabel(
            'finger_3', 'Finger 3', 'red', True, stretch=True)
        finger_4 = photo_descript_lbl.PhotoDescriptionLabel(
            'finger_4', 'Finger 4', 'red', True, stretch=True)
        finger_5 = photo_descript_lbl.PhotoDescriptionLabel(
            'finger_5', 'Finger 5', 'red', True, stretch=True)

        knuckle_m_1 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_m_1', 'Knuckle m 1', 'green', True, stretch=True)
        knuckle_m_2 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_m_2', 'Knuckle m 2', 'green', True, stretch=True)
        knuckle_m_3 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_m_3', 'Knuckle m 3', 'green', True, stretch=True)
        knuckle_m_4 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_m_4', 'Knuckle m 4' , 'green', True, stretch=True)
        knuckle_m_5 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_m_5', 'Knuckle m 5' , 'green', True, stretch=True)

        knuckle_M_5 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_M_5', 'Knuckle M 5', '#40E0D0' , True, stretch=True)
        knuckle_M_4 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_M_4', 'Knuckle M 4', '#40E0D0' , True, stretch=True)
        knuckle_M_3 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_M_3', 'Knuckle M 3', '#40E0D0', True , stretch=True)
        knuckle_M_2 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_M_2', 'Knuckle M 2', '#40E0D0' , True, stretch=True)
        knuckle_M_1 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_M_1', 'Knuckle M 1', '#40E0D0' , True, stretch=True)

        knuckle_b_1 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_b_1', 'Knuckle B 1', 'purple', True, stretch=True)
        knuckle_b_2 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_b_2', 'Knuckle B 2', 'purple', True, stretch=True)
        knuckle_b_3 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_b_3', 'Knuckle B 3', 'purple', True, stretch=True)
        knuckle_b_4 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_b_4', 'Knuckle B 4', 'purple', True, stretch=True)
        knuckle_b_5 = photo_descript_lbl.PhotoDescriptionLabel(
            'knuckle_b_5', 'Knuckle B 5', 'purple', True, stretch=True)

        self._fingers = [finger_1, finger_2, finger_3, finger_4, finger_5]
        self._knuckles_m = [knuckle_m_1, knuckle_m_2, knuckle_m_3, knuckle_m_4, knuckle_m_5]
        self._knuckles_M = [knuckle_M_1, knuckle_M_2, knuckle_M_3, knuckle_M_4, knuckle_M_5]
        self._knuckles_b = [knuckle_b_1, knuckle_b_2, knuckle_b_3, knuckle_b_4, knuckle_b_5]

        for label in self._fingers:
            label.set_height(self._label_height)
            label.set_width(self._label_width)
        for label in self._knuckles_m:
            label.set_height(self._label_height)
            label.set_width(self._label_width)
        for label in self._knuckles_M:
            label.set_height(self._label_height)
            label.set_width(self._label_width)
        for label in self._knuckles_b:
            label.set_height(self._label_height)
            label.set_width(self._label_width)


    # set the viever label variable to the current photo shown
    def set_photo_viewer_label(self, photo_viewer_label):
        self._photo_viewer_label = photo_viewer_label

    # get the viewer label variable
    def get_photo_viewer_label(self):
        return self._photo_viewer_label


    # retrurn the widget that contains the whole tab
    def get_tab(self):
        return self._screen_widget



    # set all the labels to the correct subimages
    # after frcnn is run on the image and the subimage coordanes are found
    def set_photo_labels(self, model_output, img_np_array, finger_angles_dict):
        self._photo_ready = True
        self._angle_dict = finger_angles_dict
        self._img_np_array = img_np_array
        self._model_output = model_output
        self.delete_labels()
        self.set_initial_state_labels()
        self.set_img_from_bndbox_dict(model_output, img_np_array, finger_angles_dict)


    # set all the labels to the correct subimages
    def set_img_from_bndbox_dict(self, model_output, img_np_array, finger_angles_dict):
        output_dict = {}
        output_dict['f'] = [model_output['f1'], model_output['f2'], model_output['f3'], model_output['f4'], model_output['f5']]
        output_dict['k_m'] = [model_output['k_m1'], model_output['k_m2'], model_output['k_m3'], model_output['k_m4']]
        output_dict['k_M'] = [model_output['k_M1'], model_output['k_M2'], model_output['k_M3'], model_output['k_M4'], model_output['k_M5']]
        output_dict['k_b'] = [model_output['k_b1'], model_output['k_b2'], model_output['k_b3'], model_output['k_b4'], model_output['k_b5']]

        self.set_images(output_dict, img_np_array, finger_angles_dict)
        self._all_included.setChecked(True)
        self.paint_buttons()




    def set_images(self,model_output, img_np_array, finger_angles_dict):
        self._model_output_dict = model_output
        for ct in [0, 1, 2, 3, 4]:
            if model_output['f'][ct] is not None:
                self._fingers[ct].set_image_cropped(
                    model_output['f'][ct][0], model_output['f'][ct][1], model_output['f'][ct][2], model_output['f'][ct][3],
                    img_np_array, finger_angles_dict[ct + 1])
            if ct < 4:
                if model_output['k_m'][ct] is not None:
                    self._knuckles_m[ct].set_image_cropped(
                        model_output['k_m'][ct][0], model_output['k_m'][ct][1], model_output['k_m'][ct][2],
                        model_output['k_m'][ct][3], img_np_array, finger_angles_dict[ct + 1])
            if model_output['k_M'][ct] is not None:
                self._knuckles_M[ct].set_image_cropped(
                    model_output['k_M'][ct][0], model_output['k_M'][ct][1], model_output['k_M'][ct][2],
                    model_output['k_M'][ct][3], img_np_array, finger_angles_dict[ct + 1])
            if model_output['k_b'][ct] is not None:
                self._knuckles_b[ct].set_image_cropped(
                    model_output['k_b'][ct][0], model_output['k_b'][ct][1], model_output['k_b'][ct][2],
                    model_output['k_b'][ct][3], img_np_array, finger_angles_dict[ct + 1])


    # get the x ccordinate of the box center
    def get_box_center_x(self, box):
        return (box[0] + box[1]) / 2


    # calculate the relative position of the subimage to the main image
    def calculate_relative_position(self, image_coords, subimage_coords, margin=0):

        image_x_center = self.get_box_center_x(image_coords)
        subimage_x_center = self.get_box_center_x(subimage_coords)

        relative_min_y = image_coords[1] - subimage_coords[1]
        relative_max_y = image_coords[3] - subimage_coords[3]

        if image_x_center > subimage_x_center:
            relative_min_x = image_coords[0] - subimage_coords[0]
            relative_max_x = image_coords[2] - subimage_coords[2]
        else:
            relative_min_x = subimage_coords[0] - image_coords[0]
            relative_max_x = subimage_coords[2] - image_coords[2]
            relative_min_y *= -1
            relative_max_y *= -1

        if relative_min_x < 0:
            relative_min_x = 0
        if relative_min_y < 0:
            relative_min_y = 0 + margin

        return relative_min_x, relative_min_y, relative_max_x, relative_max_y

    # delete all the labels between each image change
    def delete_labels(self):
        for finger in self._fingers:
            finger.delete()
        for knuckle_m in self._knuckles_m:
            knuckle_m.delete()
        for knuckle_M in self._knuckles_M:
            knuckle_M.delete()
        for knuckle_b in self._knuckles_b:
            knuckle_b.delete()

    # main method called for initialising the labels and the bounding boxes
    # called after each state chantes in the toolbar checkboxes
    def paint_buttons(self):

        widget_counter = 0
        if self._all_included.isChecked():
            self._finger_btn.setChecked(True)
            self._knuckle_m_btn.setChecked(True)
            self._knuckle_M_btn.setChecked(True)
            self._knuckle_b_btn.setChecked(True)
            self._all_included.setChecked(False)
            self.paint_buttons()

        if self._finger_btn.isChecked():
            i = 0
            for finger in self._fingers:
                self._grid_layout.addWidget(finger, widget_counter, i)
                i += 1
                finger.show()
            widget_counter += 1
        else:
            self._all_included.setChecked(False)
            for finger in self._fingers:
                self._grid_layout.removeWidget(finger)
                finger.hide()

        if self._knuckle_m_btn.isChecked():
            i=0
            for knuckle_m in self._knuckles_m:
                self._grid_layout.addWidget(knuckle_m, widget_counter, i)
                i += 1
                knuckle_m.show()

            widget_counter += 1
        else:
            for knuckle_m in self._knuckles_m:
                self._grid_layout.removeWidget(knuckle_m)
                knuckle_m.hide()

        if self._knuckle_M_btn.isChecked():
            i = 0
            for knuckle_M in self._knuckles_M:
                self._grid_layout.addWidget(knuckle_M, widget_counter, i)
                i += 1
                knuckle_M.show()
            widget_counter += 1
        else:
            for knuckle_M in self._knuckles_M:
                self._grid_layout.removeWidget(knuckle_M)
                knuckle_M.hide()

        if self._knuckle_b_btn.isChecked():
            i=0
            for knuckle_b in self._knuckles_b:
                self._grid_layout.addWidget(knuckle_b, widget_counter, i)
                i += 1
                knuckle_b.show()
            widget_counter += 1
        else:
            for knuckle_b in self._knuckles_b:
                self._grid_layout.removeWidget(knuckle_b)
                knuckle_b.hide()

        self._main_window.reset_left_photo_label(self._name)

        label = self._main_window.get_left_photo_label_by_name(self._name)

        # draw the bounding boxes on the main image label for each feature if that specific checkbox in checked
        if self._add_bndboxes.isChecked():
            if self._photo_ready:
                height_r = label.get_height_ratio()
                width_r = label.get_width_ratio()
                if self._finger_btn.isChecked():
                    ct = 0
                    for finger in self._model_output_dict['f']:
                        if finger:
                            label.add_bounding_box((finger[0]+ 7.5) * height_r, (finger[1]+ 7.5) * width_r,
                                                                                 (finger[2]+ 7.5) * height_r, (finger[3]+ 7.5) * width_r,
                                                                                 'red', 'f' + str(ct + 1))
                        ct+=1

                if self._knuckle_m_btn.isChecked():
                    ct = 0
                    for knuckle_m in self._model_output_dict['k_m']:
                        if knuckle_m:
                            label.add_bounding_box((knuckle_m[0]+ 7.5) * height_r,
                                                                                 (knuckle_m[1]+ 7.5) * width_r,
                                                                                 (knuckle_m[2]+ 7.5) * height_r,
                                                                                 (knuckle_m[3]+ 7.5) * width_r,
                                                                                 'green', 'km' + str(ct + 1))
                        ct += 1

                if self._knuckle_M_btn.isChecked():
                    ct = 0
                    for knuckle_M in self._model_output_dict['k_M']:
                        if knuckle_M:
                            label.add_bounding_box((knuckle_M[0]+ 7.5) * height_r,
                                                                                 (knuckle_M[1]+ 7.5) * width_r,
                                                                                 (knuckle_M[2]+ 7.5) * height_r,
                                                                                 (knuckle_M[3]+ 7.5) * width_r,
                                                                                 '#40E0D0', 'kM' + str(ct + 1))
                        ct+=1
                if self._knuckle_b_btn.isChecked():
                    ct = 0
                    for knuckle_b in self._model_output_dict['k_b']:
                        if knuckle_b:
                            label.add_bounding_box((knuckle_b[0]+ 7.5) * height_r,
                                                                                 (knuckle_b[1]+ 7.5) * width_r,
                                                                                 (knuckle_b[2]+ 7.5) * height_r,
                                                                                 (knuckle_b[3]+ 7.5) * width_r,
                                                                                 'purple', 'kb' + str(ct + 1))
                        ct+=1
        else:
            label.remove_bounding_box()


#------------------------------------------------------------------------
#----------------------  METHODS FOR THE MENU BAR -------------------------
#------------------------------------------------------------------------

    # show the legend on the main image label
    # each feature name with the color of the bounding box
    def show_legend(self):
        self._main_window.flk_label.draw_text('Fingernails', 'red')
        self._main_window.flk_label.draw_text('Knuckles minor', 'green')
        self._main_window.flk_label.draw_text('Knuckles Major', '#40E0D0')
        self._main_window.flk_label.draw_text('Knuckles base', 'purple')

    # hide the legend on the main image label
    def hide_legend(self):
        self._main_window.flk_label.delete_text()

# ------------------------------------------------------------------------
# ----------------------  METHODS FOR THE MENU BAR -------------------------
# ------------------------------------------------------------------------

    def change_label_dimension(self):
        sender = self.sender().objectName()
        if self._small_labels.isChecked() and sender == 'small_labels':
            self._medium_labels.setChecked(False)
            self._large_labels.setChecked(False)
            height = 400
            width = 300
        elif self._medium_labels.isChecked() and sender == 'medium_labels':
            self._small_labels.setChecked(False)
            self._large_labels.setChecked(False)
            height = 550
            width = 400
        elif self._large_labels.isChecked() and sender == 'large_labels':
            self._small_labels.setChecked(False)
            self._medium_labels.setChecked(False)
            height = 750
            width = 600
        else:
            return
        self._small_labels.setDisabled(True)
        self._medium_labels.setDisabled(True)
        self._large_labels.setDisabled(True)

        self._label_height = height
        self._label_width = width

        if self._photo_ready:
            self.set_photo_labels(self._model_output, self._img_np_array, self._angle_dict)
        else:
            for label in self._fingers:
                label.set_height(height)
                label.set_width(width)
            for label in self._knuckles_m:
                label.set_height(height)
                label.set_width(width)
            for label in self._knuckles_M:
                label.set_height(height)
                label.set_width(width)
            for label in self._knuckles_b:
                label.set_height(height)
                label.set_width(width)


        self._small_labels.setDisabled(False)
        self._medium_labels.setDisabled(False)
        self._large_labels.setDisabled(False)


    def toggle_hand_side(self, checked):
        if checked:
            self._togle_left_right.setText("right")
            self._hand_side = 'left'
        else:
            self._togle_left_right.setText("right")
            self._hand_side = 'left'

    def toggle_palmar_position(self, checked):
        if checked:
            self._toggle_palmar_dorsal.setText("Palmar")
            self._hand_position = 'palmar'
        else:
            self._toggle_palmar_dorsal.setText("Dorsal")
            self._hand_position = 'dorsal'

    def get_hand_side(self):
        return self._hand_side

    def get_hand_position(self):
        return self._hand_position


    def set_conf_threshold(self):
        self._main_window.set_confidence_threshold_flk(float(self._input_conf_threshold.text()))

    # initialise the toolbar containing the checkboxes
    def tool_bar(self):
        tool_bar =  QToolBar()
        tool_bar.setMovable(False)
        self._finger_btn = check_box.CheckBox('finger_check', 'Fingers', self)
        self._knuckle_m_btn = check_box.CheckBox('knuckle_m_check','Knuckles minor', self)
        self._knuckle_M_btn = check_box.CheckBox('knuckle_M_check','Knuckles major', self)
        self._knuckle_b_btn = check_box.CheckBox('knuckle_b_check','Knuckles base', self)
        self._all_included = check_box.CheckBox('all_included', 'Select all', self)
        self._add_bndboxes = check_box.CheckBox('add_bndboxes', 'Add Bounding Boxes', self)
        self._small_labels = check_box.CheckBox('small_labels', 'Small Labels', self)
        self._medium_labels = check_box.CheckBox('medium_labels', 'Medium Labels', self)
        self._large_labels = check_box.CheckBox('large_labels', 'Large Labels', self)
        self._input_conf_threshold = QLineEdit()
        self._input_conf_threshold.setPlaceholderText('Confidence Threshold')
        self._input_conf_threshold.setFixedWidth(150)
        self._input_conf_threshold.setFixedHeight(30)
        self._input_conf_threshold.setFont(QFont('Arial', 15))

        self._conf_button = QPushButton('Set Threshold')
        self._conf_button.clicked.connect(self.set_conf_threshold)

        self._togle_left_right = QAction("Left", self)
        self._togle_left_right.setFont(QFont('Arial', 15))
        self._togle_left_right.setCheckable(True)
        self._togle_left_right.triggered.connect(self.toggle_hand_side)

        self._small_labels.setChecked(True)
        self._all_included.setChecked(True)

        self._finger_btn.stateChanged.connect(self.paint_buttons)
        self._knuckle_m_btn.stateChanged.connect(self.paint_buttons)
        self._knuckle_M_btn.stateChanged.connect(self.paint_buttons)
        self._knuckle_b_btn.stateChanged.connect(self.paint_buttons)
        self._all_included.stateChanged.connect(self.paint_buttons)
        self._add_bndboxes.stateChanged.connect(self.paint_buttons)
        self._small_labels.stateChanged.connect(self.change_label_dimension)
        self._medium_labels.stateChanged.connect(self.change_label_dimension)
        self._large_labels.stateChanged.connect(self.change_label_dimension)


        tool_bar.addWidget(self._finger_btn)
        tool_bar.addWidget(self._knuckle_m_btn)
        tool_bar.addWidget(self._knuckle_M_btn)
        tool_bar.addWidget(self._knuckle_b_btn)
        tool_bar.addWidget(self._all_included)
        tool_bar.addWidget(self._add_bndboxes)
        tool_bar.addWidget(self._small_labels)
        tool_bar.addWidget(self._medium_labels)
        tool_bar.addWidget(self._large_labels)
        tool_bar.addAction(self._togle_left_right)
        tool_bar.addWidget(self._input_conf_threshold)
        tool_bar.addWidget(self._conf_button)

        return tool_bar







