import graphlab as gl
import time
import util


class Recommender(object):
    def train(self, data, user_id='userId', item_id='movieId', target='rating', item_data=None):
        return gl.recommender.create(data, user_id=user_id, item_id=item_id, target=target, item_data=item_data)


class ItemSimilarityRecommender(Recommender):
    def train(self, data, user_id='userId', item_id='movieId', target='rating',  item_data=None):
        return gl.recommender.item_similarity_recommender.create(data, user_id=user_id, item_id=item_id, target=target, item_data=item_data)


class FactorizationRecommender(Recommender):
    def train(self, data, user_id='userId', item_id='movieId', target='rating',  item_data=None):
        return gl.recommender.factorization_recommender.create(data, user_id=user_id, item_id=item_id, target=target, item_data=item_data)


class PopularityRecommender(Recommender):
    def train(self, data, user_id='userId', item_id='movieId', target='rating', item_data=None):
        return gl.recommender.popularity_recommender.create(data, user_id=user_id, item_id=item_id, target=target, item_data=item_data)


class RecommendationEngine(object):
    def __init__(self, dataset, recommender=None, train_model=False):
        self.dataset = dataset
        self.model = None

        if not recommender:
            recommender = Recommender()

        self.recommender = recommender

        if train_model:
            self.train_model()

    @util.timing
    def load_model(self, fpath):
        self.model = gl.load_model(fpath)

    @util.timing
    def train_model(self):
        item_info = self.dataset.movies.select_columns(['movieId', 'genres', 'year'])
        self.model = self.recommender.train(self.dataset.ratings, user_id='userId', item_id='movieId', target='rating', item_data=item_info)
        return self.model

    @util.timing
    def save_model(self, fpath):
        if self.model:
            self.model.save(fpath)

    @util.timing
    def get_recommendations(self, request_data, top_k=None, min_count=10):
        if not top_k:
            top_k = 20

        mapped = map(util.map_dict_value_as_array, request_data['ratings'])
        reduced = reduce(util.merge_two_dicts, mapped)

        nb_ratings = len(reduced['movieId'])

        reduced['userId'] = [999999 for x in range(nb_ratings)]

        reduced = gl.SFrame(reduced)

        recommendations = self.model.recommend(users=[999999], k=500, new_observation_data=reduced)

        recommendations = self.dataset.movies.join(recommendations, on='movieId')

        recommendations = recommendations[recommendations['ratingCount'] > min_count]

        if 'filter' in request_data:
            filtered = recommendations\
                .flat_map(['genres', 'movieId'],
                          lambda x: [[g, x['movieId']] for g in x['genres'] for i in range(0, len(x['genres']))])\
                .filter_by(request_data['filter'], 'genres')

            recommendations = recommendations.filter_by(filtered['movieId'], 'movieId')

        recommendations = recommendations.remove_column('userId')

        return util.sframe_to_list(recommendations, top_k)
