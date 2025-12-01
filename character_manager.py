"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

CLASS_STATS = {
    "Warrior": {"health": 120, "strength": 15, "magic": 5},
    "Mage": {"health": 80, "strength": 8, "magic": 20},
    "Rogue": {"health": 90, "strength": 12, "magic": 10},
    "Cleric": {"health": 100, "strength": 10, "magic": 15},
}
VALID_CLASSES = list(CLASS_STATS.keys())
SAVE_FILE_EXTENSION = "_save.txt"
SAVE_FIELD_ORDER = [
    "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", 
    "MAGIC", "EXPERIENCE", "GOLD", "INVENTORY", "ACTIVE_QUESTS", 
    "COMPLETED_QUESTS"
]

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    if character_class not in VALID_CLASSES:
        # Step 1: Validate class name and raise custom exception
        raise InvalidCharacterClassError(
            f"Invalid character class: '{character_class}'. Valid classes are: {', '.join(VALID_CLASSES)}"
        )
    
    base_stats = CLASS_STATS[character_class]
    
    # Step 2: Assemble the character dictionary
    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'health': base_stats['health'],
        'max_health': base_stats['health'],
        'strength': base_stats['strength'],
        'magic': base_stats['magic'],
        'experience': 0,
        'gold': 100,
        'inventory': [],  # List of item names
        'active_quests': [],  # List of quest IDs
        'completed_quests': [], # List of quest IDs
    }
    
    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    os.makedirs(save_directory, exist_ok=True)
    
    # Construct the file path
    filename = character['name'] + SAVE_FILE_EXTENSION
    file_path = os.path.join(save_directory, filename)
    
    try:
        with open(file_path, 'w') as f:
            for field in SAVE_FIELD_ORDER:
                key = field.lower() # Keys in the character dict are lowercase
                value = character.get(key)
                
                # Convert lists to comma-separated strings for saving
                if isinstance(value, list):
                    value_str = ",".join(map(str, value))
                else:
                    value_str = str(value)

                # Write in the required NAME: value format
                f.write(f"{field}: {value_str}\n")

    except OSError as e:
        # Re-raise file-system errors for appropriate handling by main.py
        raise OSError(f"Failed to write save file for '{character['name']}': {e}")
        
    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = character_name + SAVE_FILE_EXTENSION
    file_path = os.path.join(save_directory, filename)

    # 1. Check if file exists
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"No save file found for character '{character_name}'")

    character_data = {}
    
    try:
        # 2. Try to read file
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # Expected format: KEY: VALUE
                if ":" not in line:
                    raise InvalidSaveDataError(f"Line {line_num}: Missing separator ':'")

                key_str, value_str = line.split(":", 1)
                key = key_str.strip().lower() # Convert key to lowercase for dict
                value = value_str.strip()
                
                # 3. Parse and convert data types
                if key in ['level', 'health', 'max_health', 'strength', 'magic', 'experience', 'gold']:
                    try:
                        value = int(value)
                    except ValueError:
                        raise InvalidSaveDataError(f"Line {line_num}: Expected integer for '{key}', got '{value}'")
                
                elif key in ['inventory', 'active_quests', 'completed_quests']:
                    # Convert comma-separated string back to list
                    value = [item.strip() for item in value.split(',') if item.strip()] # Handles empty list string
                
                character_data[key] = value
    except IOError as e:
        # Catches file reading errors (e.g., permissions, unexpected end of file)
        raise SaveFileCorruptedError(f"Failed to read save file '{character_name}': {e}")
    except InvalidSaveDataError:
        # Re-raise the already specific data error
        raise
    except Exception as e:
        # Catch unexpected errors during parsing
        raise SaveFileCorruptedError(f"An unexpected error occurred while parsing '{character_name}': {e}")

    # 4. Final validation before returning
    validate_character_data(character_data)
    
    return character_data

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []
        
    try:
        saved_files = os.listdir(save_directory)
        
        # Filter files ending with the correct extension and extract the name
        names = []
        for filename in saved_files:
            if filename.endswith(SAVE_FILE_EXTENSION):
                # Remove the extension to get the character name
                name = filename[:-len(SAVE_FILE_EXTENSION)]
                names.append(name)
        
        return names
        
    except OSError:
        # Catch permissions errors, etc.
        return []

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = character_name + SAVE_FILE_EXTENSION
    file_path = os.path.join(save_directory, filename)
    
    # 1. Verify file exists
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Cannot delete. No save file found for character '{character_name}'")

    try:
        # 2. Attempt deletion
        os.remove(file_path)
        return True
    except OSError as e:
        # Catch file-system errors during deletion
        print(f"Warning: Could not delete file due to OS error: {e}")
        return False # Or you could raise a custom error here if required

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if is_character_dead(character):
        raise CharacterDeadError(f"{character['name']} cannot gain experience while dead.")
        
    if xp_amount < 0:
        raise ValueError("XP amount must be non-negative.")

    character['experience'] += xp_amount
    
    # Check for level up
    while True:
        level = character['level']
        level_up_xp = level * 100
        
        if character['experience'] >= level_up_xp:
            # Consume XP for level up
            character['experience'] -= level_up_xp
            character['level'] += 1
            
            # Apply stat bonuses
            character['max_health'] += 10
            character['strength'] += 2
            character['magic'] += 2
            
            # Restore health
            character['health'] = character['max_health']
            
            print(f"*** {character['name']} leveled up to Lvl {character['level']}! ***")
        else:
            break
            
    return character['experience']

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_gold = character['gold'] + amount
    
    if new_gold < 0:
        raise ValueError(f"Cannot perform transaction. Character only has {character['gold']} gold, result would be negative.")
        
    character['gold'] = new_gold
    return new_gold

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    current_health = character['health']
    max_health = character['max_health']
    
    health_needed = max_health - current_health
    actual_heal = min(amount, health_needed)
    
    character['health'] += actual_heal
    
    return actual_heal

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character['health'] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if not is_character_dead(character):
        return False

    max_health = character['max_health']
    # Restore health to half of max_health (using integer division)
    character['health'] = max_health // 2
    
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_fields = {
        'name': str, 'class': str, 
        'level': int, 'health': int, 'max_health': int, 
        'strength': int, 'magic': int, 
        'experience': int, 'gold': int, 
        'inventory': list, 'active_quests': list, 'completed_quests': list
    }

    for key, expected_type in required_fields.items():
        if key not in character:
            raise InvalidSaveDataError(f"Character data missing required field: '{key}'")
            
        value = character[key]
        
        # Check type
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(
                f"Invalid type for field '{key}'. Expected {expected_type.__name__}, got {type(value).__name__}"
            )

        # Additional value checks for numeric fields
        if key in ['level', 'max_health', 'strength', 'magic']:
            if value <= 0:
                raise InvalidSaveDataError(f"Numeric stat '{key}' must be positive, got {value}")
        if key in ['health']:
             if value < 0:
                raise InvalidSaveDataError(f"Health cannot be negative, got {value}")
        if key == 'health' and value > character['max_health']:
            # Allow this, but maybe warn or correct it in a real game. For assignment, it's an error in the save file structure.
            raise InvalidSaveDataError(f"Current health ({value}) exceeds max health ({character['max_health']}).")
        
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

    try:
        char = create_character("TestWarrior", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}/{char['max_health']}, STR={char['strength']}, MAG={char['magic']}, Gold={char['gold']}")
        
        create_character("BadName", "Sorcerer")
    except InvalidCharacterClassError as e:
        print(f"SUCCESS: Invalid class error caught: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected error during class validation: {e}")

    # --- Test 2: Saving and Loading ---
    print("\n--- Testing Save/Load ---")
    try:
        save_character(char, "temp_saves")
        print(f"SUCCESS: Character '{char['name']}' saved.")
        
        loaded = load_character("TestWarrior", "temp_saves")
        print(f"SUCCESS: Loaded character: {loaded['name']} (Lvl {loaded['level']})")

    except Exception as e:
        print(f"FAIL: Save/Load error: {e}")

    # --- Test 3: Operations (XP, Gold, Healing) ---
    print("\n--- Testing Operations ---")
    
    # XP and Level Up
    gain_experience(char, 99)
    print(f"XP after 99: {char['experience']} (Lvl {char['level']})")
    gain_experience(char, 1) # Should level up to 2 (100xp needed)
    print(f"XP after +1: {char['experience']} (Lvl {char['level']}). New Max HP: {char['max_health']}")
    
    # Gold
    add_gold(char, -50)
    print(f"Gold after spending 50: {char['gold']}")
    try:
        add_gold(char, -1000)
    except ValueError as e:
        print(f"SUCCESS: Negative gold error caught: {e}")
        
    # Death/Revive
    char['health'] = 0
    print(f"Is character dead? {is_character_dead(char)}")
    revive_character(char)
    print(f"Health after revive: {char['health']} (Expected {char['max_health'] // 2})")

    # --- Cleanup ---
    try:
        delete_character("TestWarrior", "temp_saves")
        os.rmdir("temp_saves")
        print("\nCleanup successful.")
    except Exception as e:
        print(f"Cleanup failed: {e}")
