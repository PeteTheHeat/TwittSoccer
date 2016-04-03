#This code just reads in all the JSON files in the #FCBLive and #VillarrealFCB dirs 
#and parses the data we care about into a tweet class, and stores all these tweets 
#in individual lists

import json
import time
import calendar
from pprint import pprint

time_format = "%a %b %d  %H:%M:%S +0000 %Y"

class Tweet:
  def __init__(self, text, created_at, retweet_count, screen_name, followers_count, verified):
  	self.text = text
  	self.created_at = created_at
  	self.created_at_unix = calendar.timegm(time.strptime(created_at, time_format))
  	self.retweet_count = retweet_count
  	self.screen_name = screen_name
  	self.followers_count = followers_count
  	self.verified = verified


def get_tweets():
	VillarrealFCB_tweets, CFCLive_tweets = [],[]
	for i in range(1736):
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

	for i in range(2593):
		file_name = '#CFCLive/CFCLive' + str(i) + '.json'
		tweet_file = open(file_name, 'r')
		tweets = json.loads(tweet_file.read())

		for j in range(len(tweets['statuses'])):
			CFCLive_tweets.append(Tweet(
				tweets['statuses'][j]['text'], 
				tweets['statuses'][j]['created_at'], 
				tweets['statuses'][j]['retweet_count'], 
				tweets['statuses'][j]['user']['screen_name'], 
				tweets['statuses'][j]['user']['followers_count'], 
				tweets['statuses'][j]['user']['verified']))

	return VillarrealFCB_tweets, CFCLive_tweets
