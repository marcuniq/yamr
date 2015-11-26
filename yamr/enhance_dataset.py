import tmdbsimple
import graphlab as gl
from ipyparallel import Client
import time
import dateutil
from yamr.dataset import OriginalDataset
import tmdb_util
import util

"""
    before running this script, do

    activate dato-env
    ipcluster start -n 4
"""


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

tmdbsimple.API_KEY = tmdbsimple._get_env_key('TMDB_API_KEY')

original = OriginalDataset('datasets/ml-latest')

try:
    enhanced = gl.SFrame(data='datasets/ml-latest-enhanced/movies.csv')
except:
    import unicodedata
    init_tmdb_info = tmdb_util.get_tmdb_info(original.movies[0])
    sf_tmdb_info = gl.SFrame(init_tmdb_info)
    enhanced = original.movies.join(sf_tmdb_info, on='movieId')
    enhanced.export_csv('datasets\\ml-latest-enhanced\\movies.csv')

not_yet_enhanced_movies = original.movies.filter_by(enhanced['movieId'], 'movieId', exclude=True)
not_yet_enhanced_movies, dropped_movies = not_yet_enhanced_movies.dropna_split(columns='tmdbId')

# create client & view
rc = Client()
dv = rc[:]  # use all engines
v = rc.load_balanced_view()

with dv.sync_imports():
    import tmdbsimple
    tmdbsimple.API_KEY = tmdbsimple._get_env_key('TMDB_API_KEY')
    import unicodedata

for chunk in chunks(not_yet_enhanced_movies, 16):
    print "chunk starting with movieId %d" % chunk[0]['movieId']
    chunk = util.sframe_to_list(chunk)
    list_tmdb_info = dv.map_sync(tmdb_util.get_tmdb_info, chunk)
    mapped_tmdb_info = map(util.map_dict_list, list_tmdb_info)
    dict_tmdb_info = reduce(util.merge_two_dicts, mapped_tmdb_info)
    if len(dict_tmdb_info) == 0:
        break
    sf_tmdb_info = gl.SFrame(dict_tmdb_info)
    movie_enhanced = original.movies.join(sf_tmdb_info, on='movieId')
    enhanced = enhanced.append(movie_enhanced)
    enhanced.export_csv('datasets\\ml-latest-enhanced\\movies.csv')
    time.sleep(3)

movies_have_year, movies_no_year = enhanced.dropna_split(columns='year')
for movie in movies_no_year:
    info = tmdbsimple.Movies(movie['tmdbId']).info()
    year = dateutil.parser.parse(info['release_date']).year
    movie['year'] = long(year)
    movie = map(util.map_dict_list, [movie])[0]
    movies_have_year = movies_have_year.append(gl.SFrame(movie))

movies_have_year.export_csv('datasets\\ml-latest-enhanced\\movies.csv')
print "finished"
