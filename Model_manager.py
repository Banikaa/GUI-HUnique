import cv2, numpy as np
from PIL import Image
from PyQt5.QtCore import QTimer

# models
from  models.Inference_lunules import infer as lunule_inf
from models.Inference_veins import EAB_Demo as vein_inf
from models.Inference_tatoos.inference import TatooInference as tatoos_inf
import models.FRCNN.inference_FRCNN_test as frcnn_inf

# threads
from threads.Lunule_thread import Lunule_model_thread
from threads.Vein_thread import Vein_model_thread
from threads.Decorations_thread import Tattoo_model_thread
from threads.FRCNN_thread import FRCNN_model_thread

# cam worker
from threads.Cam_worker import CamWorker


class ModelManager:
    _main_class = None
    _output_tabs_object_dict = None
    _photo_ready = False
    _img: np.array = None
    _cam_worker = None

    _vein_model = None
    _tattoo_inference = None
    _frcnn_thread = None
    _lunule_threads = None


    def __init__(self, main_class, output_tabs_object_dict):
        self._main_class = main_class
        self._output_tabs_object_dict = output_tabs_object_dict

        # model innit
        self._vein_model = vein_inf.initialize_model('rgb')

        self._tattoo_inference = tatoos_inf()
        self._tattoo_inference.build_model('')

        self._lunule_inference = lunule_inf.LunuleInference()
        self._lunule_inference.build_model('')


        model_dict = {
            'tattoo': self._tattoo_inference,
            'vein': self._vein_model,
            'lunule': self._lunule_inference,
            'flk': frcnn_inf
        }

        self._frcnn_thread = FRCNN_model_thread(frcnn_inf)
        self._frcnn_thread.signal.connect(self.flk_results)
        self._vein_thread = Vein_model_thread(self._vein_model)
        self._vein_thread.signal.connect(self._main_class.get_tab_by_name('vein').set_img_to_labels)
        self._tattoo_thread = Tattoo_model_thread(self._tattoo_inference)
        self._tattoo_thread.signal.connect(self._main_class.get_tab_by_name('decorations').set_img_to_labels)
        self._lunule_threads = [Lunule_model_thread(self._lunule_inference) for _ in range(5)]

        self._cam_worker = CamWorker(main_class, model_dict)
        self._cam_worker.signal.connect(self._main_class.set_left_viewer_labels)
        self._cam_worker.signal_flk.connect(self._main_class.set_flk_results)

    def start_threads(self, img):
        self._frcnn_thread.run_inference(img, self._main_class.get_hand_side(), self._main_class.get_hand_position())
        self._vein_thread.run_inference(img)
        self._tattoo_thread.run_inference(img)


    def flk_results(self, result_dict, angles, img):
        fingers = [result_dict['f1'], result_dict['f2'], result_dict['f3'], result_dict['f4'], result_dict['f5']]
        self._main_class.set_flk_results(result_dict, angles, img)

        subimages = {}
        for i in range(5):
            if fingers[i] is not None:
                fingernail_subimg = self.extract_subimg(img, fingers[i])
                subimages[i+1] = fingernail_subimg
                self._lunule_threads[i].run_inference(fingernail_subimg, i + 1)

        timer = QTimer()
        timer.timeout.connect(lambda: self.update_lunule_results(subimages, fingers))
        timer.start(50)


    def update_lunule_results(self, fingernail_subimg, fingernail_coord):
        lunule_mask_dict = {}

        for lunule_thread in self._lunule_threads:
            lunule_thread.mutex.lock()
            lunule_mask_dict[lunule_thread.get_finger_number()] = lunule_thread.lunule_mask_dict[lunule_thread.get_finger_number()]
            lunule_thread.mutex.unlock()

        for finger in range(1,6):
            if finger in lunule_mask_dict.keys() and lunule_mask_dict[finger] is not None:
                continue
            else:
                lunule_mask_dict[finger] = None

        if not any([threads.isRunning() for threads in self._lunule_threads]):
            self._main_class.set_lunule_results(lunule_mask_dict, fingernail_subimg, fingernail_coord)



    def load_image(self, img_path: str):
        if img_path == '':
            return

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.load_image_from_np_array(img)


    def load_image_from_np_array(self, img: np.array):
        self._photo_ready = True
        self._main_class.set_left_viewer_labels(img)
        self._img = img
        self.start_threads(img)


    def start_live_cam(self):
        self._cam_worker.start()

    def stop_live_cam(self):
        self._cam_worker.stop()

    def get_live_cam_status(self):
        return self._cam_worker.is_running()

    def extract_subimg(self, img, box):
        try:
            xmin = int(max(0, box[0]))
            ymin = int(max(0, box[1]))
            xmax = int(min(img.shape[1], box[2]))
            ymax = int(min(img.shape[0], box[3]))
            return img[ymin:ymax, xmin:xmax]
        except:
            return None











