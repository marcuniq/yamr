import tmdbsimple
import unicodedata


def get_tmdb_info(movie):
    if movie['tmdb.id'] is not None:
        result = {}
        try:
            tmdb_info = tmdbsimple.Movies(movie['tmdb.id']).info()

            result['movieId'] = [movie['movieId']]
            result['tmdb.poster_path'] = [str(tmdb_info['poster_path']) if tmdb_info['poster_path'] else None]
            result['tmdb.title'] = [unicodedata.normalize('NFKD', tmdb_info['title']).encode('ascii', 'ignore') if tmdb_info['title'] else None]
            result['tmdb.overview'] = [unicodedata.normalize('NFKD', tmdb_info['overview']).encode('ascii', 'ignore') if tmdb_info['overview'] else None]
        except:
            print ""

        return result


def add_poster(movie, size='M'):
    if size is 'M':
        poster_url = 'http://image.tmdb.org/t/p/w185'
    elif size is 'L':
        poster_url = 'http://image.tmdb.org/t/p/w342'

    movie['poster'] = poster_url + movie['tmdb.poster_path']

    return movie


def add_trailer(movie):
    tmdb_movie = tmdbsimple.Movies(movie['tmdb.id'])
    youtube_videos = filter(lambda r: r['site'] == 'YouTube', tmdb_movie.videos()['results'])
    if len(youtube_videos) != 0:
        youtube_key = youtube_videos[0]['key']
        youtube_url = 'https://www.youtube.com/embed/' + str(youtube_key)
        movie['trailer'] = youtube_url

    return movie


def add_poster_and_trailer(movie):
    movie = add_poster(movie)
    movie = add_trailer(movie)
    return movie
