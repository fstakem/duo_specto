import os
basedir = os.path.abspath(os.path.dirname(__file__))

env = 'prod'

CSRF_ENABLED = True
SECRET_KEY = 'I like apples!'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024