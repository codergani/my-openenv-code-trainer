---
title: My Assistant Bot Environment Server
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
---

# 🧠 Code Trainer: AI Coding Training Environment

A training environment where AI agents learn to solve Python coding challenges. 10 challenges across 3 difficulty levels. The agent answers each challenge and receives graded feedback with scores normalized to 0.0–1.0.

## Quick Start

```bash
python -m my_assistant_bot.server.app
```

Then visit: **http://localhost:8000/elite**

## Environment API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset` | POST | Reset environment, get first challenge |
| `/step`  | POST | Submit answer `{"action":{"message":"4"}}` |
| `/state` | GET  | Get current state |
| `/schema`| GET  | Get action/observation schemas |

### Action Schema: `{"message": "your answer"}`
### Observation Schema: `{"echoed_message": "...", "reward": 0.0-1.0, "done": false}`

## Tasks & Grading

The environment has **3 task categories** with graders:

| Task | Challenges | Max Raw Score | Grader |
|------|-----------|---------------|--------|
| **Easy** (Output, Types, Bug Fix) | 1–3 | 3.0 | Exact match |
| **Medium** (Data Structures, Algorithms, Completion) | 4–7 | 6.0 | Exact match |
| **Hard** (Generators, OOP, Error Handling) | 8–10 | 6.0 | Exact match |

**Rewards are normalized to 0.0–1.0 range** (raw_score / max_possible_score).

## Inference

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-token"
python inference.py
```
