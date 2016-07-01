import sys
import time
import requests
import re
import random
from my_app import config
from my_app import utils
from pprint import pprint as pp


# static variables
RECENT = "new"
TOP = "top"
RANDOM = "random"
HOT = "hot"

GENRE = 0
YEAR = 1






# TO DO:
# Make the regex for artist/title handle long dash ('\xe2') as well as short dash (-)
# Change print statements to logging instead
# Add assertions/error checking for things like request failures
# Create function to scrub user input genre type to remove all bad characters (just alphanumeric and spaces allowed probably)
# Store stuff in database to reduce request time? The songs dont seem to change too much when we go back as far as we do
# Make sure no duplicates in database
# Clean up HTML
# Remove extra normal dash showing up in artist by updating regex
# Add functionality to search by year to HTML code
# Convert timestamp to a Date



class Post:
    # Post class to store/format the attributes for each song post
    def __init__(self):
        pass

    @classmethod
    def create_from_post_JSON(cls, post_json):
        """Create a Post object from the post's JSON
    
        Keyword arguments:
        post_title -- the post title
        """
        if not post_json:
            raise Exception() # TODO: better error handling
        post_object = cls()
        post_title = post_json['data']['title']
        p = re.compile(r"""
                (?P<artist>.+)  # The artist
                \s*-+\s*        # Skip some spaces and dashes
                (?P<title>.*)   # The title
                \s*\[           # Skip some spaces and opening bracket
                (?P<genre>.*)   # The genre
                \]\s*\(         # Skip closing bracket, spaces and opening parenthesis
                (?P<year>\d+)   # The year
                \)              # Skip closing parenthesis
                    """, re.VERBOSE | re.IGNORECASE)
        m = p.search(post_title)
        
        if m.group("artist"):
            post_object.artist = m.group("artist")
        else:
            raise Exception("Poor artist formatting") # TODO: better error handling
            
        if m.group("title"):
            post_object.title = m.group("title")
        else:
            raise Exception("Poor title formatting.") # TODO: better error handling
            
        if m.group("genre"):
            post_object.genre = m.group("genre")
        else:
            raise Exception("Poor genre formatting.") # TODO: better error handling
            
        if m.group("year"):
            post_object.year = m.group("year")
        else:
            raise Exception("Poor year formatting") # TODO: better error handling
        
        # Get the rest of the data from json info
        post_object.score = post_json['data']['score']
        post_object.url = post_json['data']['url']
        post_object.timestamp = post_json['data']['created_utc']
        post_object.thumbnail = post_json['data']['thumbnail']
        
        return post_object

def access_token():
    """
    Returns OAuth access token
    """
    data = {'grant_type': 'client_credentials'}
    headers = {'User-Agent': 'ChangeMeClient/0.1 by YourUsername'}
    for _ in range(5):
        try:
            r = requests.post("https://www.reddit.com/api/v1/access_token", auth=(config.CLIENT_ID,
                                                                                  config.CLIENT_SECRET), data=data,
                              headers=headers, timeout=(3.05, 20))
            r.raise_for_status()
            break
        except (requests.ConnectionError, requests.Timeout):
            continue
        except requests.HTTPError:
            if r.status_code == 401:
                print("INVALID CLIENT CREDENTIALS: Please verify that you are properly sending HTTP Basic "
                      "Authorization headers and that the client's credentials are correct")
                break
            else:
                r.raise_for_status()
        except requests.RequestException as e:
            print(e)
            sys.exit(1)
    token = r.json()['access_token']
    return token


def save_JSON_data(JSON_list): #TODO: More descriptive name
    """Creates post objects from JSON data and calculates statistics from processing 

    Keyword arguments:
    jsonData -- data from the API request
    """
    song_count = 0
    omit_count = 0
    other_count = 0
    all_song_posts = []
    for JSON_data in JSON_list:
        for post in JSON_data['data']['children']:
            if post['data']['media'] != None:
                try:            
                    all_song_posts.append(Post.create_from_post_JSON(post))
                except:
                    # print(post["data"]["title"])
                    # Count songs that have formatting errors
                    omit_count += 1
                # Count songs that are successfully received
                song_count += 1
            else: 
                # Count songs that don't have media data (no link to song)
                other_count += 1
    return all_song_posts, song_count, omit_count, other_count


