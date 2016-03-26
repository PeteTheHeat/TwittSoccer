#This code just reads in all the JSON files in the #FCBLive and #VillarrealFCB dirs 
#and parses the data we care about into a tweet class, and stores all these tweets 
#in individual lists

import json
from pprint import pprint

class Tweet:
  def __init__(self, text, created_at, retweet_count, screen_name, followers_count, verified):
  	self.text = text
  	self.created_at = created_at
  	self.retweet_count = retweet_count
  	self.screen_name = screen_name
  	self.followers_count = followers_count
  	self.verified = verified

FCBlive_tweets, VillarrealFCB_tweets= [],[]

for i in range(181):
	file_name = '#FCBLive/FCBLive' + str(i) + '.json'
	tweet_file = open(file_name, 'r')
	tweets = json.loads(tweet_file.read())

	for j in range(len(tweets['statuses'])):
		FCBlive_tweets.append(Tweet(
			tweets['statuses'][j]['text'], 
			tweets['statuses'][j]['created_at'], 
			tweets['statuses'][j]['retweet_count'], 
			tweets['statuses'][j]['user']['screen_name'], 
			tweets['statuses'][j]['user']['followers_count'], 
			tweets['statuses'][j]['user']['verified']))

for i in range(299):
	file_name = '#VillarrealFCB/VillarrealFCB' + str(i) + '.json'
	tweet_file = open(file_name, 'r')
	tweets = json.loads(tweet_file.read())

	for j in range(len(tweets['statuses'])):
		VillarrealFCB_tweets.append(Tweet(
			tweets['statuses'][j]['text'], 
			tweets['statuses'][j]['created_at'], 
			tweets['statuses'][j]['retweet_count'], 
			tweets['statuses'][j]['user']['screen_name'], 
			tweets['statuses'][j]['user']['followers_count'], 
			tweets['statuses'][j]['user']['verified']))

print(len(FCBlive_tweets))
print(len(VillarrealFCB_tweets))
