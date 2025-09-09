import cv2
import numpy as np
from PyQt5.QtCore import QThread, QTimer, pyqtSignal

from models.Inference_veins import EAB_Demo as vein_inf

class CamWorker(QThread):
    _main_window = None
    _running = False
    _timer = None
    _tattoo_model = None
    _vein_model = None
    _lunule_model = None
    _flk_model = None

    def __init__(self, main_window, model_dict, fps=30, infrared=False):
        super(CamWorker, self).__init__()
        self._running = False
        self._tattoo_model = model_dict['tattoo']
        self._vein_model = model_dict['vein']
        self._lunule_model = model_dict['lunule']
        self._flk_model = model_dict['flk']
        self._main_window = main_window


    signal = pyqtSignal(np.ndarray, str, np.ndarray, np.ndarray, bool)
    signal_flk = pyqtSignal(dict, dict, np.ndarray)


    def run(self):
        cap = cv2.VideoCapture(0)
        self._running = True

        while self._running:
            ret, frame = cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)

                active_tab = self._main_window.get_active_tab()

                if active_tab == 'flk':
                    self.flk_model_inference(frame)
                elif active_tab == 'lunule':
                    self.lunule_model_inference(frame)
                elif active_tab == 'vein':
                    self.vein_model_inference(frame)
                elif active_tab == 'decorations':
                    self.tattoo_model_inference(frame)

        cap.release()

    # run inference on the image depending on the current active tab
    def flk_model_inference(self, img):
        result_dict, fingers, angles = self._flk_model.start_frcnn(img, self._main_window.get_hand_side(), self._main_window.get_hand_position())
        self.signal_flk.emit(result_dict, angles, img)

    def lunule_model_inference(self, img):
        result_dict, fingers, angles = self._flk_model.start_frcnn(img, self._main_window.get_hand_side(), self._main_window.get_hand_position())
        cropped_frame = self.get_cropped_img(img, fingers[self._main_window.get_lunule_index()-1])
        mask = self._lunule_model.inference(cropped_frame)
        finger_nb = self._main_window.get_lunule_index()
        self.signal.emit(img, 'lunule-'+str(finger_nb), mask, cropped_frame, True)



    def vein_model_inference(self, img):
        mask = vein_inf.process_image(self._vein_model, img)
        self.signal.emit(img, 'vein', mask, np.array([0]), True)

    def tattoo_model_inference(self, img):
        mask = self._tattoo_model.inference(img)
        self.signal.emit(img, 'decorations', mask, np.array([0]), True)


    def stop(self):
        self._running = False
        self.quit()

    def is_running(self):
        return self._running


    def get_cropped_img(self, img, box):
        try:
            xmin = max(0, int(box[0]))
            ymin = max(0, int(box[1]))
            xmax = min(img.shape[1], int(box[2]))
            ymax = min(img.shape[0], int(box[3]))
            return img[ymin:ymax, xmin:xmax]
        except:
            return np.array(np.zeros((100,100,3)))
