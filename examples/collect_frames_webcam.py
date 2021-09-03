from labrador_camera import LabradorWebcam
from datetime import datetime
import sys, os, time

device = sys.argv[1] if len(sys.argv) == 2 else 0

lab_webcam = LabradorWebcam(device=device)
lab_webcam.open()

frames_path = os.getcwd() + f"/frames-{device}/"
if not os.path.exists(frames_path):
    os.mkdir(frames_path)

def save_webcam(params):
    lab_webcam.set_params(**params)
    filename = frames_path + f"{datetime.now()}-{params['resolution']}.jpg"
    print(f"Saving {filename}")
    lab_webcam.save_frame(filename)

while True:
    save_webcam({"resolution": "hd"})
    save_webcam({"resolution": "hd"})
    save_webcam({"resolution": "hd"})
    save_webcam({"resolution": "hd"})
    save_webcam({"resolution": "hd"})
    time.sleep(0.2)

    save_webcam({"resolution": "full-hd"})
    save_webcam({"resolution": "full-hd"})
    save_webcam({"resolution": "full-hd"})
    save_webcam({"resolution": "full-hd"})
    save_webcam({"resolution": "full-hd"})
    time.sleep(0.2)
