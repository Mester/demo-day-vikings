import os
import markdown
from flask import Flask, render_template
from flask import Markup
from my_app import app


@app.route('/')
def index():
    #show search params: genre (maybe year), filter (hot, top, random, new)
    #redirect to results page
    return render_template('index.html')

#mock
@app.route('/list/<genre>/<filter>')
def show_results():
    #next_listing()
    #other data handling
    return render_template('results.html')

@app.route('/about')
def show_about():
    with open('README.md') as f:
        readme = Markup(markdown.markdown(f.read()))
        print readme
    return render_template('about.html', readme=readme)