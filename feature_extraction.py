import utility

google_news = utility.headlines_for('google')
#print google_news.head()

feature_vector = google_news.message.apply(lambda x: utility.get_feature_vector(x))
print feature_vector.head()
