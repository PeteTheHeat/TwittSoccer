# coding=utf-8

import re
from JSON_formatting import get_tweets
from EventTime import get_event_times, get_tweet_minute, get_event_fuzziness, generate_tweet_volume_graph
from UserCredibility import get_minute_credibility, get_users_credibility, get_cred_fuzziness
from FuzzyMembership import compute_certainty
from EventPlayer import get_event_list

"""
Main function to control execution of the twitter analyzer
"""

# Control which game we are looking at
#game = 0 # barcelona vs villareal
game = 1 # chelsea vs aston villa

# Barcelona vs. Villareal
if game == 0:
    start_time = 1458485967
    team1 = "Barcelona"
    team2 = "Villareal"
    import Barcelona
    import Villareal
    players = Barcelona.players + Villareal.players

    def get_player_name(player):
        if Barcelona.get_player_name(player):
            return Barcelona.get_player_name(player)
        else:
            return Villareal.get_player_name(player)

# Chelsea vs Aston Villa
if game == 1:
    start_time = 1459597560
    team1 = "Chelsea"
    team2 = "Aston Villa"
    import Chelsea
    import AstonVilla
    players = Chelsea.players + AstonVilla.players

    def get_player_name(player):
        if Chelsea.get_player_name(player):
            return Chelsea.get_player_name(player)
        else:
            return AstonVilla.get_player_name(player)

print "Analyzing {} vs {}".format(team1, team2)

# Variables for event detection
time_threshold = 50
goal_center = 20
goal_scaling = 0.25
yellow_center = 10
yellow_scaling = 0.25

# Regex 
goal_regex = re.compile('g+o+a*l+', re.IGNORECASE)
red_regex = re.compile('red', re.IGNORECASE)
yellow_regex = re.compile('yellow|amarilla', re.IGNORECASE)
half_regex = re.compile('half', re.IGNORECASE)
end_regex = re.compile('end|close|full|final|over', re.IGNORECASE)

# Pull in our list of tweets
print "Getting Tweets and Game Metadata"
tweets = get_tweets()[game]
generate_tweet_volume_graph(tweets, start_time)

# Parse tweets into halftime, fulltime
half_tweets = []
end_tweets = []

for tweet in tweets:
    if half_regex.search(tweet.text):
        half_tweets.append(tweet)
    if end_regex.search(tweet.text):
        end_tweets.append(tweet)

# Step 1: Figure out when each half ends
half_time = get_event_times(half_tweets, time_threshold, start_time)[0]
end_time = get_event_times(end_tweets, time_threshold, start_time)[0]
if end_time < 45+15+45:
    end_time = 45+5+15+45+5 # worst case average game time, if we can't detect it
half_stoppage = half_time - 45
second_start = half_time + 15
end_stoppage = end_time - (second_start + 45)

# Step 2: Filter tweets into each minute of the game
print "Filtering Tweets"
goals_regulartime = [[] for x in range(0, 90)] 
yellows_regulartime = [[] for x in range(0, 90)] 
goals_half_stoppage = [[] for x in range(0, half_stoppage)]
yellows_half_stoppage = [[] for x in range(0, half_stoppage)]
goals_end_stoppage= [[] for x in range(0, end_stoppage)]
yellows_end_stoppage= [[] for x in range(0, end_stoppage)]

for tweet in tweets:
    tweet_minute = get_tweet_minute(tweet, start_time)
    if tweet_minute < 0: continue
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
print "Computing fuzzy scores"
goal_game_fuzz, goal_half_fuzz, goal_end_fuzz = get_event_fuzziness(goals_regulartime, goals_half_stoppage, goals_end_stoppage, goal_center, goal_scaling)
yellow_game_fuzz, yellow_half_fuzz, yellow_end_fuzz = get_event_fuzziness(yellows_regulartime, yellows_half_stoppage, yellows_end_stoppage, yellow_center, yellow_scaling)
users_credibility = get_users_credibility(tweets)
cred_goal_game_fuzz, cred_goal_half_fuzz, cred_goal_end_fuzz = get_cred_fuzziness(goals_regulartime, goals_half_stoppage, goals_end_stoppage, users_credibility)
cred_yellow_game_fuzz, cred_yellow_half_fuzz, cred_yellow_end_fuzz = get_cred_fuzziness(yellows_regulartime, yellows_half_stoppage, yellows_end_stoppage, users_credibility)

