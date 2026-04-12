#!/usr/bin/env python3
"""Comprehensive validation of graders and environment."""

print('=== COMPREHENSIVE GRADER & CONFIG TEST ===')
print()

# Test 1: Import graders
print('Test 1: Import graders...')
try:
    from my_graders import grade_easy, grade_medium, grade_hard
    print('✓ Graders imported successfully')
except Exception as e:
    print(f'✗ Import failed: {e}')
    exit(1)

# Test 2: Import models
print()
print('Test 2: Import models...')
try:
    from models import MyAssistantBotState
    print('✓ Models imported successfully')
except Exception as e:
    print(f'✗ Import failed: {e}')
    exit(1)

# Test 3: Test graders with states
print()
print('Test 3: Test grader return types and ranges...')
states = [
    ('Zero scores', MyAssistantBotState()),
    ('Easy only', MyAssistantBotState(easy_score=3, medium_score=0, hard_score=0)),
    ('Easy partial', MyAssistantBotState(easy_score=1, medium_score=0, hard_score=0)),
    ('All scores', MyAssistantBotState(easy_score=3, medium_score=8, hard_score=9)),
]

all_valid = True
for desc, state in states:
    e = grade_easy(state)
    m = grade_medium(state)
    h = grade_hard(state)
    
    # Check types
    e_type_ok = isinstance(e, float)
    m_type_ok = isinstance(m, float)
    h_type_ok = isinstance(h, float)
    
    # Check ranges
    e_range_ok = 0.0 < e < 1.0
    m_range_ok = 0.0 < m < 1.0
    h_range_ok = 0.0 < h < 1.0
    
    if not (e_type_ok and m_type_ok and h_type_ok):
        print(f'✗ {desc}: Type error')
        print(f'  e: {type(e).__name__} = {e}')
        print(f'  m: {type(m).__name__} = {m}')
        print(f'  h: {type(h).__name__} = {h}')
        all_valid = False
    elif not (e_range_ok and m_range_ok and h_range_ok):
        print(f'✗ {desc}: Range error')
        print(f'  e: {e:.4f} valid={e_range_ok} (0.0 < {e} < 1.0)')
        print(f'  m: {m:.4f} valid={m_range_ok} (0.0 < {m} < 1.0)')
        print(f'  h: {h:.4f} valid={h_range_ok} (0.0 < {h} < 1.0)')
        all_valid = False
    else:
        print(f'✓ {desc}: e={e:.4f}, m={m:.4f}, h={h:.4f}')

if not all_valid:
    print('\n✗ FAILED')
    exit(1)

# Test 4: Test dict state format
print()
print('Test 4: Test with dict state...')
dict_state = {'easy_score': 2, 'medium_score': 4, 'hard_score': 6}
try:
    e = grade_easy(dict_state)
    m = grade_medium(dict_state)
    h = grade_hard(dict_state)
    
    if 0.0 < e < 1.0 and 0.0 < m < 1.0 and 0.0 < h < 1.0:
        print(f'✓ Dict state: e={e:.4f}, m={m:.4f}, h={h:.4f}')
    else:
        print(f'✗ Dict state range error:')
        print(f'  e={e:.4f} (valid={0.0 < e < 1.0})')
        print(f'  m={m:.4f} (valid={0.0 < m < 1.0})')
        print(f'  h={h:.4f} (valid={0.0 < h < 1.0})')
        exit(1)
except Exception as ex:
    print(f'✗ Dict state exception: {ex}')
    exit(1)

# Test 5: Check openenv.yaml parsing
print()
print('Test 5: Validate openenv.yaml...')
try:  
    import yaml
    with open('openenv.yaml', 'r') as f:
        config = yaml.safe_load(f)
    num_tasks = len(config.get('tasks', []))
    print(f'✓ openenv.yaml loaded: {num_tasks} tasks found')
    for task in config.get('tasks', []):
        task_id = task.get('id', '?')
        grader = task.get('grader', '?')
        print(f'  - {task_id}: grader={grader}')
except Exception as e:
    print(f'✗ YAML error: {e}')
    exit(1)

# Test 6: Check inference.py exists and is executable
print()
print('Test 6: Check inference.py...')
import os
if not os.path.exists('inference.py'):
    print('✗ inference.py not found in root directory')
    exit(1)
print('✓ inference.py exists in root directory')

# Test 7: Check environment exists
print()
print('Test 7: Check environment module...')
try:
    from my_assistant_bot import MyAssistantBotEnv
    print('✓ MyAssistantBotEnv imported successfully')
except Exception as e:
    print(f'✗ Environment import failed: {e}')
    exit(1)

print()
print('=' * 50)
print('✅ ALL VALIDATION TESTS PASSED')
print('=' * 50)
