from dice import roll_dice, reroll_dice
from scoring import scoring, categories
from boss import boss_list
from player import player, score_plus
import copy, random

def print_available(main_key, sub_key):
    print("\n=== Available Categories ===")
    print(f"main: {main_key}")
    print(f"sub: {sub_key}")
    
def play_stage(stage_num, target_score, is_boss=False):
    count = 0
    total_score = 0
    reroll_num = 2
    blocker = False
    
    main_key = list(categories['main'].keys())
    sub_key = list(categories['sub'].keys())
    
    score_board = copy.deepcopy(categories)
    
    print(f"\n===== Stage {stage_num} =====")
    print(f"\nTarget Score: {target_score}")
    
    if is_boss:
        print("\n*** Boss Stage ***")
        stage_boss = random.choice(list(boss_list.keys()))
            
        if stage_boss == "The Roller":
            reroll_num = 1
            print(boss_list[stage_boss]['description'])
                
        elif stage_boss == "The Blocker":
            blocker = True
            print(boss_list[stage_boss]['description'])
            
    while count < 12:
        dice = roll_dice()
        print(f"\n{count+1}/12  Roll: {dice}")
        
        for _ in range(reroll_num):
            choice = input("Reroll indexes or press Enter to keep: ").strip()
            if not choice:
                break
            
            indexes = list(map(int, choice.split()))
            dice = reroll_dice(dice, indexes)
            print("New Roll: ", dice)
            
        print_available(main_key, sub_key)
        
        group = input("Choose group (main/sub): ").strip()
        if group not in ["main", "sub"]:
            print("Invalid group!")
            continue
        
        name = input("Choose category name: ").strip()
        
        target_list = main_key if group == "main" else sub_key
        if name not in target_list:
            print("Invalid or already used category!")
            continue
        
        if blocker:
            for i in range(len(dice)):
                if (dice[i] % 2) != 0:
                    dice[i] = 0
        
        score_board = scoring(dice, [group, name], score_board)
                    
        gained = score_board[group][name] * score_plus(name)
        target_list.remove(name)
        
        total_score += gained
        count += 1
        
        print(f"\nYou gained {gained} points.")
        print(f"Total: {total_score}/{target_score}")
        
        if total_score >= target_score:
            print("\nStage Clear!")
            return True
    else:
        print("\nStage Fail!")
        return False
    
def run_game():
    print("=== YACHT ROGUELIKE === ")
    
    round_num = 1
    growing_target_score = 0
    
    while True:
        print(f"\n##### Round {round_num} #####")
        
        if not play_stage(1, target_score=15 + growing_target_score):
            print("\nGame Over")
            return
        
        if not play_stage(2, target_score=20 + growing_target_score):
            print("\nGame Over")
            return
        
        if not play_stage(3, target_score=30 + growing_target_score, is_boss=True):
            print("\nThe boss defeated you")
            return
        
        print("\nRound Clear!")
        round_num += 1
        growing_target_score += player['level'] * 10
        
        while True:
            try:
                level_up = input("Please enter the category you want level up in").strip()
                if level_up not in list(player.keys()):
                    raise ValueError
                
                player[level_up] += 1
                print(f"The {level_up} has been leveled up")
                break
            except ValueError:
                print("Invalid category!")
        
if __name__ == "__main__":
    run_game()