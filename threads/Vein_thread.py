from models.Inference_veins import EAB_Demo as vein_inf
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class Vein_model_thread(QThread):
    signal = pyqtSignal(np.ndarray, np.ndarray)

    _img = None
    _model = None
    _running = False


    def __init__(self, model):
        super().__init__()
        self._model = model

    def run_inference(self, img):
        print('running vein inference')
        self._img = img
        self._running = True
        self.run()


    def run(self):
        while self._running:
            mask = vein_inf.process_image(self._model, self._img)
            self.signal.emit(self._img, mask)
            self._running = False
            self.quit()

    def stop(self):
        self._running = False