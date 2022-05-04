import time, logging, os, subprocess, json, cv2, threading, queue
from datetime import datetime

class TomateCameraSD():
    # Note: this class requires a directory containing the camera tomate scripts.

    def __init__(self, scripts_dir, photos_dir):
        if not os.path.exists(scripts_dir):
            raise f"{scripts_dir} not found"
        self.scripts_dir = scripts_dir
        self.photos_dir = photos_dir
        self.latest_frame_info = False, None
        self.queue1 = queue.Queue()

    def open(self, with_thread=True):
        os.system(f"cd {self.scripts_dir} && ./load_scripts.sh && ./adb_set_mode.sh photo")
        if with_thread:
            self.start_continous_reader_thread()

    def read(self):
        ret, img = self.latest_frame_info
        if ret:
            self.latest_frame_info = False, None
            return ret, img
        else:
            return False, None

    def release(self):
        logging.debug("Will release capture.")
        self.stop_continous_reader_thread()

    def stop_continous_reader_thread(self):
        self.continous_reader_thread_running = False
        self.continous_reader_thread.join()

    def start_continous_reader_thread(self):
        self.continous_reader_thread = threading.Thread(target=self.continous_reader)
        self.continous_reader_thread_running = True
        self.continous_reader_thread.start()

    # read frames as soon as they are available, keeping only most recent one
    def continous_reader(self):
        logging.info("continous_reader started.")
        while self.continous_reader_thread_running:
            ret, frame = self.read_sync()
            if not ret:
                break
            self.latest_frame_info = ret, frame
            # if not self.queue1.empty():
            #     try:
            #         self.queue1.get_nowait()   # discard previous (unprocessed) frame
            #     except queue.Empty:
            #         pass
            # self.queue1.put(frame)   # add most recent frame to queue
        logging.info("continous_reader stopped.")

    def read_sync(self):
        photo_info = self.save_frame()
        if photo_info:
            try:
                img = cv2.imread(photo_info["new_photo"])
                return True, img
            except Exception as e:
                print(e)
                return False, None
        else:
            return False, None

    def save_frame(self):
        cmd = f"cd {self.scripts_dir} && ./adb_take_photo.sh one {self.photos_dir}"
        logging.debug(f"Will run cmd: {cmd}")
        resp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out = resp.stdout.decode()
            photo_info = list(filter(lambda l: '{"new_photo":' in l, out.split("\n")))[0]
            photo_info = json.loads(photo_info)
            print("Photo was saved: ", photo_info)
            return photo_info
        except Exception as e:
            logging.exception(f"Error saving frame.")

    def get_dimensions(self):
        return 3456, 4608 # considering 4K images
