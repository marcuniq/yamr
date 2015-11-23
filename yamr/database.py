import os
import re
import graphlab as gl
import graphlab.aggregate as agg


class Database(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.movies = self.__parse_movies(dataset_path)
        self.ratings = self.__parse_ratings(dataset_path)

    def __parse_movies(self, dataset_path):
        movies_path = os.path.join(dataset_path, 'movies.csv')
        movies = gl.SFrame(data=movies_path)

        def get_year(title):
            m = re.search(r'\d\d\d\d', title)
            if m:
                return int(m.group())
            else:
                print title

        movies['year'] = movies['title'].apply(get_year)
        movies['title'] = movies['title'].apply(lambda t: t.split('(')[0])
        movies['genres'] = movies['genres'].apply(lambda s: s.split('|'))

        # join links
        links_path = os.path.join(dataset_path, 'links.csv')
        links = gl.SFrame(data=links_path)
        movies = movies.join(links, on='movieId', how='inner')

        movies['imdb'] = movies['imdbId'].apply(lambda imdb_id: 'http://www.imdb.com/title/tt{}/'.format(imdb_id))
        movies.remove_column('imdbId')

        movies['tmdbId']
        return movies

    def __parse_ratings(self, dataset_path):
        ratings_path = os.path.join(dataset_path, 'ratings.csv')
        ratings = gl.SFrame(data=ratings_path)

        return ratings

    def find_movie_by_id(self, movieId):
        movie = self.movies.filter_by(movieId, 'movieId')
        return movie[0]

    def find_top_rated(self, min_count=50, top_k=20):
        grouped = self.ratings.groupby(key_columns='movieId', operations={'count': agg.COUNT(),
                                                                          'mean_rating': agg.MEAN('rating')})
        top_rated = grouped[grouped['count'] > min_count].sort('mean_rating', False)[:top_k]

        return top_rated.join(self.movies, on='movieId', how='inner').sort('mean_rating', False)

    def search(self, query, top_k=20):
        query_re = '.*{}.*'.format(query)
        p = re.compile(query_re, re.IGNORECASE)
        found_movies = self.movies[self.movies['title'].apply(lambda t: 1 if p.match(t) else 0)]
        top_k = min(top_k, found_movies.shape[0])

        # hack to convert SFrame to list of dict
        movies = []
        for i in xrange(top_k):
            movies += [found_movies[i]]

        return movies
