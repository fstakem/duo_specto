# <-----------------------------------------< Header >----------------------------------------->
#
#       camera_controller.py
#       By: Fredrick Stakem
#       Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to control the raspberry pi camera.

"""


# Libraries
import argparse
import os
import datetime
from threading import Thread
from flask import Flask, request, send_from_directory
from mock_capture import simple_capture
from file_download import get_images


# Command line
parser = argparse.ArgumentParser(description='Server command line options.')
parser.add_argument('--port', 
                    default=8080,
                    type=int,
                    help='port for the server')
parser.add_argument('--debug', 
                    dest='debug',
                    action='store_true',
                    help='debug version of server')
parser.add_argument('--prod', 
                    dest='debug',
                    action='store_false',
                    help='production version of server')
parser.set_defaults(debug=False)
args = parser.parse_args()


# Path variables
file_path = os.path.realpath(__file__)
directories = file_path.split('/')[:-1]
src_path = '/'.join(directories)
directories.append('recent_imgs')
recent_imgs_path = '/'.join(directories)
directories[-1] = 'old_imgs'
old_imgs_path = '/'.join(directories)


flask_app = Flask(__name__)


@flask_app.route('/', methods=['GET'])
def index():
    return 'Client up and running.'

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
    tarball_path = get_images(recent_imgs_path, old_imgs_path, src_path)
    tarball = tarball_path.split('/')[-1]

    return send_from_directory(src_path, tarball, as_attachment=True)

if __name__ == '__main__':
    flask_app.run(debug=args.debug, port=args.port)
