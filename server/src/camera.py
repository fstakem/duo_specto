# <-----------------------------------------< Header >----------------------------------------->
#
#       camera.py
#       By: Fredrick Stakem
#       Date: 3.3.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to hold information about a raspberry pi camera.

"""


# Libraries
# None

class Camera(object):

	def __init__(self):
		self.name = ''
		self.ip_address = ''
		self.recent_imgs = []

	def __str__(self):
		output = 'Camera: %s @ %s' % (self.name, self.ip_address)
		return output