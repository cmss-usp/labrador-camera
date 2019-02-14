from labrador_camera import LabradorCamera
from datetime import datetime
import sys, os, time, re

device = sys.argv[1] if len(sys.argv) == 2 else "rtsp://admin:caninos123%21%40%23@192.168.1.64:554/"

ip_port = re.sub(r'.*@(.*)/+.*', '\\1', device)
frames_path = os.getcwd() + f"/frames-{ip_port}/"
print(f"frames_path is {frames_path}")
if not os.path.exists(frames_path):
    os.mkdir(frames_path)

lab_ipcam = LabradorCamera(device=device)
lab_ipcam.open()

def save_ipcam():
    filename = frames_path + f"{datetime.now()}.jpg"
    print(f"Saving {filename}")
    lab_ipcam.save_frame(filename)

while True:
    save_ipcam()
