import twitter

api = twitter.Api(consumer_key='6u5reXpW9MG6reYgGceVzsDLM',
                  consumer_secret='I6w4MQjvkpUTxTxXtUTAwVi00tguWui7p1xgO3osvPSuVqkGV4',
                  access_token_key='41324420-1XD5E5aO9pAssAo7mpssB8cTMGMzfQoz0dXBm239j',
                  access_token_secret='5aSVkHVNeRd3VyKZU4fqGHSNo2Uif4VahvxhTLgq2HCGF')
#print api.GetUser("business")
statuses = api.GetUserTimeline(screen_name="business", max_id=1457282574, since_id=1)
print [s.created_at_in_seconds for s in statuses]

# goog_search = api.GetSearch('from:ReutersBiz since:2016-02-25 until:2015-02-29 JPMorgan')
# print goog_search
