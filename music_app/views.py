import os
import markdown
from flask import Flask, render_template, request
from flask import Markup
from tinydb import TinyDB, Query
from music_app import app
from music_app.post import Post
from music_app.settings import DATABASE_NAME
from music_app.get_json import get_songs

GENRE = 0
YEAR = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(GENRE, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    return render_template('search.html')

@app.route('/list/<search_term>/<sort_type>', methods=['POST', 'GET'])
def show_results(search_term, sort_type):
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(GENRE, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    song_list = get_songs(GENRE, sort_type, search_term)
    return render_template('results.html', song_list=song_list)

@app.route('/about')
def show_about():
    with open('README.md') as f:
        readme = Markup(markdown.markdown(f.read()))
    return render_template('about.html', readme=readme)
