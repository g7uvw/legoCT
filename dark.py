#!/usr/bin/python
import picamera
import time

print('Taking Dark Frame - turn off lights')

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 25
#    camera.color_effects = (128,128)
    camera.iso = 800
    camera.exposure_compensation = 2
    camera.shutter_speed = 100000
    #camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = 5.0
    time.sleep(2)
    camera.start_preview()
    camera.capture('dark.jpeg')
    camera.stop_preview()
