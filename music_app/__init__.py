import logging
import threading
from time import sleep
from flask import Flask
from music_app.settings import LOGLEVEL, UPDATE_INTERVAL
from music_app.get_json import main

logger = logging.getLogger('music_app')
logger.setLevel(getattr(logging, LOGLEVEL))
ch = logging.StreamHandler()
ch.setLevel(getattr(logging, LOGLEVEL))
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def update_db():
    logger.info("Triggering Update")
    while True:
        sleep(UPDATE_INTERVAL * 60)
        main()

app = Flask(__name__)

import music_app.views
t = threading.Thread(target=update_db)
t.start()

