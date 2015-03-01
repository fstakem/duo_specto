# <-----------------------------------------< Header >----------------------------------------->
#
#		basic_capture.py
#		By: Fredrick Stakem
#		Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to test the basic camera ability of the raspberry pi.

"""


# Libraries
import time
import picamera


def simple_capture(output_file, resolution):
	with picamera.PiCamera() as camera:
		camera.resolution = (2592, 1944)
		camera.capture(output_file)
