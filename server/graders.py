"""
Grader functions for the Code Trainer environment.

Each grader evaluates the agent's performance on a specific category of tasks.
Scores are returned strictly between 0 and 1 (exclusive — never 0.0 or 1.0).
"""


def _clamp_score(raw_score: float, max_score: float) -> float:
    """
    Normalize a raw score to a value strictly between 0 and 1
    (never exactly 0.0 or 1.0).
    """
    if max_score <= 0:
        return 0.5
    
    # Normalize to [0, 1]
    normalized = raw_score / max_score
    
    # Clamp to strictly within (0, 1). 
    # The platform rejects 0.0 and 1.0.
    clamped = min(max(normalized, 0.001), 0.999)
    return float(clamped)


def _get_val(state, key: str, default=0.0):
    """Safe retrieval of values from state (handles dict, object, or env instance)."""
    if state is None:
        return default
        
    # Standard OpenEnv pattern: if passed an environment instance, get its state
    if hasattr(state, "state"):
        potential_state = state.state
        # If it's a property/attribute, it might be the state we want
        if potential_state is not None:
            state = potential_state
        
    # Handle dictionary
    if isinstance(state, dict):
        return state.get(key, default)
    
    # Handle Pydantic or other objects
    try:
        # Try direct attribute access
        return getattr(state, key, default)
    except Exception:
        # Fallback for complex objects: try to convert to dict if possible
        try:
            if hasattr(state, "model_dump"):
                return state.model_dump().get(key, default)
            elif hasattr(state, "dict"):
                return state.dict().get(key, default)
        except Exception:
            pass
        return default


def grade_easy(state) -> float:
    """
    Grade Easy challenges (IDs 1-3).
    Max raw score = 3 (3 challenges x 1 point each).
    """
    easy_score = _get_val(state, "easy_score", 0.0)
    easy_max = 3.0
    return _clamp_score(easy_score, easy_max)


def grade_medium(state) -> float:
    """
    Grade Medium challenges (IDs 4-7).
    Max raw score = 8 (4 challenges x 2 points each).
    """
    medium_score = _get_val(state, "medium_score", 0.0)
    medium_max = 8.0
    return _clamp_score(medium_score, medium_max)


def grade_hard(state) -> float:
    """
    Grade Hard challenges (IDs 8-10).
    Max raw score = 9 (3 challenges x 3 points each).
    """
    hard_score = _get_val(state, "hard_score", 0.0)
    hard_max = 9.0
    return _clamp_score(hard_score, hard_max)
