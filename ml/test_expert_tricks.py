import pandas as pd
import numpy as np
from data_loader import load_all_data

def test_satta_tricks():
    print("Fetching data for expert trick analysis...")
    df = load_all_data()
    if df.empty:
        print("No data found!")
        return

    # Sort by date
    df = df.sort_values('date')
    
    # 1. CUT NUMBER THEORY
    # 0-5, 1-6, 2-7, 3-8, 4-9
    cut_map = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', '5':'0', '6':'1', '7':'2', '8':'3', '9':'4'}
    
    def get_cut(val):
        if pd.isna(val) or val == '--': return '--'
        s = str(val).zfill(2)
        return cut_map.get(s[0], '0') + cut_map.get(s[1], '0')

    # 2. OTC (Open To Close) - Simple Addition Trick
    # Prediction = (Last Result Digits Sum)
    def calculate_otc(val):
        if pd.isna(val) or val == '--': return 0
        s = str(val).zfill(2)
        return (int(s[0]) + int(s[1])) % 10

    results = []
    
    # We test on the last 100 records
    test_df = df.tail(100).copy()
    
    print("\n--- Testing Expert Tricks on Last 100 Draws ---")
    
    for col in ['gm', 'ls1', 'ak', 'ls2', 'ls3']:
        hits_cut = 0
        hits_otc = 0
        
        for i in range(1, len(test_df)):
            prev_val = test_df.iloc[i-1][col]
            curr_val = test_df.iloc[i][col]
            
            if prev_val == '--' or curr_val == '--': continue
            
            # Trick A: Does the current number contain the 'Cut' digit of the previous?
            cut_val = get_cut(prev_val)
            if cut_val[0] in str(curr_val) or cut_val[1] in str(curr_val):
                hits_cut += 1
                
            # Trick B: OTC Sum Match
            otc_pred = calculate_otc(prev_val)
            if str(otc_pred) in str(curr_val):
                hits_otc += 1
        
        print(f"Column {col.upper()}:")
        print(f"  - Cut Theory Success: {hits_cut}%")
        print(f"  - OTC Sum Success: {hits_otc}%")

if __name__ == "__main__":
    test_satta_tricks()
