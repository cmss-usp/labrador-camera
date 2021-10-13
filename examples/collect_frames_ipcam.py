from labrador_camera import LabradorCameraCV
from datetime import datetime
import sys, os, time

device = sys.argv[1] if len(sys.argv) == 2 else "rtsp://admin:caninos123%21%40%23@192.168.1.64:554/"

lab_ipcam = LabradorCameraCV(device=device)
lab_ipcam.open()

frames_path = os.getcwd() + f"/frames-{device[-17:-5]}/"
if not os.path.exists(frames_path):
    os.mkdir(frames_path)

def save_ipcam():
    filename = frames_path + f"{datetime.now()}.jpg"
    print(f"Saving {filename}")
    lab_ipcam.save_frame(filename)

while True:
    save_ipcam()
