import requests
import config
import re
from pprint import pprint as pp

# For this to work you need to make a new file called config.py in this folder and copy the key I posted to slack in it

song_posts = []

class Post:
    # Post class to store the attributes for each song post
    def __init__(self, title, artist, genre, year, score, url, timestamp, thumbnail):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year
        self.score = score
        self.url = url
        self.timestamp = timestamp
        self.thumbnail = thumbnail

def getAuthToken():
    client_auth = requests.auth.HTTPBasicAuth(config.client_id, config.client_secret)
    post_data = {"grant_type": "client_credentials"}
    reddit_headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    r = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=reddit_headers)
    print("### ACCESS TOKEN REQUEST ###")
    print(r.status_code)
    if r.ok:
        pp(r.json())
        token = r.json()['access_token']
        return token
    # need a while loop or something until we get the token, for now... this
    return "ERROR"


def getAPIdata(token):
    headers = {"Authorization": "bearer " + token, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    r = requests.get("https://oauth.reddit.com/r/ListenToThis/hot", headers=headers)
    print(r.status_code)
    print("### REDDIT API DATA REQUEST ###")
    if r.ok:
        for post in r.json()['data']['children']:
            if post['data']['media'] != None:
                print("##################################")
                pp(post['data'])
                # title = 
                # artist = 
                # genre = 
                # year = 
                # score = post['data']['score']
                # url = post['data']['url']
                # timestamp = post['data']['created_utc']
                # thumbnail = post['data']['thumbnail']
                # song_posts.append(Post(title, artist, genre, year, score, url, timestamp, thumbnail))


token = getAuthToken()
getAPIdata(token)
pp(song_posts)