import os
import binascii

from my_app import app, settings

if __name__ == '__main__':
    app.debug = True
    app.secret_key = binascii.hexlify(os.urandom(24))
    app.config['DATABASE'] = (0, settings.DATABASE_NAME)

    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)

