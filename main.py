"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

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

def get_integer_input(prompt, min_val, max_val=None):
    """Generic integer input validation function."""
    while True:
        try:
            value = input(prompt).strip()
            num = int(value)
            if max_val is not None and (num < min_val or num > max_val):
                print(f"Please enter a number between {min_val} and {max_val}.")
                continue
            elif num < min_val:
                print(f"Please enter a number greater than or equal to {min_val}.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def get_valid_input(prompt, valid_options):
    """Generic input validation function."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            if choice.isdigit():
                return int(choice)
            return choice
        print(f"Invalid input. Please choose from: {', '.join(map(str, valid_options))}")
                   
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
    print("\n--- Main Menu ---")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    return get_integer_input("Enter choice (1-3): ", 1, 3)

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    global current_character, game_running
    
    name = input("Enter your character's name: ").strip()
    
    if not name:
        print("Character name cannot be empty. Returning to main menu.")
        return

    print("\nAvailable Classes:")
    print(f"{', '.join(character_manager.VALID_CLASSES)}")
    
    # Get and validate class selection
    char_class = get_valid_input("Enter your chosen class: ", character_manager.VALID_CLASSES)

    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"\nWelcome, {current_character['name']} the {current_character['class']}!")
        print("Starting your adventure...")
        
        # Save game immediately after creation
        save_game()
        
        game_loop()
        
    except InvalidCharacterClassError as e:
        print(f"\nError creating character: {e}")
        print("Please try again.")
    except OSError as e:
        print(f"\nFATAL: Could not save the new game. {e}")

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
    global current_character, game_running
    
    saved_games = character_manager.list_saved_characters()
    
    if not saved_games:
        print("\nNo saved games found.")
        return
        
    print("\n--- Saved Games ---")
    for i, name in enumerate(saved_games, 1):
        print(f"{i}. {name}")
    
    choice = get_integer_input("Enter the number of the game to load (or 0 to cancel): ", 0, len(saved_games))
    
    if choice == 0:
        return
        
    char_name = saved_games[choice - 1]
    
    try:
        current_character = character_manager.load_character(char_name)
        print(f"\nLoaded game for {current_character['name']} the {current_character['class']} (Level {current_character['level']}).")
        game_loop()
        
    except CharacterNotFoundError as e:
        print(f"\nError: {e}")
    except SaveFileCorruptedError as e:
        print(f"\nError: The save file for '{char_name}' is corrupted or unreadable: {e}")
    except InvalidSaveDataError as e:
        print(f"\nError: The save file for '{char_name}' contains invalid data: {e}")

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
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        
        # Check for death first
        if character_manager.is_character_dead(current_character):
            handle_character_death()
            if not game_running: # If the player chose to quit after death
                continue

        choice = game_menu()
        
        try:
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
                print("\nSaving game...")
                save_game()
                game_running = False
                
            # Auto-save after every action (except quit, which saves above)
            if game_running:
                 save_game()
                 
        except Exception as e:
            # Catch unexpected errors during game actions
            print(f"\n[CRITICAL GAME ERROR] An unexpected error occurred: {e}")
            # Do not quit the game, allow the user to save/quit gracefully

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
    print(f"\n--- {current_character['name']} (Lvl {current_character['level']}) ---")
    print(f"HP: {current_character['health']}/{current_character['max_health']} | Gold: {current_character['gold']} | XP: {current_character['experience']}")
    print("-------------------------")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battle)")
    print("5. Shop")
    print("6. Save and Quit")
    
    return get_integer_input("Enter choice (1-6): ", 1, 6)

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    print("\n--- Character Details ---")
    print(f"Name: {current_character['name']} (The {current_character['class']})")
    print(f"Level: {current_character['level']}")
    print(f"XP: {current_character['experience']}")
    print(f"Gold: {current_character['gold']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")
    
    # Display Equipment (Requires new character keys from inventory_system logic)
    weapon_id = current_character.get('equipped_weapon')
    armor_id = current_character.get('equipped_armor')
    
    weapon_name = all_items.get(weapon_id, {}).get('name', 'None')
    armor_name = all_items.get(armor_id, {}).get('name', 'None')
    
    print("\n-- Equipment --")
    print(f"Weapon: {weapon_name}")
    print(f"Armor: {armor_name}")

    # Show quest progress using quest_handler
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    pass

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
    inventory_system.display_inventory(current_character, all_items)

    print("\n--- Inventory Actions ---")
    print("1. Use Consumable")
    print("2. Equip Item")
    print("3. Back")
    
    action_choice = get_valid_input("Enter choice (1-3): ", ['1', '2', '3'])
    if action_choice == 3:
        return
        
    item_id = input("Enter item ID (e.g., 'potion', 'sword'): ").strip().lower()
    item_data = all_items.get(item_id)
    
    if not item_data:
        print(f"Error: Item ID '{item_id}' not recognized.")
        return

    try:
        if action_choice == 1:
            # Use Consumable
            result = inventory_system.use_item(current_character, item_id, item_data)
            print(f"\n[INVENTORY] {result}")
        elif action_choice == 2:
            # Equip Weapon/Armor
            if item_data['type'] in ['weapon', 'armor']:
                result = inventory_system.equip_item(current_character, item_id, item_data)
                print(f"\n[INVENTORY] {result}")
            else:
                print(f"Cannot equip item of type '{item_data['type']}'.")

    except ItemNotFoundError as e:
        print(f"\n[INVENTORY ERROR] {e}")
    except InvalidItemTypeError as e:
        print(f"\n[INVENTORY ERROR] {e}")
    except InventoryFullError as e:
        print(f"\n[INVENTORY ERROR] {e} (Cannot unequip old item)")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("\n... Exploring the wilderness ...")
    
    if not character_manager.can_character_fight(current_character):
        print(f"{current_character['name']} is too injured to fight!")
        return
        
    try:
        # Generate random enemy
        enemy = combat_system.get_random_enemy_for_level(current_character['level'])
        
        # Start combat
        battle = combat_system.SimpleBattle(current_character, enemy)
        results = battle.start_battle()
        
        # Process results
        if results['winner'] == 'player':
            # Grant rewards
            character_manager.gain_experience(current_character, results['xp_gained'])
            character_manager.add_gold(current_character, results['gold_gained'])
            # Note: This is where you'd check for quest completion condition (e.g., kill X goblins)
            print(f"\n[COMBAT] You won! Gained {results['xp_gained']} XP and {results['gold_gained']} Gold.")
            
        elif results['winner'] == 'enemy':
            print("\n[COMBAT] You were defeated! Returning to safety...")
            
    except CharacterDeadError as e:
        print(f"\n[COMBAT ERROR] {e}")
    except InvalidTargetError as e:
        print(f"\n[COMBAT ERROR] {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    print("\n--- The General Store ---")
    print(f"Your Gold: {current_character['gold']}")
    print("-------------------------")
    
    # Display available items (all items for simplicity)
    print("\nAvailable Items:")
    for item_id, data in all_items.items():
        print(f"  {item_id:<15} - {data['name']} ({data['type']}) | Cost: {data['cost']} | Effect: {data['effect']}")
        
    print("\n--- Shop Actions ---")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")
    
    choice = get_valid_input("Enter choice (1-3): ", ['1', '2', '3'])
    if choice == 3:
        return

    item_id = input("Enter Item ID: ").strip().lower()
    item_data = all_items.get(item_id)
    
    if not item_data:
        print(f"Item ID '{item_id}' not found in shop database.")
        return

    try:
        if choice == 1:
            # Buy Item
            inventory_system.purchase_item(current_character, item_id, item_data)
            print(f"\n[SHOP] Purchased {item_data['name']} for {item_data['cost']} gold. Gold remaining: {current_character['gold']}")
        elif choice == 2:
            # Sell Item
            sell_price = inventory_system.sell_item(current_character, item_id, item_data)
            print(f"\n[SHOP] Sold {item_data['name']} for {sell_price} gold. Gold total: {current_character['gold']}")
            
    except InsufficientResourcesError as e:
        print(f"\n[SHOP ERROR] {e}")
    except InventoryFullError as e:
        print(f"\n[SHOP ERROR] {e}")
    except ItemNotFoundError as e:
        print(f"\n[SHOP ERROR] {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
        print(f"Game saved for {current_character['name']}.")
    except OSError as e:
        print(f"\n[SAVE ERROR] Failed to save game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    global all_quests, all_items
    
    # Try to load quest data
    all_quests = game_data.load_quests()
    
    # Try to load item data
    all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    global current_character, game_running
    
    print("=" * 30)
    print(f"!!! {current_character['name']} HAS FALLEN !!!")
    print("=" * 30)

    revive_cost = current_character['level'] * 50
    print(f"You must be revived to continue. Revival costs {revive_cost} gold.")
    
    print("\n1. Pay to Revive")
    print("2. Quit Game (Character remains dead)")
    
    choice = get_integer_input("Enter choice (1-2): ", 1, 2)
    
    if choice == 1:
        if current_character['gold'] >= revive_cost:
            try:
                character_manager.add_gold(current_character, -revive_cost)
                character_manager.revive_character(current_character)
                print(f"\nRevived! You paid {revive_cost} gold and are back to life with half health.")
            except ValueError as e:
                # Should not happen if check is done, but safe guard
                print(f"Error during revival cost: {e}")
            except Exception:
                print("An error occurred during revival. Returning to main menu.")
        else:
            print(f"You only have {current_character['gold']} gold. Not enough to revive. You must quit.")
            game_running = False
            
    elif choice == 2:
        game_running = False
        print("Your adventure ends here. Quitting game.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

