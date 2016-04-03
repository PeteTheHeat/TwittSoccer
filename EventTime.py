import numpy as np

"""
Estimate the time of an event of get the fuzzy score of an event
"""

bucket_size = 60 # 1 minute buckets

def derivatives(counts):
    deriv_list = [0]
    for i in range(1, len(counts)):
        deriv_list.append(counts[i] - counts[i-1])
    return deriv_list

def get_tweet_minute(tweet, start_time):
    return int(tweet.created_at_unix - start_time) / bucket_size

def get_event_times(tweets, threshold, start_time):
    buckets = {}
    for tweet in tweets:
        bucket = get_tweet_minute(tweet, start_time)
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

def compute_fuzzy_score(derivative, center, scaling):
    return 1.0/(1.0 + np.exp(-scaling * (derivative - center)))

def get_event_fuzziness(game, half_stoppage, end_stoppage, center, scaling):
    game_derivs = [0]
    for i in range(1, 45):
        game_derivs.append(len(game[i]) - len(game[i-1]))
    
    half_derivs = [len(half_stoppage[0]) - len(game[44])]
    for i in range(1, len(half_stoppage)):
        half_derivs.append(len(half_stoppage[i]) - len(half_stoppage[i-1]))
    
    game_derivs.append(0)
    for i in range(46, 90):
        game_derivs.append(len(game[i]) - len(game[i-1]))
    
    end_derivs = [len(end_stoppage[0]) - len(game[-1])]
    for i in range(1, len(end_stoppage)):
        end_derivs.append(len(end_stoppage[i]) - len(end_stoppage[i-1]))

    game_fuzz = [compute_fuzzy_score(x, center, scaling) for x in game_derivs]
    half_fuzz = [compute_fuzzy_score(x, center, scaling) for x in half_derivs]
    end_fuzz = [compute_fuzzy_score(x, center, scaling) for x in end_derivs]

    return game_fuzz, half_fuzz, end_fuzz
