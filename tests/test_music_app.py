import os
import tempfile
import unittest

from tinydb import TinyDB
import flask

from music_app import app, settings, get_json


class TestMusicApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testing secret key'
        app.config['DATABASE'] = tempfile.mkstemp()
        self.db = TinyDB(app.config['DATABASE'][1])
        self.client = app.test_client()

    def load_fixtures(self):
        db = self.db
        json_data = get_json.get_json_from_subreddit("hot")
        json_list = []
        for data in json_data:
            for post in data['data']['children']:
                if get_json.is_post_valid(post):
                    j = get_json.convert_post_to_json(post)
                    if j is not None:
                        get_json.insert_into_database(db, j)


class TestSearch(TestMusicApp):

    def test_search_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form', response.data)

    def test_search_post(self):
        with app.test_request_context(path='/', method='POST', data={'search_term': 'indie', 'sort_type': 'top'}):
            self.assertEqual(flask.request.form['search_term'], 'indie')
            self.assertEqual(flask.request.form['sort_type'], 'top')




