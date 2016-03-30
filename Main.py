import re
from JSON_formatting import get_tweets
from EventTime import get_event_times, get_tweet_minute, get_event_fuzziness
from UserCredibility import get_minute_credibility, get_users_credibility, get_cred_fuzziness

"""
Main function to control execution of the twitter analyzer
"""

# Variables for event detection
time_threshold = 50
goal_center = 20
goal_scaling = 0.25
yellow_center = 10
yellow_scaling = 0.25

# Regex 
goal_regex = re.compile('g+o+a*l+', re.IGNORECASE)
yellow_regex = re.compile('yellow|amarilla', re.IGNORECASE)
half_regex = re.compile('half', re.IGNORECASE)
end_regex = re.compile('end|close|full|final|over', re.IGNORECASE)

# Pull in our list of tweets
tweets = get_tweets()

# Parse tweets into halftime, fulltime
half_tweets = []
end_tweets = []

for tweet in tweets:
    if half_regex.search(tweet.text):
        half_tweets.append(tweet)
    if end_regex.search(tweet.text):
        end_tweets.append(tweet)

# Step 1: Figure out when each half ends
half_time = get_event_times(half_tweets, time_threshold)[0]
end_time = get_event_times(end_tweets, time_threshold)[0]
half_stoppage = half_time - 45
second_start = half_time + 15
end_stoppage = end_time - (second_start + 45)

# Step 2: Filter tweets into each minute of the game
goals_regulartime = [[] for x in range(0, 90)] 
yellows_regulartime = [[] for x in range(0, 90)] 
goals_half_stoppage = [[] for x in range(0, half_stoppage)]
yellows_half_stoppage = [[] for x in range(0, half_stoppage)]
goals_end_stoppage= [[] for x in range(0, end_stoppage)]
yellows_end_stoppage= [[] for x in range(0, end_stoppage)]

for tweet in tweets:
    tweet_minute = get_tweet_minute(tweet)
    # place tweet in appropriate list
    if tweet_minute < 45 and goal_regex.search(tweet.text):
        goals_regulartime[tweet_minute].append(tweet)
    elif tweet_minute < 45 and yellow_regex.search(tweet.text):
        yellows_regulartime[tweet_minute].append(tweet)
    elif tweet_minute - 45 < half_stoppage and goal_regex.search(tweet.text):
        goals_half_stoppage[tweet_minute-45].append(tweet)
    elif tweet_minute - 45 < half_stoppage and yellow_regex.search(tweet.text):
        yellows_half_stoppage[tweet_minute-45].append(tweet)
    elif tweet_minute >= second_start and tweet_minute - second_start < 45 and goal_regex.search(tweet.text):
        goals_regulartime[tweet_minute - second_start + 45].append(tweet)
    elif tweet_minute >= second_start and tweet_minute - second_start < 45 and yellow_regex.search(tweet.text):
        yellows_regulartime[tweet_minute - second_start + 45].append(tweet)
    elif tweet_minute > second_start and tweet_minute - (second_start + 45) < end_stoppage and goal_regex.search(tweet.text):
        goals_end_stoppage[tweet_minute - (second_start + 45)].append(tweet)
    elif tweet_minute > second_start and tweet_minute - (second_start + 45) < end_stoppage and yellow_regex.search(tweet.text):
        yellows_end_stoppage[tweet_minute - (second_start + 45)].append(tweet)

# Step 3: Compute fuzzy event and credibility for each minute of the game
goal_game_fuzz, goal_half_fuzz, goal_end_fuzz = get_event_fuzziness(goals_regulartime, goals_half_stoppage, goals_end_stoppage, goal_center, goal_scaling)
yellow_game_fuzz, yellow_half_fuzz, yellow_end_fuzz = get_event_fuzziness(yellows_regulartime, yellows_half_stoppage, yellows_end_stoppage, yellow_center, yellow_scaling)

users_credibility = get_users_credibility(tweets)
cred_goal_game_fuzz, cred_goal_half_fuzz, cred_goal_end_fuzz = get_cred_fuzziness(goals_regulartime, goals_half_stoppage, goals_end_stoppage, users_credibility)
cred_yellow_game_fuzz, cred_yellow_half_fuzz, cred_yellow_end_fuzz = get_cred_fuzziness(yellows_regulartime, yellows_half_stoppage, yellows_end_stoppage, users_credibility)



