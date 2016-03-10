import pandas
import numpy

headlines = pandas.read_csv('../data/headlines_20.txt', parse_dates=[0])
print headlines.dtypes
# print headlines.loc[0][0].date()

goog_stock = pandas.read_csv('../data/google.csv', parse_dates=[0])
goog_stock = goog_stock[['Date', 'Close', 'Volume', 'Threshold Change']] # Columns we are extracting. Add more here.
#print goog_stock

print goog_stock[goog_stock['Threshold Change'] == '1']
