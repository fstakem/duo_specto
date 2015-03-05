# <-----------------------------------------< Header >----------------------------------------->
#
#       start.py
#       By: Fredrick Stakem
#       Date: 3.4.14
#
#
# <-----------------------------------------<---~~--->----------------------------------------->

"""
This file is used to start the raspberry pi server.

"""


# Libraries
import argparse
import os
from app import flask_app, logger

# Get command line arguments
parser = argparse.ArgumentParser(description='Command line options.')
parser.add_argument('--port', type=int, default=8080)
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

# Setup project
script_name = os.path.basename(__file__).split('.')[0]


# Main loop
if __name__ == "__main__":
    logger.debug('Starting server...')
    logger.debug('Server port: %d' % (args.port))
    flask_app.run(host='0.0.0.0', port=args.port, debug=args.debug)