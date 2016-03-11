import utility
from sklearn.naive_bayes import GaussianNB
import numpy
from sklearn import linear_model, cross_validation, neural_network
from sklearn.svm import SVC

goog = utility.get_news_prices('google')

model = utility.pipeline_setup(SVC(kernel='linear', probability=True, random_state=40))
model_fitted = model.fit(goog['message'], goog['Threshold Change'])

x = goog['message']
y = goog['Threshold Change']

predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')

print 'All RMSEs',  numpy.sqrt(-scores)
print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))