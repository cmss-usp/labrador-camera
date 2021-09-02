from labrador_camera import LabradorCamera

lab_cam = LabradorCamera()

lab_cam.open()

lab_cam.save_frame(f"frame-sd.jpg")

lab_cam.set_params(resolution="hd")
lab_cam.save_frame(f"frame-hd.jpg")

lab_cam.set_params(resolution="hd", video_codec="mjpg")
lab_cam.save_frame(f"frame-hd-mjpg.jpg")
