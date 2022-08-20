
from flask import Flask, request, render_template, url_for, redirect, jsonify
import time
from utils import get_db

def check_login(email_, password_):

    if email_ != '' or password_ != '':

        data = enter_email().check_loginfo(email, password)

        if data is not None: return data

        else: return False


app = Flask(__name__)

@app.route('/')

def index():
    return redirect(url_for('login'))

@app.route('/bookmarks/username=<username>')

def index_page(username):
    links = get_db().out_db(username)

    return render_template('index.html', username=username, links=links)

@app.route('/bookmark/add/bookmark=<bookmark>,username=<username>')

def add_bookmark():
    link = bookmark
    username = username

    get_db().add_link(username, link)


@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == "POST":
        username, password = request.form['email'], request.form['password']
        
        # adding database
        get_db().in_db(username, password)
        get_db().add_bookmark_db(username)
 
        return redirect(url_for('index_page', username=username))

    else: return render_template("login.html")


if __name__=='__main__':
    app.run(debug=True)
