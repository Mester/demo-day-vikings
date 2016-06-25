import requests
import config
import re
from pprint import pprint as pp

# static variables
RECENT = 0
TOP = 1
RANDOM = 2

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
    def __init__(self):
        pass

    @classmethod
    def create_from_post_JSON(cls, post_json):
        """Create a Post object from the post JSON
    
        Keyword arguments:
        post_title -- the post title
        """
        if not post_json:
            raise Exception() # TODO: better error handling
        post_object = cls()
        post_title = post_json['data']['title'].lower()
        
        # Get artist from post
        artist_regex = re.search(r'(.+) -', post_title)
        if artist_regex:
            post_object.artist = artist_regex.group(1)
        else:
            raise Exception("Poor artist formatting") # TODO: better error handling
        
        # Get title from post
        title_regex = re.search(r'- (.*) \[', post_title)
        if title_regex:
            post_object.title = title_regex.group(1)
        else:
            raise Exception("Poor title formatting.") # TODO: better error handling
        
         # Get genre from post
        genre_regex = re.search(r'\[(.*)\]', post_title)
        if genre_regex:
            post_object.genre = genre_regex.group(1)
        else:
            raise Exception("Poor genre formatting.") # TODO: better error handling
        
        # Get year from post
        year_regex = re.search(r'\((\d+)\)', post_title)
        if year_regex:
            post_object.year = year_regex.group(1)
        else:
            raise Exception("Poor year formatting") # TODO: better error handling

        # Get the rest of the data from json info
        post_object.score = post_json['data']['score']
        post_object.url = post_json['data']['url']
        post_object.timestamp = post_json['data']['created_utc']
        post_object.thumbnail = post_json['data']['thumbnail']
        
        return post_object

def getAuthToken():
    """Description here
    """
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
    """Description here

    Keyword arguments:
    """
    global song_count
    global omit_count
    global other_count
    for post in jsonData['data']['children']:
        if post['data']['media'] != None:
            # print("##################################")
            # pp(post['data'])
            try:            
                all_song_posts.append(Post.create_from_post_JSON(post))
            except:
                omit_count += 1
            song_count += 1
        else: 
            other_count += 1


def get_list_from_hot():
    """Description here

    Keyword arguments:
    """
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
    """Description here

    Keyword arguments:
    """
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
    """Description here

    Keyword arguments:
    """
    print("#######################")
    print(str(song_count) + " songs posted successfully received from reddit API.")
    print(str(other_count) + " posts were omitted because they were not songs.")
    print(str(omit_count) + " songs were omitted due to poor formatting. See top of output for info.")
    total = song_count + other_count + omit_count
    print(str(total) + " posts processed.")


def searchGenre(genre):
    """Description here

    Keyword arguments:
    """
    genre_count = 0
    print("#######################")
    for song in all_song_posts:
        if genre.lower() in song.genre.lower():
            genre_count += 1
            # print(song.genre + ": " + song.artist + " - " + song.title)
            genre_songs.append(song)
    print(str(genre_count) + " songs found for " + genre + " genre were stored in genre_songs list.")


# Need to make sure this function handles situations where less than 10 songs exist for a genre
def get10Songs(list_type): #TODO: more descriptive name
    """Description here

    Keyword arguments:
    list_type -- one of the types RECENT, TOP, RANDOM
    """
    # Going to give the user the option to select 10 most recent, 10 most upvotes, or 10 random songs
    if list_type == RECENT:
        # List comprehension to sort genre_songs by timestamp
        pass
    elif list_type == TOP:
        # List comprehension to sort genre_songs by score
        pass
    elif list_type == RANDOM:
        # get out that old math.random nonsense and spit out 10 numbers and use the index to get songs from genre_songs list (use set on the number list to guarantee no duplicates)
        pass
    else:
        # add assertion here or something
        print("Error: invalid list type")


def temporaryMain():

    get_list_from_hot()
    # printSongInfo(all_song_posts)
    printSongStatistics()
    searchGenre("Rock")
    # printSongInfo(genre_songs)

token = getAuthToken()
temporaryMain()