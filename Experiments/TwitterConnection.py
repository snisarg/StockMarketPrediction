import twitter

api = twitter.Api(consumer_key='6u5reXpW9MG6reYgGceVzsDLM', consumer_secret='I6w4MQjvkpUTxTxXtUTAwVi00tguWui7p1xgO3osvPSuVqkGV4',
	access_token_key='41324420-1XD5E5aO9pAssAo7mpssB8cTMGMzfQoz0dXBm239j', access_token_secret='5aSVkHVNeRd3VyKZU4fqGHSNo2Uif4VahvxhTLgq2HCGF')
print api.VerifyCredentials()
