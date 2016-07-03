class Post:
    """
    A Class to represent a Post on r/ListenToThis
    Instances of this class will be used to render 
    information on the UI
    """
    def __init__(self, title, artist, genre, year, score, thumbnail, timestamp, url):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year
        self.score = score
        self.thumbnail = thumbnail
        self.timestamp = timestamp
        self.url = url
    #TODO: Add more getter and setters if required in future
