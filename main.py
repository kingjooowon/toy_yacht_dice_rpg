from dice import roll_dice, reroll_dice
from scoring import scoring, categories
import copy

def print_available(group="", name="", first=True):
    if first:
        main_key = list(categories['main'].keys())
        sub_key = list(categories['sub'].keys())
        first = False
        print("=== Available Categories ===")
        print(f"main: {main_key} / sub: {sub_key}")
        return
    
    if group == 'main':
        main_key = main_key.removed(name)
    elif group == 'sub':
        sub_key = sub_key.removed(name)
    
    print("=== Available Categories ===")
    print(f"main: {main_key} / sub: {sub_key}")
    return
    
def play_stage(stage_num, target_score, is_boss=False):
    count = 0
    first = True
    
    while count < 12:
        
        print(f"\n===== Stage {stage_num} =====")
        if is_boss:
            print("*** Boss Stage ***")
        print(f"\nTarget Score: {target_score}")
        
        score_board = copy.deepcopy(categories)
        total_score = 0
        
        dice = roll_dice()
        print("Roll: ", dice)
        
        for _ in range(1,3):
            choice = input("Reroll indexes or press Enter to keep: ").strip()
            if not choice:
                break
            
            indexes = list(map(int, choice.split()))
            dice = reroll_dice(dice, indexes)
            print("Roll: ", dice)
            
        if first == True:
            print_available()
        
        full_name = []
        group = input("Choose group (main/sub): ").strip()
        name = input("Choose category name: ").strip()
        full_name.append(group)
        full_name.append(name)
        
        score_board = scoring(dice, full_name, score_board)
        gained = score_board[group][name]
        
        total_score += gained
        
        print(f"\nYou gained {gained} points.")
        print(f"Total Score: {total_score}")
        
        count += 1
        
        if total_score >= target_score:
            break
        
    if total_score >= target_score:
        print("\nStage Clear!")
        return True
    else:
        print("\nStage Fail!")
        return False
    
def run_game():
    print("=== YACHT ROGUELIKE === ")
    
    round_num = 1
    
    while True:
        print(f"\n##### Round {round_num} #####")
        
        if not play_stage(1, target_score=15):
            print("\nGame Over")
            return
        
        if not play_stage(2, target_score=20):
            print("\nGame Over")
            return
        
        if not play_stage(3, target_score=30, is_boss=True):
            print("\nThe boss defeated you")
            return
        
        print("\nRound Clear!")
        round_num += 1
        
if __name__ == "__main__":
    run_game()