import logging
from flask import Flask
from music_app.settings import LOGLEVEL

logger = logging.getLogger('music_app')
logger.setLevel(getattr(logging, LOGLEVEL))
ch = logging.StreamHandler()
ch.setLevel(getattr(logging, LOGLEVEL))
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Flask(__name__)

import music_app.views
