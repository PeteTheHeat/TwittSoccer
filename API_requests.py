#This code searches for tweets with "#VillarrealFCB" from March20th and writes to json file
#Since only 15 tweets are returned at a time, store the max_id of the last 15 tweets and 
#make sure there aren't any duplicates in the next 15 by passing the param to the query  

import json
import requests
import oauth2 

consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''

consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth2.Token(key=access_token_key, secret=access_token_secret)
client = oauth2.Client(consumer, token)

#run the query once without this param, then find it in the search_metadata returned
max_id = 711613582916644863

for i in range(300):
	#Change the term after q=... to change search terms (url encoded) 
	url = "https://api.twitter.com/1.1/search/tweets.json?q=%23VillarrealFCB&since=2016-03-20&until=2016-03-21&max_id=" + str(max_id)
	response, data = client.request(url, method="GET", body="", headers=None)

	file_name = "#VillarrealFCB/VillarrealFCB" + str(i) +".json" 
	file_data = open(file_name, 'w')
	file_data.write(data)

	tweets = json.loads(data)
	for j in range(0,len(tweets['statuses'])):
		if int(tweets['statuses'][j]['id']) < max_id:
			max_id = int(tweets['statuses'][j]['id'])
