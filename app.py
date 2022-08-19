
from flask import Flask, request, render_template, url_for, redirect, jsonify


app = Flask(__name__)

@app.route('/')

def index_page():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
