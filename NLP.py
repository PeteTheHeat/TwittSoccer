import re
from JSON_formatting import get_tweets

[t1, t2] = get_tweets()

game_tweets, yellow_tweets, goal_tweets = [], [], []
players = ["neymar", "bakambu", "rakitic", "mathieu", "arda", "messi", "suarez", "mascherano", "pique", "alves", "alba", "busquets", "soldado", "soriano", "trigueros", "castillejo", "bailly", "ruiz", "asenjo", "mario", "rukavina", "bruno", "adrian", "pina", "baptistao", "bravo", "roberto"]
goal_counters, yellow_counters = [], []
regexs = []
time_format = "%a %b %d  %H:%M:%S +0000 %Y"

#setup
for i in range(0, len(players)):
    goal_counters.append(0)
    yellow_counters.append(0)
    regexs.append(re.compile(players[i], re.IGNORECASE))

#filter out tweets from game that aren't retweets
for i in range (0,len(t2)):
    if t2[i].created_at_unix < 1458493324:
        if not "RT" in t2[i].text:
            game_tweets.append(t2[i])

#filter out goals and yellow tweets
for i in range (0, len(game_tweets)):
    goal_regex = re.compile('go+a*l', re.IGNORECASE)
    own_regex = re.compile('own goal', re.IGNORECASE)
    yellow_regex = re.compile('yellow', re.IGNORECASE)
    if goal_regex.search(t2[i].text) and not own_regex.search(t2[i].text):
        goal_tweets.append(t2[i])
    if yellow_regex.search(t2[i].text):
        yellow_tweets.append(t2[i])

goal_tweets.sort(key=lambda x:x.created_at_unix)
yellow_tweets.sort(key=lambda x:x.created_at_unix)

#count player names from goal tweets
for i in range(0,len(goal_tweets)):
    for j in range(0,len(players)):
        if regexs[j].search(goal_tweets[i].text):
            goal_counters[j]+=1

#count player names from yellow tweets
for i in range(0,len(yellow_tweets)):
    for j in range(0,len(players)):
        if regexs[j].search(yellow_tweets[i].text):
            yellow_counters[j]+=1

#print number of player mentions in tweets 
for i in range(0,len(players)):
    print(players[i] + " " + str(goal_counters[i]) + " goals and " + str(yellow_counters[i]) + " yellows")
