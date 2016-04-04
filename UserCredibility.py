import numpy as np
from JSON_formatting import get_tweets
from EventTime import get_event_times

#This function reads all tweets from result of JSON_formatting, removes duplicate users, and sets credibility score 
#based on number of followers and verification. FCBlive_users and VillarrealFCB_users are dicts with {key:value}
#being {screen_name:{followers_count,verified,credibility}}

def get_users_credibility(tweets):
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

def get_minute_credibility(users_credibility, minute_tweets):
	creds = []
	for tweet in minute_tweets:
		creds.append(users_credibility[tweet.screen_name]['credibility'])
	avg_cred = float(sum(creds))/len(creds)
	return compute_fuzzy_score(avg_cred)

def compute_fuzzy_score(avg_cred):
    return 1.0/(1.0 + np.exp(-10 * (avg_cred - 0.5)))

def get_cred_fuzziness(game, half_stoppage, end_stoppage, users_credibility):
	all = [game, half_stoppage, end_stoppage]
	cred_fuzz_all = []
	for period in all:
		cred_fuzz = []
		for minute_tweets in period:
			if minute_tweets:
				avg_fuzz = get_minute_credibility(users_credibility, minute_tweets)
				cred_fuzz.append(avg_fuzz)
			else:
				cred_fuzz.append(0.0)
		cred_fuzz_all.append(cred_fuzz)
	return cred_fuzz_all[0], cred_fuzz_all[1], cred_fuzz_all[2]








	
