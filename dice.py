import random

def roll_dice(n=5):
    return [random.randint(1,6) for _ in range(n)]

def reroll_dice(dice, indexes):
    result = dice.copy()
    
    for i in indexes:
        if 0 <= i < len(result):
            result[i] = random.randint(1,6)
            
    return result