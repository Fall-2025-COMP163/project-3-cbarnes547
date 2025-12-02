"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""
import random

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_type = enemy_type.lower()

    enemies = {
        "goblin": {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in enemies:
        raise InvalidTargetError(f"unknown enemy type: {enemy_type}")

    return enemies[enemy_type].copy()

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character 
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 1
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character["health"] <= 0:
            raise CharacterDeadError("character is already dead")

        winner = None

        while self.combat_active:
            # player turn
            self.player_turn()
            winner = self.check_battle_end()
            if winner:
                break

            # enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                break

            self.turn += 1

        # build result packet
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }
        else:
            return {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0
            }
        
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("combat is not active")

        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)
        display_battle_log(f"you hit the {self.enemy['name']} for {damage}")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("combat is not active")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"the {self.enemy['name']} hits you for {damage}")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        dmg = attacker["strength"] - (defender["strength"] // 4)
        if dmg < 1:
            dmg = 1
        return dmg
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        roll = random.random()
        if roll < 0.5:
            self.combat_active = False
            display_battle_log("you escaped successfully")
            return True
        else:
            display_battle_log("escape failed")
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character['class']
    
    if char_class == 'Warrior':
        return warrior_power_strike(character, enemy)
    elif char_class == 'Mage':
        return mage_fireball(character, enemy)
    elif char_class == 'Rogue':
        return rogue_critical_strike(character, enemy)
    elif char_class == 'Cleric':
        return cleric_heal(character)
    else:
        raise InvalidTargetError("unknown class")

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    dmg = max(1, character["strength"] * 2)
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"warrior uses power strike for {dmg}"


def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    dmg = max(1, character["magic"] * 2)
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"mage casts fireball for {dmg}"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    crit = random.random() < 0.5
    if crit:
        dmg = max(1, character["strength"] * 3)
        note = "critical hit"
    else:
        dmg = max(1, character["strength"])
        note = "normal hit"

    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"rogue critical strike: {note}, {dmg} damage"

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    character["health"] += 30
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]
    return "cleric heals for 30"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character['health'] > 0


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
    test_char_warrior = {
        'name': 'Alistair',
        'class': 'Warrior',
        'level': 1,
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5,
        'inventory': [], 
        'experience': 0,
        'gold': 100,
        'active_quests': [], 
        'completed_quests': [], 
    }
    
    # --- Test 1: Enemy Creation & Level Selection ---
    print("\n--- Test 1: Enemy Creation ---")
    try:
        goblin = create_enemy("goblin")
        dragon = get_random_enemy_for_level(8)
        print(f"Created {goblin['name']} (HP: {goblin['health']}, STR: {goblin['strength']})")
        print(f"Level 8 enemy: {dragon['name']} (HP: {dragon['health']}, XP: {dragon['xp_reward']})")
        bad_enemy = create_enemy("Slime")
    except InvalidTargetError as e:
        print(f"SUCCESS: Invalid enemy error caught: {e}")
    
    # --- Test 2: Basic Damage Calculation ---
    print("\n--- Test 2: Damage Calc ---")
    
    # Warrior (STR 15) vs Goblin (STR 8) -> Defense = 8//4 = 2. Damage = 15 - 2 = 13
    temp_battle = SimpleBattle(test_char_warrior, goblin)
    damage_to_goblin = temp_battle.calculate_damage(test_char_warrior, goblin)
    print(f"Warrior (STR 15) hits Goblin (DEF 2) for: {damage_to_goblin} damage.")
    
    # Goblin (STR 8) vs Warrior (STR 15) -> Defense = 15//4 = 3. Damage = 8 - 3 = 5
    damage_to_warrior = temp_battle.calculate_damage(goblin, test_char_warrior)
    print(f"Goblin (STR 8) hits Warrior (DEF 3) for: {damage_to_warrior} damage.")
    
    # --- Test 3: Special Ability (Warrior Power Strike) ---
    print("\n--- Test 3: Warrior Ability ---")
    goblin_for_ability = create_enemy("goblin")
    print(f"Goblin HP before: {goblin_for_ability['health']}")
    
    warrior_message = warrior_power_strike(test_char_warrior, goblin_for_ability)
    print(f"{warrior_message}")
    print(f"Goblin HP after: {goblin_for_ability['health']}")
    
    # --- Test 4: Full Battle Loop ---
    print("\n--- Test 4: Full Battle Loop (Manual Input Required) ---")
    
    test_char_warrior['health'] = test_char_warrior['max_health'] # Reset HP
    enemy_orc = create_enemy("orc")
    
    battle_instance = SimpleBattle(test_char_warrior, enemy_orc)
    try:
        results = battle_instance.start_battle()
        print(f"\nFINAL BATTLE RESULTS: {results}")
    except CharacterDeadError as e:
        print(f"Battle failed to start: {e}")
