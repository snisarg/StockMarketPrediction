import pandas


def get_prices(stock_name):
    stock = pandas.read_csv('data/'+stock_name+'.csv', parse_dates=[0])
    stock = stock[['Date', 'Close', 'Volume', 'Threshold Change']] # Columns we are extracting. Add more here.
    return stock


def get_headlines():
    return pandas.read_csv('../data/headlines_20.txt', parse_dates=[0])

