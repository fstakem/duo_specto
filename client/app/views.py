# <-----------------------------------------< Header >----------------------------------------->
#
#       views.py
#       By: Fredrick Stakem
#       Date: 3.4.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is for the web server controller functions.

"""


# Libraries
from app import flask_app, logger
from app import project_path, app_path, recent_imgs_path, old_imgs_path, working_path
from flask import Flask, request, send_from_directory
import datetime
from threading import Thread
#from mock_capture import simple_capture
from basic_capture import simple_capture
from file_download import get_images


@flask_app.route('/', methods=['GET'])
def index():
    output = 'Client up and running.'
    logger.debug(output)

    return output

@flask_app.route('/capture', methods=['GET'])
def capture():
    filename = request.args.get('filename')
    width = request.args.get('width')
    height = request.args.get('height')

    output_file = recent_imgs_path + '/generic_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.jpg'
    resolution = (2592, 1944)

    if filename != None and len(filename) > 5 and filename[-4:] == 'jpg':
        output_file = recent_imgs_path + '/' + filename

    if width != None and height != None:
        resolution = (int(width), int(height))

    thread = Thread(target=simple_capture, args=[output_file, resolution])
    thread.start()

    return 'Image captured'

@flask_app.route('/fetch_imgs', methods=['GET'])
def fetch_imgs():
    tarball_path = get_images(recent_imgs_path, old_imgs_path, working_path)
    tarball = tarball_path.split('/')[-1]

    return send_from_directory(working_path, tarball, as_attachment=True)



