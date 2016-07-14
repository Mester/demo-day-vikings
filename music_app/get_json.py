import requests
import os
import logging
import re
import random
import datetime
from tinydb import TinyDB, Query
from music_app.utils import parse_title
from music_app.settings import DATABASE_NAME
from music_app.post import Post


# static variables
GENRE = 0
YEAR = 1

logger = logging.getLogger('music_app.get_json')
db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
q = Query()


def get_songs_from_db():
    """
    Method to get the songs from the database
    TODO: Implement search_type and sort_type:
    Right now we just use the search term
    """
    results = db.all()
    return [ create_post_object(r) for r in results]


def create_post_object(j):
    """
    Takes a json from the database and returns
    an instance of type Post
    """
    return Post(j['title'], j['artist'], j['genre'].title(), j['year'], j['score'], j['thumbnail'], datetime.datetime.fromtimestamp(int(j['timestamp'])), j['url'])


def get_json_from_subreddit(sort_type, limit):
    """
    Method to get the json from listentothis subreddit
    """
    json_list = []
    url = "https://www.reddit.com/r/ListenToThis/{}.json?limit={}".format(sort_type, limit)
    headers = {"User-Agent":"ChangeMeClient/0.1 by username"}
    logger.debug("Fetching: {}".format(url))
    r = requests.get(url.format(sort_type), headers=headers)
    if r.ok:
        before = r.json()['data']['before']
        after = r.json()['data']['after']
        json_list.append(r.json())
        while after != None:
            new_url = url + "&after={}".format(after)
            logger.debug("Fetching: {}".format(new_url))
            r = requests.get(new_url, headers=headers)
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
    post_json = parse_title(post['data']['title'])
    if post_json is None:
        return None
    post_json['score'] = post['data']['score']
    post_json['url'] = post['data']['url']
    post_json['timestamp'] = post['data']['created_utc']
    post_json['thumbnail'] = post['data']['thumbnail']

    return post_json

def update_score(db, json_object):
    """
    Method to update the score of the song
    """
    q = Query()
    j = db.search(q.url == json_object['url'])[0]
    logger.debug("Duplicate post found: {}".format(j['title'].encode('ascii', 'ignore')))
    logger.debug("Old Score: {}".format(j['score']))
    logger.debug("Now Score: {}".format(json_object['score']))
    if int(j['score']) != int(json_object['score']):
        logger.debug("Updating Score for {}".format(j['title'].encode('ascii', 'ignore')))
        db.update({'score':json_object['score']}, q.url == json_object['url'])
    else:
        logger.debug("The scores are still the same, not updating")

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
        json_object['genre'] = json_object['genre'].lower()
        db.insert(json_object)
    else:
        update_score(db, json_object)


def search_genre(all_song_posts, genre):
    """Searches all song data for songs that match user inputted Genre

    Keyword arguments:
    genre -- The genre to be searched for
    """

    matching_songs = []

    genre_count = 0
    logger.info("#######################")
    for song in all_song_posts:
        if genre.lower() in song.genre.lower():
            genre_count += 1
            matching_songs.append(song)
    logger.info(str(genre_count) + " songs found for " + genre + " genre were stored in matching_songs list.")
    return matching_songs


def search_year(all_song_posts, year):
    """Searches all song data for songs that match user inputted Year

    Keyword arguments:
    year -- The year to be searched for
    """

    matching_songs = []

    year_count = 0
    logger.info("#######################")
    for song in all_song_posts:
        if str(year) in str(song.year):
            year_count += 1
            matching_songs.append(song)
    logger.info(str(year_count) + " songs found for the year " + str(year) + " were stored in matching_songs list.")
    return matching_songs


def get_10_songs(list_type, matching_songs): #TODO: more descriptive name
    """Pulls 10 songs from the list of songs user selected (genre or year)

    Keyword arguments:
    list_type -- user can select how songs are sorted: RECENT, TOP, RANDOM (HOT to be added)
    matching_songs -- songs that match user entered genre or year
    """

    sorted_song_list = []
    if list_type.lower() == "recent":
        # Sort songs by RECENT first and log them out
        matching_songs.sort(key=lambda x: x.timestamp, reverse=True)
        for i in range(min(10, len(matching_songs))):
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
    elif list_type.lower() == "top":
        # Sort songs by TOP first and log them out
        matching_songs.sort(key=lambda x: x.score, reverse=True)
        for i in range(min(10, len(matching_songs))):
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
    elif list_type.lower() == "random":
        # Sort songs randomly and log them out
        # Create a random list of 10 indexes (if possible) and print out songs from the list using them
        random_index_list = []
        while len(random_index_list) <= 10 and len(random_index_list) != len(matching_songs):
            temp_idx = random.randint(0,len(matching_songs) - 1)
            if temp_idx not in random_index_list:
                random_index_list.append(temp_idx)
        for i in random_index_list:
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
    else:
        # add assertion here or something
        logger.info("Error: invalid list type: ", list_type)


def get_songs(search_type, sort_type, search_term):
    """Temporary main function to run all code

    Keyword arguments:
    search_type -- lets user search for GENRE or YEAR
    sort_type --lets user sort list by RECENT, TOP, RANDOM (can add HOT to this)
    search_term -- user input search term for genre or year to search for
    """

    all_song_posts = get_songs_from_db()
    if search_type == GENRE:
        matching_songs = search_genre(all_song_posts, search_term)
    elif search_type == YEAR:
        matching_songs = search_year(all_song_posts, search_term)
    else:
        raise Exception("Invalid Search Type") # TODO: better error handling
    song_list = get_10_songs(sort_type, matching_songs)
    return song_list

if __name__ == '__main__':
    db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
    json_data = get_json_from_subreddit("hot", 100)
    json_list = []
    for data in json_data:
        for post in data['data']['children']:
            if is_post_valid(post):
                j = convert_post_to_json(post)
                if j is not None:
                    insert_into_database(db, j)
