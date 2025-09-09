import cv2

from tabs.Split_tab import Split_tab as Split_Tab


class Jewellery_tab(Split_Tab):
    _graph_points = []


    def detect_white_points(self, image_path):
        image = cv2.imread(image_path)
        border_points = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 2, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            border_points.append(contour.squeeze())
        return border_points



    def draw_points(self):
        self.central_widget.draw_points(self._graph_points)
        self.right_widget.draw_points(self._graph_points)

    def set_img_to_labels(self, img_fname):
        graph_output = self.get_graph_img(img_fname)
        self._graph_points = self.detect_white_points(graph_output)
        self.central_widget.draw_points(self._graph_points)
        self.right_widget.draw_points(self._graph_points)
        self.w3.setChecked(True)
        self.w3_clicked()

