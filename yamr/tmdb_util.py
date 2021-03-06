import tmdbsimple
import unicodedata


def get_tmdb_info(movie):
    if movie['tmdbId'] is not None:
        result = {}
        try:
            tmdb_info = tmdbsimple.Movies(movie['tmdbId']).info()

            result['movieId'] = [movie['movieId']]
            result['tmdbPosterPath'] = [str(tmdb_info['poster_path']) if tmdb_info['poster_path'] else None]
            result['tmdbTitle'] = [unicodedata.normalize('NFKD', tmdb_info['title']).encode('ascii', 'ignore') if tmdb_info['title'] else None]
            result['tmdbOverview'] = [unicodedata.normalize('NFKD', tmdb_info['overview']).encode('ascii', 'ignore') if tmdb_info['overview'] else None]
        except:
            print ""

        return result


def add_trailer(movie):
    tmdb_movie = tmdbsimple.Movies(movie['tmdbId'])
    youtube_videos = filter(lambda r: r['site'] == 'YouTube', tmdb_movie.videos()['results'])
    if len(youtube_videos) != 0:
        youtube_key = youtube_videos[0]['key']
        youtube_url = 'https://www.youtube.com/embed/' + str(youtube_key)
        movie['trailer'] = youtube_url

    return movie
