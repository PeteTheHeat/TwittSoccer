# coding=utf-8

players = [
    "remy",
    "kenedy",
    "pedro",
    "loftus|cheek",
    "mikel",
    "cesc|f.bregas", 
    "azpilicueta", 
    "ivanovic", 
    "miazga", 
    "baba|rahman", 
    "courtois", 
    "alexandre|pato",
    "oscar",
    "clarke|salter"
]

def get_player_name(player):
    if player == "cesc|f.bregas":
        return "fábregas"
    elif player == "loftus|cheek":
        return "Loftus-Cheek"
    elif player == "baba|rahman":
        return "Baba Rahman"
    elif player == "alexandre|pato":
        return "Alexandre Pato"
    elif player == "clarke|salter":
        return "Clarke-Salter"
    return player
