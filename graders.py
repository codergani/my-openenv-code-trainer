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
    """Grade easy task. Returns float strictly between 0 and 1."""
    score = _get_score(state, "easy_score")
    max_points = 3.0
    if max_points <= 0:
        normalized = 0.5
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    result = 0.15 + (normalized * 0.7)
    if result <= 0.0 or result >= 1.0:
        result = 0.5
    return float(result)


def grade_medium(state) -> float:
    """Grade medium task. Returns float strictly between 0 and 1."""
    score = _get_score(state, "medium_score")
    max_points = 8.0
    if max_points <= 0:
        normalized = 0.5
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    result = 0.15 + (normalized * 0.7)
    if result <= 0.0 or result >= 1.0:
        result = 0.5
    return float(result)


def grade_hard(state) -> float:
    """Grade hard task. Returns float strictly between 0 and 1."""
    score = _get_score(state, "hard_score")
    max_points = 9.0
    if max_points <= 0:
        normalized = 0.5
    else:
        normalized = min(max(score / max_points, 0.0), 1.0)
    result = 0.15 + (normalized * 0.7)
    if result <= 0.0 or result >= 1.0:
        result = 0.5
    return float(result)
