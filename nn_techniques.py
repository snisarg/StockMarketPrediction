import utility
from sklearn.naive_bayes import GaussianNB
import pandas
import numpy
from sklearn import linear_model, cross_validation, neural_network
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from nltk.corpus import verbnet

goog = utility.get_news_prices('google')
goog.append(utility.get_news_prices('microsoft'))
goog.append(utility.get_news_prices('apple'))
goog.append(utility.get_news_prices('yahoo'))
goog.append(utility.get_news_prices('adobe'))
goog.append(utility.get_news_prices('ford'))

# Select model of computation:
model = neural_network.MLPRegressor([len(verbnet.classids()), 200, 8], 'relu', 'adam', 0.0001, 200, 'constant', 0.001, 0.5, 200,
                                     True, None, 0.0001, False, False, 0.9, True, False, 0.1, 0.9, 0.999, 1e-08)
# model = RandomForestRegressor(n_estimators=50, max_features=30, max_depth=9, n_jobs=1)
# model = SVC(kernel='linear', probability=True, random_state=40)
# model = linear_model.LinearRegression()

# model = utility.pipeline_setup(model)

# model_fitted = model.fit(goog['message'], goog['Threshold Change'])

# Select columns:
x = goog.message.apply(lambda sentence: utility.get_feature_vector(sentence+".")[0])
# x.to_csv('data/google_msg_id.csv')
# x = pandas.read_csv('data/google_msg_id.csv')
# print x
# x = goog['message']
# x = x.apply(lambda i: utility.one_hot(i))
array = numpy.zeros((len(x), len(verbnet.classids())))
for results in range(len(x)):
    for i in x[results]:
        # print i
        array[results][i] = 1

# print array.shape
x = array
# print array
#x=numpy.reshape(x,(len(x), (len(verbnet.classids()))))

# y = goog['Threshold Change'].astype(int)
y = goog['Direction']

# print y

predicted = cross_validation.cross_val_predict(model, x, y, 10, 1, 0, None, 0)
scores = cross_validation.cross_val_score(model, x, y,  cv=10, scoring='mean_squared_error')

print 'All RMSEs',  numpy.sqrt(-scores)
print 'Mean RMSE',  numpy.mean(numpy.sqrt(-scores))
print 'Best RMSE',  numpy.min(numpy.sqrt(-scores))

# Could consider ROC curves
