from collections import Counter
import copy

small_straight = [
    [1,2,3,4],
    [2,3,4,5],
    [3,4,5,6]
]

large_straight = [
    [1,2,3,4,5],
    [2,3,4,5,6]
]

categories = {
        "main" : {
            "choice" : 0,
            "4 of a kind" : 0,
            "full house" : 0,
            "s.straight" : 0,
            "l.straight" : 0,
            "yacht" : 0
        },
        "sub" : {
            "aces" : 0,
            "deuces" : 0,
            "threes" : 0,
            "fours" : 0,
            "fives" : 0,
            "sixes" : 0
        },
        "bonus" : 0,
        "sub total" : 0,
        "total" : 0
    }

def sum_sub(dice, n):
    return sum(x for x in dice if x == n)

def scoring(dice, name, category=None):
    counts = Counter(dice)
    
    if category is None:
        result = copy.deepcopy(categories)
    else:    
        result = category
    
    if name[0] == "main":
        if name[1] == "choice":
           result['main']['choice'] = sum(dice)
           
        elif name[1] == "4 of a kind":
           if 4 in counts.values():
               result['main']['4 of a kind'] = sum(dice)
           elif 5 in counts.values():
               result['main']['4 of a kind'] = sum(dice)
           else:
               result['main']['4 of a kind'] = 0
        
        elif name[1] == "full house":
            if sorted(counts.values()) == [2, 3]:
                result['main']['full house'] = sum(dice)
            else:
                result['main']['full house'] = 0
                
        elif name[1] == "s.straight":
            sorted_dice = sorted(set(dice))
            
            for straight in small_straight:
                if all(n in sorted_dice for n in straight):
                    result['main']['s.straight'] = 15
                    break
            else:
                result['main']['s.straight'] = 0
                
        elif name[1] == "l.straight":
            sorted_dice = sorted(set(dice))
            if sorted_dice in large_straight:
                result['main']['l.straight'] = 30
            else:
                result['main']['l.straight'] = 0
        
        elif name[1] == "yacht":
            if 5 in counts.values():
                result['main']['yacht'] = 50
            else:
                result['main']['yacht'] = 0
        
        else:
            return None

    else: # sub
        if name[1] == "aces":
            result['sub']['aces'] = sum_sub(dice, 1)
        elif name[1] == "deuces":
            result['sub']['deuces'] = sum_sub(dice, 2)
        elif name[1] == "threes":
            result['sub']['threes'] = sum_sub(dice, 3)
        elif name[1] == "fours":
            result['sub']['fours'] = sum_sub(dice, 4) 
        elif name[1] == "fives":
            result['sub']['fives'] = sum_sub(dice, 5) 
        elif name[1] == "sixes":
            result['sub']['sixes'] = sum_sub(dice, 6) 
        else:
            return None
        
    if sum(result['sub'].values()) >= 63:
        result['bonus'] = 35
        
    result['sub total'] = sum(result['sub'].values())
    result['total'] = sum(result['sub'].values()) + sum(result['main'].values()) + result['bonus']
        
    return result