from yamr.dataset import EnhancedDataset
from yamr.recommender import RecommendationEngine, ItemSimilarityRecommender, FactorizationRecommender, PopularityRecommender

dataset_path = 'datasets/ml-latest-enhanced'
ds = EnhancedDataset(dataset_path)

#recommender = ItemSimilarityRecommender()
#recommender = FactorizationRecommender()
recommender = PopularityRecommender()
re = RecommendationEngine(ds, recommender=recommender)
re.train_model()
re.save_model('popularity_model')
