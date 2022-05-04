from labrador_camera import TomateCameraSD
from datetime import datetime
import sys, os, time
import cv2

scripts_dir = os.getenv("TOMATE_SCRIPTS_DIR") or "/home/geovane/dev/cmss/cmss-scripts/camera-tomate/"
photos_dir = os.getenv("PHOTOS_DIR") or os.getcwd() + "/frames-tomate/"
tomate_cam_sd = TomateCameraSD(scripts_dir=scripts_dir, photos_dir=photos_dir)
tomate_cam_sd.open()
while True:
    ret, img = tomate_cam_sd.read()

    if ret:
        print("Got reading")
        cv2.namedWindow('tomate_sd frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('tomate_sd frame', 400, 400)
        cv2.imshow('tomate_sd frame', img)
        cv2.waitKey(1)
    else:
        print("Empty reading")

    # simulate processing time...
    print("Processing 1 ..")
    time.sleep(0.5)
    print("Processing 2 ..")
    time.sleep(0.5)
