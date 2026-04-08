import requests

def test_magical_environment():
    base_url = "http://127.0.0.1:8000"
    
    print("🪄 Starting Magical Test Suite...")
    
    # 1. Reset
    print("\n--- Step 1: RESET ---")
    response = requests.post(f"{base_url}/reset", json={})
    print(f"Server says: {response.json()['observation']['echoed_message']}")
    
    # 2. Email 1: URGENT
    print("\n--- Step 2: ACTION (URGENT) ---")
    # Email 1 is URGENT: Server Down
    response = requests.post(f"{base_url}/step", json={"action": {"message": "This is URGENT"}})
    obs = response.json()
    print(f"Observation: {obs['observation']['echoed_message'][:60]}...")
    print(f"Reward: {obs['reward']} (Expected +1.0)")
    
    # 3. Email 2: SPAM
    print("\n--- Step 3: ACTION (DELETE SPAM) ---")
    # Email 2 is SPAM: Win a Free iPhone
    # Respond with 'delete' for extra points!
    response = requests.post(f"{base_url}/step", json={"action": {"message": "Please DELETE this spam"}})
    obs = response.json()
    print(f"Observation: {obs['observation']['echoed_message'][:60]}...")
    print(f"Reward: {obs['reward']} (Expected +2.2 total)")
    
    # 4. Check State
    print("\n--- Step 4: GETTING STATE ---")
    response = requests.get(f"{base_url}/state")
    print(f"Current State: {response.json()}")

if __name__ == "__main__":
    test_magical_environment()