# Step 5: Compute the certainty value at each minute
print "Computing certainty scores"
goal_certainty = [compute_certainty(goal_game_fuzz[i], cred_goal_game_fuzz[i]) for i in range(0, 90)]
goal_half_certainty = [compute_certainty(goal_half_fuzz[i], cred_goal_half_fuzz[i]) for i in range(0, half_stoppage)]
goal_end_certainty = [compute_certainty(goal_end_fuzz[i], cred_goal_end_fuzz[i]) for i in range(0, end_stoppage)]

yellow_certainty = [compute_certainty(yellow_game_fuzz[i], cred_yellow_game_fuzz[i]) for i in range(0, 90)]
yellow_half_certainty = [compute_certainty(yellow_half_fuzz[i], cred_yellow_half_fuzz[i]) for i in range(0, half_stoppage)]
yellow_end_certainty = [compute_certainty(yellow_end_fuzz[i], cred_yellow_end_fuzz[i]) for i in range(0, end_stoppage)]

# Output everything to file
with open('goal_certainty.csv', 'w') as goalfile:
    with open('yellow_certainty.csv', 'w') as yellowfile:
        for i in range(0, 45):
            goalfile.write('{},{},{},{}\n'.format(i, goal_game_fuzz[i], cred_goal_game_fuzz[i], goal_certainty[i]))
            yellowfile.write('{},{},{},{}\n'.format(i, yellow_game_fuzz[i], cred_yellow_game_fuzz[i], yellow_certainty[i]))
        for i in range(0, half_stoppage):
            goalfile.write('{},{},{},{}\n'.format(i, goal_half_fuzz[i], cred_goal_half_fuzz[i], goal_half_certainty[i]))
            yellowfile.write('{},{},{},{}\n'.format(i, yellow_half_fuzz[i], cred_yellow_half_fuzz[i], yellow_half_certainty[i]))
        for i in range(45, 90):
            goalfile.write('{},{},{},{}\n'.format(i, goal_game_fuzz[i], cred_goal_game_fuzz[i], goal_certainty[i]))
            yellowfile.write('{},{},{},{}\n'.format(i, yellow_game_fuzz[i], cred_yellow_game_fuzz[i], yellow_certainty[i]))
        for i in range(0, end_stoppage):
            goalfile.write('{},{},{},{}\n'.format(i, goal_end_fuzz[i], cred_goal_end_fuzz[i], goal_end_certainty[i]))
            yellowfile.write('{},{},{},{}\n'.format(i, yellow_end_fuzz[i], cred_yellow_end_fuzz[i], yellow_end_certainty[i]))

# identify which players were involved in events with certainty over 0.6
print "Identifying Players"
certainty_threshold = 0.6
goals =  get_event_list(goals_regulartime, goals_half_stoppage, goals_end_stoppage, goal_certainty, goal_half_certainty, goal_end_certainty, certainty_threshold, half_stoppage, end_stoppage, players)
yellows =  get_event_list(yellows_regulartime, yellows_half_stoppage, yellows_end_stoppage, yellow_certainty, yellow_half_certainty, yellow_end_certainty, certainty_threshold, half_stoppage, end_stoppage, players)

summary_string = "Summary of {} vs {}".format(team1, team2)
print summary_string
print "-"*len(summary_string)
print "Goals"
print '\n'.join(["{}' {}".format(x[1], get_player_name(x[0]).capitalize()) for x in goals])
print "Yellows"
print '\n'.join(["{}' {}".format(x[1], get_player_name(x[0]).capitalize()) for x in yellows])

