"""
Grader functions for the Code Trainer environment.
Scores are returned strictly between 0.1 and 0.9.
"""

def _clamp_score(raw_score: float, max_score: float) -> float:
    """Normalize score to [0.1, 0.9]."""
    if max_score <= 0:
        return 0.5
    # Standard normalized value [0, 1]
    normalized = min(max(float(raw_score) / float(max_score), 0.0), 1.0)
    # Stretch [0, 1] to [0.1, 0.9]
    return float(0.1 + (normalized * 0.8))

def _get_val(state, key: str, default=0):
    """Robust value retrieval from potentially various state object types."""
    if state is None:
        return default
    
    # If passed an object with a .state attribute (common in some OpenEnv versions)
    if hasattr(state, "state") and getattr(state, "state") is not None:
        state = getattr(state, "state")
        
    # Handle dictionary
    if isinstance(state, dict):
        return state.get(key, default)
    
    # Handle object attributes
    try:
        return getattr(state, key, default)
    except Exception:
        # Fallback for Pydantic v2
        try:
            if hasattr(state, "model_dump"):
                return state.model_dump().get(key, default)
            elif hasattr(state, "dict"):
                return state.dict().get(key, default)
        except Exception:
            pass
    return default

def grade_easy(state) -> float:
    score = _get_val(state, "easy_score", 0)
    return _clamp_score(score, 3)

def grade_medium(state) -> float:
    score = _get_val(state, "medium_score", 0)
    return _clamp_score(score, 8)

def grade_hard(state) -> float:
    score = _get_val(state, "hard_score", 0)
    return _clamp_score(score, 9)
