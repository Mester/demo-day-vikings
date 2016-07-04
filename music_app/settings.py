import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = "db.json"
LOGLEVEL = "DEBUG"
UPDATE_INTERVAL = 20
BROKER = "amqp://localhost:5001"
