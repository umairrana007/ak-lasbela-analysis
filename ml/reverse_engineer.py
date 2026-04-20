import pandas as pd
import numpy as np
from data_loader import load_all_data

def reverse_engineer_formulas():
    df = load_all_data()
    if df.empty: return
    
    print(f"AI Reverse-Engineering: Scanning {len(df)} days for mathematical correlations...")
    
    def get_digits(n):
        s = str(int(n)).zfill(2)
        return int(s[0]), int(s[1])

    # --- Strategy A: The "Sum to Open" Correlation ---
    # Formula: (Yesterday GM Open + Yesterday LS1 Close) % 10 == Today AK Open
    matches_a = 0
    for i in range(1, len(df)):
        g_o, g_c = get_digits(df.iloc[i-1]['gm'])
        l_o, l_c = get_digits(df.iloc[i-1]['ls1'])
        target_o, target_c = get_digits(df.iloc[i]['ak'])
        
        if (g_o + l_c) % 10 == target_o:
            matches_a += 1
    
    print(f"Formula A (Cross-Sum): (Prev GM Open + Prev LS1 Close) -> Today AK Open: {matches_a} matches ({(matches_a/len(df))*100:.1f}%)")

    # --- Strategy B: The "Difference" Logic ---
    # Formula: |GM - LS1| last digit == AK Haruf
    matches_b = 0
    for i in range(len(df)):
        diff = abs(df.iloc[i]['gm'] - df.iloc[i]['ls1']) % 10
        target_o, target_c = get_digits(df.iloc[i]['ak'])
        if diff == target_o or diff == target_c:
            matches_b += 1
            
    print(f"Formula B (Draw Diff): |GM - LS1| Last Digit -> Today AK Haruf: {matches_b} matches ({(matches_b/len(df))*100:.1f}%)")

    # --- Strategy C: The "Date Multiplier" ---
    # Formula: (Date * 2) % 10 == AK Haruf
    matches_c = 0
    for i in range(len(df)):
        date_digit = (df.iloc[i]['date'].day * 2) % 10
        target_o, target_c = get_digits(df.iloc[i]['ak'])
        if date_digit == target_o or date_digit == target_c:
            matches_c += 1
            
    print(f"Formula C (Date Multiplier): (Date * 2) Last Digit -> Today AK Haruf: {matches_c} matches ({(matches_c/len(df))*100:.1f}%)")

    # --- Strategy D: The "Diagonal Repeat" ---
    # Formula: Yesterday LS1 == Today AK
    matches_d = 0
    for i in range(1, len(df)):
        if df.iloc[i-1]['ls1'] == df.iloc[i]['ak']:
            matches_d += 1
    print(f"Formula D (Diagonal Repeat): Prev LS1 == Today AK: {matches_d} matches ({(matches_d/len(df))*100:.1f}%)")

if __name__ == "__main__":
    reverse_engineer_formulas()
