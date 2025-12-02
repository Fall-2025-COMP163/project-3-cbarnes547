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

ENEMY_STATS = {
    "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
    "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
    "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
}
VALID_ENEMIES = list(ENEMY_STATS.keys())

# --- Cooldown tracking for special abilities (basic, not fully implemented for persistence) ---
ABILITY_COOLDOWN = 2 # Example: 2 turns cooldown after use
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
    enemy_type_lower = enemy_type.lower()
    
    if enemy_type_lower not in VALID_ENEMIES:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' is not recognized.")
        
    base_stats = ENEMY_STATS[enemy_type_lower]
    
    enemy = {
        'name': enemy_type.capitalize(),
        'type': enemy_type_lower,
        'health': base_stats['health'],
        'max_health': base_stats['health'],
        'strength': base_stats['strength'],
        'magic': base_stats['magic'],
        'xp_reward': base_stats['xp_reward'],
        'gold_reward': base_stats['gold_reward'],
    }
    return enemy

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
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
        
    return create_enemy(enemy_type)

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
        self.turn_counter = 0
        # Basic ability cooldown tracking (stores the turn number when ability was last used)
        self.ability_cooldown_turn = 0
    
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
        if self.character['health'] <= 0:
            raise CharacterDeadError(f"{self.character['name']} cannot start a battle while dead.")
            
        self.combat_active = True
        self.turn_counter = 0
        display_battle_log(f"A wild {self.enemy['name']} appeared!")
        
        while self.combat_active:
            self.turn_counter += 1
            display_combat_stats(self.character, self.enemy)
            
            # 1. Player's Turn
            action_result = self.player_turn()
            
            # Check for immediate end (escape or player death from self-inflicted damage/status)
            if not self.combat_active:
                return action_result 

            # Check if player action ended battle (i.e., enemy died)
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                break
                
            # 2. Enemy's Turn
            self.enemy_turn()
            
            # Check if enemy action ended battle (i.e., player died)
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                break
        
        # Battle concluded (not escaped)
        if winner == 'player':
            rewards = get_victory_rewards(self.enemy)
            display_battle_log(f"You defeated the {self.enemy['name']}!")
            display_battle_log(f"Gained {rewards['xp']} XP and {rewards['gold']} Gold.")
            # Important: The rewards are returned for `main.py` to apply using `character_manager` functions
            return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
        elif winner == 'enemy':
            display_battle_log(f"The {self.enemy['name']} defeated you!")
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
        
        # Should not be reached if logic is correct, but handles unexpected end
        return {'winner': 'unknown', 'xp_gained': 0, 'gold_gained': 0}
    
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
            raise CombatNotActiveError("Cannot take player turn, combat is not active.")

        can_use_ability = self.turn_counter >= (self.ability_cooldown_turn + ABILITY_COOLDOWN)
        
        print("\n--- Your Turn ---")
        print("1. Basic Attack")
        print(f"2. Special Ability ({self.character['class']} - {'Ready' if can_use_ability else 'CD'})")
        print("3. Try to Run")
        
        while True:
            choice = input("Enter choice (1-3): ").strip()
            
            if choice == '1':
                damage = self.calculate_damage(self.character, self.enemy)
                self.apply_damage(self.enemy, damage)
                display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
                return {'action': 'attack'}
            
            elif choice == '2':
                if not can_use_ability:
                    display_battle_log("Ability is on cooldown! Choose another action.")
                    continue
                
                try:
                    message = use_special_ability(self.character, self.enemy)
                    display_battle_log(f"** {message} **")
                    self.ability_cooldown_turn = self.turn_counter # Set cooldown
                    return {'action': 'ability'}
                except Exception as e:
                    # Catch any other specific errors from ability use
                    display_battle_log(f"Error using ability: {e}")
                    continue
                    
            elif choice == '3':
                if self.attempt_escape():
                    self.combat_active = False
                    display_battle_log(f"{self.character['name']} successfully escaped the battle!")
                    return {'winner': 'escape', 'xp_gained': 0, 'gold_gained': 0}
                else:
                    display_battle_log(f"{self.character['name']} failed to escape!")
                    return {'action': 'run_failed'}
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
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
            raise CombatNotActiveError("Cannot take enemy turn, combat is not active.")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        defense = defender['strength'] // 4
        
        # Raw damage
        raw_damage = attacker['strength'] - defense
        
        # Apply minimum damage rule
        final_damage = max(1, raw_damage)
        
        return final_damage
    
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
        if self.enemy['health'] <= 0:
            return 'player'
        if self.character['health'] <= 0:
            return 'enemy'
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
        if random.random() < 0.5:
            return True
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
        # Should be caught by character creation, but good for safety
        return "Unknown class ability. Nothing happened."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    temp_attacker = character.copy()
    temp_attacker['strength'] *= 2
    
    # Since this isn't inside SimpleBattle, we need a temp instance for damage calc
    temp_battle = SimpleBattle(character, enemy)
    damage = temp_battle.calculate_damage(temp_attacker, enemy)
    
    temp_battle.apply_damage(enemy, damage)
    
    return f"Power Strike! Deals a massive {damage} damage to {enemy['name']}."

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    raw_magic_damage = character['magic'] * 2
    damage = max(1, raw_magic_damage)

    # Apply damage directly (or use apply_damage logic on a temp battle instance)
    enemy['health'] -= damage
    if enemy['health'] < 0:
        enemy['health'] = 0

    return f"Fireball! Explodes on {enemy['name']} for {damage} magical damage."

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    multiplier = 1
    if random.random() < 0.5: # 50% chance
        multiplier = 3
        
    temp_attacker = character.copy()
    temp_attacker['strength'] *= multiplier
    
    temp_battle = SimpleBattle(character, enemy)
    damage = temp_battle.calculate_damage(temp_attacker, enemy)
    
    temp_battle.apply_damage(enemy, damage)

    if multiplier == 3:
        return f"Critical Strike! Lands a devastating {damage} damage!"
    else:
        return f"Critical Strike failed to proc. Deals {damage} damage."

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    HEAL_AMOUNT = 30
    
    current_health = character['health']
    max_health = character['max_health']
    
    health_needed = max_health - current_health
    actual_heal = min(HEAL_AMOUNT, health_needed)
    
    character['health'] += actual_heal
    
    if actual_heal > 0:
        return f"Cleric heals! Restores {actual_heal} health."
    else:
        return f"Cleric attempts to heal but is already at full health ({max_health} HP)."

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
    char_hp = f"💚 {character['health']}/{character['max_health']}"
    enemy_hp = f"❤️ {enemy['health']}/{enemy['max_health']}"
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
