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
    boss_flags = {
        "blocker": False, "glitch": False, "taxman": False, "fog": False, "gambler": False, "mirror": False,
        "shuffler": False
    }
    
    main_key = list(categories['main'].keys())
    sub_key = list(categories['sub'].keys())
    
    score_board = copy.deepcopy(categories)
    
    print(f"\n===== Stage {stage_num} =====")
    print(f"\nTarget Score: {target_score}")
    
    if is_boss:
        print("\n*** Boss Stage ***")
        stage_boss = random.choice(list(boss_list.keys()))
        print(f"Stage Boss: {stage_boss}\n")
        print(boss_list[stage_boss]['description'])
        
        boss_key = stage_boss.replace("The ", "").lower()
        if boss_key in boss_flags:
            boss_flags[boss_key] = True
            
        if stage_boss == "The Roller":
            reroll_num = 1
            target_score *= boss_list[stage_boss]['target_score_mod']
            
    while count < 12:
        dice = roll_dice()
        if boss_flags['glitch']:
            for i in range(len(dice)):
                if dice[i] == 6:
                    dice[i] = 1
                    print("Boss changed one of number 6 to 1!")
                    break
                
        if boss_flags['fog']:
            fog_indices = random.sample(range(5), 2)
            display_dice = list(dice)
            for i in fog_indices:
                display_dice[i] = "?"
            print(f"\n{count+1}/12 Roll: {display_dice}")
        else:
            print(f"\n{count+1}/12  Roll: {dice}")
        
        for _ in range(reroll_num):
            choice = input("Reroll indexes or press Enter to keep: ").strip()
            if not choice: break
            
            indexes = list(map(int, choice.split()))
            dice = reroll_dice(dice, indexes)
            
            if boss_flags['glitch']:
                for i in range(len(dice)):
                    if dice[i] == 6:
                        dice[i] = 1
                        print("Boss changed one of number 6 to 1!")
                        break
                
            current_display = list(dice)
            if boss_flags['fog']:
                for i in fog_indices: current_display[i] = "?"
                print("New Roll: ", current_display)
            else:
                print("New Roll: ", dice)
        
        if boss_flags['shuffler']:
            temp_main = copy.deepcopy(main_key)
            if temp_main:
                banned_index = random.randint(0, len(temp_main)-1)
                temp_main[banned_index] += "(Banned)"
            print_available(temp_main, sub_key)
        else: 
            print_available(main_key, sub_key)
        
        while True:
            try:
                group = input("Choose group (main/sub): ").strip()
                if group not in ["main", "sub"]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid group!")
                
        while True:
            try:    
                name = input("Choose category name: ").strip()
                
                if boss_flags['shuffler']:
                    if any(name in item and "(Banned)" in item for item in temp_main):
                        print("That category is BANNED by the boss!")
                        continue
    
                target_list = main_key if group == "main" else sub_key
                if name not in target_list:
                    raise ValueError
                break
            except ValueError:
                    print("Invalid or already used category!")
                    
        if boss_flags['blocker']:
            for i in range(len(dice)):
                if dice[i] in boss_list[stage_boss]['restricted_dice']:
                    dice[i] = 0
        
        score_board = scoring(dice, [group, name], score_board)
                    
        gained = int(round(score_board[group][name] * score_plus(name), 1) * 10)
        if boss_flags['taxman']:
            gained = int(gained * (1-boss_list[stage_boss]['tax_rate']))
            print("Boss deducted your final score!")
            
        elif boss_flags['gambler']:
            if gained < 80:
                gained = 0
                score_board[group][name] = 0
                print("Boss deleted your score!")
                
        elif boss_flags['mirror']:
            if (sum(dice) % 2) != 0:
                gained = int(gained / 2)
                print("Boss halved your final score!")
        
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
        
        if not play_stage(1, target_score=300 + growing_target_score):
            print("\nGame Over")
            return
        
        if not play_stage(2, target_score=400 + growing_target_score):
            print("\nGame Over")
            return
        
        if not play_stage(3, target_score=500 + growing_target_score, is_boss=True):
            print("\nThe boss defeated you")
            return
        
        print("\nRound Clear!")
        round_num += 1
        
        if round_num == 6:
            print("\n===== GAME CLEAR =====")
            break
        
        growing_target_score += player['level'] * 130
        
        upgrade_pool = [k for k in player.keys() if k != 'level']
        options = random.sample(upgrade_pool, 3)
        print(f"\n Choose your reward: {options}")
        while True:
            try:
                level_up = input("Selection: ").strip()
                if level_up not in options:
                    raise ValueError
                    
                player[level_up] += 1
                print(f"The {level_up} has been leveled up")
                print(f"\n[Current Status] {player}")
                break
            except ValueError:
                print("Please choose one for the options!")
                print(f"\n[Current Status] {player}")
                
        if random.random() <= 0.2:
            while True:
                try:
                    level_up = input("Please enter the category you want level up in: ").strip()
                    if level_up not in list(player.keys()):
                        raise ValueError
                    
                    player[level_up] += 1
                    print(f"The {level_up} has been leveled up")
                    break
                except ValueError:
                    print("Invalid category!")
        
if __name__ == "__main__":
    run_game()