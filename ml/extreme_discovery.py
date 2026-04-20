import pandas as pd
import numpy as np
from data_loader import load_all_data

def extreme_discovery():
    df = load_all_data()
    if df.empty: return
    
    print(f"AI Super-Detective Mode: Analyzing {len(df)} days of results...")
    
    # --- Trick 1: The "Haruf Fusion" (Open + Close relationships) ---
    def get_digits(n):
        s = str(int(n)).zfill(2)
        return int(s[0]), int(s[1])

    matches_fusion = 0
    for i in range(1, len(df)):
        prev_gm_open, prev_gm_close = get_digits(df.iloc[i-1]['gm'])
        curr_ak_open, curr_ak_close = get_digits(df.iloc[i]['ak'])
        
        # Check if yesterday's GM open/close appears in today's AK
        if prev_gm_open in [curr_ak_open, curr_ak_close] or prev_gm_close in [curr_ak_open, curr_ak_close]:
            matches_fusion += 1
            
    print(f"Trick Found (Haruf Fusion): Yesterday's GM digits appeared in Today's AK {matches_fusion} times ({(matches_fusion/len(df))*100:.1f}% success).")

    # --- Trick 2: The "Date Math" Trick ---
    matches_date = 0
    for i in range(len(df)):
        date_val = df.iloc[i]['date'].day
        ak_val = df.iloc[i]['ak']
        ak_o, ak_c = get_digits(ak_val)
        
        # Simple Date-Haruf relation
        if date_val % 10 == ak_o or date_val % 10 == ak_c:
            matches_date += 1
            
    print(f"Trick Found (Date-Haruf): Current Date digit matches AK Haruf {matches_date} times ({(matches_date/len(df))*100:.1f}% success).")

    # --- Trick 3: The "Draw Addition" (GM + LS1 = AK Haruf) ---
    matches_add = 0
    for i in range(len(df)):
        gm = df.iloc[i]['gm']
        ls1 = df.iloc[i]['ls1']
        ak = df.iloc[i]['ak']
        total = (gm + ls1) % 10
        ak_o, ak_c = get_digits(ak)
        
        if total == ak_o or total == ak_c:
            matches_add += 1
            
    print(f"Trick Found (Addition Haruf): (GM + LS1) Last Digit matches AK Haruf {matches_add} times ({(matches_add/len(df))*100:.1f}% success).")

    # --- Trick 4: The "Mirror Follower" ---
    def mirror(n): return (n + 5) % 10
    matches_mirror = 0
    for i in range(1, len(df)):
        prev_ak = df.iloc[i-1]['ak']
        curr_ak = df.iloc[i]['ak']
        p_o, p_c = get_digits(prev_ak)
        c_o, c_c = get_digits(curr_ak)
        
        if mirror(p_o) in [c_o, c_c] or mirror(p_c) in [c_o, c_c]:
            matches_mirror += 1
            
    print(f"Trick Found (Mirror Follow): Yesterday's AK Mirror digit appeared in Today's AK {matches_mirror} times ({(matches_mirror/len(df))*100:.1f}% success).")

if __name__ == "__main__":
    extreme_discovery()
