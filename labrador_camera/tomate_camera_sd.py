import time, logging, os, subprocess, json, cv2

class TomateCameraSD():
    # Note: this class requires a directory containing the camera tomate scripts.

    def __init__(self, scripts_dir, photos_dir):
        if not os.path.exists(scripts_dir):
            raise f"{scripts_dir} not found"
        self.scripts_dir = scripts_dir
        self.photos_dir = photos_dir

    def open(self):
        os.system(f"cd {self.scripts_dir} && ./load_scripts.sh && ./adb_set_mode.sh photo")

    def release(self):
        pass

    def read(self):
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
        resp = subprocess.run(f"cd {self.scripts_dir} && ./adb_take_photo.sh one {self.photos_dir}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
