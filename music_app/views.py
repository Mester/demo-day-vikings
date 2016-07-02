import os
import markdown
from music_app.api_access import get_songs
from flask import Flask, render_template, request
from flask import Markup
from music_app import app, api_access, database

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(api_access.GENRE, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    return render_template('search.html')


@app.route('/list/<search_term>/<sort_type>', methods=['POST', 'GET'])
def show_results(search_term, sort_type):
    if request.method == 'POST':
        search_term = request.form['search_term']
        sort_type = request.form['sort_type']
        song_list = get_songs(api_access.GENRE, sort_type, search_term)
        return render_template('results.html', song_list=song_list)
    song_list = get_songs(api_access.GENRE, sort_type, search_term)
    return render_template('results.html', song_list=song_list)


@app.route('/about')
def show_about():
    with open('README.md') as f:
        readme = Markup(markdown.markdown(f.read()))
    return render_template('about.html', readme=readme)
