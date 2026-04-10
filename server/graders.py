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
    normalized = raw_score / max_score
    # Clamp to strictly within (0, 1) — the validator rejects 0.0 and 1.0
    return round(min(max(normalized, 0.01), 0.99), 4)


def _get_val(state, key: str, default=0.0):
    """Safe retrieval of values from state (handles dict or object)."""
    if isinstance(state, dict):
        return state.get(key, default)
    return getattr(state, key, default)


def grade_easy(state) -> float:
    """
    Grade Easy challenges (IDs 1-3).
    Max raw score = 3.0 (3 challenges x 1.0 points each).
    """
    easy_score = _get_val(state, "easy_score", 0.0)
    easy_max = 3.0
    return _clamp_score(easy_score, easy_max)


def grade_medium(state) -> float:
    """
    Grade Medium challenges (IDs 4-7).
    Max raw score = 6.0 (4 challenges x 1.5 points each).
    """
    medium_score = _get_val(state, "medium_score", 0.0)
    medium_max = 6.0
    return _clamp_score(medium_score, medium_max)


def grade_hard(state) -> float:
    """
    Grade Hard challenges (IDs 8-10).
    Max raw score = 6.0 (3 challenges x 2.0 points each).
    """
    hard_score = _get_val(state, "hard_score", 0.0)
    hard_max = 6.0
    return _clamp_score(hard_score, hard_max)
