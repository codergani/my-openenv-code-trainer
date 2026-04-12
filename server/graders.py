"""
Grader functions for the Code Trainer environment.
Scores are returned strictly between 0.05 and 0.95 to satisfy platform constraints.
"""

def _clamp_score(raw_score: float, max_score: float) -> float:
    """Normalize score to [0.1, 0.9]."""
    if max_score <= 0:
        return 0.5
    normalized = min(max(raw_score / max_score, 0.0), 1.0)
    # Stretch [0, 1] to [0.1, 0.9]
    # formula: lower + (normalized * (upper - lower))
    clamped = 0.1 + (normalized * 0.8)
    return float(clamped)

def _get_val(state, key: str, default=0):
    """Robust value retrieval."""
    if state is None: return default
    if hasattr(state, "state") and state.state is not None:
        state = state.state
    if isinstance(state, dict):
        return state.get(key, default)
    try:
        return getattr(state, key, default)
    except:
        try:
            if hasattr(state, "model_dump"): return state.model_dump().get(key, default)
            if hasattr(state, "dict"): return state.dict().get(key, default)
        except: pass
    return default

def grade_easy(state) -> float:
    val = _get_val(state, "easy_score", 0)
    return _clamp_score(float(val), 3.0)

def grade_medium(state) -> float:
    val = _get_val(state, "medium_score", 0)
    return _clamp_score(float(val), 8.0)

def grade_hard(state) -> float:
    val = _get_val(state, "hard_score", 0)
    return _clamp_score(float(val), 9.0)
