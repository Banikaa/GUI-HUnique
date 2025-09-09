# app imports
import sys, copy

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton

# class imports
from Mode_selector import Mode_selector
from widgets.labels.PhotoDescriptionLabel import PhotoDescriptionLabel as photo_lbl
from widgets.labels.Label import Label as lbl
from widgets.buttons.Button import Button as btn

# display imports
from tabs.Vein_pattern_tab import VainPatternTab as vein
from tabs.Lunule_seg_tab import LunuleSegTab as lunule
from tabs.flk_tab import FlkTab as flk
from tabs.Decorations_tab import DecorationsTab as dec

from Model_manager import ModelManager as model_manager

# COLOR imports (delete later if not used)
from PyQt5.QtWidgets import QWidget



class Main():

    # global variables
    _active_tab = None
    _main_window = None
    _current_tab = None
    _photo_ready = False
    _mode_list = ['compare', 'show']
    _gui_mode = None
    _main_window_layout = None
    _image_viewer_labels = []
    _model_manager = None
    _left_side_photo_viewer = None

    # tab objects
    _output_tabs_widget = None
    _tab_names = ['vein', 'lunule', 'decorations', 'flk']
    _output_tabs_dict = {}      # store all the widgets that will be displayed in the _output_tabs_widget
    _output_tab_object_dict = {}  # store all the tab object instances

    # add here more classes if needed
    _vein_pattern_tab_object = None
    _lunule_segmentation_tab_object = None
    _decorations_segmentation_tab_object = None
    _fingers_lunule_knuckle_tab_object = None
    # tabs that will be displayed
    _vein_pattern_tab = None
    _lunule_segmentation_tab = None
    _decorations_segmentation_tab = None
    _fingers_lunule_knuckle_tab = None


    def __init__(self):
        app = QApplication(sys.argv)

        # Define the main window
        self._main_window = QMainWindow()
        self._main_window.setWindowTitle("HUnique GUI")
        self._main_window.setGeometry(100, 100, 2100, 1000)

        # Create the mode selector widget
        mode_selector_class = Mode_selector(self)
        mode_selector_widget = mode_selector_class.selector_widget()

        # Create a central widget for the main window
        central_widget = QWidget(self._main_window)

        # Create a layout for the central widget and add the mode selector widget
        self._main_window_layout = QVBoxLayout(central_widget)
        self._main_window_layout.addWidget(mode_selector_widget, alignment=Qt.AlignCenter)

        self._main_window.setCentralWidget(central_widget)

        # Show the main window
        self._main_window.show()
        sys.exit(app.exec_())


    def set_mode(self, mode):
        self._gui_mode = mode
        print('Mode set to:', mode)
        self.set_layout()


    def set_layout(self):
        if self._gui_mode == 'compare':
            print('COMPARE MODE NOT IMPLEMENTED YET')
        elif self._gui_mode == 'show':
            self._main_window_layout.removeWidget(self._main_window_layout.itemAt(0).widget())
            self.set_show_mode_layout()


    # ----------------------------------------------------------------------
    # SHOW MODE LAYOUT
    # ----------------------------------------------------------------------
    def set_show_mode_layout(self):
        # Create a central widget
        central_widget = QWidget(self._main_window)

        # Create a horizontal layout for the main window
        main_layout = QHBoxLayout(central_widget)

        # Create the left section (1/3 of the width)
        left_section = QWidget()
        left_layout = QVBoxLayout(left_section)
        self._left_side_photo_viewer = self.left_side()
        left_layout.addWidget(self._left_side_photo_viewer)
        left_section.setLayout(left_layout)
        left_section.setStyleSheet("background-color: grey;")

        # Create the right section (2/3 of the width)
        right_section = QWidget()
        right_layout = QVBoxLayout(right_section)
        right_layout.addWidget(self.right_side())
        right_section.setLayout(right_layout)
        right_section.setStyleSheet("background-color: grey;")

        # Add the sections to the main layout
        main_layout.addWidget(left_section, stretch=1)  # 1/3
        main_layout.addWidget(right_section, stretch=2)  # 2/3

        self._main_window.setCentralWidget(central_widget)


    def left_side(self):
        left_side_photo_viewer = photo_lbl('photo_viewer', 'Photo Viewer', 'grey', False)

        # setting up the live and add image buttons
        buttons_box = QWidget()
        buttons_box.setMaximumHeight(100)
        buttons = QHBoxLayout()
        add_img_button = btn(self, 'photo_selector', 'change/select photo',
                                    None, 'insert_photo')
        add_img_button.setObjectName('add_img_button')
        add_img_button.setMaximumHeight(80)
        add_img_button.setStyleSheet("border: 3px solid black; background-color: grey; border-radius: 5px")

        live_cam_button = QPushButton('Live Feed')
        live_cam_button.setObjectName('live_cam_button')
        live_cam_button.setMaximumHeight(80)
        live_cam_button.setStyleSheet("border: 3px solid black; background-color: grey; border-radius: 5px")
        live_cam_button.clicked.connect(self.live_cam)

        buttons.addWidget(add_img_button, 1)
        buttons.addWidget(live_cam_button, 1)
        buttons_box.setLayout(buttons)
        left_side_photo_viewer.set_text_part_to_button(buttons_box)

        # setting up the labels
        for tab in self._tab_names:
            self._image_viewer_labels.append(lbl(tab + '_label', tab + '_label',
                                                parent=self, drag_and_drop=True))

        left_side_photo_viewer.set_image_part(self._image_viewer_labels[0])


        return left_side_photo_viewer

    # this is the model output layout, whre the results of all the models is displayed
    def right_side(self):
        tab_layout = QVBoxLayout()
        self._output_tabs_widget = QTabWidget()
        # flk tab
        flk_tab_object = flk(self, 'flk')
        flk_tab = flk_tab_object.get_tab()
        # vein pattern tab
        vein_tab_object = vein(self, 'Vein Pattern', 'vein')
        vein_tab = vein_tab_object.get_tab()
        # lunule segmentation tab
        lunule_tab_object = lunule(self, 'Lunule Segmentation', 'lunule')
        lunule_tab = lunule_tab_object.get_tab()
        # decorations segmentation tab
        decorations_tab_object = dec(self, 'Decorations Segmentation', 'decorations')
        decorations_tab = decorations_tab_object.get_tab()

        # populate the _output_tabs_dict with the tabs
        # add more tabs if needed
        self._output_tabs_dict['vein'] = vein_tab
        self._output_tabs_dict['lunule'] = lunule_tab
        self._output_tabs_dict['decorations'] = decorations_tab
        self._output_tabs_dict['flk'] = flk_tab

        self._output_tab_object_dict['vein'] = vein_tab_object
        self._output_tab_object_dict['lunule'] = lunule_tab_object
        self._output_tab_object_dict['decorations'] = decorations_tab_object
        self._output_tab_object_dict['flk'] = flk_tab_object

        # add the tabs to the tab layout
        for tab in self._output_tabs_dict:
            self._output_tabs_widget.addTab(self._output_tabs_dict[tab], tab)

        self._model_manager = model_manager(self, self._output_tab_object_dict)

        tab_layout.addWidget(self._output_tabs_widget)
        self._output_tabs_widget.currentChanged.connect(self.tab_changed)
        self.tab_changed()
        return self._output_tabs_widget


    def tab_changed(self):
        name = self._output_tabs_widget.currentWidget().objectName()
        tab_index = self._tab_names.index(name)
        label = self._image_viewer_labels[tab_index]
        self._left_side_photo_viewer.set_image_part(label)


    def set_left_viewer_labels(self, img: np.array, tab_name=None, mask=None, extra_img=None, one_img = False):

        print(tab_name)

        if not one_img:
            for label in self._image_viewer_labels:
                label.set_label_img_from_np_array(copy.deepcopy(img))
                label.update()
        else:
            if 'lunule' in tab_name:
                tab_name, finger_nb = tab_name.split('_')[0], int(tab_name.split('-')[1])
                print('set img to lunule-' + str(finger_nb))
                self._image_viewer_labels[self._tab_names.index("lunule")].set_label_img_from_np_array(
                    copy.deepcopy(img))
            elif tab_name == 'vein':
                print('set img to vein')
                self._image_viewer_labels[self._tab_names.index('vein')].set_label_img_from_np_array(
                    copy.deepcopy(img))
            elif tab_name == 'decorations':
                print('set img to decorations')
                self._image_viewer_labels[self._tab_names.index('decorations')].set_label_img_from_np_array(
                    copy.deepcopy(img))



    def set_tab_ouput_img_mask(self, tab_name, img, mask, ):
        self._output_tab_object_dict[tab_name].set_photo_labels(img, mask)



    def set_flk_results(self, result_dict, angles, img):
        self._image_viewer_labels[self._tab_names.index('flk')].set_label_img_from_np_array(copy.deepcopy(img))
        self._output_tab_object_dict['flk'].set_photo_labels(result_dict, img, angles)


    def set_lunule_results(self, lunule_mask_dict, finger_img, finger_coord):
        print('set lunule results')
        self._output_tab_object_dict['lunule'].input_lunule_dict (lunule_mask_dict, finger_img, finger_coord)


    def reset_left_photo_label(self, label_name):
        self._image_viewer_labels[self._tab_names.index(label_name)].remove_bounding_box()

    def update_left_photo_label(self, label_name):
        self._image_viewer_labels[self._tab_names.index(label_name)].update()



    def get_left_photo_label_by_name(self, label_name):
        return self._image_viewer_labels[self._tab_names.index(label_name)]

    def get_hand_side(self):
        # return self._fingers_lunule_knuckle_tab_object.get_hand_side()
        return 'left'

    def get_hand_position(self):
        # return self._fingers_lunule_knuckle_tab_object.get_hand_position()
        return 'dorsal'

    def set_photo_ready(self, ready):
        self._photo_ready = ready
        for tab in self._output_tab_object_dict:
            self._output_tab_object_dict[tab].set_photo_ready(ready)

    def get_tab_by_name(self, name):
        return self._output_tab_object_dict[name]

    def get_active_tab(self):
        return self._output_tabs_widget.currentWidget().objectName()

    def get_lunule_index(self):
        return self._output_tab_object_dict['lunule'].get_lunule_index()

    def input_photo(self, img_path):
        self._photo_ready = True
        self._model_manager.load_image(img_path)

    def live_cam(self):
        if self._model_manager.get_live_cam_status():
            self._main_window.findChild(QPushButton, 'live_cam_button').setText('Live Feed')
            self._model_manager.stop_live_cam()
        else:
            self._model_manager.start_live_cam()
            self._main_window.findChild(QPushButton, 'live_cam_button').setText('Stop Live Feed')
    # ----------------------------------------------------------------------
    # END OF SHOW MODE LAYOUT
    # ----------------------------------------------------------------------





main_class = Main()
