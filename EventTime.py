"""
Estimate the time of an event of get the fuzzy score of an event
"""

bucket_size = 60 # 1 minute buckets
first_tweet = 1458485967 # actually find the start of tweets TODO

def derivatives(counts):
    deriv_list = [0]
    for i in range(1, len(counts)):
        deriv_list.append(counts[i] - counts[i-1])
    return deriv_list

def get_tweet_minute(tweet):
    return int(tweet.created_at_unix - first_tweet) / bucket_size

def get_event_times(tweets, threshold):
    buckets = {}
    for tweet in tweets:
        bucket = get_tweet_minute(tweet)
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

    derivs = derivatives(counts)

    events = []
    for i in range(0, len(derivs)):
        if derivs[i] > threshold:
            events.append(i)
    return events
