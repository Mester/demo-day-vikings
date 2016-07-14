import os
import re
import json
import unittest
import responses
from music_app.settings import BASE_DIR

class BaseMusicAppTestCase(unittest.TestCase):

    def setUp(self):
        url = r'https://www.reddit.com/r/ListenToThis/.*.json\?limit=1.*'
        fake_responses = [
                (responses.GET, url, 200, 'reddit.json'),
                ]
        for method, uri, status, fixture_file in fake_responses:
            fixture_path = os.path.join(BASE_DIR, 'tests', 'fixtures', fixture_file)
            with open(fixture_path) as f:
                json_fixture = json.load(f)
            responses.add(method, re.compile(url), json=json_fixture, status=status, content_type='application/json', match_querystring=True)
