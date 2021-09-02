import cv2, time, logging


class LabradorCamera(object):
    resolutions = {
        "sd": {"width": 640, "height": 480},
        "hd": {"width": 1280, "height": 720},
        "full-hd": {"width": 1920, "height": 1080},
    }

    def __init__(self, device=0):
        self.device = device

    def open(self):
        try:
            self.capture = cv2.VideoCapture(self.device)
            if not self.capture.isOpened():
                # sometimes, the capture will not open at object instantiation
                # however it may work when retrying with the open() method on the now existing object
                retries, max_retries = 0, 3
                while retries < max_retries and not self.capture.isOpened():
                    time.sleep(2)
                    self.capture.open(device)
                    retries += 1
        except Exception as e:
            logging.error("Can't connect to camera {}".format(str(device)))
            logging.error("Reason: {}".format(str(e)))
            return None

        if self.capture is None or not self.capture.isOpened():
            logging.error("Can't connect to camera {}".format(str(device)))
            return None

        if self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) == 0 or self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT) == 0:
            self.capture.release()
            logging.error("Câmera {} não está funcionando corretamente. WIDTH/HEIGH == 0".format(str(device)))
            return None

        return True

    def set_resolution(self, target_res):
        target_res = target_res.lower()

        if target_res not in LabradorCamera.resolutions.keys():
            logging.error("Invalid target video resolution. Should be one of: sd, hd, full-hd. Given: {}.".format(target_res))
            return False

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,  LabradorCamera.resolutions[target_res]["width"])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, LabradorCamera.resolutions[target_res]["height"])
        
        # Show camera resolution after adjustment. It can be different from specified 
        # in command line due to limitations of camera
        logging.debug("Camera adjusted for image with width %s and height %s" % (self.capture.get(cv2.CAP_PROP_FRAME_WIDTH), self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) == 0 or self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT) == 0:
            logging.error("Abort: effective camera width or height is zero.")
            return False
        
        return True

    def set_params(self, resolution="sd", video_frame_rate=7.0, video_codec="default"):
        if video_codec == "mjpg":
            self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

        if not self.set_resolution(resolution):
            logging.error("Error setting camera resolution.")
            return None

        return True

    def read(self):
        return self.capture.read()

    def save_frame(self, filename):
        ret, frame = self.read()
        if not ret:
            logging.error("Error reading frame.")
            return False

        cv2.imwrite(filename, frame)
        return True

    def __del__(self):
        self.capture.release()