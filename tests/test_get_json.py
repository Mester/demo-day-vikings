import unittest
import responses
import requests
from music_app.get_json import get_json_from_subreddit
from music_app.get_json import convert_post_to_json, is_post_valid
from tests import BaseMusicAppTestCase

class TestGetJson(BaseMusicAppTestCase):
    """Class to test get_json"""
    
    @responses.activate
    def test_return_value_list(self):
        expected = get_json_from_subreddit("hot", 1)
        self.assertTrue(isinstance(expected, list))

    @responses.activate
    def test_return_value_length(self):
        expected = get_json_from_subreddit("hot", 1)
        self.assertEqual(len(expected), 1)

    @responses.activate
    def test_json_to_posts(self):
        expected = get_json_from_subreddit("hot", 1)
        j = []
        for data in expected:
            for post in data['data']['children']:
                if is_post_valid(post):
                    j.append(convert_post_to_json(post))
        self.assertEqual(len(j), 1)

    @responses.activate
    def test_all_keys(self):
        expected = get_json_from_subreddit("hot", 1)
        j = []
        for data in expected:
            for post in data['data']['children']:
                if is_post_valid(post):
                    j.append(convert_post_to_json(post))
        self.assertEqual(j[0].keys(), ['title', 'url', 'timestamp', 'artist', 'score', 'year', 'genre', 'thumbnail'])

    def test_is_post_valid_false_key(self):
        test_json = {
                'data': {
                    'media' : None
                    } 
                }
        self.assertFalse(is_post_valid(test_json))

    def test_is_post_valid_true_key(self):
        test_json = {
                'data': {
                    'media' : True
                    } 
                }
        self.assertTrue(is_post_valid(test_json))
