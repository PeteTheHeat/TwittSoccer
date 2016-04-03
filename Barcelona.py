# coding=utf-8

players = [
    "bravo",
    "roberto",
    "piqu.",
    "mascherano",
    "alba",
    "rakitic",
    "busquets",
    "arda",
    "messi",
    "su.rez",
    "neymar",
    "mathieu",
    "alves"
]

def get_player_name(player):
    if player == "piqu.":
        return "piqué"
    if player == "su.rez":
        return "suárez"
    elif player in players:
        return player
    return ""
