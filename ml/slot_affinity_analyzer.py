import pandas as pd
import json
import os
from collections import defaultdict

def analyze_slot_affinity():
    processed_data_path = 'ml/processed_data.csv'
    if not os.path.exists(processed_data_path):
        print("Processed data not found.")
        return

    df = pd.read_csv(processed_data_path)
    
    # Define slots
    slots = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Load expert rules
    with open('ml/expert_rules.json', 'r') as f:
        rules = json.load(f)

    expert_followups = rules.get('expert_followups', {})
    
    # Results structure: {trigger: {slot: count}}
    slot_hits = defaultdict(lambda: defaultdict(int))
    trigger_totals = defaultdict(int)
    
    # Flatten sequence with slot metadata
    # List of (value, slot_name, day_offset)
    sequence = []
    for day_idx, row in df.iterrows():
        for slot in slots:
            sequence.append({
                'val': int(row[slot]),
                'slot': slot,
                'day': day_idx
            })

    print("\nCalculating Slot Affinity (Where do targets hit most?)...")

    for trigger, followups in expert_followups.items():
        trigger_int = int(trigger)
        
        for i in range(len(sequence)):
            if sequence[i]['val'] == trigger_int:
                trigger_totals[trigger] += 1
                
                # Search next 10 slots
                for j in range(i + 1, min(i + 11, len(sequence))):
                    if sequence[j]['val'] in followups:
                        target_slot = sequence[j]['slot']
                        slot_hits[trigger][target_slot] += 1
                        break # Count only the first hit

    # Prepare for JSON
    affinity_rules = {}
    for trigger, hits in slot_hits.items():
        total_hits = sum(hits.values())
        # Sort slots by probability
        sorted_slots = sorted(hits.items(), key=lambda x: x[1], reverse=True)
        affinity_rules[trigger] = {
            "best_slots": [s[0].upper() for s in sorted_slots],
            "probabilities": {s[0].upper(): round(s[1]/total_hits*100, 2) for s in sorted_slots}
        }

    with open('ml/slot_affinity_rules.json', 'w') as f:
        json.dump(affinity_rules, f, indent=2)

    print("="*70)
    print(f"\nSlot affinity rules saved to ml/slot_affinity_rules.json")

if __name__ == "__main__":
    analyze_slot_affinity()
