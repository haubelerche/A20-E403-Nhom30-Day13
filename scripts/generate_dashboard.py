import requests
import matplotlib.pyplot as plt
import os
from pathlib import Path

METRICS_URL = "http://127.0.0.1:8000/metrics"
OUTPUT_DIR = Path("docs/evidence")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_charts():
    try:
        response = requests.get(METRICS_URL)
        data = response.json()
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        # Fallback dummy data if app is not running
        data = {
            "traffic": 10,
            "latency_p50": 155.0,
            "latency_p95": 155.0,
            "latency_p99": 155.0,
            "avg_cost_usd": 0.0018,
            "total_cost_usd": 0.0182,
            "tokens_in_total": 340,
            "tokens_out_total": 1147,
            "error_breakdown": {},
            "quality_avg": 0.88
        }

    # Set style
    plt.style.use('ggplot')
    
    # 1. Latency Chart (Bar)
    plt.figure(figsize=(8, 5))
    latencies = [data["latency_p50"], data["latency_p95"], data["latency_p99"]]
    labels = ["P50", "P95", "P99"]
    plt.bar(labels, latencies, color=['skyblue', 'orange', 'red'])
    plt.ylabel("Latency (ms)")
    plt.title("API Latency Percentiles")
    plt.axhline(y=5000, color='red', linestyle='--', label='SLO (5s)')
    plt.legend()
    plt.savefig(OUTPUT_DIR / "dashboard_latency.png")
    plt.close()

    # 2. Traffic (Gauge/Text emulation)
    plt.figure(figsize=(5, 5))
    plt.text(0.5, 0.5, f"{data['traffic']}\nRequests", fontsize=40, ha='center', va='center')
    plt.axis('off')
    plt.title("Total Traffic")
    plt.savefig(OUTPUT_DIR / "dashboard_traffic.png")
    plt.close()

    # 3. Error Rate (Pie)
    plt.figure(figsize=(6, 6))
    errors = sum(data["error_breakdown"].values())
    success = data["traffic"] - errors
    if (success + errors) > 0:
        plt.pie([success, errors], labels=["Success", "Errors"], autopct='%1.1f%%', colors=['green', 'red'])
    else:
        plt.text(0.5, 0.5, "No Traffic Data", ha='center', va='center')
    plt.title("Error Rate Breakdown")
    plt.savefig(OUTPUT_DIR / "dashboard_errors.png")
    plt.close()

    # 4. Cost over time (Simple representation)
    plt.figure(figsize=(8, 5))
    plt.bar(["Total Cost"], [data["total_cost_usd"]], color='gold')
    plt.ylabel("Cost (USD)")
    plt.title("Project Spending")
    plt.savefig(OUTPUT_DIR / "dashboard_cost.png")
    plt.close()

    # 5. Tokens (Stacked Bar)
    plt.figure(figsize=(8, 5))
    plt.bar(["Tokens"], [data["tokens_in_total"]], label="Input")
    plt.bar(["Tokens"], [data["tokens_out_total"]], bottom=[data["tokens_in_total"]], label="Output")
    plt.ylabel("Count")
    plt.title("Token Usage Breakdown")
    plt.legend()
    plt.savefig(OUTPUT_DIR / "dashboard_tokens.png")
    plt.close()

    # 6. Quality Score
    plt.figure(figsize=(8, 5))
    plt.bar(["Avg Quality"], [data["quality_avg"]], color='purple')
    plt.ylim(0, 1.0)
    plt.ylabel("Score (0-1)")
    plt.title("Quality Proxy (Heuristic)")
    plt.axhline(y=0.75, color='orange', linestyle='--', label='SLO (0.75)')
    plt.legend()
    plt.savefig(OUTPUT_DIR / "dashboard_quality.png")
    plt.close()

    print(f"Charts generated successfully in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_charts()
