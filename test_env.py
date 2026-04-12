import requests

def test_code_trainer():
    base_url = "http://127.0.0.1:8000"
    
    print("Starting Final Verification...")
    
    # 1. Reset
    print("\n--- Step 1: RESET ---")
    try:
        response = requests.post(f"{base_url}/reset", json={})
        response.raise_for_status()
        print("Reset successful")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return
    
    # 2. Correct step
    print("\n--- Step 2: CORRECT ANSWER ---")
    response = requests.post(f"{base_url}/step", json={"action": {"message": "4"}})
    obs = response.json()
    print(f"Reward: {obs['reward']} (Float required)")
    
    # 3. Check State
    print("\n--- Step 3: GETTING STATE ---")
    response = requests.get(f"{base_url}/state")
    state = response.json()
    # If state is wrapped in a 'state' key, we check there
    s = state.get('state', state)
    print(f"Total Score Type: {type(s.get('total_score'))}")
    print(f"Total Score Value: {s.get('total_score')}")

if __name__ == "__main__":
    test_code_trainer()
