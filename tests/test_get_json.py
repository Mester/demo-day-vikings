import unittest
import responses
import requests
from music_app.get_json import get_json_from_subreddit
from tests import BaseMusicAppTestCase

class TestGetJson(BaseMusicAppTestCase):
    """Class to test get_json"""
    
    @responses.activate
    def test_return_value_list(self):
        expected = get_json_from_subreddit("hot", 1)
        self.assertTrue(isinstance(expected, list))
