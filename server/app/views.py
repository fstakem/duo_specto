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
import simplejson
import time
from app import flask_app, logger
from app import db
from app import project_path, app_path, imgs_path, working_path
from app.models import Crash, Device
from flask import Flask, request, Response
from flask import render_template
from werkzeug import secure_filename
from flask import send_from_directory
import urllib2
import datetime
from threading import Thread
import shutil
from camera import Camera
import tarfile


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





