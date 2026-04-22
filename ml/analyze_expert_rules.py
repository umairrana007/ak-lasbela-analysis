import pandas as pd
import json
import os
import numpy as np

def analyze_hits():
    # Load data
    processed_data_path = 'ml/processed_data.csv'
    if not os.path.exists(processed_data_path):
        print("Processed data not found. Please run data_loader.py first.")
        return

    df = pd.read_csv(processed_data_path)
    
    # Flatten the data to a sequential list of numbers
    # Each row has gm, ls1, ak, ls2, ls3 (5 slots)
    sequence = []
    for _, row in df.iterrows():
        sequence.extend([int(row['gm']), int(row['ls1']), int(row['ak']), int(row['ls2']), int(row['ls3'])])

    # Load expert rules
    with open('ml/expert_rules.json', 'r') as f:
        rules = json.load(f)

    expert_followups = rules.get('expert_followups', {})
    
    results = {}

    print("\n" + "="*80)
    print(f"{'TRIGGER':<10} | {'HITS/TOTAL':<12} | {'HIT RATE':<10} | {'AVG DELAY (DAYS)':<18} | {'TARGETS'}")
    print("-" * 80)

    for trigger, followups in expert_followups.items():
        trigger_int = int(trigger)
        occurrences = [i for i, x in enumerate(sequence) if x == trigger_int]
        
        if not occurrences:
            continue
            
        hits = 0
        total = 0
        delays = []
        
        for idx in occurrences:
            # Check the next 15 draws (approx 3 days)
            window = sequence[idx + 1 : idx + 16]
            if not window:
                continue
            
            total += 1
            # Check if any of the followups are in the window
            hit_found = False
            for step, num in enumerate(window):
                if num in followups:
                    hits += 1
                    delays.append((step + 1) / 5.0) # Convert draw steps to days (5 draws/day)
                    hit_found = True
                    break
        
        hit_rate = (hits / total * 100) if total > 0 else 0
        avg_delay = np.mean(delays) if delays else 0
        
        results[trigger] = {
            "hits": hits, 
            "total": total, 
            "rate": f"{hit_rate:.2f}%",
            "avg_delay_days": round(avg_delay, 2)
        }
        
        targets_str = ", ".join(map(str, followups[:5])) + ("..." if len(followups) > 5 else "")
        print(f"{trigger:<10} | {hits:>4}/{total:<7} | {hit_rate:>8.2f}% | {avg_delay:>16.2f} | {targets_str}")

    print("="*80)

    # Save results
    with open('ml/expert_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis saved to ml/expert_analysis_results.json")

if __name__ == "__main__":
    analyze_hits()
