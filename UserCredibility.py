from JSON_formatting import get_tweets
from EventTime import get_event_times

#This function reads all tweets from result of JSON_formatting, removes duplicate users, and sets credibility score 
#based on number of followers and verification. FCBlive_users and VillarrealFCB_users are dicts with {key:value}
#being {screen_name:{followers_count,verified,credibility}}

def get_user_credibility():
	tweets = get_tweets()
	users = {}
	unique_users = []

	#Remove duplicate users
	for tweet in tweets:
		if tweet.screen_name not in users:
			users[tweet.screen_name] = 1
			unique_users.append(tweet)

	# Sort based on followers_count
	s = sorted(unique_users, key = lambda x: x.followers_count, reverse = True)

	total_users = len(unique_users)
	for j in range(len(s)):
		# Credibility score = 1.0 if verified, else based on ranking of followers among sample set
		credibility = 1.0 if s[j].verified else (float(total_users - j) / total_users)
		users[s[j].screen_name] = {
			"followers_count": s[j].followers_count,
			"verified": s[j].verified,
			"credibility": credibility
		}
	return users

def get_minute_credibility(tweets):
	user_credibilities = get_user_credibility()
	creds = []
	for tweet in tweets:
		creds.append(user_credibilities[tweet.screen_name]['credibility'])
	return float(sum(creds))/len(creds)







	
