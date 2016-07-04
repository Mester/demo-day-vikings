import os
from time import sleep
from tinydb import TinyDB
from celery import Celery
from music_app.get_json import *
from music_app.settings import UPDATE_INTERVAL, BROKER

app = Celery('tasks', broker=BROKER)

@app.task
def update_database():
    while True:
        print "Updating Database"
        db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
        json_data = get_json_from_subreddit("hot")
        json_list = []
        for data in json_data:
            for post in data['data']['children']:
                if is_post_valid(post):
                    j = convert_post_to_json(post)
                    if j is not None:
                        insert_into_database(db, j)
        print "Done... Now sleeping"
        sleep( 60 * UPDATE_INTERVAL )
