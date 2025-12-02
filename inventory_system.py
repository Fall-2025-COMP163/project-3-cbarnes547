"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Inventory is full. Max capacity: {MAX_INVENTORY_SIZE}")
    
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if item_id not in character.get('inventory', []):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    
    # Use list.remove() which raises ValueError if not found, 
    # but the check above should prevent that.
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get('inventory', [])

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character.get('inventory', []).count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    return MAX_INVENTORY_SIZE - len(character.get('inventory', []))

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    removed_items = character.get('inventory', [])[:] # Copy the list
    character['inventory'] = []
    
    # Note: Does NOT unequip items. The main game loop should handle this before calling clear.
    
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot use. Item '{item_id}' not found in inventory.")
        
    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError(f"Cannot use item of type '{item_data['type']}'. Only 'consumable' items can be used.")
        
    effect_string = item_data['effect']
    stat_name, value = parse_item_effect(effect_string)
    
    apply_stat_effect(character, stat_name, value)
    
    # Remove item after use
    remove_item_from_inventory(character, item_id)
    
    return f"Used {item_data['name']}. Applied {value} to {stat_name}."

def _handle_equip_logic(character, item_id, item_data, slot_key, unequip_func):
    """Internal helper to manage equip/unequip flow."""
    # 1. Check if something is currently equipped in this slot
    current_equipped_id = character.get(slot_key)
    
    if current_equipped_id:
        # 2. Unequip the current item first
        unequip_func(character) # This will add the old item back to inventory
        
    # 3. Apply item bonuses and update slot
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    character[slot_key] = item_id
    
    # 4. Remove the new item from inventory
    remove_item_from_inventory(character, item_id)
    
    return f"Equipped {item_data['name']} as {slot_key.replace('_', ' ')}. Bonus: +{value} {stat_name}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    item_type = item_data['type']
    
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot equip. Item '{item_id}' not found in inventory.")

    if item_type == 'weapon':
        return _handle_equip_logic(character, item_id, item_data, 'equipped_weapon', unequip_weapon)
    elif item_type == 'armor':
        return _handle_equip_logic(character, item_id, item_data, 'equipped_armor', unequip_armor)
    else:
        raise InvalidItemTypeError(f"Item type '{item_type}' cannot be equipped. Must be 'weapon' or 'armor'.")

def equip_item(character, item_id, item_data):
    """
    Generic function to handle both weapon and armor equipping.
    """
    item_type = item_data['type']
    
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot equip. Item '{item_id}' not found in inventory.")

    if item_type == 'weapon':
        return _handle_equip_logic(character, item_id, item_data, 'equipped_weapon', unequip_weapon)
    elif item_type == 'armor':
        return _handle_equip_logic(character, item_id, item_data, 'equipped_armor', unequip_armor)
    else:
        raise InvalidItemTypeError(f"Item type '{item_type}' cannot be equipped. Must be 'weapon' or 'armor'.")
    
def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if item_data['type'] != 'armor':
        raise InvalidItemTypeError(f"Item type is '{item_data['type']}'. Only 'armor' can be equipped here.")
    return equip_item(character, item_id, item_data)

def _handle_unequip_logic(character, slot_key):
    """Internal helper to manage unequip flow."""
    equipped_item_id = character.get(slot_key)
    
    if not equipped_item_id:
        return None # Nothing to unequip
    
