import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from widgets.labels.Label import Label as lbl


class PhotoDescriptionLabel(lbl):
    _label_name = ''
    _label_description = ''
    _color = 'grey'
    _param_setup = True
    _zoom_feature = False
    _stretch = False
    _bounding_boxes = []
    _image_part = None
    _text_part = None
    _photo_label_layout = None

    '''
    label_name: str = name of the label
    label_description: str = description of the label
    extra_part: bool = extra part of the label
    color: str = color of the label
    param_setup: bool = setup of the label
    zoom_feature: bool = set if the user can zoom the image part
    stretch: bool = set the widgets to stretch inside the layout
    '''

    def __init__(self, label_name, label_description, color='grey', param_setup=True, zoom_feature=False,
                 stretch=False):
        super().__init__(label_name, label_description)
        self._label_name = label_name
        self._zoom_feature = zoom_feature
        self._label_description = label_description
        # self._extra_part = extra_part
        self._color = color
        self.setObjectName(label_name)
        self.setStyleSheet("border: 1px solid black;")

        if param_setup:
            self.param_setup()

        # setting the layout of the whole widget
        self.set_layout(stretch)
        # setting the image part of the widget
        self.innit_image_part(label_name, label_description, color, zoom_feature)
        # setting up the text part of the widget
        self.innit_text_part(label_description, color)

        self.setLayout(self._photo_label_layout)

    # setting the layout of the whole widget
    def set_layout(self, stretch=False):
        self._photo_label_layout = QVBoxLayout()
        self._photo_label_layout.setContentsMargins(0, 0, 0, 0)
        self._photo_label_layout.setSpacing(0)
        self._photo_label_layout.setStretch(0, 8)
        self._photo_label_layout.setStretch(1, 2)
        if stretch:
            self._photo_label_layout.addStretch()

    def innit_image_part(self, label_name, label_description, color, zoom_feature=False):
        self._image_part = lbl(label_name, label_description, zoom_feature=zoom_feature)
        self._image_part.setStyleSheet(
            "border: 3px solid " + 'black' + "; background-color: " + color + "; font-size: 18pt;")
        self._photo_label_layout.addWidget(self._image_part, stretch=8)

    def innit_text_part(self, label_description, color):
        self._text_part = QLabel()
        self._text_part.setStyleSheet(
            "border: 3px solid " + 'black' + "; background-color: " + color + "; font-size: 18pt;")
        self._text_part.setText(label_description)
        self._text_part.setAlignment(Qt.AlignCenter)
        self._text_part.setMaximumHeight(50)
        self._photo_label_layout.addWidget(self._text_part, stretch=2)

    # setting basic parameters for flk tab
    def param_setup(self):
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)
        self.setMaximumWidth(300)
        self.setMinimumWidth(300)

    # changing the text part to a button
    def change_text_part_to_button(self, button_text, action_class_function):
        self._photo_label_layout.removeWidget(self._text_part)
        self._text_part = QPushButton()
        self._text_part.setObjectName(self._label_name)
        self._text_part.setText(button_text)
        self._text_part.clicked.connect(action_class_function)
        self._text_part.setStyleSheet(
            "border: 3px solid " + 'black' + "; background-color: " + self._color + "; font-size: 18pt;")
        self._text_part.setMaximumHeight(50)
        self._text_part.setMinimumHeight(50)
        self._photo_label_layout.addWidget(self._text_part, stretch=2)
        self.update()

    # changing the text part to a buttons as a paramenter function
    def set_text_part_to_button(self, button):
        self._photo_label_layout.removeWidget(self._text_part)
        self._text_part = button
        self._photo_label_layout.addWidget(self._text_part, stretch=2)
        self.update()

    # set the image label size to the width and height free space
    def update_parts(self):
        self._image_part.set_width(self.width())
        self._image_part.set_height(self.height() - self._text_part.height())

    # set the image label to another label sent as a parameter
    def set_image_part(self, new_image_part):
        self._photo_label_layout.removeWidget(self._image_part)
        self._photo_label_layout.removeWidget(self._text_part)
        self._image_part.hide()
        self._image_part = new_image_part
        self._photo_label_layout.addWidget(self._image_part, stretch=8)
        self._photo_label_layout.addWidget(self._text_part, stretch=2)
        self._image_part.show()
        self.update()

    # set the image label to an image sent as a np array
    def set_img_from_np_array(self, img_np_array, updtate_parts=True):
        if updtate_parts:
            self.update_parts()
        self._image_part.set_label_img_from_np_array(img_np_array)
        self._image_part.setText('')
        self.update()

    # set the image label to an image sent as a filepath
    def set_image_from_path(self, image_path, updtate_parts=True):
        if updtate_parts:
            self.update_parts()
        self._image_part.set_image(image_path)
        self._image_part.setText('')
        self.update()

    #  rotate the image by the angle sent as a parameter
    # return the rotated image
    def rotate_image(self, image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        return np.asarray(rotated)

    # set the image in the image_label to the cropped image
    def set_image_cropped(self, xmin, ymin, xmax, ymax, input_image, angle=0):
        self._photo_label_layout.removeWidget(self._image_part)
        self._photo_label_layout.removeWidget(self._image_part)
        print(type(input_image))
        image = np.array(input_image[ymin:ymax, xmin:xmax])
        # image = self.rotate_image(input_image[ymin:ymax, xmin:xmax], angle)
        self.set_img_from_np_array(image)
        self._photo_label_layout.addWidget(self._image_part, stretch=8)
        self._photo_label_layout.addWidget(self._text_part, stretch=2)

    # set the width of the overall photolabel and both labels inside
    def set_width(self, width):
        width = int(width)
        self._text_part.setMaximumWidth(width)
        self._text_part.setMinimumWidth(width)
        self._image_part.set_width(width)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
        self.update()

    # set the height of the overall photolabel
    def set_height(self, height):
        height = int(height)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.update()

    # get the image label
    def get_label(self):
        return self._image_part

    def get_label_ratio(self):
        return self._image_part.get_ratio()

    # set the image label
    def set_label(self, label):
        self._image_part = label
        self.update()

    # get the top margin of the photolabel
    def get_top_margin(self):
        return (self.height() - self.newHeight - self._text_part.height()) * .5

    # change the text of the text label
    def change_text(self, text):
        self._text_part.setText(text)
        self.update()

    # get the width ratio of the image label
    def get_width_ratio(self):
        return self._image_part.get_width_ratio()

    # get the height ratio of the image label
    def get_height_ratio(self):
        return self._image_part.get_height_ratio()

    # add a bounding box to the image label
    def add_bounding_box(self, minx, miny, maxx, maxy, color, text=None):
        self._image_part.add_bounding_box(minx, miny, maxx, maxy, color, text)

    # remove all bounding boxes from the image label
    def remove_bounding_box(self):
        self._image_part.remove_bounding_box()
