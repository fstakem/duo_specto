# <-----------------------------------------< Header >----------------------------------------->
#
#		mock_capture.py
#		By: Fredrick Stakem
#		Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to mock the capture of an image from the raspberry pi.

"""


# Libraries
# None


def simple_capture(output_file, resolution):
	print 'Capture image: %s with resolution: (%d, %d)' % (output_file, resolution[0], resolution[1]) 