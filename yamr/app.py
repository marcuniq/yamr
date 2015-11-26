from flask import Flask, jsonify, render_template, request
import tmdbsimple as tmdb
from yamr.dataset import EnhancedDataset
from yamr.recommender import RecommendationEngine
import tmdb_util
import util

app = Flask(__name__)

tmdb.API_KEY = tmdb._get_env_key('TMDB_API_KEY')

dataset_path = 'datasets/ml-latest-enhanced'
ds = EnhancedDataset(dataset_path)

recommender = RecommendationEngine(ds)
recommender.load_model('item_sim_model')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/movies/<int:movieId>')
def movie_detail(movieId):
    movie = ds.find_movie_by_id(movieId)
    movie = tmdb_util.add_poster(movie, size='L')
    movie = tmdb_util.add_trailer(movie)
    return jsonify(movie)


@app.route('/api/movies/top_rated')
def top_rated():
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movies = ds.find_top_rated(top_k=top_k)
    movies = map(lambda m: tmdb_util.add_poster(m), movies)
    return jsonify(items=movies)


@app.route('/api/movies/random')
def random():
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movies = ds.get_random(top_k=top_k)
    movies = map(lambda m: tmdb_util.add_poster(m), movies)
    return jsonify(items=movies)


@app.route('/api/search')
def search():
    query = str(request.args.get('query'))
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movies = ds.search(query, top_k=top_k)
    movies = map(lambda m: tmdb_util.add_poster(m), movies)
    return jsonify(items=movies)


@app.route('/api/recommend', methods=['POST'])
def recommend():
    top_k = request.args.get('top_k')
    top_k = int(request.args.get('top_k')) if top_k else None
    movie_ratings = util.convert_unicode_to_str(request.json)
    movies = recommender.get_recommendations(movie_ratings, top_k)
    movies = map(lambda m: tmdb_util.add_poster(m), movies)
    return jsonify(items=movies)


if __name__ == '__main__':
    app.debug = True
    app.run()
