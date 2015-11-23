from flask import Flask, jsonify, render_template, request
from json import dumps

app = Flask(__name__)

from yamr.database import Database

dataset_path = 'datasets/ml-latest'
db = Database(dataset_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/movies/<int:movieId>')
def movie_detail(movieId):
    movie = db.find_movie_by_id(movieId)
    return jsonify(movie)


@app.route('/api/search')
def search():
    query = str(request.args.get('query'))
    movies = db.search(query)
    return jsonify(items=movies)

if __name__ == '__main__':
    app.debug = True
    app.run()
