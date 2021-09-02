Capture frames from a camera connected to the Labrador. 

- relies on OpenCV as layer for camera capture
- offers easy options to set: resolution, video_codec
- will retry opening camera to circunvent timeout issues with Labrador

# Install

```bash
git clone https://github.com/cmss-usp/labrador-camera.git
cd labrador-camera
pip3 install -e .
```

# Run

`python3 examples/simple.py`
