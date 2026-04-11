import uuid
from typing import Optional, Any
try:
    from my_assistant_bot.models import MyAssistantBotAction, MyAssistantBotObservation, MyAssistantBotState
except (ImportError, ValueError):
    from models import MyAssistantBotAction, MyAssistantBotObservation, MyAssistantBotState

from openenv.core.env_server import Environment


class MyAssistantBotEnvironment(Environment):
    """
    Code Trainer: An AI training environment for learning Python coding.

    The AI agent is presented with coding challenges one by one.
    It must submit an answer. The environment grades the answer
    and provides feedback, then moves to the next challenge.

    Uses CLASS-LEVEL state so state persists across HTTP requests.
    """

    # ===== CLASS-LEVEL SHARED STATE =====
    _challenges = None
    _env_state = None

    # ===== CODING CHALLENGES =====
    CHALLENGE_POOL = [
        {
            "id": 1,
            "difficulty": "Easy",
            "category": "Output Prediction",
            "question": "What is the output of this Python code?\n\n```python\nprint(len([10, 20, 30, 40]))\n```",
            "accept": ["4"],
            "hint": "len() returns the number of elements in a list.",
            "points": 1.0,
        },
        {
            "id": 2,
            "difficulty": "Easy",
            "category": "Data Types",
            "question": "What is the output of this Python code?\n\n```python\nprint(type(3.14).__name__)\n```",
            "accept": ["float"],
            "hint": "3.14 is a decimal number. What type is that in Python?",
            "points": 1.0,
        },
        {
            "id": 3,
            "difficulty": "Easy",
            "category": "Bug Fix",
            "question": "This function has a bug. What should the operator be?\n\n```python\ndef add(a, b):\n    return a - b   # BUG HERE\n```\n\nWhat operator should replace `-` to fix it?",
            "accept": ["+", "plus"],
            "hint": "The function is called 'add'. What operation does addition use?",
            "points": 1.0,
        },
        {
            "id": 4,
            "difficulty": "Medium",
            "category": "Data Structures",
            "question": "Which data structure follows the FIFO (First In, First Out) principle?\n\nA) Stack\nB) Queue\nC) Tree\nD) Graph",
            "accept": ["b", "queue"],
            "hint": "Think of a line at a store — first person in line is served first.",
            "points": 1.5,
        },
        {
            "id": 5,
            "difficulty": "Medium",
            "category": "Algorithms",
            "question": "What is the time complexity of Binary Search on a sorted array of n elements?\n\nA) O(n)\nB) O(n²)\nC) O(log n)\nD) O(1)",
            "accept": ["c", "log n", "o(log n)", "log"],
            "hint": "Binary search divides the search space in half each step.",
            "points": 1.5,
        },
        {
            "id": 6,
            "difficulty": "Medium",
            "category": "Output Prediction",
            "question": "What is the output of this Python code?\n\n```python\nresult = [x ** 2 for x in range(4)]\nprint(result)\n```",
            "accept": ["[0, 1, 4, 9]", "0, 1, 4, 9", "0,1,4,9"],
            "hint": "range(4) gives 0, 1, 2, 3. Square each one.",
            "points": 1.5,
        },
        {
            "id": 7,
            "difficulty": "Medium",
            "category": "Code Completion",
            "question": "Fill in the blank to complete this function:\n\n```python\ndef is_even(n):\n    return n ___ 2 == 0\n```\n\nWhat operator goes in the blank?",
            "accept": ["%", "mod", "modulo"],
            "hint": "Which operator gives the remainder of division?",
            "points": 1.5,
        },
        {
            "id": 8,
            "difficulty": "Hard",
            "category": "Python Concepts",
            "question": "What Python keyword is used to create a generator function (instead of returning a list all at once)?\n\nExample: A function that produces values one at a time lazily.",
            "accept": ["yield"],
            "hint": "It's similar to 'return' but pauses the function instead of ending it.",
            "points": 2.0,
        },
        {
            "id": 9,
            "difficulty": "Hard",
            "category": "OOP",
            "question": "In Object-Oriented Programming, what do you call a function that is defined inside a class?\n\nA) Procedure\nB) Method\nC) Module\nD) Package",
            "accept": ["b", "method"],
            "hint": "It's a special kind of function that belongs to an object.",
            "points": 2.0,
        },
        {
            "id": 10,
            "difficulty": "Hard",
            "category": "Error Handling",
            "question": "What Python keyword is used to handle exceptions (errors) in code?\n\n```python\n___:\n    risky_operation()\nexcept Exception as e:\n    print(e)\n```\n\nWhat keyword fills the blank?",
            "accept": ["try"],
            "hint": "You 'attempt' something before catching the error.",
            "points": 2.0,
        },
    ]

    def __init__(self):
        super().__init__()
        if MyAssistantBotEnvironment._challenges is None:
            MyAssistantBotEnvironment._challenges = list(self.CHALLENGE_POOL)
            MyAssistantBotEnvironment._env_state = MyAssistantBotState()

    def reset(self, seed: Optional[int] = None, episode_id: Optional[str] = None, **kwargs: Any) -> MyAssistantBotObservation:
        MyAssistantBotEnvironment._challenges = list(self.CHALLENGE_POOL)
        MyAssistantBotEnvironment._env_state = MyAssistantBotState(episode_id=episode_id)

        ch = MyAssistantBotEnvironment._challenges[0]
        total = len(MyAssistantBotEnvironment._challenges)
        msg = (
            f"🧠 CODE TRAINER — Session Started!\n"
            f"You will be given {total} coding challenges.\n"
            f"Answer each one. You get points for correct answers.\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Challenge 1/{total}  |  {ch['difficulty']}  |  {ch['category']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{ch['question']}\n\n"
            f"💡 Hint: {ch['hint']}"
        )
        return MyAssistantBotObservation(echoed_message=msg, reward=0.01, done=False)

    def _normalized_reward(self):
        """Return reward normalized to 0.01-0.99 range."""
        st = MyAssistantBotEnvironment._env_state
        challenges = MyAssistantBotEnvironment._challenges
        max_score = sum(c['points'] for c in challenges)
        if max_score <= 0:
            return 0.5
        score = st.total_score / max_score
        # Ensure it is STRICTLY between 0 and 1 (not 0.0 and not 1.0)
        return round(min(max(score, 0.01), 0.99), 4)

    def step(self, action: MyAssistantBotAction) -> MyAssistantBotObservation:
        st = MyAssistantBotEnvironment._env_state
        challenges = MyAssistantBotEnvironment._challenges

        st.step_count += 1
        idx = st.current_challenge_index

        if idx >= len(challenges):
            return MyAssistantBotObservation(
                echoed_message="Session finished. Click Reset to start again.",
                reward=0.01, done=True
            )

        ch = challenges[idx]
        answer = action.message.strip().lower()

        # Grade the answer
        correct = any(accepted.lower() in answer for accepted in ch['accept'])

        if correct:
            st.total_score += ch['points']
            st.correct_count += 1
            # Track category-specific scores for graders
            if ch["difficulty"] == "Easy":
                st.easy_score += ch["points"]
            elif ch["difficulty"] == "Medium":
                st.medium_score += ch["points"]
            elif ch["difficulty"] == "Hard":
                st.hard_score += ch["points"]
            feedback = f"✅ CORRECT! +{ch['points']} points"
        else:
            st.wrong_count += 1
            expected = ch['accept'][0]
            feedback = f"❌ WRONG. The answer was: {expected}"

        st.current_challenge_index += 1
        
        # Calculate incremental reward for this step
        total_max_points = sum(c['points'] for c in challenges)
        current_step_reward = (ch["points"] / total_max_points) if correct else 0.0
        # Clamp it strictly between 0 and 1 just in case, but usually a single step is fine.
        current_step_reward = round(min(max(current_step_reward, 0.0), 0.99), 4)

        # Show next challenge or finish
        if st.current_challenge_index < len(challenges):
            nxt = challenges[st.current_challenge_index]
            num = st.current_challenge_index + 1
            total = len(challenges)
            msg = (
                f"{feedback}\n"
                f"Score: {st.total_score:.1f}  |  ✅ {st.correct_count}  ❌ {st.wrong_count}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Challenge {num}/{total}  |  {nxt['difficulty']}  |  {nxt['category']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{nxt['question']}\n\n"
                f"💡 Hint: {nxt['hint']}"
            )
            return MyAssistantBotObservation(
                echoed_message=msg,
                reward=current_step_reward,
                done=False
            )
        else:
            max_score = sum(c['points'] for c in challenges)
            pct = (st.total_score / max_score * 100) if max_score > 0 else 0
            if pct >= 80:
                rank = "🏆 CODE MASTER"
            elif pct >= 50:
                rank = "⭐ DEVELOPER"
            else:
                rank = "📝 BEGINNER"

            msg = (
                f"{feedback}\n\n"
                f"🏁 TRAINING COMPLETE!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Final Score: {st.total_score:.1f} / {max_score:.1f}\n"
                f"Correct: {st.correct_count}  |  Wrong: {st.wrong_count}\n"
                f"Accuracy: {pct:.0f}%\n"
                f"Rank: {rank}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            return MyAssistantBotObservation(
                echoed_message=msg,
                reward=current_step_reward,
                done=True
            )

    @property
    def state(self) -> MyAssistantBotState:
        return MyAssistantBotEnvironment._env_state