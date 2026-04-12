"""
Grader functions for the Code Trainer environment.
Scores are returned strictly between 0 and 1 (excluding 0.0 and 1.0).
"""

def _get_score(state, key: str) -> int:
    """Safely extract a score value from state (dict or object)."""
    try:
        if state is None:
            return 0
        
        # Handle dict
        if isinstance(state, dict):
            return int(state.get(key, 0)) if state.get(key) is not None else 0
        
        # Handle Pydantic model
        if hasattr(state, "model_dump"):
            data = state.model_dump()
            return int(data.get(key, 0)) if data.get(key) is not None else 0
        
        # Handle object attribute
        if hasattr(state, key):
            val = getattr(state, key, 0)
            return int(val) if val is not None else 0
            
        return 0
    except Exception:
        return 0


def grade_easy(state) -> float:
    """
    Grade the easy task.
    Returns a float strictly between 0 and 1.
    """
    try:
        score = _get_score(state, "easy_score")
        max_points = 3  # 3 easy challenges × 1 point each
        
        # Normalize to [0, 1]
        if max_points <= 0:
            normalized = 0.0
        else:
            normalized = min(float(score) / float(max_points), 1.0)
        
        # Map [0, 1] to [0.15, 0.85] to ensure strictly between 0 and 1
        grade = float(0.15 + (normalized * 0.7))
        
        # Ensure it's a float and in valid range
        if not isinstance(grade, float) or not (0.0 < grade < 1.0):
            return float(0.5)
        
        return grade
        
    except Exception as e:
        # Fallback to middle value
        return float(0.5)


def grade_medium(state) -> float:
    """
    Grade the medium task.
    Returns a float strictly between 0 and 1.
    """
    try:
        score = _get_score(state, "medium_score")
        max_points = 8  # 4 medium challenges × 2 points each
        
        # Normalize to [0, 1]
        if max_points <= 0:
            normalized = 0.0
        else:
            normalized = min(float(score) / float(max_points), 1.0)
        
        # Map [0, 1] to [0.15, 0.85] to ensure strictly between 0 and 1
        grade = float(0.15 + (normalized * 0.7))
        
        # Ensure it's a float and in valid range
        if not isinstance(grade, float) or not (0.0 < grade < 1.0):
            return float(0.5)
        
        return grade
        
    except Exception as e:
        # Fallback to middle value
        return float(0.5)


def grade_hard(state) -> float:
    """
    Grade the hard task.
    Returns a float strictly between 0 and 1.
    """
    try:
        score = _get_score(state, "hard_score")
        max_points = 9  # 3 hard challenges × 3 points each
        
        # Normalize to [0, 1]
        if max_points <= 0:
            normalized = 0.0
        else:
            normalized = min(float(score) / float(max_points), 1.0)
        
        # Map [0, 1] to [0.15, 0.85] to ensure strictly between 0 and 1
        grade = float(0.15 + (normalized * 0.7))
        
        # Ensure it's a float and in valid range
        if not isinstance(grade, float) or not (0.0 < grade < 1.0):
            return float(0.5)
        
        return grade
        
    except Exception as e:
        # Fallback to middle value
        return float(0.5)
