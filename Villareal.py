# coding=utf-8

players = [
    "asenjo",
    "mario",
    "bailly",
    "ruiz",
    "rukavina",
    "castillejo",
    "trigueros",
    "bruno",
    "suarez",
    "soldado",
    "bakambu",
    "adri.n",
    "pina",
    "baptistao"
]

def get_player_name(player):
    if player == "adri.n":
        return "adrián"
    elif player in players:
        return player
    return ""
