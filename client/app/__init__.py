import logging
import os
from flask import Flask

flask_app = Flask(__name__)
flask_app.config.from_object('config')


logger = logging.getLogger('Pi IOT Server')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d | %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

project_path = '/'.join( os.path.realpath(__file__).split('/')[:-2] )
app_path = '/'.join( os.path.realpath(__file__).split('/')[:-1] )
recent_imgs_path = project_path + '/' + 'recent_imgs'
old_imgs_path  = project_path + '/' + 'old_imgs'
working_path = project_path + '/' + 'tmp'


from app import views