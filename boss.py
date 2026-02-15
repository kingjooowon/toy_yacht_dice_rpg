boss_list = {
    "The Roller": {
        "description": "Limit rerolls to 1",
        "reroll_limit": 1,
        "target_score_mod": 1.2
    },
    "The Blocker": {
        "description": "Odd-number dice do not count toward the score",
        "restricted_dice": [1, 3 ,5]
    },
    "The Glitch": {
        "description": "Each time you roll the dice, force one die that rolls a 6 to change to a 1",
        "changed_dice": [6, 1]
    },
    "The Taxman": {
        "descriptions": "After Calculating all the category scores, 15% is deducted from the final score",
        "tax_rate": 0.15
    },
    "The Fog": {
        "description": "After the first roll, two of the five dice will have their markings covered by ?'s and will not be visible during the stage",
    },
    "The Gambler" : {
        "description": "If you gained a final score of less than 80, it will always be treated as 0 points",
        "cut_score": 20
    },
    "The Mirror": {
        "description": "If the sum of the dice numbers is odd, the points earned for that turn are halved"
    },
    "The Shuffler": {
        "description": "Each turn, make a random one of the main categories unselectable for this turn only"
    }
}