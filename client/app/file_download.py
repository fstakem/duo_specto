# <-----------------------------------------< Header >----------------------------------------->
#
#		file_download.py
#		By: Fredrick Stakem
#		Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to compress image files for download.

"""


# Libraries
import tarfile
import os
import shutil

def delete_img(img_name):
	try:
	    os.remove(img_name)
	except OSError:
	    pass

def delete_imgs(paths):
	shutil.rmtree(paths + '/*')


def get_images(from_path, to_path, working_path):
	tarball_name = 'tmp.tar.gz'
	tarball_src_path = working_path + '/' + tarball_name
	tarball_dest_path = to_path + '/' + tarball_name

	remove_tarball(tarball_src_path)
	create_tarball(from_path, tarball_src_path)
	shutil.copy(tarball_src_path, tarball_dest_path)
	extract_tarball(tarball_dest_path, to_path)
	remove_tarball(tarball_dest_path)
	remove_imgs(from_path)
		
	return tarball_src_path

def remove_tarball(tarball_path):
	if os.path.isfile(tarball_path):
		os.remove(tarball_path) 

def create_tarball(from_path, tarball_path):
	tar = tarfile.open(tarball_path, "w:gz")

	for filename in os.listdir(from_path):
		tar.add(from_path + '/' + filename, filename)

	tar.close()

def extract_tarball(tarball_path, to_path):
	tar = tarfile.open(tarball_path)
	tar.extractall(to_path)
	tar.close()

def remove_imgs(path):
	files = os.listdir(path)
	for filename in files:
		if filename != '.gitignore':
 			os.remove(path + '/' + filename)
	

if __name__ == '__main__':
	file_path = os.path.realpath(__file__)
	directories = file_path.split('/')[:-1]
	src_path = '/'.join(directories)
	directories.append('recent_imgs')
	recent_imgs_path = '/'.join(directories)
	directories[-1] = 'old_imgs'
	old_imgs_path = '/'.join(directories)
	
	get_images(recent_imgs_path, old_imgs_path, src_path)
