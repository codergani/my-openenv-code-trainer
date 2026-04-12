import requests

def test_final():
    base_url = "http://127.0.0.1:8000"
    print("Running Final Pass Test...")
    
    try:
        # Reset
        requests.post(f"{base_url}/reset")
        
        # Step
        resp = requests.post(f"{base_url}/step", json={"action": {"message": "4"}})
        print(f"Step Result: {resp.json()['reward']}")
        
        # State
        resp = requests.get(f"{base_url}/state")
        print(f"State: {resp.json()}")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_final()
