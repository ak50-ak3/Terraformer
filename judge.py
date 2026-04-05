import httpx
import asyncio
import time
import sys

async def fetch_node(client, name, url, payload):
    start = time.perf_counter()
    # Timeout set to 90 seconds
    resp = await client.post(url, json=payload, timeout=90.0)
    latency = time.perf_counter() - start
    data = resp.json()
    return name, latency, data.get('node_identity'), data.get('model_output')

async def run_benchmarks(iterations=10):
    endpoints = {
        "Stable": "http://localhost:4040/predict",
        "Candidate": "http://localhost:4041/predict"
    }
    payload = {"prompt": "SYSTEM_HEALTH_CHECK_001"}
    
    history = {"Stable": [], "Candidate": []}
    identities = {"Stable": None, "Candidate": None}

    print(f"\n--- Shadow-Model Benchmark: {iterations} Iterations ---")
    print(f"Timeout: 90s | Mode: Async Parallel | Device: MacBook Air\n")

    async with httpx.AsyncClient() as client:
        for i in range(1, iterations + 1):
            print(f"Running Iteration [{i}/{iterations}]...", end="\r", flush=True)
            
            # This fires both requests at the same time
            tasks = [fetch_node(client, name, url, payload) for name, url in endpoints.items()]
            results = await asyncio.gather(*tasks)

            for name, latency, identity, _ in results:
                history[name].append(latency)
                if i == 1:
                    identities[name] = identity

    # Final Statistics Calculation
    print("\n\n" + "="*60)
    print("FINAL PERFORMANCE BENCHMARK (AVERAGES)")
    print("="*60)

    avg_metrics = {}
    for name in ["Stable", "Candidate"]:
        avg_latency = sum(history[name]) / len(history[name])
        avg_metrics[name] = avg_latency
        
        bar_length = max(1, int(avg_latency)) 
        bar = "#" * bar_length
        print(f"{name:10} | Avg: {avg_latency:.4f}s {bar}")

    delta = abs(avg_metrics["Stable"] - avg_metrics["Candidate"])
    print(f"\nAverage Latency Delta: {delta:.4f}s")
    print(f"Identities: Stable ({identities['Stable']}) vs Candidate ({identities['Candidate']})")
    print("="*60)

    if identities["Stable"] != identities["Candidate"]:
        print("\nSUCCESS: Multi-node routing verified.")
    else:
        print("\nWARNING: Identical node identities detected!")

if __name__ == "__main__":
    # pip install httpx
    try:
        asyncio.run(run_benchmarks(10))
    except Exception as e:
        print(f"\nConnection Error: {e}")
        sys.exit(1)
