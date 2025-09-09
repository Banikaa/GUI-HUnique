import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint, QPointF, QRect
from PyQt5.QtGui import QFont, QPixmap, QImage, QMouseEvent, QPainter, QPen, QColor


class Label(QLabel):
    _color = 'black'
    _parent = None
    _image_file = ''
    _zoom_feature = False
    _drag_and_drop = False
    _image_inserted = False
    _bounding_boxes = {}
    _bounding_boxes_text = {}
    _graph_points = {}
    _point_objects = []
    _legend_text = {}
    _ratio = 0
    _pen_point_width = 1
    _point_color = 'green'
    _label_name = ''
    _bounding_boxes_counter = 0
    _focal_point = None
    _is_dragging = False
    _zoom_sync = False
    _np_array = np.array([])
    _zoom_factor = 1
    _new_x_pos, _new_y_pos = 0, 0
    _delta_x, _delta_y = 0, 0
    _start = QPoint(0, 0)
    _newHeight, _newWidth = 0, 0
    _pixmap = None

    def __init__(self, label_name, label_description, color = 'black', parent = None, zoom_feature = False, drag_and_drop = False):
        super(Label, self).__init__()
        self._color = color
        self._parent = parent
        self._zoom_feature = zoom_feature
        self._drag_and_drop = drag_and_drop
        self._label_name = label_name

        self.setAcceptDrops(drag_and_drop)

        self.setScaledContents(True)
        self.setText(label_description)
        self.setFont(QFont('Arial', 15))
        self.setStyleSheet("border: 4px solid " + color + "; background-color: #121212; font-size: 15pt;")
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName(label_name)

        self._newHeight, self._newWidth = self.height(), self.width()


    def set_pen_point_width(self, width):
        self._pen_point_width = width
        self.update()


    def get_pen_point_width(self):
        return self._point_pen_width


    def change_text(self, text):
        self.setText(text)
        self.update()


    def set_height(self, height):
        height = int(height)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.update()


    def set_width(self, width):
        width = int(width)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
        self.update()


    def set_parent(self, parent):
        self._parent = parent


    def get_parent(self):
        return self._parent


    def set_sync_bool(self, bool_val):
        self._zoom_sync = bool_val


    def sync_zoom(self, zoom_factor):
        self._zoom_factor = zoom_factor
        self.update()


    def set_delta_pixmap(self, delta_x, delta_y):
        self._new_x_pos = delta_x
        self._new_y_pos = delta_y
        self.update()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()


    # for this the parent should be the main class
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        self.set_image(file_path)
                        self.setText("")
                        event.acceptProposedAction()
                        self._parent.input_photo(file_path)
                        break
        else:
            event.ignore()


    def set_label_img_from_np_array(self, img_np_array):
        if img_np_array is None:
            return
        self._image_inserted = True
        img_np_array = np.copy(img_np_array)
        self._np_array = img_np_array
        pixmap = QPixmap()
        pixmap.convertFromImage(
            QImage(img_np_array.data, img_np_array.shape[1], img_np_array.shape[0], img_np_array.shape[1]*3, QImage.Format_RGB888))

        image = QPixmap(pixmap)
        img_height, img_width = pixmap.height(), pixmap.width()

        if self.width() / img_width > self.height() / img_height:
            scaled_width = int(self.height() / img_height * img_width)
            self._newWidth = scaled_width
            self._newHeight = self.height()
            self.set_height(self._newHeight)
            self.set_width(self._newWidth)
            self._ratio = self._newWidth / img_width
            self._pixmap = image.scaled(self._newWidth, self.height(), Qt.KeepAspectRatio)
        else:
            scaled_height = int(self.width() / img_width * img_height)
            self._newHeight = scaled_height
            self._newWidth = self.width()
            self.set_height(self._newHeight)
            self.set_width(self._newWidth)
            self._ratio = self._newHeight / img_height
            self._pixmap = image.scaled(self._newWidth, self.height(), Qt.KeepAspectRatio)
        self.update()


    def set_image(self, image_path):
        image_file = image_path
        if image_path != '':
            self._image_inserted = True
            image = QPixmap(image_file)

            img_height, img_width = image.height(), image.width()

            if self.width() / img_width > self.height() / img_height:
                scaled_width = int(self.height() / img_height * img_width)
                self._newWidth = scaled_width
                self._newHeight = self.height()
                self.set_height(self._newHeight)
                self.set_width(self._newWidth)
                self._ratio = self._newWidth / image.width()
                self._pixmap = image.scaled(self._newWidth, self.height(), Qt.KeepAspectRatio)
            else:
                scaled_height = int(self.width() / img_width * img_height)
                self._newHeight = scaled_height
                self._newWidth = self.width()
                self.set_height(self._newHeight)
                self.set_width(self._newWidth)
                self._ratio = self._newHeight / image.height()
                self._pixmap = image.scaled(self._newWidth, self.height(), Qt.KeepAspectRatio)
        else:
            self._image_inserted = False
            self._pixmap = QPixmap()
            self.update()


    # mouse controls for interacting with the image
    # for label moving, zooming and dragg and dropping
    def wheelEvent(self, event):
        if self._zoom_feature:
            zoom_in_factor = .02
            if event.angleDelta().y() > 0:
                self._zoom_factor += zoom_in_factor
            else:
                self._zoom_factor -= zoom_in_factor
            if self._zoom_sync:
                self._parent.sync_zoom(self._zoom_factor, self._new_x_pos, self._new_y_pos)
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self._zoom_feature:
            if event.button() == Qt.LeftButton:
                try:
                    if self._pixmap and self._pixmap.rect().contains(event.pos()):
                        self._start = event.pos()
                        self._is_dragging = True
                except Exception as e:
                    print(e)
                    pass

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._zoom_feature:
            if self._is_dragging:
                self._delta_x = event.pos().x() - self._start.x()
                self._delta_y = event.pos().y() - self._start.y()
                self._new_x_pos, self._new_y_pos = self._new_x_pos + self._delta_x, self._new_y_pos + self._delta_y
                if self._zoom_sync:
                    self._parent.sync_zoom(self._zoom_factor, self._new_x_pos, self._new_y_pos)
                self._start = event.pos()
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._zoom_feature:
            if event.button() == Qt.LeftButton:
                self._is_dragging = False
    # ------------------------------------------------


    # set the image on the label and draw any contours, graphs, text or bounding boxes
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        point_pen = QPen(QColor(self._point_color))
        point_pen.setWidth(self._pen_point_width)
        painter.setPen(point_pen)

        # set the pixmap to the label
        if self._image_inserted:
            scaled_pixmap = self._pixmap.scaled(int(self._newWidth * self._zoom_factor), int(self._newHeight * self._zoom_factor),
                                          Qt.KeepAspectRatio)
            painter.drawPixmap(self._new_x_pos, self._new_y_pos, scaled_pixmap)
        # ------------------------------------------------
        # draw points with lines connecting them (eg. for lunule or tatoos)
        if self._point_objects:
            for points in self._point_objects:
                for i in range(len(points)):
                    if i < len(points)-1:
                        p1 = QPointF(points[i][0] * self._zoom_factor + self._new_x_pos, points[i][1] * self._zoom_factor + self._new_y_pos)
                        p2 = QPointF(points[i+1][0] * self._zoom_factor + self._new_x_pos, points[i+1][1] * self._zoom_factor + self._new_y_pos)
                        painter.drawLine(p1, p2)
                    else:
                        p1 = QPointF(points[-1][0] * self._zoom_factor + self._new_x_pos, points[-1][1] * self._zoom_factor + self._new_y_pos)
                        p2 = QPointF(points[0][0] * self._zoom_factor + self._new_x_pos, points[0][1] * self._zoom_factor + self._new_y_pos)
                        painter.drawLine(p1, p2)
        # ------------------------------------------------
        # draw graph from points on label(eg vain pattern segmentation)
        def is_connected(point1, point2):
            return abs(point1[0] - point2[0]) <= 1 and abs(point1[1] - point2[1]) <= 1

        def are_points_connected(points, index1, index2):
            return is_connected(points[index1], points[index2])

        for color in self._graph_points:
            for i in range(len(self.graph_points[color]) - 1):
                if are_points_connected(self._graph_points[color], i, i + 1):
                    p1 = QPointF(self._graph_points[color][i][0] * self._zoom_factor * self.ratio + self._new_x_pos, self._graph_points[color][i][1] * self._zoom_factor * self._ratio + self._new_y_pos)
                    p2 = QPointF(self._graph_points[color][i + 1][0] * self._zoom_factor * self._ratio + self._new_x_pos, self._graph_points[color][i + 1][1] * self._zoom_factor * self._ratio + self._new_y_pos)
                    painter.drawLine(p1, p2)
                else:
                    p1 = QPointF(self._graph_points[color][i][0] * self._zoom_factor * self._ratio + self._new_x_pos, self._graph_points[color][i][1] * self._zoom_factor * self._ratio + self._new_y_pos)
                    painter.drawPoint(p1)
        # ------------------------------------------------
        # draw bounding boxes on label
        for color in self._bounding_boxes:
            for box in self._bounding_boxes[color]:
                pen = QPen(QColor(color))
                pen.setWidth(2)
                painter.setPen(pen)
                box = QRect(box.x() * self._zoom_factor + self._new_x_pos, box.y() * self._zoom_factor + self._new_y_pos,
                            box.width() * self._zoom_factor, box.height() * self._zoom_factor)
                painter.drawRect(box)
            for text in self._bounding_boxes_text[color]:
                font = QFont()
                font.setPointSize(15)
                font.setBold(False)
                painter.setFont(font)
                painter.drawText(text[1], text[2], text[0])
        # ------------------------------------------------
        # add text to the label
        if self._legend_text:
            ct = 0
            for color in self._legend_text:
                pen = QPen(QColor(color))
                painter.setPen(pen)
                font = QFont()
                font.setPointSize(15)
                font.setBold(False)
                painter.setFont(font)
                painter.drawText(10, self.height() - 10 - 20 * ct, self._legend_text[color][0])
                ct += 1
        # ------------------------------------------------


    # add a bounding box to the label
    def add_bounding_box(self, minx, miny, maxx, maxy, color = '', text = None):
        self._color = color
        minx = int(minx)
        miny = int(miny)
        maxx = int(maxx)
        maxy = int(maxy)
        box = QRect(minx, miny, maxx - minx, maxy - miny)
        if color in self._bounding_boxes.keys():
            self._bounding_boxes[color].append(box)
            self._bounding_boxes_text[color].append([text, minx, miny-3])
        else:
            self._bounding_boxes[color] = [box]
            self._bounding_boxes_text[color] = [[text, minx, miny-3]]


    # set new contoru to draw on the label
    def draw_points(self, contours):
        self._point_objects = []
        for points in contours:
            if len(points) > 1:
                try:
                    self._point_objects.append([(int(point[0] * self._ratio), int(point[1] * self._ratio)) for point in points])
                except IndexError:
                    pass
        self.update()

    # draw points on the label without ratio
    def draw_points_no_ratio(self, points):
        for color in points:
            self._graph_points[color] = [(int(point[0]), int(point[1])) for point in points[color]]
        self.update()

    # draw graph from points on the label
    def draw_graph(self, points):
        for color in points:
            self._graph_points[color] = [(int(point[0]), int(point[1])) for point in points[color]]
        self.update()

    # remove all points from the label (graphs and contours)
    def delete_points(self):
        self._graph_points = {}
        self._point_objects = []
        self.update()

    # set the color of the contours
    def set_point_color(self, color):
        self._point_color = color
        self.update()

    # add text to the label and set the color of the text
    def draw_text(self, text, color):
        if color in self._legend_text.keys():
            self._legend_text[color].append(text)
        else:
            self._legend_text[color] = [text]
        self.update()

    # remove all text from the label
    def delete_text(self):
        self._legend_text = {}
        self.update()

    # remove all bounding boxes from the label
    def remove_bounding_box(self):
        self._bounding_boxes = {}
        self._bounding_boxes_text = {}
        self.update()

    # get the image filepath
    def get_img(self):
        return self.image_file

    # get the image as a numpy array
    def get_np_array(self):
        return self._np_array

    # get the width ratio of the label from when the image was inserted
    def get_width_ratio(self):
        return self._ratio

    # get the height ratio of the label from when the image was inserted
    def get_height_ratio(self):
        return self._ratio

    def get_ratio(self):
        return self._ratio

    # get the ratio of the label
    def set_ratio(self, ratio):
        self._ratio = ratio
        self.update()

    # get the graph points
    def get__graph_points(self):
        return self._graph_points

    # get the width of the label
    def get_width(self):
        return self.width()

    # get the height of the label
    def get_height(self):
        return self.height()

    def get_new_width(self):
        return self._newWidth

    def get_new_height(self):
        return self._newHeight

    # delete the label
    def delete(self):
        self.setParent(None)
        self.deleteLater()

