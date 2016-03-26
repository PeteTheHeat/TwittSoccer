from JSON_formatting import get_tweets

#This reads all tweets from result of JSON_formatting, removes duplicate users, and sets credibility score 
#based on number of followers and verification. FCBlive_users and VillarrealFCB_users are dicts with {key:value}
#being {screen_name:{followers_count,verified,credibility}}

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

	#Sort by follower count descending
	s = sorted(unique_users, key = lambda x: (x.followers_count, x.verified), reverse=True)
	total_users = len(unique_users)

	for j in range(total_users):
		#Credibility score = 1.0 if verified, else based on ranking of twitter followers within sample set
		credibility = 1.0 if s[j].verified is True else (float(total_users - j) / total_users)
		i[1][s[j].screen_name] = {
			"followers_count": s[j].followers_count,
			"verified": s[j].verified,
			"credibility": credibility
		}
print len(VillarrealFCB_users.keys())
print len(FCBlive_users.keys())


	
