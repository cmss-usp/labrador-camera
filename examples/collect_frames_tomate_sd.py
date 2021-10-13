from labrador_camera import TomateCameraSD
from datetime import datetime
import sys, os, time
import cv2

# TOMATE_SCRIPTS_DIR=~/bin/android/platform-tools/camera-tomate-scripts PHOTOS_DIR=~/.cmss_dev/evidences/frames python examples/collect_frames_tomate_sd.py

scripts_dir = os.getenv("TOMATE_SCRIPTS_DIR") or "/home/geovane/bin/android/platform-tools/camera-tomate-scripts"
photos_dir = os.getenv("PHOTOS_DIR") or os.getcwd() + "/frames-tomate/"
tomate_cam_sd = TomateCameraSD(scripts_dir=scripts_dir, photos_dir=photos_dir)
tomate_cam_sd.open()
while True:
    tomate_cam_sd.save_frame()
    # img = tomate_cam_sd.read()
    time.sleep(0.1)
