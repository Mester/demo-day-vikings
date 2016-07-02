from flask import Flask
from config import LOGLEVEL

app = Flask(__name__)

import my_app.views


