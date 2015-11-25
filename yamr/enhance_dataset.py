import tmdbsimple
from yamr.dataset import OriginalDataset, sframe_to_list
import graphlab as gl
from ipyparallel import Client
import time


def get_tmdb_info(movie):
    if movie['tmdb.id'] is not None:
        result = {}
        try:
            info = tmdbsimple.Movies(movie['tmdb.id']).info()

            result['movieId'] = [movie['movieId']]
            result['tmdb.poster_path'] = [str(info['poster_path']) if info['poster_path'] else None]
            result['tmdb.title'] = [unicodedata.normalize('NFKD', info['title']).encode('ascii', 'ignore') if info['title'] else None]
            result['tmdb.overview'] = [unicodedata.normalize('NFKD', info['overview']).encode('ascii', 'ignore') if info['overview'] else None]
        except:
            print ""

        return result


def merge_two_dicts(x, y):

    if x:
        for k, v in x.iteritems():
            if type(v) != list:
                x[k] = [v]
    else:
        x = {}

    if y:
        for k, v in y.iteritems():
            if k not in x:
                x[k] = []
            if type(v) != list:
                x[k] += [v]
            else:
                x[k] += v

    return x


def save_tmdb_info(dict_tmdb_info, original, enhanced):
    sf_tmdb_info = gl.SFrame(dict_tmdb_info)
    movie_enhanced = original.movies.join(sf_tmdb_info, on='movieId')

    enhanced = enhanced.append(movie_enhanced)
    enhanced.export_csv('datasets\\ml-latest-enhanced\\movies.csv')


def get_and_save_tmdb_info(movie):
    dict_tmdb_info = get_tmdb_info(movie)

    if dict_tmdb_info:
        save_tmdb_info(dict_tmdb_info, original, enhanced)


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
    init_tmdb_info = get_tmdb_info(original.movies[0])
    sf_tmdb_info = gl.SFrame(init_tmdb_info)
    enhanced = original.movies.join(sf_tmdb_info, on='movieId')
    enhanced.export_csv('datasets\\ml-latest-enhanced\\movies.csv')

not_yet_enhanced_movies = original.movies.filter_by(enhanced['movieId'], 'movieId', exclude=True)
not_yet_enhanced_movies, dropped_movies = not_yet_enhanced_movies.dropna_split(columns='tmdb.id')

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
    chunk = sframe_to_list(chunk)
    list_tmdb_info = dv.map_sync(get_tmdb_info, chunk)
    dict_tmdb_info = reduce(merge_two_dicts, list_tmdb_info)
    sf_tmdb_info = gl.SFrame(dict_tmdb_info)
    movie_enhanced = original.movies.join(sf_tmdb_info, on='movieId')
    enhanced = enhanced.append(movie_enhanced)
    enhanced.export_csv('datasets\\ml-latest-enhanced\\movies.csv')
    time.sleep(3)
