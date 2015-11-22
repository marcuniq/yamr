import os
import re
import graphlab as gl

sf = gl.SFrame({'user_id': ["0", "0", "0", "1", "1", "2", "2", "2"],
                      'item_id': ["a", "b", "c", "a", "b", "b", "c", "d"],
                      'rating': [1, 3, 2, 5, 4, 1, 4, 3]})

model = gl.recommender.create(sf, target='rating')

recs = model.recommend()
print recs

model.save('model_file')


class RecommendationEngine(object):
    def __init__(self, dataset_path, train_model=False):
        self.dataset_path = dataset_path

        self.__set_movies()

        if train_model:
            self.__train_model()

    def __set_movies(self):
        movies_path = os.path.join(self.dataset_path, 'movies.csv')
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
        self.movies = movies


    def __train_model(self):
        ratings_path = os.path.join(self.dataset_path, 'ratings.csv')
        self.ratings = gl.SFrame(data=ratings_path)
        self.model = gl.recommender.create(self.ratings, user_id='userId', item_id='movieId', target='rating')

    def get_recommendations(self, movie_ratings):
