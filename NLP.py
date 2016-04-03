# -*- coding: utf-8 -*-

import re
import numpy
from JSON_formatting import get_tweets

FCBtweets, CFCtweets = get_tweets()

barca_players = ["neymar", "rakitic", "mathieu", "arda|turan", "messi", "suarez", "mascherano", "piqué|pique", "alves", "alba", "busquets", "bravo", "roberto"]
villareal_players = ["bakambu", "soldado", "soriano", "trigueros", "castillejo", "bailly", "ruiz", "asenjo", "mario", "rukavina", "bruno", "adrian", "pina", "baptistao"]
chelsea_players = ["remy", "kenedy", "pedro", "loftus|cheek", "mikel", "cesc|fabregas|fàbregas", "azpilicueta", "ivanovic", "miazga", "baba|rahman", "courtois", "alexandre|pato", "oscar", "clarke|salter"]
aston_villa_players = ["guzan", "hutton", "richards", "lescott", "cissokho", "sanchez|sànchez", "westwood", "gueye", "carles|gil", "gestede", "jordan|ayew"]
all_players = barca_players + villareal_players + chelsea_players + aston_villa_players
regexs = []

#setup
for i in range(0, len(all_players)):
    regexs.append(re.compile(all_players[i], re.IGNORECASE))

#Pass in a list of tweets, outputs which player occurs the most
def get_most_likely_player(tweets):
	player_counter = [0] * len(all_players)
	for i in range(0, len(tweets)):
		for j in range(0, len(all_players)):
			player_counter[j]+=1 if regexs[j].search(tweets[i].text) else 0
  	return all_players[numpy.argmax(player_counter)]
