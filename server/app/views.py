# <-----------------------------------------< Header >----------------------------------------->
#
#       views.py
#       By: Fredrick Stakem
#       Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is has the IOT server controller functions.

"""


# Libraries
from app import flask_app, logger
from app import project_path, app_path, imgs_path, working_path
from flask import Flask, request, Response
from flask import render_template
from werkzeug import secure_filename
from flask import send_from_directory
import urllib2
from urllib2 import URLError
import datetime
from threading import Thread
import shutil
from camera import Camera
import tarfile
import json


ALLOWED_EXTENSIONS = set(['data', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
cameras = [ Camera('left', '192.168.1.4'), Camera('right', '192.168.1.5') ]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(flask_app.config['UPLOAD_FOLDER'],
                               filename)

@flask_app.route('/', methods=['GET'])
def index():
    logger.debug('Rendering main page.')

    return render_template('index.html')

@flask_app.route('/cameras', methods=['GET'])
def cameras():
    logger.debug('Rendering camera page.')

    return render_template('cameras.html')

@flask_app.route('/capture_photo', methods=['POST'])
def capture_photo():
    logger.debug('Capturing photos.')

    data = json.loads(request.data)
    for camera in data['cameras']:
        camera_name = camera['name']
        camera_ip = camera['ip_address']

        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        resolution = (2592, 1944)
        filename =  'pic_' + camera_name + '_' + timestamp + '.jpg'

        url = 'http://%s:8080/capture?filename=%s&width=%s&height=%s' % (camera_ip, filename, str(resolution[0]), str(resolution[1]))
        response = urllib2.urlopen(url)
        html = response.read()
        logger.debug('Making a call to: %s' % url)

        try:
            response = urllib2.urlopen(url)
            html = response.read()

            if html != 'image captured':
                logger.error('Error capturing image from %s(%s): %s' % (camera_name, camera_ip, str(e))
                return 'capture_error'

        except URLError as e:
            logger.error('Error capturing image from %s(%s): %s' % (camera_name, camera_ip, str(e))
            return 'capture_error'

    return 'successful capture'

@flask_app.route('/fetch_photo', methods=['POST'])
def fetch_photo():
    logger.debug('Fetching photos.')

    return 'Fetch!'

@flask_app.route('/search_camera', methods=['POST'])
def search_camera():
    logger.debug('Searching for camera.')
    ip_address = request.data

    url = 'http://%s:8080/' % ip_address[1:-1]
    logger.debug('Making a call to: %s' % url)

    try:
        response = urllib2.urlopen(url)
        html = response.read()

        if html == 'Client up and running.':
            return 'found'
    except URLError as e:
        logger.error('Error searching for camera: ' + str(e))


    return 'not_found'

@flask_app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], filename))

            if args.debug:
                return redirect( url_for('uploaded_file', filename=filename) )
            else:
                return 'success'
    else:
        return render_template('upload.html')

def capture_image(camera, filename, resolution):
    url = 'http://%s:8080/capture?filename=%s&width=%s&height=%s' % (camera.ip_address, filename, str(resolution[0]), str(resolution[1]))
    response = urllib2.urlopen(url)
    html = response.read()

@flask_app.route('/capture', methods=['GET'])
def capture():
    filename = request.args.get('filename')
    width = request.args.get('width')
    height = request.args.get('height')

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    resolution = (2592, 1944)

    if width != None and height != None:
        resolution = (int(width), int(height))

    for camera in cameras:
        filename_end =  '_' + camera.name + '_' + timestamp + '.jpg'

        if filename != None and len(filename) > 0:
            filename = filename + filename_end
        else:
            filename = 'img' + filename_end

        thread = Thread(target=capture_image, args=[camera, filename, resolution])
        thread.start()

    return 'Images captured'

def download_imgs(camera):
    url = 'http://%s:8080/fetch_imgs' % (camera.ip_address)
    output_filename = 'imgs_' + camera.name + '.tar.gz'
    f = urllib2.urlopen(url)

    with open(os.path.basename(output_filename), "wb") as local_file:
        local_file.write(f.read())

    img_path = working_path + '/' + camera.name
    if not os.path.exists(img_path):
        os.mkdir(img_path)

    files = os.listdir(img_path)
    for filename in files:
        if filename != '.gitignore':
            os.remove(img_path + '/' + filename)

    shutil.move('./' + output_filename, img_path)

    tarball_path = img_path + '/' + output_filename
    tar = tarfile.open(tarball_path)
    tar.extractall(img_path)
    tar.close()
    os.remove(tarball_path)

    files = os.listdir(img_path)
    for filename in files:
        if filename != '.gitignore':
            camera.recent_imgs.append(img_path + '/' + filename)

@flask_app.route('/fetch_imgs', methods=['GET'])
def fetch_imgs():
    for camera in cameras:
        thread = Thread(target=download_imgs, args=[camera])
        thread.start()

    return 'Images downloaded'





