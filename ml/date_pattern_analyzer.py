import pandas as pd
import json
import os

def analyze_date_patterns():
    csv_path = 'ml/processed_data.csv'
    if not os.path.exists(csv_path):
        print("Error: processed_data.csv not found.")
        return

    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_month'] = df['date'].dt.day

    patterns = {}
    draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']

    for day in range(1, 32):
        day_data = df[df['day_of_month'] == day]
        if day_data.empty:
            continue
        
        day_patterns = {}
        for draw in draws:
            # Get top 5 most frequent numbers for this day and this draw
            top_nums = day_data[draw].value_counts().head(5)
            day_patterns[draw] = [
                {"number": int(num), "count": int(count)} 
                for num, count in top_nums.items()
            ]
        
        patterns[day] = day_patterns

    # Save to JSON
    with open('ml/historical_date_patterns.json', 'w') as f:
        json.dump(patterns, f, indent=2)
    
    print("Historical Date Patterns analyzed and saved to ml/historical_date_patterns.json")
    
    # Show some interesting findings for today (assuming 22nd)
    today_day = 22
    if today_day in patterns:
        print(f"\n--- Historical Analysis for Day {today_day} of any month ---")
        for draw in draws:
            top = patterns[today_day][draw][0] if patterns[today_day][draw] else None
            if top:
                print(f"{draw.upper()}: Most frequent is {top['number']} (hit {top['count']} times historically)")

if __name__ == "__main__":
    analyze_date_patterns()
