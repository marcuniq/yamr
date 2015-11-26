from flask import Flask, jsonify, render_template, request
import tmdbsimple as tmdb
app = Flask(__name__)

from yamr.dataset import EnhancedDataset
dataset_path = 'datasets/ml-latest-enhanced'
ds = EnhancedDataset(dataset_path)

tmdb.API_KEY = tmdb._get_env_key('TMDB_API_KEY')


def extend_movie_info(movie, poster=True, trailer=False):
    if poster:
        poster_url = 'http://image.tmdb.org/t/p/w185' + movie['tmdb.poster_path']
        movie['poster'] = poster_url

    if trailer:
        tmdb_m = tmdb.Movies(movie['tmdb.id'])
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
    movie = ds.find_movie_by_id(movieId)
    movie = extend_movie_info(movie, poster=True, trailer=True)
    return jsonify(movie)


@app.route('/api/movies/top_rated')
def top_rated():
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movies = ds.find_top_rated(top_k=top_k)
    movies = map(lambda m: extend_movie_info(m), movies)
    return jsonify(items=movies)


@app.route('/api/search')
def search():
    query = str(request.args.get('query'))
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movies = ds.search(query, top_k=top_k)
    movies = map(lambda m: extend_movie_info(m), movies)
    return jsonify(items=movies)

if __name__ == '__main__':
    app.debug = True
    app.run()
