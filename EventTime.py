import re
import time
import calendar
from JSON_formatting import get_tweets

bucket_size = 60 # 1 minute buckets
event_threshold = 20 # Threshold for increase signifying an event
# 20 for goals
# 6 for yellows
# 50 for halftime, end of game

first_tweet = 1458485967 # actually find the start of tweets TODO


def smooth_list(list):
    smoothed = []
    smoothed.append((2*list[0] + list[1])/3.0)
    for i in range(1, len(list)-1):
        smoothed.append((list[i-1] + 2*list[i] + list[i+1])/4.0)
    smoothed.append((list[-2] + 2*list[-1])/3.0)
    return smoothed

def derivatives(counts):
    deriv_list = [0]
    for i in range(1, len(counts)):
        deriv_list.append(counts[i] - counts[i-1])
    return deriv_list

def get_event_times(tweets):
    tweettimes = []
    for tweet in tweets:
        goal_regex = re.compile('go+a*l', re.IGNORECASE)
        own_regex = re.compile('own goal', re.IGNORECASE)
        yellow_regex = re.compile('yellow|amarilla', re.IGNORECASE)
        half_regex = re.compile('half', re.IGNORECASE)
        end_regex = re.compile('end|close|full|final', re.IGNORECASE)
        if goal_regex.search(tweet.text):
            tweettimes.append(tweet.created_at_unix)

    buckets = {}
    for ttime in tweettimes:
        bucket = int(ttime - first_tweet) / bucket_size
        if bucket not in buckets:
            buckets[bucket] = 0
        buckets[bucket] += 1

    # cut off tweets after the game
    counts = []
    for i in range(0, 150):
        if i in buckets:
            counts.append(buckets[i])
        else:
            counts.append(0)

    with open('yellowcount.csv', 'w') as outfile:
        for i in range(0, 150):
            outfile.write(str(i) + ',' + str(counts[i]) + '\n')

    derivs = derivatives(counts)

    events = []
    for i in range(0, len(derivs)):
        if derivs[i] > event_threshold:
            events.append(i)
    return events

[t1, t2] = get_tweets()
print get_event_times(t2)
