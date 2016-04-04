# coding=utf-8

players = [
    "guzan", 
    "hutton", 
    "richards", 
    "lescott", 
    "cissokho", 
    "s.nchez", 
    "westwood",
    "gueye",
    "carles|gil", 
    "gestede", 
    "jordan|ayew",
    "grealish",
    "bacuna",
    "lyden",
]

def get_player_name(player):
    if player == "s.nchez":
        return "sànchez"
    if player == "carles|gil":
        return "Carles Gil"
    if player == "jordan|ayew":
        return "Jordan Ayew"
    return player
