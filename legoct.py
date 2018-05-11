#!/usr/bin/python
#Frederick Henry Brutton fredbrutton@gmail.com
#David Mills d.mills@qmul.ac.uk

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import io
import shutil
import time
import atexit
import picamera

#GPIO pin for the light source
from gpiozero import LED
light = LED(6)

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

    
def Test():
    while True:
		camera.start_preview()
		time.sleep(5)
		camera.stop_preview()
		Choice = raw_input("Is this brightness acceptable?(Y/N)\n")
		if Choice == "Y":
			break
		if Choice == "N":
			Speed = int(input("Input new brightness:\n"))
			camera.shutter_speed = Speed
		else:
			print("Only enter either Y or N")

def outputs():
    stream = io.BytesIO()
    global NumImage
    global ScanName
    for i in range(NumImage):
        # This returns the stream for the camera to capture to
        yield stream
        # Once the capture is complete, the loop continues here
        # (read up on generator functions in Python to understand
        # the yield statement). Here you could do some processing
        # on the image...
        stream.seek(0)
        filename = ScanName + '_%03d.jpeg'
        with open(filename %i, 'wb') as f:
             shutil.copyfileobj(stream, f, length=131072)
        #img = Image.open(stream)
        # Finally, reset the stream for the next capture
 	myStepper.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
        stream.seek(0)
        stream.truncate()



with picamera.PiCamera() as camera:
    light.on()
    camera.vflip = 1
    camera.resolution = (640,480)
    #camera.resolution = (320, 240)
    camera.framerate = 25
    #camera.color_effects = (128,128)
    #camera.iso = 800
    camera.shutter_speed = 100000 #100000
    camera.exposure_compensation = 2 #2
    #camera.exposure_mode = 'off'
    #g = camera.awb_gains
    #print(g)
    #camera.awb_mode = 'off'
    camera.awb_gains = 5.0 #5.0
    #raw_input("PUT ON ITEM FOR SCANNING TEST (press ENTER)")
    #Test()
    #raw_input("REMOVE OBJECT (press ENTER)")
    #time.sleep(2)
    #camera.capture("light.jpeg")
    #raw_input("TURN THE LIGHT OFF AND REPLACE THE OBJECT(press ENTER)")
    #time.sleep(2)
    #camera.capture("dark.jpeg")
    ScanName = raw_input("What is the item?")
    
    NumImage = 201
    camera.start_preview()
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    print('Captured % images at %.2ffps' % (NumImage, 40 / (finish - start)))
    camera.stop_preview()
    light.off()
