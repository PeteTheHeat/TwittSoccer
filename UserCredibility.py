from JSON_formatting import get_tweets

#This function reads all tweets from result of JSON_formatting, removes duplicate users, and sets credibility score 
#based on number of followers and verification. FCBlive_users and VillarrealFCB_users are dicts with {key:value}
#being {screen_name:{followers_count,verified,credibility}}

def get_user_credibility():
	FCBlive_tweets, VillarrealFCB_tweets = get_tweets()
	FCBlive_users = {}
	VillarrealFCB_users = {}
	all_users = [[FCBlive_tweets,FCBlive_users],[VillarrealFCB_tweets, VillarrealFCB_users]]


	for i in all_users:
		unique_users = []
		#Remove duplicate users
		for tweet in i[0]:
			if tweet.screen_name not in i[1]:
				i[1][tweet.screen_name] = 1
				unique_users.append(tweet)

		#Get max follower count in sample set
		max_followers = max(unique_users, key = lambda x: x.followers_count).followers_count

		for j in range(len(unique_users)):
			#Credibility score = 1.0 if verified, else based on ratio of followers_count:max_followers
			credibility = 1.0 if unique_users[j].verified else (float(unique_users[j].followers_count) / max_followers)
			i[1][unique_users[j].screen_name] = {
				"followers_count": unique_users[j].followers_count,
				"verified": unique_users[j].verified,
				"credibility": credibility
			}
	# print len(VillarrealFCB_users.keys())
	# print len(FCBlive_users.keys())
	return FCBlive_users, VillarrealFCB_users


	