def get_list_from_API(sort_type=HOT):
    """Get a list of song data from Reddit API , usually around 1000 posts are gotten

    Keyword arguments:
    sort_type -- determines type of API request - HOT, RECENT, TOP, or RANDOM valid
    """

    headers = {"Authorization": "bearer " + token, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    
    # For the initial request we don't have pagination information so have to do a different request
    r = requests.get("https://oauth.reddit.com/r/ListenToThis/" + sort_type + ".json?limit=100", headers=headers)
    if r.ok:
        JSON_list = []
        before = r.json()['data']['before']
        after = r.json()['data']['after']
        JSON_list.append(r.json())

        # Now we have "after" data to page through the reddit API data
        while after != None:
            r = requests.get("https://oauth.reddit.com/r/ListenToThis/" + sort_type + ".json?limit=100&after=" + after, headers=headers)
            if r.ok:
                before = r.json()['data']['before']
                after = r.json()['data']['after']
                JSON_list.append(r.json())
            else: 
                print("Request fail")
                break
        return JSON_list
    else:
        print("Request fail")
       

def print_song_info(song_list):
    """Debug function that outputs song information

    Keyword arguments:
    song_list -- list of songs to print out information for
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


def print_song_statistics(song_count, omit_count, other_count):
    """Debug function that outputs song statistics

    Keyword arguments:
    """
    print("#######################")
    print(str(song_count) + " songs posted successfully received from reddit API.")
    print(str(other_count) + " posts were omitted because they were not songs.")
    print(str(omit_count) + " songs were omitted due to poor formatting. See top of output for info.")
    total = song_count + other_count + omit_count
    print(str(total) + " posts processed.")


def search_genre(all_song_posts, genre):
    """Searches all song data for songs that match user inputted Genre

    Keyword arguments:
    genre -- The genre to be searched for
    """

    matching_songs = []

    genre_count = 0
    print("#######################")
    for song in all_song_posts:
        if genre.lower() in song.genre.lower():
            genre_count += 1
            matching_songs.append(song)
    print(str(genre_count) + " songs found for " + genre + " genre were stored in matching_songs list.")
    return matching_songs


def search_year(all_song_posts, year):
    """Searches all song data for songs that match user inputted Year

    Keyword arguments:
    year -- The year to be searched for
    """

    matching_songs = []

    year_count = 0
    print("#######################")
    for song in all_song_posts:
        if str(year) in str(song.year):
            year_count += 1
            matching_songs.append(song)
    print(str(year_count) + " songs found for the year " + str(year) + " were stored in matching_songs list.")
    return matching_songs


def get_10_songs(list_type, matching_songs): #TODO: more descriptive name
    """Pulls 10 songs from the list of songs user selected (genre or year)

    Keyword arguments:
    list_type -- user can select how songs are sorted: RECENT, TOP, RANDOM (HOT to be added)
    matching_songs -- songs that match user entered genre or year
    """

    sorted_song_list = []

    if list_type == RECENT or list_type.lower() == "recent":
        # Sort songs by RECENT first and print them out
        matching_songs.sort(key=lambda x: x.timestamp, reverse=True)
        for i in range(min(10, len(matching_songs))):
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
            # print(str(i + 1) + " " + matching_songs[i].artist + " - " + matching_songs[i].title + " " + str(matching_songs[i].timestamp))
    elif list_type == TOP or list_type.lower() == "top":
        # Sort songs by TOP first and print them out
        matching_songs.sort(key=lambda x: x.score, reverse=True)
        for i in range(min(10, len(matching_songs))):
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
            # print(str(i + 1) + " " + matching_songs[i].artist + " - " + matching_songs[i].title + " " + str(matching_songs[i].score))
    elif list_type == RANDOM or list_type.lower() == "random":
        # Sort songs randomly and print them out
        # Create a random list of 10 indexes (if possible) and print out songs from the list using them
        random_index_list = []
        while len(random_index_list) <= 10 and len(random_index_list) != len(matching_songs):
            temp_idx = random.randint(0,len(matching_songs) - 1)
            if temp_idx not in random_index_list:
                random_index_list.append(temp_idx)
        for i in random_index_list:
            sorted_song_list.append(matching_songs[i])
        return sorted_song_list
            # print(str(i + 1) + " " + matching_songs[i].artist + " - " + matching_songs[i].title)
    else:
        # add assertion here or something
        print("Error: invalid list type: ", list_type)


def get_songs(search_type, sort_type, search_term):
    """Temporary main function to run all code

    Keyword arguments:
    search_type -- lets user search for GENRE or YEAR
    sort_type --lets user sort list by RECENT, TOP, RANDOM (can add HOT to this)
    search_term -- user input search term for genre or year to search for
    """

    # Hardcoding it to have the reddit API search from HOT, TOP does not return 1000 results. RECENT would be okay too
    # Might want to search HOT normally, but use RECENT for our RECENT list


    # Need to empty the lists or we get duplicate results if they keep searching, probably a nicer way to do this...
    # all_song_posts = []
    # matching_songs = []
    # song_list = []

    JSON_list = get_list_from_API(HOT)
    all_song_posts, song_count, omit_count, other_count = save_JSON_data(JSON_list)
    # print_song_info(all_song_posts)
    print_song_statistics(song_count, omit_count, other_count)
    if search_type == GENRE:
        matching_songs = search_genre(all_song_posts, search_term)
    elif search_type == YEAR:
        matching_songs = search_year(all_song_posts, search_term)
    else:
        raise Exception("Invalid Search Type") # TODO: better error handling
    # print_song_info(matching_songs)
    song_list = get_10_songs(sort_type, matching_songs)
    return song_list

token = access_token()

# TRY IT OUT! 
# get_songs(GENRE, RANDOM, "Rock")
# get_songs(YEAR, TOP, 2015)
