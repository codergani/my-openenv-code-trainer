import requests
import json

def run_benchmark():
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 --- ELITE INBOX COMMANDER BENCHMARK ---")
    
    # 1. Reset
    print("\n[RESETTING ENVIRONMENT]")
    try:
        response = requests.post(f"{base_url}/reset", json={})
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Could not connect to server at {base_url}. Make sure to run 'python -m my_assistant_bot.server.app' first.")
        return

    obs = response.json()['observation']['echoed_message']
    print(obs)
    
    # Simple automated agent
    for i in range(8):
        print(f"\n[STEP {i+1}] Determining action...")
        
        # Look at the last observation to decide
        # In a real scenario, the agent would parse this.
        # Here we just fetch the state to 'cheat' for the benchmark demo or just try common keywords
        current_state = requests.get(f"{base_url}/state").json()
        
        # We'll just respond 'URGENT' if we see urgent-looking words, or 'DELETE' if spam
        if "URGENT" in obs:
            action = "URGENT"
        elif "SPAM" in obs or "iPhone" in obs or "Pills" in obs:
            action = "DELETE"
        elif "Security" in obs or "Login" in obs:
            action = "SECURITY"
        else:
            action = "WORK"
            
        print(f"Agent Action: {action}")
        
        response = requests.post(f"{base_url}/step", json={"action": {"message": action}})
        data = response.json()
        obs = data['observation']['echoed_message']
        reward = data['reward']
        done = data['done']
        
        print(obs)
        if done:
            break

    print("\n" + "="*50)
    print("BENCHMARK COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_benchmark()
