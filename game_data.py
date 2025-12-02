"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

DATA_DIR = "data/"
QUEST_FILE = DATA_DIR + "quests.txt"
ITEM_FILE = DATA_DIR + "items.txt"

REQUIRED_QUEST_FIELDS = [
    "QUEST_ID", "TITLE", "DESCRIPTION", "REWARD_XP", 
    "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"
]

REQUIRED_ITEM_FIELDS = [
    "ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"
]
VALID_ITEM_TYPES = ["weapon", "armor", "consumable"]

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    lines = _read_data_file(filename)
    all_quests = {}
    current_quest_lines = []
    
    for line in lines:
        if not line:
            # Blank line indicates end of a quest block
            if current_quest_lines:
                try:
                    quest_data = parse_quest_block(current_quest_lines)
                    validate_quest_data(quest_data)
                    
                    quest_id = quest_data.get('quest_id')
                    if not quest_id:
                        raise InvalidDataFormatError("Quest block missing required 'quest_id' field.")
                        
                    if quest_id in all_quests:
                        raise InvalidDataFormatError(f"Duplicate 'quest_id' found: {quest_id}")
                        
                    all_quests[quest_id] = quest_data
                except InvalidDataFormatError:
                    # Reraise as specific error
                    raise
                except Exception as error:
                    # Catch all other unexpected errors
                    raise CorruptedDataError(f"Unexpected error processing quest block: {error}")
            current_quest_lines = []
        else:
            current_quest_lines.append(line)
            
    # Process the final block if file doesn't end with a blank line
    if current_quest_lines:
        try:
            quest_data = parse_quest_block(current_quest_lines)
            validate_quest_data(quest_data)
            
            quest_id = quest_data.get('quest_id')
            if not quest_id:
                raise InvalidDataFormatError("Final quest block missing required 'quest_id' field.")
            
            if quest_id in all_quests:
                raise InvalidDataFormatError(f"Duplicate 'quest_id' found: {quest_id}")
                
            all_quests[quest_id] = quest_data
        except InvalidDataFormatError:
            raise
        except Exception as error:
            raise CorruptedDataError(f"Unexpected error processing final quest block: {error}")
            
    return all_quests

def _read_data_file(filename):
    """
    Reads all lines from a data file.
    
    Returns: List of stripped lines.
    Raises: MissingDataFileError, CorruptedDataError.
    """
    try:
        # Use filename variable (snake_case)
        with open(filename, 'r', encoding='utf-8') as file:
            # Use file variable (snake_case)
            lines = [line.strip() for line in file]
            return lines
    except FileNotFoundError:
        # Raise custom exception for missing file
        raise MissingDataFileError(f"Required data file not found: {filename}")
    except IOError as error:
        # Raise custom exception for corrupted/unreadable file
        raise CorruptedDataError(f"Failed to read data file '{filename}': {error}")
    except Exception as error:
        # Catch unexpected errors during reading
        raise CorruptedDataError(f"Unexpected error reading file '{filename}': {error}")
    
