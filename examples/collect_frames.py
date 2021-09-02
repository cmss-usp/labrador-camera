from labrador_camera import LabradorCamera
from datetime import datetime
import sys, os, time

device = int(sys.argv[1]) if len(sys.argv) == 2 else 0

lab_cam = LabradorCamera(device)
lab_cam.open()

frames_path = os.getcwd() + f"/frames-{device}/"
if not os.path.exists(frames_path):
    os.mkdir(frames_path)

def save(params):
    lab_cam.set_params(**params)
    filename = frames_path + f"{datetime.now()}-{params['resolution']}.jpg"
    print(f"Saving {filename}")
    lab_cam.save_frame(filename)

while True:
    save({"resolution": "sd"})
    time.sleep(0.2)

    save({"resolution": "hd"})
    time.sleep(0.2)

    save({"resolution": "full-hd"})
    time.sleep(0.2)
