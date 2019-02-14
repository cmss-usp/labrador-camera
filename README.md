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

## Simple example
`python3 examples/simple.py`

## Image collection example with IP camera

If using HikVision:
```bash
python examples/collect_frames_ipcam.py 'rtsp://admin:caninos123%21%40%23@192.168.1.64:554/'
```

If using aivision:
```bash
python examples/collect_frames_ipcam.py 'rtsp://root:pass@192.168.150.146:554/ufirststream'
```

