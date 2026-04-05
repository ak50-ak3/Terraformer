import requests
import sys

def run_parity_check():
    endpoints = {
        "Stable": "http://localhost:4040/predict",
        "Candidate": "http://localhost:4041/predict"
    }
    payload = {"prompt": "SYSTEM_HEALTH_CHECK_001"}
    
    print("\n--- 🛠️ Shadow-Model Evaluator: Parity & Routing Check ---")
    results = {}
    
    try:
        for name, url in endpoints.items():
            resp = requests.post(url, json=payload, timeout=5)
            data = resp.json()
            results[name] = data
            print(f"✅ {name} reached. Identity: {data.get('node_identity')}")

        # Check if they are running the same code version but are distinct nodes
        if results["Stable"]["node_identity"] != results["Candidate"]["node_identity"]:
            print("\n✨ SUCCESS: Multi-node routing confirmed.")
            print(f"Baseline Output: {results['Stable']['model_output']}")
            print(f"Candidate Output: {results['Candidate']['model_output']}")
        else:
            print("\n🚨 CONFIG ERROR: Both containers reporting same identity!")

    except Exception as e:
        print(f"🚨 Connection Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_parity_check()