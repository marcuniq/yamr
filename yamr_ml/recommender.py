import os
import graphlab as gl
from graphlab import SFrame

sf = gl.SFrame({'user_id': ["0", "0", "0", "1", "1", "2", "2", "2"],
                      'item_id': ["a", "b", "c", "a", "b", "b", "c", "d"],
                      'rating': [1, 3, 2, 5, 4, 1, 4, 3]})

model = gl.recommender.create(sf, target='rating')

recs = model.recommend()
print recs

model.save('model_file')


class RecommendationEngine(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def __train_model(self):
        ratings_path = os.path.join(self.dataset_path, 'ratings.csv')
        ratings = SFrame(data=ratings_path)
        self.model = gl.recommender.create(ratings, user_id='userId', item_id='movieId', target='rating')
