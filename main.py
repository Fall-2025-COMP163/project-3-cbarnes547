"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Chloe Barnes

AI Usage: AI was used to make Readme, help make variable names, and make comments.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *
import os

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================
                   
def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input("Enter choice (1-3): ").strip()
    while choice not in ["1", "2", "3"]:
        print("Invalid choice.")
        choice = input("Enter choice (1-3): ").strip()

    return int(choice)


def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

    load_game_data()

    print("\n=== NEW GAME ===")
    name = input("Enter your character name: ").strip()

    print("\nChoose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Enter choice (1-4): ").strip()
    while class_choice not in ["1", "2", "3", "4"]:
        print("Invalid choice.")
        class_choice = input("Enter choice (1-4): ").strip()

    class_map = {
        "1": "Warrior",
        "2": "Mage",
        "3": "Rogue",
        "4": "Cleric"
    }

    char_class = class_map[class_choice]

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
    except InvalidCharacterClassError:
        print("Invalid class.")
        return

    game_loop()


def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    load_game_data()

    print("\n=== LOAD GAME ===")
    saved_chars = character_manager.list_saved_characters()

    if len(saved_chars) == 0:
        print("No saved characters found.")
        return

    for i, name in enumerate(saved_chars, 1):
        print(f"{i}. {name}")

    choice = input("Pick a character number: ").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(saved_chars):
        print("Invalid choice.")
        choice = input("Pick a character number: ").strip()

    char_name = saved_chars[int(choice) - 1]

    try:
        current_character = character_manager.load_character(char_name)
    except (CharacterNotFoundError, SaveFileCorruptedError, InvalidSaveDataError):
        print("Error loading save.")
        return

    game_loop()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Goodbye.")
            game_running = False


def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Enter choice (1-6): ").strip()
    while choice not in ["1", "2", "3", "4", "5", "6"]:
        print("Invalid choice.")
        choice = input("Enter choice (1-6): ").strip()

    return int(choice)

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    c = current_character

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c['name']}")
    print(f"Class: {c['class']}")
    print(f"Level: {c['level']}")
    print(f"Health: {c['health']}/{c['max_health']}")
    print(f"Strength: {c['strength']}")
    print(f"Magic: {c['magic']}")
    print(f"Gold: {c['gold']}")
    print(f"XP: {c['experience']}")
    print(f"Active Quests: {len(c['active_quests'])}")
    print(f"Completed Quests: {len(c['completed_quests'])}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

    print("\nOptions:")
    print("1. Use an item")
    print("2. Drop an item")
    print("3. Equip weapon")
    print("4. Equip armor")
    print("5. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.use_item(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "3":
        item_id = input("Enter weapon_id: ").strip()
        try:
            inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "4":
        item_id = input("Enter armor_id: ").strip()
        try:
            inventory_system.equip_armor(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest")
    print("7. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        active = quest_handler.get_active_quests(current_character, all_quests)
        for q in active:
            quest_handler.display_quest_info(q)

    elif choice == "2":
        available = quest_handler.get_available_quests(current_character, all_quests)
        for q in available:
            quest_handler.display_quest_list([q])

    elif choice == "3":
        completed = quest_handler.get_completed_quests(current_character, all_quests)
        for q in completed:
            quest_handler.display_quest_info(q)

    elif choice == "4":
        qid = input("Enter quest_id: ").strip()
        try:
            quest_handler.accept_quest(current_character, qid, all_quests)
            print("Quest accepted.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "5":
        qid = input("Enter quest_id: ").strip()
        try:
            quest_handler.abandon_quest(current_character, qid)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "6":
        qid = input("Enter quest_id: ").strip()
        try:
            rewards = quest_handler.complete_quest(current_character, qid, all_quests)
            print("Quest completed.")
            print(f"XP: {rewards['xp']}")
            print(f"Gold: {rewards['gold']}")
        except Exception as e:
            print(f"Error: {e}")


def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("\n... Exploring the wilderness ...")
    
    enemy = combat_system.get_random_enemy_for_level(current_character["level"])
    print(f"A wild {enemy['name']} appears.")

    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()
        print(f"Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
    except CharacterDeadError:
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    print("\n--- The General Store ---")
    print(f"You have {current_character['gold']} gold.\n")

    for item_id, data in all_items.items():
        print(f"{item_id}: {data['name']} - {data['cost']} gold")

    print("\nOptions:")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            print("Purchase successful.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
        item_id = input("Enter item_id: ").strip()
        try:
            gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
            print(f"Sold for {gold} gold.")
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    if current_character is None:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception:
        print("Error saving game.")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        all_quests = game_data.load_quests("data/quests.txt")
        all_items = game_data.load_items("data/items.txt")
    except MissingDataFileError:
        game_data.create_default_data_files()
        all_quests = game_data.load_quests("data/quests.txt")
        all_items = game_data.load_items("data/items.txt")
    except InvalidDataFormatError:
        all_quests = {}
        all_items = {}

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\nYou died.")
    print("1. Revive for 25 gold")
    print("2. Quit")

    choice = input("Choose: ").strip()
    while choice not in ["1", "2"]:
        choice = input("Choose: ").strip()

    if choice == "1":
        if current_character["gold"] < 25:
            print("Not enough gold. Game over.")
            game_running = False
            return

        current_character["gold"] -= 25
        character_manager.revive_character(current_character)
        print("Revived.")
    else:
        print("Goodbye.")
        game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("QUEST CHRONICLES")
    print("=" * 50)
    print("Welcome to Quest Chronicles.\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    load_game_data()

    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Thanks for playing.")
            break

if __name__ == "__main__":
    main()

