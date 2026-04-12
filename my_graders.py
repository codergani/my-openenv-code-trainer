"""
Grader functions for the Code Trainer environment.
Scores are returned strictly between 0 and 1 (excluding 0.0 and 1.0).
"""

def _get_score(state, key: str) -> float:
    """Safely extract a score value from state (dict or object) as a number."""
    try:
        if state is None:
            return 0.0
        
        val = None
        
        # Handle dict first
        if isinstance(state, dict):
            val = state.get(key)
        # Handle Pydantic model with model_dump
        elif hasattr(state, "model_dump"):
            try:
                data = state.model_dump()
                val = data.get(key)
            except:
                pass
        
        # If still None, try direct attribute access
        if val is None and hasattr(state, key):
            val = getattr(state, key, None)
        
        # Convert to float if we got a value
        if val is not None:
            return float(val)
        
        return 0.0
        
    except Exception:
        return 0.0


def grade_easy(state) -> float:
    """
    Grade the easy task (3 challenges × 1 point = 3 max points).
    Returns a float strictly between 0 and 1.
    Range: 0 points -> 0.15, 3 points -> 0.85
    """
    # Get the score
    score = _get_score(state, "easy_score")
    max_points = 3.0
    
    # Normalize: score / max_points gives [0, 1]
    if max_points <= 0:
        normalized = 0.5  # Safe middle value
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    
    # Map [0, 1] -> [0.15, 0.85]
    result = 0.15 + (normalized * 0.7)
    
    # Final safety validation
    # result should always be between 0.15 and 0.85, but ensure it
    if result <= 0.0 or result >= 1.0:
        result = 0.5  # Fallback to middle if somehow invalid
    
    return float(result)


def grade_medium(state) -> float:
    """
    Grade the medium task (4 challenges × 2 points = 8 max points).
    Returns a float strictly between 0 and 1.
    Range: 0 points -> 0.15, 8 points -> 0.85
    """
    # Get the score
    score = _get_score(state, "medium_score")
    max_points = 8.0
    
    # Normalize: score / max_points gives [0, 1]
    if max_points <= 0:
        normalized = 0.5  # Safe middle value
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    
    # Map [0, 1] -> [0.15, 0.85]
    result = 0.15 + (normalized * 0.7)
    
    # Final safety validation
    # result should always be between 0.15 and 0.85, but ensure it
    if result <= 0.0 or result >= 1.0:
        result = 0.5  # Fallback to middle if somehow invalid
    
    return float(result)


def grade_hard(state) -> float:
    """
    Grade the hard task (3 challenges × 3 points = 9 max points).
    Returns a float strictly between 0 and 1.
    Range: 0 points -> 0.15, 9 points -> 0.85
    """
    # Get the score
    score = _get_score(state, "hard_score")
    max_points = 9.0
    
    # Normalize: score / max_points gives [0, 1]
    if max_points <= 0:
        normalized = 0.5  # Safe middle value
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    
    # Map [0, 1] -> [0.15, 0.85]
    result = 0.15 + (normalized * 0.7)
    
    # Final safety validation
    # result should always be between 0.15 and 0.85, but ensure it
    if result <= 0.0 or result >= 1.0:
        result = 0.5  # Fallback to middle if somehow invalid
    
    return float(result)
