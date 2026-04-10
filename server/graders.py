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


def grade_easy(state: dict) -> float:
    """
    Grade Easy challenges (IDs 1-3).
    Max raw score = 3.0 (3 challenges x 1.0 points each).

    Args:
        state: Dictionary containing environment state with per-difficulty scores.

    Returns:
        A float strictly between 0 and 1.
    """
    easy_score = state.get("easy_score", 0.0)
    easy_max = 3.0  # 3 easy challenges x 1.0 points each
    return _clamp_score(easy_score, easy_max)


def grade_medium(state: dict) -> float:
    """
    Grade Medium challenges (IDs 4-7).
    Max raw score = 6.0 (4 challenges x 1.5 points each).

    Args:
        state: Dictionary containing environment state with per-difficulty scores.

    Returns:
        A float strictly between 0 and 1.
    """
    medium_score = state.get("medium_score", 0.0)
    medium_max = 6.0  # 4 medium challenges x 1.5 points each
    return _clamp_score(medium_score, medium_max)


def grade_hard(state: dict) -> float:
    """
    Grade Hard challenges (IDs 8-10).
    Max raw score = 6.0 (3 challenges x 2.0 points each).

    Args:
        state: Dictionary containing environment state with per-difficulty scores.

    Returns:
        A float strictly between 0 and 1.
    """
    hard_score = state.get("hard_score", 0.0)
    hard_max = 6.0  # 3 hard challenges x 2.0 points each
    return _clamp_score(hard_score, hard_max)
