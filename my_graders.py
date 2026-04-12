"""
Grader functions for the Code Trainer environment.
Scores are returned strictly between 0.1 and 0.9.
"""

def _clamp_score(raw_score: float, max_score: float) -> float:
    """Normalize score to strictly between 0.1 and 0.9."""
    try:
        raw_score = float(raw_score) if raw_score is not None else 0.0
    except (TypeError, ValueError):
        raw_score = 0.0
    
    if max_score <= 0:
        return 0.5
    
    # Standard normalized value [0, 1]
    normalized = min(max(raw_score / float(max_score), 0.0), 1.0)
    
    # Stretch [0, 1] to [0.1, 0.9] - ensures strictly between 0 and 1
    clamped = float(0.1 + (normalized * 0.8))
    
    # Safety check: ensure value is strictly between 0 and 1
    if clamped <= 0.0 or clamped >= 1.0:
        clamped = 0.5
    
    return clamped

def _get_val(state, key: str, default=0):
    """Robust value retrieval from potentially various state object types."""
    if state is None:
        return default
    
    try:
        # If passed an object with a .state attribute (common in some OpenEnv versions)
        if hasattr(state, "state") and getattr(state, "state") is not None:
            state = getattr(state, "state")
        
        # Handle dictionary
        if isinstance(state, dict):
            val = state.get(key, default)
            return val if val is not None else default
        
        # Handle object attributes - try direct attribute first
        if hasattr(state, key):
            val = getattr(state, key, default)
            return val if val is not None else default
        
        # Fallback for Pydantic models
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
            val = state_dict.get(key, default)
            return val if val is not None else default
        elif hasattr(state, "dict"):
            state_dict = state.dict()
            val = state_dict.get(key, default)
            return val if val is not None else default
    except Exception:
        pass
    
    return default

def grade_easy(state) -> float:
    """Grade easy task - evaluates easy_score from state."""
    try:
        # Get easy_score, don't fallback on zero (zero is valid - earned 0 points)
        score = _get_val(state, "easy_score", None)
        if score is None:
            # Only fallback to total_score if easy_score field doesn't exist
            score = _get_val(state, "total_score", 0)
        result = _clamp_score(float(score), 3)
        # Ensure result is valid float between 0 and 1
        if isinstance(result, float) and 0.0 < result < 1.0:
            return result
        return 0.5  # Fallback safe value
    except Exception:
        return 0.5

def grade_medium(state) -> float:
    """Grade medium task - evaluates medium_score from state."""
    try:
        # Get medium_score, don't fallback on zero (zero is valid - earned 0 points)
        score = _get_val(state, "medium_score", None)
        if score is None:
            # Only fallback to total_score if medium_score field doesn't exist
            score = _get_val(state, "total_score", 0)
        result = _clamp_score(float(score), 8)
        # Ensure result is valid float between 0 and 1
        if isinstance(result, float) and 0.0 < result < 1.0:
            return result
        return 0.5  # Fallback safe value
    except Exception:
        return 0.5

def grade_hard(state) -> float:
    """Grade hard task - evaluates hard_score from state."""
    try:
        # Get hard_score, don't fallback on zero (zero is valid - earned 0 points)
        score = _get_val(state, "hard_score", None)
        if score is None:
            # Only fallback to total_score if hard_score field doesn't exist
            score = _get_val(state, "total_score", 0)
        result = _clamp_score(float(score), 9)
        # Ensure result is valid float between 0 and 1
        if isinstance(result, float) and 0.0 < result < 1.0:
            return result
        return 0.5  # Fallback safe value
    except Exception:
        return 0.5
