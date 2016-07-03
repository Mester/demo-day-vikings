import os
import markdown
from flask import Flask, render_template, request
from flask import Markup
from tinydb import TinyDB, Query
from music_app import app
from music_app.post import Post
from music_app.settings import DATABASE_NAME

db = TinyDB(os.path.join(os.getcwd(), DATABASE_NAME))
q = Query()

def get_songs(search_type, sort_type, search_term):
    """
    Method to get the songs from the database
    TODO: Implement search_type and sort_type:
    Right now we just use the search term
    """
    results = db.search(q.genre == search_term.lower())
    return [ create_post_object(r) for r in results ]

def create_post_object(j):
    """
    Takes a json from the database and returns
    an instance of type Post
    """
    return Post(j['title'], j['artist'], j['genre'].title(), j['year'], j['score'], j['thumbnail'], j['timestamp'], j['url'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(0, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    return render_template('search.html')

@app.route('/list/<search_term>/<sort_type>', methods=['POST', 'GET'])
def show_results(search_term, sort_type):
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(0, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    song_list = get_songs(api_access.GENRE, sort_type, search_term)
    return render_template('results.html', song_list=song_list)

@app.route('/about')
def show_about():
    with open('README.md') as f:
        readme = Markup(markdown.markdown(f.read()))
    return render_template('about.html', readme=readme)
