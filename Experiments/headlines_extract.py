import pandas
import numpy

headlines = pandas.read_csv('../data/headlines.txt', parse_dates=[0])
headlines = headlines[headlines['message'].notnull()]
# print headlines
# print headlines.dtypes
# print headlines.iloc[1]['msg_dt'].date()

goog_stock = pandas.read_csv('../data/google.csv', parse_dates=[0])
goog_stock = goog_stock[['Date', 'Close', 'Volume', 'Threshold Change', 'Next day']]
# Columns we are extracting. Add more here.
# print goog_stock

change_dates = goog_stock[goog_stock['Threshold Change'] == '1']

# print headlines[headlines['msg_dt'].date() == change_dates and 'Google' in headlines['message']]
headlines['msg_dt_only'] = headlines.msg_dt.map(lambda x: x.date)
# print headlines.head()

# dates_only = headlines[(headlines['msg_dt_only'] in change_dates)]
# print headlines.message.find('Google')

#print headlines[headlines['message'].isnull()]

relevant_new = headlines[headlines['message'].str.contains('microsoft', case=False)]
print relevant_new.shape



# merged = pandas.merge(left=change_dates, right=headlines)
