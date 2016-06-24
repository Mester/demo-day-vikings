import requests
import config
import re
from pprint import pprint as pp

# For this to work you need to make a new file called config.py in this folder and copy the key I posted to slack in it

song_posts = []
song_count = 0
omit_count = 0
other_count = 0


class Post:
    # Post class to store the attributes for each song post
    def __init__(self, artist, title, genre, year, score, url, timestamp, thumbnail):
        self.artist = artist
        self.title = title
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
    # print("### ACCESS TOKEN REQUEST ###")
    # print(r.status_code)
    if r.ok:
        token = r.json()['access_token']
        return token
    # need a while loop or something until we get the token, for now... this
    return "ERROR"


# We need to paginate through the API request 100 posts at a time using the before and after listings for the API
# https://www.reddit.com/r/redditdev/comments/2uymft/help_please_re_after_and_before_in_api/

def saveJSONdata(jsonData):
    global song_count
    global omit_count
    global other_count
    for post in jsonData['data']['children']:
        if post['data']['media'] != None:
            # print("##################################")
            # pp(post['data'])
            line = post['data']['title']
            # Get artist from post
            artist_regex = re.search('(.+) -', line)
            if artist_regex:
                artist = artist_regex.group(1)
            else:
                print("Poor artist formatting. Omitting the following post: ")
                print(line)
                omit_count += 1
                continue
            # Get title from post
            title_regex = re.search('- (.*) \[', line)
            if title_regex:
                title = title_regex.group(1)
            else:
                print("Poor title formatting. Omitting the following post: ")
                print(line)
                omit_count += 1
                continue
            # Get genre from post
            genre_regex = re.search('\[(.*)\]', line)
            if genre_regex:
                genre = genre_regex.group(1)
            else:
                print("Poor genre formatting. Omitting the following post: ")
                print(line)
                omit_count += 1
                continue
            # Get year from post
            year_regex = re.search('\((\d+)\)', line)
            if year_regex:
                year = year_regex.group(1)
            else:
                print("Poor year formatting. Omitting the following post: ")
                print(line)
                omit_count += 1
                continue
            # Get the rest of the data from json info
            score = post['data']['score']
            url = post['data']['url']
            timestamp = post['data']['created_utc']
            thumbnail = post['data']['thumbnail']
            song_posts.append(Post(artist, title, genre, year, score, url, timestamp, thumbnail))
            song_count += 1
        else: 
            other_count += 1


def getAPIdata(token):
    headers = {"Authorization": "bearer " + token, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    
    # For the initial request we don't have pagination information so have to do a different request
    r = requests.get("https://oauth.reddit.com/r/ListenToThis/hot.json?limit=100", headers=headers)
    if r.ok:
        before = r.json()['data']['before']
        after = r.json()['data']['after']
        saveJSONdata(r.json())

        # With pagination info, now we can do a while loop to exhaust the rest of the pages
        while after != None:
            r = requests.get("https://oauth.reddit.com/r/ListenToThis/hot.json?limit=100&after=" + after, headers=headers)
            if r.ok:
                before = r.json()['data']['before']
                after = r.json()['data']['after']
                saveJSONdata(r.json())
            else: 
                print("Request fail")
                break
    else:
        print("Request fail")
       

def printSongInfo():
    for i in range(len(song_posts)):
        print("#######################")
        print("ARTIST: " + song_posts[i].artist)
        print("TITLE: " + song_posts[i].title)
        print("GENRE: " + song_posts[i].genre)
        print("YEAR: " + song_posts[i].year)
        print("SCORE: " + str(song_posts[i].score))
        print("URL: " + song_posts[i].url)
        print("TIMESTAMP: " + str(song_posts[i].timestamp))
        print("THUMBNAIL: " + song_posts[i].thumbnail)
    print("#######################")
    print(str(song_count) + " songs posted successfully received from reddit API.")
    print(str(other_count) + " posts were omitted because they were not songs.")
    print(str(omit_count) + " songs were omitted due to poor formatting. See top of output for info.")
    total = song_count + other_count + omit_count
    print(str(total) + " posts processed.")

def temporaryMain():
    token = getAuthToken()
    getAPIdata(token)
    printSongInfo()

temporaryMain()