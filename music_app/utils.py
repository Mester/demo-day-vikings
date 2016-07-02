import sys
import requests
import re
import collections
from collections import namedtuple
from flask import session, json

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
        (?P<artist>.+)  # The artist
        \s*-+\s*        # Skip some spaces and dashes
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
