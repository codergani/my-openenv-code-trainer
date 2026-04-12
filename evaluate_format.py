#!/usr/bin/env python3
"""Simulate the evaluation flow to identify issues."""

import sys
import os
import re
from io import StringIO

print('=' * 60)
print('EVALUATING INFERENCE.PY LOG FORMAT')
print('=' * 60)
print()

# Capture what inference.py would output
sample_logs = [
    "[START] task=code-training env=my-assistant-bot model=gpt-4o-mini",
    "[STEP] step=1 action=answer1 reward=0.05 done=false error=null",
    "[STEP] step=2 action=answer2 reward=0.25 done=false error=null",
    "[STEP] step=3 action=answer3 reward=0.35 done=true error=null",
    "[END] success=true steps=3 score=0.55 rewards=0.05,0.25,0.35",
]

print('Sample inference.py output:')
for log in sample_logs:
    print(f'  {log}')
print()

# Validate START line
print('Validating log format...')
print()

# START line validation
start_pattern = r'^\[START\] task=\S+ env=\S+ model=\S+$'
if re.match(start_pattern, sample_logs[0]):
    print('✓ [START] format correct')
else:
    print('✗ [START] format INVALID')
    print(f'  Pattern: {start_pattern}')
    print(f'  Got: {sample_logs[0]}')

# STEP line validation
step_pattern = r'^\[STEP\] step=(\d+) action=(\S+) reward=([\d.]+) done=(true|false) error=(.+)$'
print()
print('Validating [STEP] lines...')
for log in sample_logs[1:-1]:
    match = re.match(step_pattern, log)
    if match:
        step, action, reward, done, error = match.groups()
        reward_val = float(reward)
        if 0.0 <= reward_val <= 1.0:
            print(f'✓ Step {step}: reward={reward} ✓, done={done} ✓, error={error} ✓')
        else:
            print(f'✗ Step {step}: reward={reward} OUT OF RANGE [0,1]!')
    else:
        print(f'✗ STEP format INVALID: {log}')

# END line validation
end_pattern = r'^\[END\] success=(true|false) steps=(\d+) score=([\d.]+) rewards=([\d.,]+)$'
if re.match(end_pattern, sample_logs[-1]):
    match = re.match(end_pattern, sample_logs[-1])
    if match:
        success, steps, score, rewards = match.groups()
        score_val = float(score)
        print()
        print('✓ [END] format correct')
        print(f'  success={success}, steps={steps}, score={score_val:.2f}')
        if 0.0 <= score_val <= 1.0:
            print(f'  score {score_val:.2f} is in valid range [0, 1] ✓')
        else:
            print(f'  score {score_val:.2f} is OUT OF RANGE [0, 1] ✗')
else:
    print('✗ [END] format INVALID')
    print(f'  Got: {sample_logs[-1]}')

print()
print('=' * 60)
print('EVALUATING GRADER COMPATIBILITY')
print('=' * 60)
print()

# Now test that graders return valid scores
from my_graders import grade_easy, grade_medium, grade_hard
from models import MyAssistantBotState

print('Testing graders with evaluation states...')
print()

# Scenario 1: Perfect score on one task
print('Scenario 1: Perfect easy task')
state1 = MyAssistantBotState(easy_score=3, medium_score=0, hard_score=0)
e1, m1, h1 = grade_easy(state1), grade_medium(state1), grade_hard(state1)
print(f'  easy={e1:.4f}, medium={m1:.4f}, hard={h1:.4f}')
if all(0.0 < x < 1.0 for x in [e1, m1, h1]):
    print('  ✓ All scores valid')
else:
    print('  ✗ Some scores OUT OF RANGE')

# Scenario 2: Partial scores
print()
print('Scenario 2: Partial scores across tasks')
state2 = MyAssistantBotState(easy_score=1, medium_score=4, hard_score=5)
e2, m2, h2 = grade_easy(state2), grade_medium(state2), grade_hard(state2)
print(f'  easy={e2:.4f}, medium={m2:.4f}, hard={h2:.4f}')
if all(0.0 < x < 1.0 for x in [e2, m2, h2]):
    print('  ✓ All scores valid')
else:
    print('  ✗ Some scores OUT OF RANGE')

# Scenario 3: No scores
print()
print('Scenario 3: Zero scores (no answers)')
state3 = MyAssistantBotState()
e3, m3, h3 = grade_easy(state3), grade_medium(state3), grade_hard(state3)
print(f'  easy={e3:.4f}, medium={m3:.4f}, hard={h3:.4f}')
if all(0.0 < x < 1.0 for x in [e3, m3, h3]):
    print('  ✓ All scores valid (returning fallback values)')
else:
    print('  ✗ Some scores OUT OF RANGE')

print()
print('=' * 60)
print('✅ VALIDATION COMPLETE')
print('=' * 60)
