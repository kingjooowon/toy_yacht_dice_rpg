player = {
    "level": 1,
    "aces": 1,
    "deuces": 1,
    "threes": 1,
    "fours": 1,
    "fives": 1,
    "sixes": 1,
    "choice": 1,
    "4 of a kind": 1,
    "full house": 1,
    "s.straight": 1,
    "l.straight": 1,
    "yacht": 1
}

def score_plus(name):
    if name not in list(player.keys()):
        return False
    
    result = 1 + ((player[name] - 1) * 0.2)
    return result