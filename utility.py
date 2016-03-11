import pandas

headlines = pandas.read_csv('../data/headlines.txt', parse_dates=[0])
headlines = headlines[headlines['message'].notnull()]


def get_prices(stock_name):
    stock = pandas.read_csv('data/'+stock_name+'.csv', parse_dates=[0])
    stock = stock[['Date', 'Close', 'Volume', 'Threshold Change', 'Next day']] # Columns we are extracting. Add more here.
    return stock


def headlines_for(topic):
    return headlines[headlines['message'].str.contains(topic, case=False)]

