import re

# scan over tweets for a given event to identify player
def get_player_for_event(players, tweets):
    counts = {}
    regexs = [re.compile(p, re.IGNORECASE) for p in players]
    for tweet in tweets:
        for i in range(0, len(players)):
            if regexs[i].search(tweet.text):
                if players[i] not in counts:
                    counts[players[i]] = 0
                counts[players[i]] += 1
    max = 0
    maxplayer = ""
    for player, count in counts.items():
        if count > max:
            max = count
            maxplayer = player
    return maxplayer

def get_event_list(regular, half, end, certainty, certainty_half, certainty_end, threshold, half_stoppage, end_stoppage, players):
    lastp = ""
    lastm = 0
    events = []
    for minute in range(0, 45):
        if certainty[minute] >= threshold:
            tweets = []
            for i in range(0, 4):
                if minute+i < 45:
                    tweets = tweets + regular[minute+i]
                elif minute+1 % 45 < half_stoppage:
                    tweets = tweets + half[minute+i % 45]
            player = get_player_for_event(players, tweets)
            if lastm+1 != minute or lastp != player:
                events.append([player, minute])
                lastp = player
            lastm = minute
    for minute in range(0, half_stoppage):
        if certainty_half[minute] >= threshold:
            tweets = []
            for i in range(0, 4):
                if minute+i < half_stoppage:
                    tweets = tweets + half[minute+i]
            player = get_player_for_event(players, tweets)
            if (minute == 0 and lastm != 44) or (minute != 0 and lastm+1 != minute) or lastp != player:
                events.append([player, "45+" + str(minute)])
                lastp = player
            lastm = minute
    for minute in range(45, 90):
        if certainty[minute] >= threshold:
            tweets = []
            for i in range(0, 4):
                if minute+i < 90:
                    tweets = tweets + regular[minute+i]
                elif minute+1 % 90 < end_stoppage:
                    tweets = tweets + half[minute+i % 90]
            player = get_player_for_event(players, tweets)
            if lastm+1 != minute or lastp != player:
                events.append([player, minute])
                lastp = player
            lastm = minute
    for minute in range(0, end_stoppage):
        if certainty_end[minute] >= threshold:
            tweets = []
            for i in range(0, 4):
                if minute+i < end_stoppage:
                    tweets = tweets + end[minute+i]
            player = get_player_for_event(players, tweets)
            if (minute == 0 and lastm != 89) or (minute != 0 and lastm+1 != minute) or lastp != player:
                events.append([player, "90+" + str(minute)])
                lastp = player
            lastm = minute
    return events

