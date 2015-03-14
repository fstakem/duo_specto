# <-----------------------------------------< Header >----------------------------------------->
#
#       photo.py
#       By: Fredrick Stakem
#       Date: 3.13.15
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to hold information about a camera photo.

"""


# Libraries
#


class Photo(object):

	def __init__(self, name, path, url):
		self.name = name
		self.path = path
		self.url = url

	def __str__(self):
		output = 'Photo: %s @ %s' % (self.name, self.short_path)
		return output