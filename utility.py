import pandas

headlines = pandas.read_csv('data/headlines.txt', parse_dates=[0])
headlines = headlines[headlines['message'].notnull()]


def get_prices(stock_name):
    stock = pandas.read_csv('data/'+stock_name+'.csv', parse_dates=[0])
    stock = stock[['Date', 'Close', 'Volume', 'Threshold Change', 'Next day', 'Price change']]
    # Columns we are extracting. Add more here.
    return stock


def get_prices_threshold(dataframe):
    return dataframe[dataframe['Threshold Change'] == '1']


def headlines_for(topic):
    return headlines[headlines['message'].str.contains(topic, case=False)]


def get_feature_vector(sentence):
    # Feature extraction code here.
    return 'result'

