import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from models.FRCNN import inference_FRCNN_test as frcnn_inf



class FRCNN_model_thread(QThread):
    signal = pyqtSignal(dict, dict, np.ndarray)  # Signal to notify when inference is done

    _model = None
    _img = None
    _hand_side = None
    _hand_position = None
    _threshold = None
    _running = False

    def __init__(self, model):
        super().__init__()
        self._model = model  # Your AI model instance


    def run_inference(self, img, handside, hand_position, threshold = 10):
        print('frcnn thread')
        self._img = img
        self._hand_side = handside
        self._hand_position = hand_position
        self._threshold = threshold
        self._running = True
        self.run()

    def run(self):
        # Main logic for running the AI model inference
        while self._running:
            final_dict, fingers, angles = frcnn_inf.start_frcnn(self._img, self._hand_side, self._hand_position, self._threshold)
            print('final_dict', final_dict)
            self.signal.emit(final_dict, angles, self._img)
            self._running = False  # Set the running flag to False
            self.quit()  # Stop the thread execution

    def stop(self):
        self._running = False
