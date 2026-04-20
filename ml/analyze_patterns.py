import pandas as pd
import json
import os

def discover_patterns():
    csv_path = 'ml/processed_data.csv'
    if not os.path.exists(csv_path):
        print("Data not found. Run data_loader.py first.")
        return

    df = pd.read_csv(csv_path)
    targets = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Convert to strings for consistent matching
    for t in targets:
        df[t] = df[t].astype(int).astype(str).str.zfill(2)

    found_rules = {}

    print("Analyzing sequences...")
    for t1 in targets:
        for t2 in targets:
            # Look for correlations: if t1 today is X, what is t2 tomorrow?
            # We use t2_lag1 which is actually t2 of today if we shift back, 
            # but let's just use shift(1) manually for clarity.
            
            cols = [t1] if t1 == t2 else [t1, t2]
            temp_df = df[list(set(cols))].copy()
            temp_df['next_val'] = df[t2].shift(-1)
            
            # Group by t1 and find most frequent next_val
            for val in temp_df[t1].unique():
                nexts = temp_df[temp_df[t1] == val]['next_val'].dropna()
                if len(nexts) > 5: # Need enough occurrences
                    top = nexts.value_counts().head(3)
                    # If the top frequency is significantly higher than random
                    if top.iloc[0] > (len(nexts) * 0.15): # More than 15% frequency
                        rule_key = f"{t1}_{val}"
                        if rule_key not in found_rules:
                            found_rules[rule_key] = []
                        found_rules[rule_key].extend([int(x) for x in top.index.tolist()])

    # Deduplicate and limit
    final_rules = {k: list(set(v))[:5] for k, v in found_rules.items() if len(v) > 0}
    
    # Extract only the strongest ones for the simple expert_followups format (val -> [nexts])
    # For now, let's just group by the value itself regardless of source draw
    simplified = {}
    for k, v in found_rules.items():
        val = k.split('_')[1]
        if val not in simplified:
            simplified[val] = []
        simplified[val].extend(v)
    
    final_simplified = {k: list(set(v))[:6] for k, v in simplified.items()}

    with open('ml/discovered_patterns.json', 'w') as f:
        json.dump(final_simplified, f, indent=2)
    
    print(f"Found {len(final_simplified)} strong patterns based on historical data.")
    return final_simplified

if __name__ == "__main__":
    discover_patterns()
