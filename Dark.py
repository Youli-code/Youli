import random
import sys

# ---------------------------
# Global game state
# ---------------------------
game_state = {
    "player_health": 100,          # Always 100
    "player_max_health": 100,      # Also 100
    "attack_power": 0,             # User can still choose
    "armor_class": 0,              # User can still choose
    "in_combat": False,

    "dire_wolf_defeated_count": 0,
    "magical_sword_found": False,
    "has_magical_sword": False,
    "elder_quest_accepted": False,

    "inventory": [],

    "bear_defeated": False,

    "chest_key_found": False,
    "chest_opened": False,
    "magic_stone_obtained": False,

    "dragon_defeated": False
}

def reset_game_state():
    """
    Resets our dictionary to original defaults for a fresh restart.
    """
    global game_state
    game_state = {
        "player_health": 100,
        "player_max_health": 100,
        "attack_power": 0,
        "armor_class": 0,
        "in_combat": False,

        "dire_wolf_defeated_count": 0,
        "magical_sword_found": False,
        "has_magical_sword": False,
        "elder_quest_accepted": False,

        "inventory": [],

        "bear_defeated": False,

        "chest_key_found": False,
        "chest_opened": False,
        "magic_stone_obtained": False,

        "dragon_defeated": False
    }

# ---------------------------
# Intro & Restart Logic
# ---------------------------
def game_introduction():
    print("You wake up in a cold, damp cave. The air is thick with the scent of moss and something... foul.")
    print("Shadows dance along the jagged walls as the dim torchlight flickers.")
    print("The last thing you remember is falling into darkness. Now, you must find a way out...")

def setup_player():
    """
    Player's HP is fixed at 100. They still choose Attack Power & Armor Class.
    """
    global game_state
    # HP is fixed:
    game_state["player_health"] = 100
    game_state["player_max_health"] = 100

    # Let them choose Attack Power & AC.
    game_state["attack_power"] = int(input("Enter Attack Power: "))
    ac_input = int(input("Enter Armor Class (Max 20): "))
    game_state["armor_class"] = min(ac_input, 20)

    print("\nDespite feeling a wave of nausea, you finally stumble out of the cave.")
    print("Outside, you spot small animal corpses and a few broken logs scattered about.")
    print("It's clear something—or someone—must have carried them here...")

def game_over():
    """
    Called when player's health <= 0. Instead of closing,
    restarts the entire game from scratch.
    """
    print("\nYour vision fades as you succumb to your wounds...")
    print("The world slips away into darkness.")

    input("\nPress ENTER to restart the game.")
    reset_game_state()  # Reset everything
    main()              # Start fresh

# ---------------------------
# Inventory & Input Helpers
# ---------------------------
def show_inventory():
    inv = game_state["inventory"]
    if not inv:
        print("\nYour inventory is currently empty.")
    else:
        print("\nYour Inventory contains:")
        for item in inv:
            print(f" - {item}")

def open_inventory_menu(current_menu_func):
    show_inventory()
    current_menu_func()

def get_player_choice(prompt, valid_options, retry_function):
    choice = input(prompt)
    if choice in valid_options:
        return choice
    print("Invalid choice.")
    retry_function()
    return None

def get_player_answer(prompt, allowed_responses, retry_func):
    ans = input(prompt)
    if ans.upper() in allowed_responses:
        return ans.upper()
    print("Invalid choice. Please try again.")
    return get_player_answer(prompt, allowed_responses, retry_func)

