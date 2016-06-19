import os

from main import app
import settings



if __name__ == '__main__':
    #app.debug = True
    #app.config['SECRET_KEY'] = "kljasdno9asud89uy981uoaisjdoiajsdm89uas980d"
    #app.config['DATABASE'] = (0, settings.DATABASE_NAME)

    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
