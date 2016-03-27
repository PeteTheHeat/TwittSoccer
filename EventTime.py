import time
import calendar
from JSON_formatting import get_tweets

time_format = "%a %b %d  %H:%M:%S +0000 %Y"
bucket_size = 60 # 1 minute buckets
event_threshold = 0.1 # Threshold for increase signifying an event

def smooth_list(list):
    smoothed = []
    smoothed.append((2*list[0] + list[1])/3.0)
    for i in range(1, len(list)-1):
        smoothed.append((list[i-1] + 2*list[i] + list[i+1])/4.0)
    smoothed.append((list[-2] + 2*list[-1])/3.0)
    return smoothed

def derivatives(list):
    deriv_list = [0]
    for i in range(1, len(list)):
        deriv_list.append((list[i] - list[i-1])/60.0)
    return deriv_list

def get_event_times(tweets):
    tweettimes = []
    for tweet in tweets:
        e_seconds = calendar.timegm(time.strptime(tweet.created_at, time_format))
        tweettimes.append(e_seconds)
    tweettimes.sort()
    first_time = tweettimes[0]

    buckets = {}
    for ttime in tweettimes:
        bucket = int(ttime - first_time) / bucket_size
        if bucket not in buckets:
            buckets[bucket] = 0
        buckets[bucket] += 1

    counts = buckets.values()
    counts = smooth_list(counts)
    derivs = derivatives(counts)
    derivs = smooth_list(derivs)
    
    events = []
    for i in range(0, len(derivs)):
        if derivs[i] > event_threshold:
            events.append(i)
    return events

[t1, t2] = get_tweets()
t = t1 + t2
print get_event_times(t)
