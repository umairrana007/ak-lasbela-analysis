import pandas as pd
import numpy as np
from data_loader import load_all_data

def discover_patterns():
    df = load_all_data()
    df = df.sort_values('date')
    
    print(f"Analyzing {len(df)} records for hidden patterns...")
    
    # 1. Check for "Total Sum" patterns (Sum of two consecutive draws)
    # Example: Does GM + LS1 yesterday predict something today?
    df['gm_ls1_sum'] = (df['gm'] + df['ls1']) % 100
    df['ak_target'] = df['ak'].shift(-1)
    
    sum_matches = (df['gm_ls1_sum'] == df['ak_target']).sum()
    print(f"Pattern 1 (Cross-Sum): GM+LS1 predicting next day AK: {sum_matches} matches found.")

    # 2. Check for Mirror patterns
    def get_mirror(n):
        return (n + 50) % 100
    
    df['gm_mirror'] = df['gm'].apply(get_mirror)
    mirror_matches = (df['gm_mirror'] == df['ak']).sum()
    print(f"Pattern 2 (Mirror Jump): GM Mirror matching AK same day: {mirror_matches} matches found.")

    # 3. Check for "Follow-up" patterns (Transcripts style)
    # If 85 comes, what comes next?
    follow_ups = {}
    for i in range(len(df)-1):
        prev = df.iloc[i]['ak']
        nxt = df.iloc[i+1]['ak']
        if prev not in follow_ups: follow_ups[prev] = []
        follow_ups[prev].append(nxt)
    
    # Find top 5 follow-up pairs
    print("\nPattern 3 (Sequence Follow-ups):")
    scored_follows = []
    for num, follows in follow_ups.items():
        if len(follows) > 10:
            most_common = pd.Series(follows).value_counts().idxmax()
            count = pd.Series(follows).value_counts().max()
            pct = (count / len(follows)) * 100
            scored_follows.append((num, most_common, count, pct))
    
    scored_follows.sort(key=lambda x: x[3], reverse=True)
    for s in scored_follows[:5]:
        print(f"If {int(s[0])} appears in AK, then {int(s[1])} appears next {s[3]:.1f}% of the time.")

    # 4. Weekday Fix Numbers (Statistical)
    print("\nPattern 4 (Statistical Weekday Fixes):")
    df['day_name'] = pd.to_datetime(df['date']).dt.day_name()
    for day in df['day_name'].unique():
        top_num = df[df['day_name'] == day]['ak'].value_counts().idxmax()
        count = df[df['day_name'] == day]['ak'].value_counts().max()
        print(f"Top number for {day}: {int(top_num)} (appeared {count} times)")

if __name__ == "__main__":
    discover_patterns()
