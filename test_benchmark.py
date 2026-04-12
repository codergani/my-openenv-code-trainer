import requests
import time

def run_benchmark():
    base_url = "http://127.0.0.1:8000"
    
    print("--- CODE TRAINER BENCHMARK ---")
    
    # 1. Reset
    print("\n[RESETTING ENVIRONMENT]")
    try:
        response = requests.post(f"{base_url}/reset", json={})
        response.raise_for_status()
    except Exception as e:
        print(f"Could not connect to server at {base_url}. Make sure to run the server first.")
        return

    data = response.json()
    obs = data['observation']['echoed_message']
    print(f"Initial Observation: {obs[:100]}...")
    
    # Pre-defined correct answers for the first few challenges
    answers = ["4", "float", "+", "b", "c"]
    
    for i, ans in enumerate(answers):
        print(f"\n[STEP {i+1}] Action: {ans}")
        
        try:
            response = requests.post(f"{base_url}/step", json={"action": {"message": ans}})
            data = response.json()
            obs = data['observation']['echoed_message']
            reward = data['reward']
            done = data['done']
            
            print(f"Reward: {reward} | Done: {done}")
            if done:
                break
        except Exception as e:
            print(f"Error during step: {e}")
            break

    print("\n" + "="*50)
    print("BENCHMARK COMPLETE")
    # Fetch final state
    state = requests.get(f"{base_url}/state").json()
    print(f"Final Total Score: {state.get('total_score')}")
    print("="*50)

if __name__ == "__main__":
    run_benchmark()
