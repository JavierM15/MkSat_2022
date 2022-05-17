from time import sleep
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1024,768)
camera.start_preview()
sleep(5)
camera.capture('prueba1.jpg')
camera.stop_preview()
sleep(10)
# Videos
# camera.start_preview()
# camera.start_recording('test_video.h264')
# sleep(5)
# camera.stop_recording()
# camera.stop_preview()