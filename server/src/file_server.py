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
root_dir = file_path.split('/')[:-3]
root_dir.append('img')
img_dir = '/'.join( root_dir )


ALLOWED_EXTENSIONS = set(['data', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

flask_app = Flask(__name__)
flask_app.config['UPLOAD_FOLDER'] = img_dir
flask_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


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

if __name__ == '__main__':
    flask_app.run(debug=args.debug, port=args.port)


