import pandas as pd
import numpy as np

def analyze_trick():
    df = pd.read_csv('c:/Users/Muhammad.Umair/Desktop/akwebapp/ml/processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    results = []
    
    # Iterate through days (except the last one)
    for i in range(len(df) - 1):
        current_day = df.iloc[i]
        next_day = df.iloc[i+1]
        
        # GM Open + LS3 Open
        # Assuming open is the tens digit
        try:
            gm_val = int(current_day['gm'])
            ls3_val = int(current_day['ls3'])
            
            gm_open = gm_val // 10
            ls3_open = ls3_val // 10
            
            sum_val = gm_open + ls3_open
            
            # What are we looking for in next_day?
            # 1. The sum itself (e.g. 12)
            # 2. Digits of the sum (1 and 2)
            # 3. Sum of digits of sum (1+2=3)
            
            next_draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
            found_sum = False
            found_digits = []
            
            # For 12, digits are 1 and 2
            # But the user might mean the last digit (2) or the individual digits.
            # "NEXT DAY 1 NUMBER ZAROOR ATA HAI" usually implies a Haroof (digit).
            # Let's check both digits.
            
            sum_str = str(sum_val).zfill(2)
            d1 = int(sum_str[0]) if len(sum_str) > 1 else None
            d2 = int(sum_str[-1])
            
            for draw in next_draws:
                val = int(next_day[draw])
                v_open = val // 10
                v_close = val % 10
                
                if val == sum_val:
                    found_sum = True
                
                # Check d2 (the last digit of sum)
                if v_open == d2: found_digits.append(f"{draw}_OPEN_d2")
                if v_close == d2: found_digits.append(f"{draw}_CLOSE_d2")
                
                # Check d1 (the first digit of sum)
                if d1 is not None:
                    if v_open == d1: found_digits.append(f"{draw}_OPEN_d1")
                    if v_close == d1: found_digits.append(f"{draw}_CLOSE_d1")

            results.append({
                "date": current_day['date'],
                "sum": sum_val,
                "hit_any_digit": len(found_digits) > 0,
                "hit_sum": found_sum,
                "hit_digits": list(set(found_digits))
            })
        except:
            continue

    res_df = pd.DataFrame(results)
    if len(res_df) == 0:
        print("No data to analyze.")
        return

    print(f"Total Days Analyzed: {458}")
    print(f"Full Number (Sum) Hit Rate: {res_df['hit_sum'].mean() * 100:.2f}%")
    print(f"At Least One Digit Hits (Anywhere): {res_df['hit_any_digit'].mean() * 100:.2f}%")
    
    digit_hits = {}
    for hits in res_df['hit_digits']:
        for h in hits:
            digit_hits[h] = digit_hits.get(h, 0) + 1
            
    print("\nTop 10 Pattern Hits (By Draw/Location/Digit):")
    sorted_hits = sorted(digit_hits.items(), key=lambda x: x[1], reverse=True)
    for k, v in sorted_hits[:20]:
        print(f"{k}: {v} hits ({v/len(res_df)*100:.2f}%)")

if __name__ == "__main__":
    analyze_trick()
