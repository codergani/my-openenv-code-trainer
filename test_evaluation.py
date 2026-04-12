#!/usr/bin/env python3
"""Simulate the exact evaluation process."""

import yaml
import importlib
from models import MyAssistantBotState

print("=" * 70)
print("SIMULATING EXACT EVALUATION PROCESS")
print("=" * 70)
print()

# Step 1: Load openenv.yaml
print("Step 1: Loading openenv.yaml...")
with open('openenv.yaml', 'r') as f:
    config = yaml.safe_load(f)

tasks = config.get('tasks', [])
print(f"✓ Found {len(tasks)} tasks")
print()

# Step 2: For each task, import and test the grader
print("Step 2: Testing each grader...")
all_pass = True

for task in tasks:
    task_id = task.get('id')
    grader_ref = task.get('grader')  # e.g., "my_graders:grade_easy"
    
    print(f"Task: {task_id}")
    print(f"  Grader: {grader_ref}")
    
    # Parse grader reference
    parts = grader_ref.split(':')
    if len(parts) != 2:
        print(f"  ✗ Invalid grader format: {grader_ref}")
        all_pass = False
        continue
    
    module_name, func_name = parts
    
    try:
        # Import the module
        module = importlib.import_module(module_name)
        print(f"  ✓ Imported module: {module_name}")
        
        # Get the function
        grader_func = getattr(module, func_name)
        print(f"  ✓ Found function: {func_name}")
        
        # Test with different states
        test_states = [
            ("Zero scores", MyAssistantBotState()),
            ("Partial scores", MyAssistantBotState(easy_score=1, medium_score=4, hard_score=5)),
            ("Full scores", MyAssistantBotState(easy_score=3, medium_score=8, hard_score=9)),
            ("As dict", {"easy_score": 2, "medium_score": 5, "hard_score": 7}),
        ]
        
        for state_name, state in test_states:
            try:
                score = grader_func(state)
                
                # Validate the score
                if not isinstance(score, float):
                    print(f"  ✗ {state_name}: Not a float! Type={type(score)}, Value={score}")
                    all_pass = False
                elif not (0.0 < score < 1.0):
                    print(f"  ✗ {state_name}: Out of range! Value={score} (need 0 < score < 1)")
                    all_pass = False
                else:
                    print(f"  ✓ {state_name}: {score:.4f}")
                    
            except Exception as e:
                print(f"  ✗ {state_name}: Exception - {e}")
                all_pass = False
        
    except Exception as e:
        print(f"  ✗ Failed to import grader: {e}")
        all_pass = False
    
    print()

print("=" * 70)
if all_pass:
    print("✅ ALL EVALUATION TESTS PASSED")
else:
    print("❌ SOME EVALUATION TESTS FAILED")
print("=" * 70)
