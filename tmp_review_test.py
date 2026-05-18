from app.page_views.review_intelligence import render_review_intelligence
from app.services.review_service import ReviewService

reviews = ReviewService.load_reviews()
print('reviews loaded', reviews.shape if reviews is not None else None)
print('sentiment', ReviewService.get_sentiment_distribution())
print('rating', ReviewService.get_rating_distribution())
print('keywords', ReviewService.get_top_keywords(n=5).head(3).to_dict(orient='records'))
