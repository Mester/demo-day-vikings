import os
import unittest
import json
from tinydb import TinyDB
from music_app.utils import *
from music_app.settings import BASE_DIR

class TestUtils(unittest.TestCase):
    """Class to test the utils module"""
    
    def setUp(self):
        with open(os.path.join(BASE_DIR, 'tests', 'fixtures', 'test.json')) as f:
            j = json.load(f)
        self.database_name = os.path.join(os.getcwd(), 'test.db')
        db = TinyDB(self.database_name)
        db.insert_multiple(j)
        db.close

    def tearDown(self):
        os.remove(self.database_name)

    def test_get_total_songs(self):
        self.assertEqual(get_total_songs(self.database_name), 10)

    def test_get_genres(self):
        genres = set(['epic melodic death metal', 'trap', 'bass', 'rock',
            'classical', 'noise rock', 'hardcore', 'atmospheric black metal', 'canadian folk metal', 'indie pop', 'post rock', 'experimental',
            'indie', 'piano', 'psychedelic'])
        self.assertEqual(get_genres(self.database_name), genres)
