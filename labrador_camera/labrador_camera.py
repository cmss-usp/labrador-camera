import cv2, time, logging, queue, threading


class LabradorCameraCV(object):
    def __init__(self, device=0):
        def str2int(device):
            try:
                return int(device)
            except Exception as e:
                return device
        self.device = str2int(device)
        self.capture = None

    def open(self):
        self.capture = cv2.VideoCapture(self.device)
        return self.capture.isOpened()

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
        logging.debug("Will release capture.")
        self.capture.release()

    def get_dimensions(self):
        width, height = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH), self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        logging.info(f"LabradorCamera dimensions are: height = {height} width = {width}")
        return height, width

    def __repr__(self):
        return str({"device": self.device, "isOpened": self.capture and self.capture.isOpened() or False})


class LabradorWebcam(LabradorCameraCV):
    resolutions = {
        "sd": {"width": 640, "height": 480},
        "hd": {"width": 1280, "height": 720},
        "full-hd": {"width": 1920, "height": 1080},
    }

    def __init__(self, low_fps_mode=True, **kwargs):
        super(LabradorWebcam, self).__init__(**kwargs)

        # this is a workaround to the following:
        #   when FPS is low, cv2's read() will not return the _latest_ frame, but a buffered one instead
        #   with this workaround we discard buffered ones and always get the latest one
        self.low_fps_mode = low_fps_mode
        if self.low_fps_mode:
            logging.debug("NOTE: using low fps mode! (will use extra thread+queue to discard buffered frames)")
            self.q = queue.Queue()

    def release(self):
        logging.debug("Will release capture.")
        self.stop_unbuffer_thread()
        self.capture.release()

    def stop_unbuffer_thread(self):
        self.unbuffer_thread_running = False
        self.unbuffer_thread.join()

    def start_unbuffer_thread(self):
        self.unbuffer_thread = threading.Thread(target=self.unbuffer_reader)
        self.unbuffer_thread_running = True
        self.unbuffer_thread.start()

    def open(self):
        try:
            self.capture = cv2.VideoCapture(self.device)
            if not self.capture.isOpened():
                # sometimes, the capture will not open at object instantiation
                # however it may work when retrying with the open() method on the now existing object
                retries, max_retries = 0, 3
                while retries < max_retries and not self.capture.isOpened():
                    time.sleep(2)
                    self.capture.open(self.device)
                    retries += 1
            if self.capture.isOpened():
                self.start_unbuffer_thread()
        except Exception as e:
            logging.error("Can't connect to camera {}".format(str(self.device)))
            logging.error("Reason: {}".format(str(e)))
            return None

        if self.capture is None or not self.capture.isOpened():
            logging.error("Can't connect to camera {}".format(str(self.device)))
            return None

        if self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) == 0 or self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT) == 0:
            self.capture.release()
            logging.error("Câmera {} não está funcionando corretamente. WIDTH/HEIGH == 0".format(str(self.device)))
            return None

        logging.info("LabradorWebcam opened")
        return True

    def set_resolution(self, target_res):
        target_res = target_res.lower()

        if target_res not in LabradorWebcam.resolutions.keys():
            logging.error("Invalid target video resolution. Should be one of: sd, hd, full-hd. Given: {}.".format(target_res))
            return False

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,  LabradorWebcam.resolutions[target_res]["width"])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, LabradorWebcam.resolutions[target_res]["height"])
        
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
        if self.low_fps_mode:
            return True, self.q.get()
        else:
            return self.capture.read()

    # read frames as soon as they are available, keeping only most recent one
    def unbuffer_reader(self):
        logging.info("unbuffer_reader started.")
        while self.unbuffer_thread_running:
            if not self.capture:
                time.sleep(1)
                continue
            ret, frame = self.capture.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)
        logging.info("unbuffer_reader stopped.")