def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    return _handle_unequip_logic(character, 'equipped_weapon')

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    return _handle_unequip_logic(character, 'equipped_armor')

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data['cost']
    
    if character.get('gold', 0) < cost:
        raise InsufficientResourcesError(f"Cannot purchase {item_data['name']}. Requires {cost} gold, character has {character.get('gold', 0)}.")
        
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError(f"Cannot purchase {item_data['name']}. Inventory is full.")
        
    # Subtract gold
    character['gold'] -= cost
    
    # Add item
    add_item_to_inventory(character, item_id)
    
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot sell. Item '{item_id}' not found in inventory.")
        
    # Calculate sell price (integer division)
    sell_price = item_data['cost'] // 2
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Add gold to character
    character['gold'] += sell_price
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    if ":" not in effect_string:
        # Assuming validation in game_data.py prevents this, but safe check
        raise ValueError(f"Invalid effect string format: {effect_string}")

    stat_name, value_str = effect_string.split(":", 1)
    
    try:
        value = int(value_str)
    except ValueError:
        raise ValueError(f"Effect value is not an integer: {value_str}")
        
    return stat_name.strip().lower(), value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name not in character:
        return 
        
    character[stat_name] += value
    
    # Special handling for health
    if stat_name == 'health':
        # Health cannot exceed max_health
        if character['health'] > character['max_health']:
            character['health'] = character['max_health']
        # Health cannot be negative
        if character['health'] < 0:
            character['health'] = 0
            
    # For max_health, ensure current health doesn't exceed the new max
    if stat_name == 'max_health':
        if character['health'] > character['max_health']:
            character['health'] = character['max_health']

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory_list = character.get('inventory', [])
    if not inventory_list:
        print("Inventory is empty.")
        return

    item_counts = {}
    for item_id in inventory_list:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1

    print("\n--- Inventory ---")
    print(f"Slots Used: {len(inventory_list)}/{MAX_INVENTORY_SIZE}")
    print(f"Gold: {character.get('gold', 0)}")
    print("-------------------")

    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, {'name': 'Unknown Item', 'type': 'N/A'})
        name = item_info['name']
        item_type = item_info['type'].capitalize()
        
        equipped_status = ""
        if character.get('equipped_weapon') == item_id or character.get('equipped_armor') == item_id:
            equipped_status = " (Equipped)"
            
        print(f"[{item_type}] {name} x{count}{equipped_status}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

    test_char = {
        'inventory': [], 
        'gold': 100, 
        'health': 80, 
        'max_health': 100,
        'strength': 10,
        'magic': 5,
        'equipped_weapon': None, # New slot
        'equipped_armor': None   # New slot
    }
    
    # Mock Item Data (Mimics output from game_data.py)
    MOCK_ITEMS = {
        'potion': {'item_id': 'potion', 'name': 'Healing Potion', 'type': 'consumable', 'effect': 'health:20', 'cost': 25},
        'sword': {'item_id': 'sword', 'name': 'Iron Sword', 'type': 'weapon', 'effect': 'strength:5', 'cost': 50},
        'plate': {'item_id': 'plate', 'name': 'Plate Mail', 'type': 'armor', 'effect': 'max_health:10', 'cost': 75},
        'junk': {'item_id': 'junk', 'name': 'Old Boot', 'type': 'junk', 'effect': 'NONE', 'cost': 1}
    }
    
    # --- Test 1: Add Item & InventoryFullError ---
    print("\n--- Test 1: Add Item & Capacity ---")
    try:
        add_item_to_inventory(test_char, "potion")
        add_item_to_inventory(test_char, "potion")
        add_item_to_inventory(test_char, "sword")
        print(f"Added items. Inventory size: {len(test_char['inventory'])}")
        
        # Fill inventory to test overflow
        for i in range(MAX_INVENTORY_SIZE - len(test_char['inventory'])):
            add_item_to_inventory(test_char, "junk")
        
        print(f"Inventory full. Remaining slots: {get_inventory_space_remaining(test_char)}")
        add_item_to_inventory(test_char, "overflow")
    except InventoryFullError as e:
        print(f"SUCCESS: InventoryFullError caught: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected error during inventory fill: {e}")
    
    # Clear for next tests (requires item removal)
    test_char['inventory'] = ['potion', 'sword', 'plate']
    test_char['health'] = 80
    test_char['max_health'] = 100
    
    # --- Test 2: Use Item & InvalidItemTypeError ---
    print("\n--- Test 2: Item Usage ---")
    print(f"Initial Health: {test_char['health']}")
    try:
        # Use consumable
        result = use_item(test_char, "potion", MOCK_ITEMS['potion'])
        print(f"SUCCESS: {result}. New Health: {test_char['health']}")
        print(f"Potion count: {count_item(test_char, 'potion')}")

        # Try to use non-consumable
        use_item(test_char, "sword", MOCK_ITEMS['sword'])
    except InvalidItemTypeError as e:
        print(f"SUCCESS: InvalidItemTypeError caught: {e}")
    except ItemNotFoundError as e:
        print(f"FAIL: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected error during item use: {e}")
        
    # --- Test 3: Equipping & Unequipping ---
    print("\n--- Test 3: Equipping ---")
    try:
        # Equip weapon
        print(f"Initial Strength: {test_char['strength']}")
        equip_weapon(test_char, "sword", MOCK_ITEMS['sword'])
        print(f"SUCCESS: Equipped sword. New Strength: {test_char['strength']}")
        
        # Unequip weapon (NOTE: Stat removal logic is mocked/external, only inventory check works fully)
        unequip_weapon(test_char)
        print(f"SUCCESS: Unequipped weapon. Weapon count: {count_item(test_char, 'sword')}")
        
    except Exception as e:
        print(f"FAIL: Equip/Unequip error: {e}")

    # --- Test 4: Selling & Purchasing ---
    print("\n--- Test 4: Shop Functions ---")
    test_char['inventory'] = ['potion']
    test_char['gold'] = 50
    
    try:
        # Purchase Item (Cost 50)
        purchase_item(test_char, "sword", MOCK_ITEMS['sword'])
        print(f"SUCCESS: Purchased sword. Gold remaining: {test_char['gold']}")
        
        # Try to purchase without gold (Cost 75)
        purchase_item(test_char, "plate", MOCK_ITEMS['plate'])
    except InsufficientResourcesError as e:
        print(f"SUCCESS: InsufficientResourcesError caught: {e}")
        
    try:
        # Sell item
        sell_gold = sell_item(test_char, "sword", MOCK_ITEMS['sword'])
        print(f"SUCCESS: Sold sword for {sell_gold} gold. New Gold: {test_char['gold']}")
        
        # Try to sell item not owned
        sell_item(test_char, "plate", MOCK_ITEMS['plate'])
    except ItemNotFoundError as e:
        print(f"SUCCESS: ItemNotFoundError caught during sell: {e}")
