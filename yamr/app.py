from flask import Flask, jsonify, render_template, request
import tmdbsimple as tmdb
app = Flask(__name__)

from yamr.database import Database
dataset_path = 'datasets/ml-latest'
db = Database(dataset_path)

tmdb.API_KEY = tmdb._get_env_key('TMDB_API_KEY')


def extend_movie_info(movie):
    tmdb_m = tmdb.Movies(movie['tmdbId'])

    poster_url = 'http://image.tmdb.org/t/p/w185' + str(tmdb_m.images()['posters'][0]['file_path'])
    movie['poster'] = poster_url

    youtube_videos = filter(lambda r: r['site'] == 'YouTube', tmdb_m.videos()['results'])
    if len(youtube_videos) != 0:
        youtube_key = youtube_videos[0]['key']
        youtube_url = 'https://www.youtube.com/embed/' + str(youtube_key)
        movie['trailer'] = youtube_url

    return movie


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/movies/<int:movieId>')
def movie_detail(movieId):
    movie = db.find_movie_by_id(movieId)
    movie = extend_movie_info(movie)
    return jsonify(movie)


@app.route('/api/movies/top_rated')
def top_rated():
    movies = db.find_top_rated()
    return jsonify(items=movies)


@app.route('/api/search')
def search():
    query = str(request.args.get('query'))
    movies = db.search(query)
    return jsonify(items=movies)

if __name__ == '__main__':
    app.debug = True
    app.run()
