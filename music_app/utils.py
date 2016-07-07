import re
import os
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
try:
    import collections.abc as collections
except ImportError:
    import collections
from music_app.settings import DATABASE_NAME, DOMAIN
from tinydb import TinyDB, Query

def parse_listing(data):
    songs = [{key:song[key] for key in song.keys() if key in ['url', 'score', 'created_utc', 'thumbnail',
                                                              'title']} for song in [flatten(thing['data']) for thing
                                                                                     in data['data']['children']
                                                                                     if thing['kind'] == 't3']]
    for song in songs:
        parsed = parse_title(song['title'])
        if parsed is None:
            continue
        song.update(parsed)
    return songs

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_title(title):
    """
    Returns parsed contents of a post's title
    """
    ro = re.compile(r"""
        (?P<artist>.+[^- ]+)  # The artist
        \s*-+\s*       # Skip some spaces and dashes
        (?P<title>.*)   # The title
        \s*\[           # Skip some spaces and opening bracket
        (?P<genre>.*)   # The genre
        \]\s*\(         # Skip closing bracket, spaces and opening parenthesis
        (?P<year>\d+)   # The year
        \)              # Skip closing parenthesis
        """, re.VERBOSE | re.IGNORECASE)
    mo = ro.search(title)
    if mo is None:
        return
    return {'artist': mo.group('artist'), 'title': mo.group('title'), 'genre': mo.group('genre'), 'year': mo.group(
        'year')}

def get_genres():
    db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
    all_genres = { song['genre'] for song in db.all() }
    specific_genres = set()
    for genre in all_genres:
        specific_genres = specific_genres.union(set(genre.strip().split('/')))
    return specific_genres

def get_total_songs():
    db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
    return len(db.all())

def convert_url_to_embed_url(url):
    """
    Method to convert the url to a video embed url
    """
    if 'you' in url:
        id = url.split('=')[-1]
        return "https://www.youtube.com/embed/" + id + "?autoplay=1&origin=" + DOMAIN
    return url
