import time, logging, os, subprocess, json, cv2

class TomateCameraSD():
    # Note: this class requires a directory with the camera tomate scripts.

    def __init__(self, scripts_dir, photos_dir):
        if not os.path.exists(scripts_dir):
            raise f"{scripts_dir} not found"
        self.scripts_dir = scripts_dir
        self.photos_dir = photos_dir

    def open(self):
        os.system(f"cd {self.scripts_dir} && ./load_scripts.sh && ./adb_set_mode.sh photo")

    def read(self):
        photo_info = self.save_frame()
        if photo_info:
            return cv2.imread(photo_info["last_photo"], 0)

    def save_frame(self):
        code = os.system(f"cd {self.scripts_dir} && ./adb_take_photo.sh one {self.photos_dir}")
        print(">>>> ", code)

        resp = subprocess.run(f"cd {self.scripts_dir} && ./adb_take_photo.sh one {self.photos_dir}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out = resp.stdout.decode()
            photo_info = list(filter(lambda l: '{"last_photo":' in l, out.split("\n")))[0]
            photo_info = json.loads(photo_info)
            print("Photo was saved: ", photo_info)
            return photo_info
        except Exception as e:
            print(f"Error saving frame: {e}")
