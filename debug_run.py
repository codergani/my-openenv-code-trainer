import subprocess
import time
import requests
import sys

def run_debug():
    print("🛠️ Starting server in background...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "my_assistant_bot.server.app", "--port", "8008"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    max_retries = 10
    started = False
    print("⌛ Waiting for server to respond on port 8008...")
    for i in range(max_retries):
        try:
            r = requests.get("http://localhost:8008/web", timeout=2)
            if r.status_code == 200:
                print("✅ Server is UP!")
                started = True
                break
        except:
            time.sleep(1)
            print(f"  Attempt {i+1}...")
    
    if not started:
        print("❌ Server failed to start in time.")
        stdout, stderr = server_proc.communicate()
        print(f"STDOUT:\n{stdout}")
        print(f"STDERR:\n{stderr}")
        server_proc.kill()
        return

    print("\n🚀 Running Benchmark...")
    try:
        # Run a single reset/step test
        resp = requests.post("http://localhost:8008/reset", json={}, timeout=5)
        print(f"Reset Response: {resp.status_code}")
        print(f"Message: {resp.json()['observation']['echoed_message'][:100]}...")
        
        resp = requests.post("http://localhost:8008/step", json={"action": {"message": "URGENT"}}, timeout=5)
        print(f"Step Response: {resp.status_code}")
        print(f"Reward: {resp.json()['reward']}")
        
        print("\n✅ DEBUG TEST PASSED!")
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        # Check if server is still alive
        if server_proc.poll() is not None:
             print("⚠️ Server actually DIED during benchmark!")
             stdout, stderr = server_proc.communicate()
             print(f"STDOUT:\n{stdout}")
             print(f"STDERR:\n{stderr}")
    finally:
        print("🛑 Closing server...")
        server_proc.terminate()
        server_proc.wait()

if __name__ == "__main__":
    run_debug()
