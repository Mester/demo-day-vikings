import requests
import config
import re
from pprint import pprint as pp

# For this to work you need to make a new file called config.py in this folder and copy the key I posted to slack in it

all_song_posts = []
genre_songs = []
song_count = 0
omit_count = 0
other_count = 0


# TO DO:
# Make the regex for artist/title handle long dash ('\xe2') as well as short dash (-)
# Change print statements to logging instead
# Add assertions/error checking for things like request failures
# Create function to scrub user input genre type to remove all bad characters (just alphanumeric and spaces allowed probably)
# Create a random function to randomize 10 songs from genre
# Create a top 10 function to get the songs from a genre with most likes
# Create a recent 10 function that pulls 10 most recent based on timestamp
# Store stuff in database to reduce request time? The songs dont seem to change too much when we go back as far as we do
# Make sure no duplicates in database



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
                # print("Poor artist formatting. Omitting the following post: ")
                # print(line)
                omit_count += 1
                continue
            # Get title from post
            title_regex = re.search('- (.*) \[', line)
            if title_regex:
                title = title_regex.group(1)
            else:
                # print("Poor title formatting. Omitting the following post: ")
                # print(line)
                omit_count += 1
                continue
            # Get genre from post
            genre_regex = re.search('\[(.*)\]', line)
            if genre_regex:
                genre = genre_regex.group(1)
            else:
                # print("Poor genre formatting. Omitting the following post: ")
                # print(line)
                omit_count += 1
                continue
            # Get year from post
            year_regex = re.search('\((\d+)\)', line)
            if year_regex:
                year = year_regex.group(1)
            else:
                # print("Poor year formatting. Omitting the following post: ")
                # print(line)
                omit_count += 1
                continue
            # Get the rest of the data from json info
            score = post['data']['score']
            url = post['data']['url']
            timestamp = post['data']['created_utc']
            thumbnail = post['data']['thumbnail']
            all_song_posts.append(Post(artist, title, genre, year, score, url, timestamp, thumbnail))
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
        # might want to change the while loop to a for loop or have a counter to prevent never ending loop
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
       

def printSongInfo(song_list):
    for song in song_list:
        print("#######################")
        print("ARTIST: " + song.artist)
        print("TITLE: " + song.title)
        print("GENRE: " + song.genre)
        print("YEAR: " + song.year)
        print("SCORE: " + str(song.score))
        print("URL: " + song.url)
        print("TIMESTAMP: " + str(song.timestamp))
        print("THUMBNAIL: " + song.thumbnail)


def printSongStatistics():
    print("#######################")
    print(str(song_count) + " songs posted successfully received from reddit API.")
    print(str(other_count) + " posts were omitted because they were not songs.")
    print(str(omit_count) + " songs were omitted due to poor formatting. See top of output for info.")
    total = song_count + other_count + omit_count
    print(str(total) + " posts processed.")


def searchGenre(genre):
    genre_count = 0
    print("#######################")
    for song in all_song_posts:
        if genre.lower() in song.genre.lower():
            genre_count += 1
            # print(song.genre + ": " + song.artist + " - " + song.title)
            genre_songs.append(song)
    print(str(genre_count) + " songs found for " + genre + " genre were stored in genre_songs list.")


# Need to make sure this function handles situations where less than 10 songs exist for a genre

def get10Songs(list_type):
    # Going to give the user the option to select 10 most recent, 10 most upvotes, or 10 random songs
    if list_type == "recent":
        # List comprehension to sort genre_songs by timestamp
        pass
    elif list_type == "top":
        # List comprehension to sort genre_songs by score
        pass
    elif list_type == "random":
        # get out that old math.random nonsense and spit out 10 numbers and use the index to get songs from genre_songs list (use set on the number list to guarantee no duplicates)
        pass
    else:
        # add assertion here or something
        print("Error: invalid list type")


def temporaryMain():
    token = getAuthToken()
    getAPIdata(token)
    # printSongInfo(all_song_posts)
    printSongStatistics()
    searchGenre("Rock")
    # printSongInfo(genre_songs)

temporaryMain()