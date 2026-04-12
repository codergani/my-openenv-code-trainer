"""
Test script to verify grader functions return valid scores.
"""
from my_graders import grade_easy, grade_medium, grade_hard
from models import MyAssistantBotState

def test_graders():
    print("Testing grader functions...")
    
    # Test 1: Empty state (no points earned)
    state = MyAssistantBotState()
    print(f"\nTest 1: Empty state (no points)")
    easy_score = grade_easy(state)
    med_score = grade_medium(state)
    hard_score = grade_hard(state)
    print(f"  Easy score: {easy_score} (should be 0.1)")
    print(f"  Medium score: {med_score} (should be 0.1)")
    print(f"  Hard score: {hard_score} (should be 0.1)")
    assert 0.0 < easy_score < 1.0, f"Easy score {easy_score} not in valid range"
    assert 0.0 < med_score < 1.0, f"Medium score {med_score} not in valid range"
    assert 0.0 < hard_score < 1.0, f"Hard score {hard_score} not in valid range"
    
    # Test 2: Partial easy score
    state = MyAssistantBotState(easy_score=1)
    print(f"\nTest 2: Easy score = 1/3")
    easy_score = grade_easy(state)
    print(f"  Easy score: {easy_score} (should be ~0.37)")
    assert 0.0 < easy_score < 1.0, f"Easy score {easy_score} not in valid range"
    
    # Test 3: Full easy score
    state = MyAssistantBotState(easy_score=3)
    print(f"\nTest 3: Easy score = 3/3")
    easy_score = grade_easy(state)
    print(f"  Easy score: {easy_score} (should be 0.9)")
    assert 0.0 < easy_score < 1.0, f"Easy score {easy_score} not in valid range"
    
    # Test 4: Full medium score
    state = MyAssistantBotState(medium_score=8)
    print(f"\nTest 4: Medium score = 8/8")
    med_score = grade_medium(state)
    print(f"  Medium score: {med_score} (should be 0.9)")
    assert 0.0 < med_score < 1.0, f"Medium score {med_score} not in valid range"
    
    # Test 5: Full hard score
    state = MyAssistantBotState(hard_score=9)
    print(f"\nTest 5: Hard score = 9/9")
    hard_score = grade_hard(state)
    print(f"  Hard score: {hard_score} (should be 0.9)")
    assert 0.0 < hard_score < 1.0, f"Hard score {hard_score} not in valid range"
    
    # Test 6: State as dictionary (alternative format)
    state_dict = {"easy_score": 2, "total_score": 5}
    print(f"\nTest 6: State as dict with easy_score=2")
    easy_score = grade_easy(state_dict)
    print(f"  Easy score: {easy_score}")
    assert 0.0 < easy_score < 1.0, f"Easy score {easy_score} not in valid range"
    
    # Test 7: None state
    print(f"\nTest 7: None state (should return 0.5)")
    easy_score = grade_easy(None)
    print(f"  Easy score: {easy_score}")
    assert 0.0 < easy_score < 1.0, f"Easy score {easy_score} not in valid range"
    
    print("\n✅ All tests passed! All scores are strictly between 0 and 1")

if __name__ == "__main__":
    test_graders()
