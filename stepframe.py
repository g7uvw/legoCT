#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import io
import time
import atexit
import picamera
#from PIL import Image

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(30)             # 30 RPM



def outputs():
    stream = io.BytesIO()
    for i in range(201):
        # This returns the stream for the camera to capture to
        yield stream
        # Once the capture is complete, the loop continues here
        # (read up on generator functions in Python to understand
        # the yield statement). Here you could do some processing
        # on the image...
        #stream.seek(0)
        #img = Image.open(stream)
        # Finally, reset the stream for the next capture
 	myStepper.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
        stream.seek(0)
        stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (800, 600)
    camera.framerate = 25
    camera.iso = 800
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    camera.start_preview()
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    print('Captured 201 images at %.2ffps' % (40 / (finish - start)))
    camera.stop_preview()

