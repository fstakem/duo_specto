# <-----------------------------------------< Header >----------------------------------------->
#
#       camera.py
#       By: Fredrick Stakem
#       Date: 3.3.15
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to hold information about a raspberry pi camera.

"""


# Libraries
#


class Camera(object):

	def __init__(self, name, ip_address):
		self.name = name
		self.ip_address = ip_address
		self.imgs = []

	def __str__(self):
		output = 'Camera: %s @ %s' % (self.name, self.ip_address)
		return output