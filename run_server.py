import os
import binascii
import logging
from my_app.config import LOGLEVEL

from my_app import app, settings


if __name__ == '__main__':
    logger = logging.getLogger('music_app')
    logger.setLevel(getattr(logging, LOGLEVEL))
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, LOGLEVEL))
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    app.debug = True
    app.secret_key = binascii.hexlify(os.urandom(24))
    app.config['DATABASE'] = (0, settings.DATABASE_NAME)

    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)

