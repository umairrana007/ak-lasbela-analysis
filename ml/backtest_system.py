import pandas as pd
import json
import os
from datetime import timedelta

def backtest():
    print("--- Starting 1-Year System Backtest ---")
    csv_path = 'ml/processed_data.csv'
    rules_path = 'ml/expert_rules.json'
    affinity_path = 'ml/slot_affinity_rules.json'

    if not os.path.exists(csv_path) or not os.path.exists(rules_path):
        print("Required files missing.")
        return

    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['date'])

    with open(rules_path, 'r') as f:
        rules = json.load(f)
    expert_followups = rules.get('expert_followups', {})

    affinity_rules = {}
    if os.path.exists(affinity_path):
        with open(affinity_path, 'r') as f:
            affinity_rules = json.load(f)

    # Filter last 1 year of data
    last_date = df['date'].max()
    start_date = last_date - timedelta(days=365)
    test_df = df[df['date'] >= start_date].copy()
    
    total_opportunities = 0
    total_hits = 0
    slot_hits = 0
    
    results = []

    # Iterate through each draw to find triggers
    # We flatten the data into a sequence of draws
    flat_draws = []
    for _, row in df.iterrows():
        for slot in ['gm', 'ls1', 'ak', 'ls2', 'ls3']:
            flat_draws.append({
                'val': int(row[slot]),
                'date': row['date'],
                'slot': slot,
                'idx': len(flat_draws)
            })

    # Only test triggers that occurred in the last year
    start_idx = 0
    for i, d in enumerate(flat_draws):
        if d['date'] >= start_date:
            start_idx = i
            break

    print(f"Testing from index {start_idx} to {len(flat_draws)}...")

    for i in range(start_idx, len(flat_draws) - 15): # 15 draws lookahead (~3 days)
        draw = flat_draws[i]
        trigger = str(draw['val']).zfill(2)
        
        if trigger in expert_followups:
            total_opportunities += 1
            targets = expert_followups[trigger]
            
            # Look ahead next 10 draws (2 days)
            lookahead = flat_draws[i+1 : i+11]
            found_hit = False
            found_slot_hit = False
            
            # Get best slots for this trigger from affinity rules
            best_slots = affinity_rules.get(trigger, {}).get('best_slots', [])
            
            for f_draw in lookahead:
                if int(f_draw['val']) in [int(t) for t in targets]:
                    found_hit = True
                    # Check if it hit in a recommended slot
                    if f_draw['slot'].upper() in [s.upper() for s in best_slots]:
                        found_slot_hit = True
                    break
            
            if found_hit:
                total_hits += 1
            if found_slot_hit:
                slot_hits += 1

    accuracy = (total_hits / total_opportunities * 100) if total_opportunities > 0 else 0
    slot_accuracy = (slot_hits / total_opportunities * 100) if total_opportunities > 0 else 0

    print("\n" + "="*40)
    print(f"BACKTEST RESULTS (LAST 1 YEAR)")
    print("="*40)
    print(f"Total Triggers Found:    {total_opportunities}")
    print(f"Total Hits (Any Slot):   {total_hits} ({accuracy:.2f}%)")
    print(f"Slot Accuracy (Timing):  {slot_hits} ({slot_accuracy:.2f}%)")
    print("="*40)
    print("Note: Slot Accuracy is high when the number hits in one of the Top 3 predicted draws.")

if __name__ == "__main__":
    backtest()
