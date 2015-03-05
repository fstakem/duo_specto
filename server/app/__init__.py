import logging
import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap

flask_app = Flask(__name__)
bootstrap = Bootstrap(flask_app)
flask_app.config.from_object('config')


logger = logging.getLogger('IoT Server')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d | %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

project_path = '/'.join( os.path.realpath(__file__).split('/')[:-2] )
app_path = '/'.join( os.path.realpath(__file__).split('/')[:-1] )
imgs_path = project_path + '/imgs'
working_path = project_path + '/tmp'


from app import views