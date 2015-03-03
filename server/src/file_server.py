# <-----------------------------------------< Header >----------------------------------------->
#
#       file_server.py
#       By: Fredrick Stakem
#       Date: 2.28.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to collect images from the raspberry pi.

"""


# Libraries
import argparse
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
import urllib2
import datetime
from threading import Thread
import shutil


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
directories = file_path.split('/')[:-2]
directories.append('imgs')
imgs_path = '/'.join(directories)
directories[-1] = 'tmp'
working_path = '/'.join(directories)


ALLOWED_EXTENSIONS = set(['data', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

flask_app = Flask(__name__)
flask_app.config['UPLOAD_FOLDER'] = imgs_path
flask_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

host_list = ['192.168.1.4']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if args.debug:
    @flask_app.route('/upload', methods=['GET'])
    def upload_file_page():
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''

    @flask_app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(flask_app.config['UPLOAD_FOLDER'],
                                   filename)

@flask_app.route('/', methods=['GET'])
def index():
    return 'Server up and running.'

@flask_app.route('/upload', methods=['POST'])
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

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def capture_image(host, filename, resolution):
    url = 'http://%s:8080/capture?filename=%s&width=%s&height=%s' % (host, filename, str(resolution[0]), str(resolution[1]))
    print url
    response = urllib2.urlopen(url)
    html = response.read()

    print 'Host: ' + host
    print html

@flask_app.route('/capture', methods=['GET'])
def capture():
    filename = request.args.get('filename')
    width = request.args.get('width')
    height = request.args.get('height')

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    resolution = (2592, 1944)

    if width != None and height != None:
        resolution = (int(width), int(height))

    for host in host_list:
        filename_end =  '_' + host + '_' + timestamp + '.jpg'

        if filename != None and len(filename) > 0:
            filename = filename + filename_end
        else:
            filename = 'img' + filename_end

        thread = Thread(target=capture_image, args=[host, filename, resolution])
        thread.start()

    return 'Images captured'

def download_imgs(host):
    url = 'http://%s:8080/fetch_imgs' % (host)
    output_filename = 'imgs_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.tar.gz'
    f = urllib2.urlopen(url)

    with open(os.path.basename(output_filename), "wb") as local_file:
        local_file.write(f.read())

    shutil.move('./' + output_filename, working_path)

@flask_app.route('/fetch_imgs', methods=['GET'])
def fetch_imgs():
    for host in host_list:
        thread = Thread(target=download_imgs, args=[host])
        thread.start()

    return 'Images downloaded'

if __name__ == '__main__':
    flask_app.run(debug=args.debug, port=args.port)


