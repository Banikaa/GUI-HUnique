from models.Inference_tatoos.inference import TatooInference as tatoos_inf
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class Tattoo_model_thread(QThread):
    signal = pyqtSignal(np.ndarray, np.ndarray)  # Signal to notify when inference is done

    _img = None
    _model = None
    _running = False

    def __init__(self, model):
        super().__init__()
        self._model = model

    def run_inference(self, img):
        print('tattoo thread started')
        self._img = img
        self._running = True
        self.run()


    def run(self):
        while self._running:
            tatoos_mask = self._model.inference(self._img)
            self.signal.emit(self._img, tatoos_mask)
            self._running = False  # Set the running flag to False
            self.quit()  # Stop the thread execution

    def stop(self):
        self._running = False
        self.quit()