# ---------------------------
# Main Menus
# ---------------------------
def choose_location():
    if game_state["in_combat"]:
        print("You are in a fight! Leaving now would make you easy prey!")
        return

    print("\nWhere would you like to travel?")
    print("1. The dark and eerie Forest")
    print("2. The distant lights of the Village")
    print("3. Stay put (do nothing for now)")
    print("4. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], choose_location)
    if not choice:
        return

    if choice == "1":
        print("You make your way into the dense, twisted trees of the Forest...")
        forest_options()
    elif choice == "2":
        print("You head toward the Village, hoping to find safety or answers to your predicament...")
        village_options()
    elif choice == "3":
        print("You decide to stay and gather your thoughts for a moment...")
    elif choice == "4":
        open_inventory_menu(choose_location)

def village_options():
    print("\nYou enter the god-forsaken village. The streets are empty, and an eerie silence fills the air.")
    print("1. Speak with the Village Elder")
    print("2. Look around the village")
    print("3. Return to the main location menu")
    print("4. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], village_options)
    if not choice:
        return

    if choice == "1":
        speak_with_elder()
    elif choice == "2":
        print("You wander through the village, witnessing the decay of what was once a thriving town.")
        village_options()
    elif choice == "3":
        choose_location()
    elif choice == "4":
        open_inventory_menu(village_options)

# ---------------------------
# Elder & Sword Logic
# ---------------------------
def speak_with_elder():
    print("\nYou approach the Village Elder, a frail man with eyes that have seen many winters.")

    if not game_state["magical_sword_found"]:
        print('"I once possessed a Magical Sword," he says gravely, "but I lost it two moons ago')
        print('when a pack of ravenous wolves chased me from the forest. If you truly seek')
        print('adventure—and that blade—you must face them. But I won’t force you to do so."')

        ans = get_player_answer("\nWill you accept the quest to recover the Magical Sword? (Y/N): ", ["Y","N"], speak_with_elder)
        if ans == "Y":
            game_state["elder_quest_accepted"] = True
            print("\nElder: \"I thank you, brave one. Return if you learn anything of the sword’s whereabouts.\"")
            print("(QUEST: Find the Magical Sword!)")
        else:
            print("\nElder: \"I understand—these are dark times, and not all are suited for such dangers.\"")
            print("(You declined the quest...)")

    else:
        # We have found the sword by killing 3 wolves, let's see if the player wants to keep it
        if game_state["has_magical_sword"]:
            print('"I see you carry the Magical Sword. You are truly a hero among these humble folk."')
            print("\nElder: \"With that blade in hand, you might just push through the darkest paths of the forest.")
            print("You may well be able to make your way out of here entirely.\"")
        else:
            print('"You have found my Magical Sword!" the Elder exclaims. "My fighting days are long behind me,')
            print('and I have no need for it now. Will you keep it?"')
            ans = get_player_answer("\nKeep the sword? (Y/N): ", ["Y","N"], speak_with_elder)
            if ans == "Y":
                game_state["has_magical_sword"] = True
                game_state["inventory"].append("Magical Sword")
                game_state["attack_power"] += 6
                print("\nElder: \"Then may it serve you well, hero.\"")
                print("You place the gleaming blade at your side, feeling its power course through your veins.")
                print("\nElder: \"With the sword in your hands, you can finally venture deeper into the forest.")
                print("Perhaps you will find a path leading beyond these cursed woods.\"")
            else:
                print("\nElder: \"Very well, I shall keep it safe. Fare thee well on your travels.\"")

    village_options()

# ---------------------------
# Forest Menus
# ---------------------------
def forest_options():
    print("\nYou stand among towering trees and creeping shadows.")
    print("1. Look around the forest")
    print("2. Confront the Dire Wolf")
    print("3. Return to the main location menu")
    print("4. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], forest_options)
    if not choice:
        return

    if choice == "1":
        if game_state["has_magical_sword"]:
            forest_crossroads()
        else:
            print("You explore the forest, discovering broken swords and footprints leading deeper into the woods...")
            forest_options()
    elif choice == "2":
        print("A pair of glowing eyes appear in the darkness—the Dire Wolf emerges, baring its teeth!")
        fight_mode = get_player_answer(
            "\nWould you like an Automatic fight or Manual fight? (A/M): ",
            ["A","M"],
            forest_options
        )
        fight_dire_wolf(fight_mode)
        if game_state["player_health"] > 0:
            forest_options()
    elif choice == "3":
        choose_location()
    elif choice == "4":
        open_inventory_menu(forest_options)

def forest_crossroads():
    print("\nAs you move beyond the familiar forest edge, you come upon a crossroads.")
    print("A chilling wind howls from the mountains, while the trees grow even darker further in.")
    print("Somewhere ahead, you hear the faint sound of running water.")
    print("\nWhich path will you take?")
    print("1. Climb up the dark mountain trail")
    print("2. Press deeper within the darkening trees")
    print("3. Head toward the nearby stream")
    print("4. Open your Inventory (or turn back)")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], forest_crossroads)
    if not choice:
        return

    if choice == "1":
        mountain_path()
    elif choice == "2":
        deeper_forest_path()
    elif choice == "3":
        stream_path()
    elif choice == "4":
        open_inventory_menu(forest_crossroads)

# ---------------------------
# Mountain Path
# ---------------------------
def mountain_path():
    print("\nYou begin a hazardous climb up the mountain trail. Loose rocks tumble beneath your feet.")
    print("Eventually, you reach a plateau of sorts, where a cluster of makeshift houses stands,")
    print("long abandoned. One of them has a chilling message scrawled on the wall:")
    print("\"Forget us, do not look for us. Only pain and suffering ahead.\"")

    print("\n1. Sleep within the houses")
    print("2. Continue further up the mountain")
    print("3. Climb down to the crossroads")
    print("4. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], mountain_path)
    if not choice:
        return

    if choice == "1":
        game_state["player_health"] = game_state["player_max_health"]
        print(f"\nYou rest in the dusty remains of one shelter. Your health is fully restored to {game_state['player_health']} HP!")
        mountain_path()
    elif choice == "2":
        check_ark()
    elif choice == "3":
        print("\nYou decide to climb back down to the crossroads, carefully retracing your steps.")
        forest_crossroads()
    elif choice == "4":
        open_inventory_menu(mountain_path)

def check_ark():
    print("\nClimbing higher, you stumble upon a large, moss-covered ark carved into the mountainside.")
    print("At its top, there's a circular slot where something appears to be missing.")

    if not game_state["magic_stone_obtained"]:
        print("\"We can't use it yet... Something is missing. Perhaps there's a piece that fits here.\"")
        print("You have no choice but to turn back for now.")
        mountain_path()
    else:
        print("\nYou hold the strange stone you found at the lake. It fits perfectly into the ark's slot!")
        print("With a brilliant glow, the ark slides open, revealing a hidden passage leading deeper into the rock.")
        print("You press on, climbing for many hours along a winding path inside the mountain...")
        final_mountain_ascent()

def final_mountain_ascent():
    print("\nAfter countless hours of wandering and walking,")
    print("you finally emerge onto a vast plateau near the mountain's summit.")
    print("The bitter cold stings your skin, and dark clouds swirl overhead...")

    input("\nPress ENTER to continue...")

    print("\nThunder rumbles in the distance, and lightning illuminates a colossal silhouette in the clouds.")
    print("The shape descends, revealing a mighty Dragon, scales shimmering with arcane energy.")
    print("Wind whips across the plateau, carrying the beast's thunderous roar into your very bones.")

    input("\n(Press ENTER to brace yourself for the final battle...)")

    fight_mode = get_player_answer(
        "\nWill you fight the Dragon in Automatic or Manual mode? (A/M): ",
        ["A","M"],
        final_mountain_ascent
    )
    fight_dragon(fight_mode)

    if not game_state["dragon_defeated"]:
        print("\nYour journey ends on the cold mountain peak...")
        return

    # Epilogue describing the epic final battle
    print("\nThe dragon collapses with one final roar, its mighty wings flailing in vain.")
    print("The echoes of your clash reverberate across the mountainside, telling a tale of courage and steel.")
    print("Cracked scales, scorched rock, and your panting breath bear witness to this epic struggle, now ended.")
    print("\nBeyond the mountain peak lies freedom—or perhaps even greater adventures. But for now, victory is yours.")
    print("\nCONGRATULATIONS, HERO! You have prevailed over the dragon and completed this quest.")

    input("\nPress ENTER to exit the game - Thank you for playing!")
    sys.exit(0)  # Quits the program entirely





# Wolf Encounter Logic
# ---------------------------
def fight_dire_wolf(fight_mode):
    """
    This function handles all the Dire Wolf's combat logic, including
    skip-turns if someone rolls a 1, etc.
    """
    game_state["in_combat"] = True

    # Dire Wolf stats
    wolf_health = 30
    wolf_ac = 12
    wolf_attack_power = 8

    # These track if the player or the wolf should skip *their next* turn
    player_skip_turn = False
    wolf_skip_turn = False

    while game_state["player_health"] > 0 and wolf_health > 0:
        # 1) Player's turn
        if player_skip_turn:
            print("\nYou skip your turn due to your previous critical miss!")
            player_skip_turn = False
        else:
            print("\nYour turn!")
            if fight_mode == "M":
                input("Press ENTER to roll the dice...")
            damage, skip_next = calculate_damage_dealt_for_player(game_state["attack_power"], wolf_ac)
            wolf_health -= damage
            print(f"Dire Wolf Health: {wolf_health}")

            # If skip_next is True => The player rolled a 1 => skip next turn
            if skip_next:
                player_skip_turn = True

            # If the wolf's health drops to 0 or below, the fight ends
            if wolf_health <= 0:
                print("You have defeated the Dire Wolf!")
                game_state["dire_wolf_defeated_count"] += 1

                # If it’s the 3rd wolf kill and the Magical Sword isn't found yet, reveal the sword
                if game_state["dire_wolf_defeated_count"] == 3 and not game_state["magical_sword_found"]:
                    print("\nAs the last wolf falls, you spot a shimmering blade hidden among the foliage...")
                    print("Could this be the fabled Magical Sword?")
                    game_state["magical_sword_found"] = True

                game_state["in_combat"] = False
                return

        # 2) Wolf's turn
        if wolf_skip_turn:
            print("\nThe Dire Wolf snarls in frustration but must skip its turn due to a critical miss!")
            wolf_skip_turn = False
        else:
            print("\nDire Wolf's turn!")
            damage, skip_next = calculate_damage_dealt_for_player(wolf_attack_power, game_state["armor_class"])
            game_state["player_health"] -= damage
            print(f"Your Health: {game_state['player_health']}")

            # If skip_next is True => The wolf rolled a 1 => skip next turn
            if skip_next:
                wolf_skip_turn = True

            # If the player's health drops to 0 or below, the fight ends
            if game_state["player_health"] <= 0:
                print("The Dire Wolf overpowers you. The forest grows silent once more...")
                game_state["in_combat"] = False
                return

    # Exiting the loop => either side might be dead or we broke out
    game_state["in_combat"] = False






# ---------------------------
# Dragon Fight
# ---------------------------
def fight_dragon(fight_mode):
    game_state["in_combat"] = True

    dragon_health = 100
    dragon_ac = 15
    dragon_attack_power = 18

    player_skip_turn = False
    dragon_skip_turn = False

    while game_state["player_health"] > 0 and dragon_health > 0:
        # Player's turn
        if player_skip_turn:
            print("\nYou skip your turn due to your previous critical miss!")
            player_skip_turn = False
        else:
            print("\nYour turn! Face the Dragon!")
            if fight_mode == "M":
                input("Press ENTER to roll the dice...")
            damage, skip_next = calculate_damage_dealt_for_player(game_state["attack_power"], dragon_ac)
            dragon_health -= damage
            print(f"Dragon's Health: {dragon_health}")

            if skip_next:
                player_skip_turn = True

            if dragon_health <= 0:
                print("The Dragon emits a final ear-splitting roar before collapsing!")
                game_state["dragon_defeated"] = True
                game_state["in_combat"] = False
                return

        # Dragon's turn
        if dragon_skip_turn:
            print("\nThe Dragon bellows in rage but must skip its turn due to a critical miss!")
            dragon_skip_turn = False
        else:
            print("\nDragon's turn!")
            damage, skip_next = calculate_damage_dealt_for_player(dragon_attack_power, game_state["armor_class"])
            game_state["player_health"] -= damage
            print(f"Your Health: {game_state['player_health']}")

            if skip_next:
                dragon_skip_turn = True

            if game_state["player_health"] <= 0:
                print("The Dragon overpowers you, and you fall to the frozen stones below...")
                game_state["in_combat"] = False
                game_over()  # Restarts the game
                return

    game_state["in_combat"] = False

# ---------------------------
# Darkening Trees - Grizzly Bear Encounter
# ---------------------------
def deeper_forest_path():
    if not game_state["bear_defeated"]:
        print("\nYou step further into the gloom. The branches twist overhead, forming a dense canopy.")
        print("Suddenly, a massive shape lumbers out from behind a gnarled tree—a Grizzly Bear!")
        fight_mode = get_player_answer(
            "\nWould you like an Automatic fight or Manual fight? (A/M): ",
            ["A","M"],
            deeper_forest_path
        )
        fight_grizzly_bear(fight_mode)

        if game_state["player_health"] > 0:
            print("\nThe Grizzly Bear lies defeated. Its fur could be valuable.")
            print("1. Skin the bear (increase AC by 2)")
            print("2. Leave it be and push further into the woods")

            choice = get_player_choice("Enter 1 or 2: ", ["1","2"], deeper_forest_path)
            if choice == "1":
                game_state["armor_class"] += 2
                print(f"\nYou skin the bear and claim its thick fur. Your Armor Class is now {game_state['armor_class']}!")
                deeper_forest_dead_end()
            else:
                print("\nYou decide to leave the bear as it is.")
                deeper_forest_dead_end()

            game_state["bear_defeated"] = True
    else:
        print("\nRecalling your battle with the Grizzly Bear, you venture further into the shadows once more...")
        deeper_forest_dead_end()

def deeper_forest_dead_end():
    print("\nYou press deeper into the woods, stepping over tangled roots and ducking beneath low branches.")
    print("Soon, you come face-to-face with a vast ravine cutting through the forest floor.")
    print("Its depth is hidden by darkness, and there's no bridge or fallen log to help you cross...")
    print("\nWith no way to continue, you reluctantly turn back to the crossroads.")
    forest_crossroads()

def fight_grizzly_bear(fight_mode):
    game_state["in_combat"] = True

    bear_health = 50
    bear_ac = 13
    bear_attack_power = 15

    player_skip_turn = False
    bear_skip_turn = False

    while game_state["player_health"] > 0 and bear_health > 0:
        # Player's turn
        if player_skip_turn:
            print("\nYou skip your turn due to your previous critical miss!")
            player_skip_turn = False
        else:
            print("\nYour turn against the Grizzly Bear!")
            if fight_mode == "M":
                input("Press ENTER to roll the dice...")
            damage, skip_next = calculate_damage_dealt_for_player(game_state["attack_power"], bear_ac)
            bear_health -= damage
            print(f"Grizzly Bear's Health: {bear_health}")

            if skip_next:
                player_skip_turn = True

            if bear_health <= 0:
                print("With a mighty blow, you have defeated the Grizzly Bear!")
                game_state["in_combat"] = False
                return

        # Bear's turn
        if bear_skip_turn:
            print("\nThe Bear roars in confusion, but must skip its turn due to a critical miss!")
            bear_skip_turn = False
        else:
            print("\nGrizzly Bear's turn!")
            damage, skip_next = calculate_damage_dealt_for_player(bear_attack_power, game_state["armor_class"])
            game_state["player_health"] -= damage
            print(f"Your Health: {game_state['player_health']}")

            if skip_next:
                bear_skip_turn = True

            if game_state["player_health"] <= 0:
                print("The Grizzly Bear overpowers you, and darkness claims your senses...")
                game_state["in_combat"] = False
                game_over()
                return

    game_state["in_combat"] = False

# ---------------------------
# Stream Path & Island
# ---------------------------
def stream_path():
    print("\nYou follow the sound of running water until you reach a small lake shrouded in mist.")
    print("Peering through the fog, you can just make out a tiny patch of land in the middle of the waters.")
    print("But the air is clammy, and an uneasy hush settles here...")

    print("\n1. Swim across the mysterious lake toward the piece of land")
    print("2. Return back to the crossroads")
    print("3. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, or 3: ", ["1","2","3"], stream_path)
    if not choice:
        return

    if choice == "1":
        swim_to_island()
    elif choice == "2":
        print("\nYou decide it's safer to head back. The mist swirls behind you as you leave the lakeshore.")
        forest_crossroads()
    elif choice == "3":
        open_inventory_menu(stream_path)

def swim_to_island():
    print("\nYou wade into the water, the cold mist clinging to your skin.")
    print("With each stroke, the murky depths remain unseen... but eventually you set foot on the island.")
    island_encounter()

def island_encounter():
    print("\nOn this forlorn patch of land, you find two human skeletons among fallen trees.")
    print("A half-buried chest juts from the ground near them.")

    print("\n1. Inspect the bodies")
    print("2. Investigate the chest")
    print("3. Return to the shore")
    print("4. Open your Inventory")

    choice = get_player_choice("Enter 1, 2, 3, or 4: ", ["1","2","3","4"], island_encounter)
    if not choice:
        return

    if choice == "1":
        inspect_bodies()
    elif choice == "2":
        investigate_chest()
    elif choice == "3":
        print("\nYou head back to the shore, diving into the cold water once again.")
        stream_path()
    elif choice == "4":
        open_inventory_menu(island_encounter)

def inspect_bodies():
    if not game_state["chest_key_found"]:
        print("\nYou kneel by the skeletal remains. Their clothes are tattered; time has not been kind.")
        print("Amid the scattered bones, you discover a small, rusted key!")
        game_state["chest_key_found"] = True
        game_state["inventory"].append("Rusted Key")
        print("You slip it into your pocket. Perhaps it will open that chest nearby.")
    else:
        print("\nYou've already searched the bodies. There’s nothing else of value here.")
    island_encounter()

def investigate_chest():
    if game_state["chest_opened"]:
        print("\nYou've already opened the chest. Empty now but for scraps of rotted cloth.")
    else:
        if not game_state["chest_key_found"]:
            print("\nThe chest is locked tight. You need some kind of key to open it.")
        else:
            print("\nUsing the rusted key, you manage to unlock the chest with a loud creak.")
            game_state["chest_opened"] = True
            game_state["inventory"].append("Mysterious Stone")
            game_state["magic_stone_obtained"] = True
            print("Inside, you find a beautiful stone covered in strange engravings and a symbol of the mountain.")
            print("This must be the piece required to open something in the mountains!")
    island_encounter()

# ---------------------------
# Combat Utility
# ---------------------------
def calculate_damage_dealt_for_player(attacker_power, defender_ac):
    """
    Renamed from 'calculate_damagedealt_for_player' to avoid PyCharm's spellcheck alert.
    """
    dice_roll = random.randint(1, 20)
    print(f"Dice Roll: {dice_roll}")

    if dice_roll == 20:
        print("Natural 20! Critical Hit! (Double Damage)")
        return attacker_power * 2, False
    elif dice_roll == 1:
        print("Natural 1! Critical Miss! You skip your next turn.")
        return 0, True
    elif dice_roll >= defender_ac:
        print("Hit!")
        return attacker_power, False
    else:
        print("Missed the attack!")
        return 0, False

# ---------------------------
# Game Start
# ---------------------------
def main():
    game_introduction()
    setup_player()
    choose_location()

if __name__ == "__main__":
    main()
