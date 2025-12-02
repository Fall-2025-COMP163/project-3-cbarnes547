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

from character_manager import gain_experience, add_gold


# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quests):
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
    if quest_id not in quests:
        raise QuestNotFoundError("Quest does not exist.")

    quest = quests[quest_id]

    # if already finished, cannot accept again
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # check prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Missing prerequisite quest.")

    # character level too low
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Not high enough level for this quest.")

    # cannot accept an already active quest
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active.")

    # add quest to active list
    character["active_quests"].append(quest_id)
    return True


def complete_quest(character, quest_id, quests):
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
    if quest_id not in quests:
        raise QuestNotFoundError("Quest does not exist.")

    # can only complete if it's active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    quest = quests[quest_id]

    # remove from active and move to completed
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    # give rewards
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    gain_experience(character, xp)
    add_gold(character, gold)

    return {"xp": xp, "gold": gold}


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quests):
    """Return full quest data for active quests"""
    return [quests[q] for q in character["active_quests"] if q in quests]


def get_completed_quests(character, quests):
    """Return full quest data for completed quests"""
    return [quests[q] for q in character["completed_quests"] if q in quests]


def get_active_quests(character, quests):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_list = []
    return [quests[q] for q in character["active_quests"] if q in quests]

def get_completed_quests(character, quests):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    return [quests[q] for q in character["completed_quests"] if q in quests]

def get_available_quests(character, quests):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available = []

    for qid, quest in quests.items():

        if qid in character["completed_quests"]:
            continue
        if qid in character["active_quests"]:
            continue

        if character["level"] < quest["required_level"]:
            continue

        prereq = quest["prerequisite"]
        if prereq != "NONE" and prereq not in character["completed_quests"]:
            continue

        available.append(quest)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character["completed_quests"]

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character["active_quests"]

def can_accept_quest(character, quest_id, quests):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quests:
        return False

    quest = quests[quest_id]

    if quest_id in character["completed_quests"]:
        return False
    if quest_id in character["active_quests"]:
        return False
    if character["level"] < quest["required_level"]:
        return False

    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        return False

    return True

def get_quest_prerequisite_chain(quest_id, quests):
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
    if quest_id not in quests:
        raise QuestNotFoundError("Quest not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quests:
            raise QuestNotFoundError("Invalid quest in chain.")

        chain.insert(0, current)

        prereq = quests[current]["prerequisite"]
        if prereq == "NONE":
            break

        current = prereq

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quests):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    if len(quests) == 0:
        return 0.0

    return (len(character["completed_quests"]) / len(quests)) * 100


def get_total_quest_rewards_earned(character, quests):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    xp_total = 0
    gold_total = 0

    for q in character["completed_quests"]:
        if q in quests:
            xp_total += quests[q]["reward_xp"]
            gold_total += quests[q]["reward_gold"]

    return {"total_xp": xp_total, "total_gold": gold_total}


def get_quests_by_level(quests, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    return [
        q for q in quests.values()
        if min_level <= q["required_level"] <= max_level
    ]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {q['title']} ===")
    print(f"Description: {q['description']}")
    print(f"Required Level: {q['required_level']}")
    print(f"Reward: {q['reward_xp']} XP, {q['reward_gold']} Gold")
    print(f"Prerequisite: {q['prerequisite']}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    for q in quest_list:
        print(f"- {q['title']} (Lvl {q['required_level']}) XP:{q['reward_xp']} Gold:{q['reward_gold']}")

def display_character_quest_progress(character, quests):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    percent = get_quest_completion_percentage(character, quests)
    rewards = get_total_quest_rewards_earned(character, quests)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active quests: {len(character['active_quests'])}")
    print(f"Completed quests: {len(character['completed_quests'])}/{len(quests)} ({percent:.2f} percent)")
    print(f"Total XP earned: {rewards['total_xp']}")
    print(f"Total Gold earned: {rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quests):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for qid, quest in quests.items():
        prereq = quest["prerequisite"]
        if prereq != "NONE" and prereq not in quests:
            raise QuestNotFoundError("Invalid prerequisite found.")
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
