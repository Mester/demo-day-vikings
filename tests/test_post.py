import unittest
from music_app.post import Post

class TestPost(unittest.TestCase):
    """Class to test the Post Class"""
    
    def test_object_creation(self):
        p = Post('Promises', 'Dreamers', 'rock', '2014', 8, 'http://example.com', 146666666.66, 'https://www.youtube.com')
        self.assertEqual(p.title, 'Promises')
        self.assertEqual(p.artist, 'Dreamers')
        self.assertEqual(p.genre, 'rock')
        self.assertEqual(p.year, '2014')
        self.assertEqual(p.score, 8)
        self.assertEqual(p.thumbnail, 'http://example.com')
        self.assertEqual(p.timestamp, 146666666.66)
        self.assertEqual(p.url, 'https://www.youtube.com')