def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    lines = _read_data_file(filename)
    all_items = {}
    current_item_lines = []
    
    for line in lines:
        if not line:
            # Blank line indicates end of an item block
            if current_item_lines:
                try:
                    item_data = parse_item_block(current_item_lines)
                    validate_item_data(item_data)
                    
                    item_id = item_data.get('item_id')
                    if not item_id:
                        raise InvalidDataFormatError("Item block missing required 'item_id' field.")

                    if item_id in all_items:
                        raise InvalidDataFormatError(f"Duplicate 'item_id' found: {item_id}")
                        
                    all_items[item_id] = item_data
                except InvalidDataFormatError:
                    raise
                except Exception as error:
                    raise CorruptedDataError(f"Unexpected error processing item block: {error}")
            current_item_lines = []
        else:
            current_item_lines.append(line)
            
    # Process the final block
    if current_item_lines:
        try:
            item_data = parse_item_block(current_item_lines)
            validate_item_data(item_data)

            item_id = item_data.get('item_id')
            if not item_id:
                raise InvalidDataFormatError("Final item block missing required 'item_id' field.")
            
            if item_id in all_items:
                raise InvalidDataFormatError(f"Duplicate 'item_id' found: {item_id}")
                
            all_items[item_id] = item_data
        except InvalidDataFormatError:
            raise
        except Exception as error:
            raise CorruptedDataError(f"Unexpected error processing final item block: {error}")
            
    return all_items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    for field_upper in REQUIRED_QUEST_FIELDS:
        field_lower = field_upper.lower() # Convert constant to lowercase for dict check
        if field_lower not in quest_dict:
            # Use .get() defensively in the error message
            raise InvalidDataFormatError(f"Quest '{quest_dict.get('quest_id', 'unknown')}' is missing required field: {field_upper}")
            
    # 2. Check data types and ranges
    
    # Access dictionary using snake_case keys
    reward_xp = quest_dict['reward_xp']
    reward_gold = quest_dict['reward_gold']
    required_level = quest_dict['required_level']

    if not isinstance(reward_xp, int) or reward_xp < 0:
        raise InvalidDataFormatError(f"Quest '{quest_dict['quest_id']}' has invalid or negative reward_xp: {reward_xp}")
        
    if not isinstance(reward_gold, int) or reward_gold < 0:
        raise InvalidDataFormatError(f"Quest '{quest_dict['quest_id']}' has invalid or negative reward_gold: {reward_gold}")

    if not isinstance(required_level, int) or required_level < 1:
        raise InvalidDataFormatError(f"Quest '{quest_dict['quest_id']}' has invalid required_level: {required_level}")
        
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    for field_upper in REQUIRED_ITEM_FIELDS:
        field_lower = field_upper.lower() # Convert constant to lowercase for dict check
        if field_lower not in item_dict:
            # Use .get() defensively in the error message
            raise InvalidDataFormatError(f"Item '{item_dict.get('item_id', 'unknown')}' is missing required field: {field_upper}")
            
    # 2. Check valid type
    item_type = item_dict['type'].lower()
    if item_type not in VALID_ITEM_TYPES:
        raise InvalidDataFormatError(f"Item '{item_dict['item_id']}' has invalid TYPE: '{item_type}'. Must be one of: {', '.join(VALID_ITEM_TYPES)}")
        
    # 3. Check cost
    item_cost = item_dict['cost']
    if not isinstance(item_cost, int) or item_cost < 0:
        raise InvalidDataFormatError(f"Item '{item_dict['item_id']}' has invalid or negative COST: {item_cost}")
        
    # 4. Check effect format (basic check: must contain ':')
    effect_str = item_dict['effect']
    # A simple check for a consumable's effect or a weapon/armor's stat effect
    if not effect_str or (effect_str != 'NONE' and ':' not in effect_str):
         raise InvalidDataFormatError(f"Item '{item_dict['item_id']}' EFFECT must be in 'STAT:VALUE' format or 'NONE'. Found: {effect_str}")
        
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError as error:
        print(f"Warning: Could not create data directory: {error}")
        return

    # Default Quests
    if not os.path.exists(QUEST_FILE):
        default_quests_content = """\
QUEST_ID: the_lost_amulet
TITLE: The Lost Amulet
DESCRIPTION: A simple task to retrieve a stolen family amulet from a goblin camp.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: the_orc_menace
TITLE: The Orc Menace
DESCRIPTION: Orcs are raiding the trade routes. Find and eliminate the chieftain.
REWARD_XP: 300
REWARD_GOLD: 150
REQUIRED_LEVEL: 3
PREREQUISITE: the_lost_amulet
"""
        try:
            with open(QUEST_FILE, 'w') as file:
                file.write(default_quests_content)
            print(f"Created default file: {QUEST_FILE}")
        except IOError as error:
            print(f"Warning: Could not write {QUEST_FILE}: {error}")

    # Default Items
    if not os.path.exists(ITEM_FILE):
        default_items_content = """\
ITEM_ID: healing_potion
NAME: Minor Healing Potion
TYPE: consumable
EFFECT: health:20
COST: 25
DESCRIPTION: Restores a small amount of health.

ITEM_ID: rusty_sword
NAME: Rusty Sword
TYPE: weapon
EFFECT: strength:3
COST: 50
DESCRIPTION: A basic, rusty sword. Better than nothing.

ITEM_ID: leather_armor
NAME: Leather Armor
TYPE: armor
EFFECT: strength:2
COST: 75
DESCRIPTION: Light and durable leather protection.
"""
        try:
            with open(ITEM_FILE, 'w') as file:
                file.write(default_items_content)
            print(f"Created default file: {ITEM_FILE}")
        except IOError as error:
            print(f"Warning: Could not write {ITEM_FILE}: {error}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_data = {} # Renamed to snake_case
    
    for line in lines:
        if not line:
            continue
            
        if ": " not in line:
            raise InvalidDataFormatError(f"Quest line missing separator: '{line}'")
            
        key_str, value_str = line.split(": ", 1)
        key_upper = key_str.strip().upper() # Temporary variable for uppercase key
        value = value_str.strip()
        
        # Convert numeric fields to integers
        if key_upper in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Quest field '{key_upper}' requires an integer value, got '{value}'")
        
        # Store key in lowercase (snake_case) in the final dictionary
        quest_data[key_upper.lower()] = value
        
    return quest_data

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_data = {} # Renamed to snake_case
    
    for line in lines:
        if not line:
            continue
            
        if ": " not in line:
            raise InvalidDataFormatError(f"Item line missing separator: '{line}'")
            
        key_str, value_str = line.split(": ", 1)
        key_upper = key_str.strip().upper() # Temporary variable for uppercase key
        value = value_str.strip()
        
        # Convert numeric field to integer
        if key_upper == "COST":
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Item field '{key_upper}' requires an integer value, got '{value}'")
        
        # Store key in lowercase (snake_case) in the final dictionary
        item_data[key_upper.lower()] = value
        
    return item_data

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

    create_default_data_files()
    
    # --- Test 2: Load Quests ---
    print("\n--- Testing Quest Loading ---")
    try:
        quests = load_quests()
        print(f"SUCCESS: Loaded {len(quests)} quests. Example: {quests['the_lost_amulet']['title']}")
        validate_quest_data(quests['the_lost_amulet'])
        print("SUCCESS: Quest data passed validation.")
    except (MissingDataFileError, InvalidDataFormatError, CorruptedDataError) as error:
        print(f"FAIL: Quest Loading Error: {error}")
    
    # --- Test 3: Load Items ---
    print("\n--- Testing Item Loading ---")
    try:
        items = load_items()
        print(f"SUCCESS: Loaded {len(items)} items. Example: {items['healing_potion']['effect']}")
        validate_item_data(items['leather_armor'])
        print("SUCCESS: Item data passed validation.")
    except (MissingDataFileError, InvalidDataFormatError, CorruptedDataError) as error:
        print(f"FAIL: Item Loading Error: {error}")

    # Example of how to manually test an InvalidDataFormatError:
    # 1. Manually edit data/quests.txt and change 'REWARD_XP: 100' to 'REWARD_XP: abc'.
    # 2. Re-run this block to see the exception raised.
