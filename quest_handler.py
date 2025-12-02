"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

try:
    from character_manager import gain_experience, add_gold
except ImportError:
    # Define minimal mock functions for local testing if the module is not found
    def gain_experience(character, xp_amount):
        character['experience'] = character.get('experience', 0) + xp_amount
        return xp_amount
    def add_gold(character, amount):
        character['gold'] = character.get('gold', 0) + amount
        return character['gold']

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' does not exist.")
    
    quest_data = quest_data_dict[quest_id]

    # 1. Check if quest already active or completed
    if is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Quest '{quest_id}' is already active.") # Using NotActiveError as a specific 'already' error for active
    
    if is_quest_completed(character, quest_id):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")

    # 2. Check level requirement
    required_level = quest_data['required_level']
    if character['level'] < required_level:
        raise InsufficientLevelError(f"Requires Level {required_level}, but character is only Level {character['level']}.")

    # 3. Check prerequisite quest
    prereq_id = quest_data['prerequisite']
    if prereq_id != "NONE":
        if not is_quest_completed(character, prereq_id):
            # The custom exception is designed for this case
            raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq_id}' must be completed first.")
            
    # If all checks pass, accept the quest
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' does not exist.")

    if not is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")
        
    quest_data = quest_data_dict[quest_id]
    
    # 1. Get rewards
    reward_xp = quest_data['reward_xp']
    reward_gold = quest_data['reward_gold']
    
    # 2. Grant rewards (using assumed imported functions)
    gain_experience(character, reward_xp)
    add_gold(character, reward_gold)
    
    # 3. Update character quest lists
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    
    return {
        'quest_id': quest_id, 
        'reward_xp': reward_xp, 
        'reward_gold': reward_gold
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if not is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Cannot abandon. Quest '{quest_id}' is not currently active.")
        
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_list = []
    for quest_id in character.get('active_quests', []):
        if quest_id in quest_data_dict:
            active_list.append(quest_data_dict[quest_id])
    return active_list

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_list = []
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            completed_list.append(quest_data_dict[quest_id])
    return completed_list

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available_list = []
    for quest_id, quest_data in quest_data_dict.items():
        if can_accept_quest(character, quest_id, quest_data_dict):
            available_list.append(quest_data)
    return available_list

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get('completed_quests', [])

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character.get('active_quests', [])

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False
    
    quest_data = quest_data_dict[quest_id]
    
    # 1. Already completed or active
    if is_quest_completed(character, quest_id) or is_quest_active(character, quest_id):
        return False
        
    # 2. Level requirement
    required_level = quest_data['required_level']
    if character['level'] < required_level:
        return False

    # 3. Prerequisite quest
    prereq_id = quest_data['prerequisite']
    if prereq_id != "NONE":
        if not is_quest_completed(character, prereq_id):
            return False
            
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' does not exist.")

    chain = [quest_id]
    current_id = quest_id
    
    # Loop backwards through prerequisites
    while True:
        prereq_id = quest_data_dict[current_id]['prerequisite']
        
        if prereq_id == "NONE":
            break
            
        if prereq_id not in quest_data_dict:
             # Should ideally be caught by validate_quest_prerequisites, but handles runtime error
            raise QuestNotFoundError(f"Prerequisite '{prereq_id}' for '{current_id}' does not exist.")
            
        # Insert at the beginning of the chain
        chain.insert(0, prereq_id)
        current_id = prereq_id
        
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
        
    # Filter completed quests to only count those that exist in quest_data_dict
    completed_quests = len([
        qid for qid in character.get('completed_quests', []) if qid in quest_data_dict
    ])
    
    percentage = (completed_quests / total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    
    for quest_id in character.get('completed_quests', []):
        quest_data = quest_data_dict.get(quest_id)
        if quest_data:
            total_xp += quest_data['reward_xp']
            total_gold += quest_data['reward_gold']
            
    return {'total_xp': total_xp, 'total_gold': total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    level_quests = []
    for quest_data in quest_data_dict.values():
        req_level = quest_data['required_level']
        if min_level <= req_level <= max_level:
            level_quests.append(quest_data)
    return level_quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    prereq = quest_data['prerequisite']
    prereq_display = prereq if prereq != "NONE" else "None"
    
    print("\n" + "=" * 30)
    print(f"** {quest_data['title']} **")
    print("=" * 30)
    print(f"Description: {quest_data['description']}")
    print("-" * 30)
    print("Requirements:")
    print(f"  Level: {quest_data['required_level']}")
    print(f"  Prerequisite: {prereq_display}")
    print("Rewards:")
    print(f"  XP: {quest_data['reward_xp']}")
    print(f"  Gold: {quest_data['reward_gold']}")
    print("=" * 30)

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests found in this list.")
        return
        
    print(f"\n| {'Title':<30} | {'Req. Lvl':>8} | {'XP':>6} | {'Gold':>6} |")
    print("-" * 65)
    for quest in quest_list:
        print(f"| {quest['title']:<30} | {quest['required_level']:>8} | {quest['reward_xp']:>6} | {quest['reward_gold']:>6} |")
    print("-" * 65)

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    stats = get_total_quest_rewards_earned(character, quest_data_dict)
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    
    print("\n--- Quest Progress Summary ---")
    print(f"Total Quests Completed: {completed_count}")
    print(f"Quests Currently Active: {active_count}")
    print(f"Global Completion Rate: {percentage:.2f}%")
    print("-" * 30)
    print(f"Total XP Earned: {stats['total_xp']}")
    print(f"Total Gold Earned: {stats['total_gold']}")
    print("------------------------------")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest_data in quest_data_dict.items():
        prereq_id = quest_data['prerequisite']
        
        if prereq_id != "NONE":
            if prereq_id not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Invalid prerequisite for quest '{quest_id}'. "
                    f"Prerequisite ID '{prereq_id}' does not exist in the quest data."
                )
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

    test_char = {
        'name': 'TestHero',
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    
    test_quests = {
        'q_1': {
            'quest_id': 'q_1', 'title': 'The Starter', 'description': 'Lvl 1 Quest', 
            'reward_xp': 50, 'reward_gold': 25, 'required_level': 1, 'prerequisite': 'NONE'
        },
        'q_2': {
            'quest_id': 'q_2', 'title': 'Mid Challenge', 'description': 'Lvl 3 Quest', 
            'reward_xp': 150, 'reward_gold': 75, 'required_level': 3, 'prerequisite': 'q_1'
        },
        'q_3': {
            'quest_id': 'q_3', 'title': 'End Game', 'description': 'Lvl 5 Quest', 
            'reward_xp': 500, 'reward_gold': 250, 'required_level': 5, 'prerequisite': 'q_2'
        },
        'invalid_prereq': {
            'quest_id': 'invalid_prereq', 'title': 'Broken', 'description': 'Requires fake', 
            'reward_xp': 1, 'reward_gold': 1, 'required_level': 1, 'prerequisite': 'fake_quest_id'
        }
    }
    
    # --- Test 1: Prerequisite Validation ---
    print("\n--- Test 1: Prerequisite Validation ---")
    try:
        validate_quest_prerequisites(test_quests)
        print("FAIL: Prerequisite validation should have raised QuestNotFoundError.")
    except QuestNotFoundError as e:
        print(f"SUCCESS: Prerequisite validation error caught: {e}")
        # Remove invalid quest for further tests
        del test_quests['invalid_prereq']
    
    # --- Test 2: Acceptance (Level/Prereq) ---
    print("\n--- Test 2: Acceptance Checks ---")
    try:
        accept_quest(test_char, 'q_2', test_quests) # Level 1 trying Lvl 3 quest
    except InsufficientLevelError as e:
        print(f"SUCCESS: InsufficientLevelError caught: {e}")
        
    try:
        test_char['level'] = 3
        accept_quest(test_char, 'q_2', test_quests) # Lvl 3 trying Q2 (requires Q1)
    except QuestRequirementsNotMetError as e:
        print(f"SUCCESS: QuestRequirementsNotMetError caught: {e}")
        
    # --- Test 3: Accept and Complete ---
    print("\n--- Test 3: Accept and Complete ---")
    try:
        # Accept Q1 (Lvl 3 is fine, no prereq)
        accept_quest(test_char, 'q_1', test_quests)
        print(f"SUCCESS: Accepted q_1. Active: {test_char['active_quests']}")
        
        # Complete Q1
        rewards = complete_quest(test_char, 'q_1', test_quests)
        print(f"SUCCESS: Completed q_1. Rewards: {rewards}")
        print(f"Active: {test_char['active_quests']}, Completed: {test_char['completed_quests']}")
        print(f"XP: {test_char['experience']}, Gold: {test_char['gold']}")
        
        # Now Q2 should be available
        accept_quest(test_char, 'q_2', test_quests)
        print(f"SUCCESS: Accepted q_2 after completing q_1.")
        
    except Exception as e:
        print(f"FAIL: Unexpected error during accept/complete: {e}")
        
    # --- Test 4: Tracking and Statistics ---
    print("\n--- Test 4: Tracking and Stats ---")
    print(f"Is q_1 completed? {is_quest_completed(test_char, 'q_1')}")
    print(f"Can accept q_3? {can_accept_quest(test_char, 'q_3', test_quests)}")
    
    chain = get_quest_prerequisite_chain('q_3', test_quests)
    print(f"Q3 Prerequisite Chain: {chain}")
    
    display_character_quest_progress(test_char, test_quests)
    display_quest_info(test_quests['q_2'])
