import os
import time
from typing import Optional, List

from my_assistant_bot import MyAssistantBotEnv, MyAssistantBotAction
from openai import OpenAI

# Required environment variables for inference
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# The endpoint where the environment server is running
# In the OpenEnv evaluation, this usually runs on localhost:8000
ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

# Task and benchmark info
TASK_NAME = "code-training"
BENCHMARK_NAME = "my-assistant-bot"
MAX_STEPS = 100
SUCCESS_SCORE_THRESHOLD = 0.5  # Require at least 50% to be successful

def extract_answer(llm_response: str) -> str:
    """Extract a concise answer from the LLM's response."""
    return llm_response.strip().lower()

def log_start(task: str, env: str, model: str) -> None:
    """Log START in required format."""
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    """Log STEP in required format."""
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    """Log END in required format."""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )

def main():
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN or "dummy-key"  # Some endpoints require a non-empty key even if ignored
    )
    
    # Initialize tracking variables
    rewards_list: List[float] = []
    steps_taken = 0
    total_score = 0.0
    success = False
    error_msg = None
    
    # Log START
    log_start(task=TASK_NAME, env=BENCHMARK_NAME, model=MODEL_NAME)
    
    try:
        with MyAssistantBotEnv(base_url=ENV_URL).sync() as env:
            result = env.reset()
            done = result.observation.done
            current_reward = result.observation.reward or 0.0
            
            step_num = 1
            
            while not done and step_num <= MAX_STEPS:
                obs_text = result.observation.echoed_message
                
                # Simple prompt for the LLM
                prompt = (
                    f"You are taking a coding challenge. Here is the challenge:\n"
                    f"{obs_text}\n\n"
                    f"Provide ONLY the short answer. For example: if it asks what 2+2 is, say '4'. Do not provide explanations."
                )
                
                # Make the LLM call
                try:
                    chat_completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0,
                        max_tokens=64
                    )
                    llm_response = chat_completion.choices[0].message.content or ""
                    action_msg = extract_answer(llm_response)
                except Exception as e:
                    # Fallback if API is missing or fails
                    action_msg = "print"
                    error_msg = str(e)
                
                # Take the step in the environment
                action = MyAssistantBotAction(message=action_msg)
                result = env.step(action)
                
                done = result.observation.done
                current_reward = result.observation.reward or 0.0
                
                # Track rewards
                rewards_list.append(current_reward)
                total_score += current_reward
                steps_taken = step_num
                
                # Log STEP in required format
                log_step(
                    step=step_num,
                    action=action_msg,
                    reward=current_reward,
                    done=done,
                    error=error_msg
                )
                
                step_num += 1
                time.sleep(0.5)  # Small delay to ensure stability
            
            # Calculate final score (normalize to [0, 1])
            # Assuming max possible is perfect scores on all tasks
            total_score = min(total_score, 1.0)  # Cap at 1.0
            success = total_score >= SUCCESS_SCORE_THRESHOLD
            
    except Exception as e:
        error_msg = str(e)
        total_score = 0.0
        success = False
    
    # Log END in required format (always happens)
    log_end(
        success=success,
        steps=steps_taken,
        score=total_score,
        rewards=rewards_list
    )

if __name__ == "__main__":
    main()
