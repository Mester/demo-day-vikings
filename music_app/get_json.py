import requests
import os
import logging
import re
from tinydb import TinyDB, Query
from music_app.utils import parse_listing
from music_app.settings import DATABASE_NAME

logger = logging.getLogger('music_app.get_json')

def get_json_from_subreddit(sort_type):
    """
    Method to get the json from listentothis subreddit
    """
    json_list = []
    url = "https://www.reddit.com/r/ListenToThis/{}.json?limit=100"
    headers = {"User-Agent":"ChangeMeClient/0.1 by username"}
    r = requests.get(url.format(sort_type), headers=headers)
    if r.ok:
        before = r.json()['data']['before']
        after = r.json()['data']['after']
        json_list.append(r.json())
        while after != None:
            url = "https://www.reddit.com/r/ListenToThis/{}.json?limit=100&after={}".format(sort_type, after)
            r = requests.get(url, headers=headers)
            if r.ok:
                before = r.json()['data']['before']
                after = r.json()['data']['after']
                json_list.append(r.json())
            else: 
                logger.debug("Request fail")
                break
        return json_list
    else:
        logger.debug("Request fail")

def is_post_valid(post):
    """
    Returns True if the post contains a media key
    Returns False otherwise
    """
    if post['data']['media'] != None:
        return True
    return False

def convert_post_to_json(post):
    """
    Returns a json object of the post
    Assumes that the post is valid
    """
    post_json = {}
    regex = re.compile(r"""
                (?P<artist>.+)  # The artist
                \s*-+\s*        # Skip some spaces and dashes
                (?P<title>.*)   # The title
                \s*\[           # Skip some spaces and opening bracket
                (?P<genre>.*)   # The genre
                \]\s*\(         # Skip closing bracket, spaces and opening parenthesis
                (?P<year>\d+)   # The year
                \)              # Skip closing parenthesis
                    """, re.VERBOSE | re.IGNORECASE)
    post_title = post['data']['title']
    m = regex.search(post_title)
    if m is None:
        return None
    if m.group('artist'):
        post_json['artist'] = m.group('artist')
    if m.group('title'):
        post_json['title'] = m.group('title')
    if m.group('genre'):
        post_json['genre'] = m.group('genre')
    if m.group('year'):
        post_json['year'] = m.group('year')
    post_json['score'] = post['data']['score']
    post_json['url'] = post['data']['url']
    post_json['timestamp'] = post['data']['created_utc']
    post_json['thumbnail'] = post['data']['thumbnail']

    return post_json

def is_json_unique(db, json_object):
    """
    Checks if the url of this post is present in 
    the database already
    """
    q = Query()
    if len(db.search(q.url == json_object['url'])) == 0:
        return True
    return False

def insert_into_database(db, json_object):
    """
    inserts the json_object into the database
    """
    if is_json_unique(db, json_object):
        db.insert(json_object)

if __name__ == '__main__':
    db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
    json_data = get_json_from_subreddit("hot")
    json_list = []
    for data in json_data:
        for post in data['data']['children']:
            if is_post_valid(post):
                j = convert_post_to_json(post)
                if j is not None:
                    insert_into_database(db, j)
