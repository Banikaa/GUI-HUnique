import cv2
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import numpy as np

class Lunule_model_thread(QThread):
    signal = pyqtSignal(np.ndarray)  # Signal to notify when inference is done

    _model = None
    _img = None
    _finger_nb = None
    _running = False
    lunule_mask_dict = {}
    mutex = None


    def __init__(self, model):
        super().__init__()
        self._model = model
        self._lunule_mask_dict = {}
        self.mutex = QMutex()


    def run_inference(self, img, finger_nb):
        self._img = img
        self._finger_nb = finger_nb
        self._running = True
        self.run()


    def run(self):
        while self._running:
            self.mutex.lock()
            mask = self._model.inference(self._img)
            self.lunule_mask_dict[self._finger_nb] = mask
            self.mutex.unlock()
            self._running = False
            self.quit()

    def isRunning(self):
        return self._running

    def get_finger_number(self):
        return self._finger_nb


    def stop(self):
        self._running = False