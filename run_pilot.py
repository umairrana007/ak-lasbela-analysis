import pandas as pd
import os
from datetime import datetime

# 1. Configuration (Line 1 Master Set: {0, 1, 2, 5, 7, 9})
MASTER_DIGITS = [0, 1, 2, 5, 7, 9]
LINE_1_PAIRS = [
    ('712', '059'), ('710', '259'), ('715', '209'), ('719', '205'),
    ('120', '759'), ('105', '729'), ('109', '725'), ('207', '915'),
    ('907', '215'), ('507', '219')
]

GAMES = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
WAIT_DAYS = 5 # Prediction ke baad 5 din tak wait karenge

def format_val(val):
    try:
        # Check if it's numeric
        s_val = str(val).strip()
        if pd.isna(val) or s_val == "" or not s_val.replace('.','',1).isdigit():
            return "xx"
        return f"{int(float(val)):02d}"
    except:
        return "xx"

def get_digits(jodi):
    if jodi == "xx" or len(str(jodi)) < 2: return set()
    try:
        return {int(str(jodi)[0]), int(str(jodi)[1])}
    except:
        return set()

# 2. Data Load & Filter (1 Feb to 19 April)
data_path = "2023-2024-2025-2026 complete data.txt"
if not os.path.exists(data_path):
    print(f"ERROR: Data file not found at {data_path}")
    exit()

# Using on_bad_lines='skip' to handle irregular rows
df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

# Filter for Pilot Project (2026)
start_date = datetime(2026, 2, 1)
end_date = datetime(2026, 4, 19)
df_pilot = df[(df['Date_dt'] >= start_date) & (df['Date_dt'] <= end_date)].copy().reset_index(drop=True)

# Format numeric strings
for g in GAMES:
    df_pilot[f'{g}_s'] = df_pilot[g].apply(format_val)

print(f"--- Pilot Project Analysis ---")
print(f"Records: {len(df_pilot)} days (Feb 1 to April 19, 2026)\n")

# 3. Prediction Functions
results = []

# Build Maps for Vertical Under
trigger_map = {}
for trig, targ in LINE_1_PAIRS:
    trigger_map[trig[:2]] = (targ, trig)
    trigger_map[trig[1:]] = (targ, trig)

# Scan for Vertical Under
for i in range(len(df_pilot)):
    today = df_pilot.iloc[i]
    for g in GAMES:
        val = today[f'{g}_s']
        if val in trigger_map:
            target, full_trig = trigger_map[val]
            
            # Check for Hit in next 5 days (Vertical)
            hit_row = None
            for d in range(1, WAIT_DAYS + 1):
                if i + d < len(df_pilot):
                    future = df_pilot.iloc[i+d]
                    f_val = future[f'{g}_s']
                    if f_val in [target[:2], target[1:], target[0]+target[2]]:
                        hit_row = future
                        break
            
            if hit_row is not None:
                results.append({
                    'Date': today['date'], 'Game': g, 'Trigger_Jodi': val, 
                    'Target_Set': target, 'Status': 'HIT', 'Hit_Date': hit_row['date'], 'Hit_Val': hit_row[f'{g}_s']
                })
            else:
                results.append({
                    'Date': today['date'], 'Game': g, 'Trigger_Jodi': val, 
                    'Target_Set': target, 'Status': 'WAIT', 'Hit_Date': '-', 'Hit_Val': '-'
                })

# 4. Lari Chain Logic (Same Day + Next 2 days)
lari_results = []
for g in GAMES:
    for i in range(len(df_pilot) - 2):
        d1, d2, d3 = df_pilot.iloc[i], df_pilot.iloc[i+1], df_pilot.iloc[i+2]
        dg1, dg2, dg3 = get_digits(d1[f'{g}_s']), get_digits(d2[f'{g}_s']), get_digits(d3[f'{g}_s'])
        
        # Check if all 3 are from Master Set
        if dg1.issubset(MASTER_DIGITS) and dg2.issubset(MASTER_DIGITS) and dg3.issubset(MASTER_DIGITS) and len(dg1)>0 and len(dg2)>0 and len(dg3)>0:
            
            hit_info = None
            # Check Same Day (d3) or Next 2 days
            for d in range(0, 3): 
                if i + 2 + d < len(df_pilot):
                    check_row = df_pilot.iloc[i+2+d]
                    check_val = check_row[f'{g}_s']
                    for _, target in LINE_1_PAIRS:
                        if check_val in [target[:2], target[1:], target[0]+target[2]]:
                            hit_info = check_row
                            break
                    if hit_info is not None: break
            
            lari_results.append({
                'Date': d3['date'], 'Game': g, 
                'Sequence': f"{d1[f'{g}_s']}->{d2[f'{g}_s']}->{d3[f'{g}_s']}", 
                'Status': 'HIT' if hit_info is not None else 'WAIT',
                'Hit_Date': hit_info['date'] if hit_info is not None else '-'
            })

# Display Summary
v_df = pd.DataFrame(results)
l_df = pd.DataFrame(lari_results)

print("VERTICAL UNDER SUMMARY:")
if not v_df.empty:
    print(v_df['Status'].value_counts())
    print("\nRecent Vertical Hits:")
    print(v_df[v_df['Status'] == 'HIT'].tail(10).to_string(index=False))
else:
    print("No vertical triggers found.")

print("\n" + "="*50)
print("LARI CHAIN SUMMARY:")
if not l_df.empty:
    print(l_df['Status'].value_counts())
    print("\nRecent Lari Hits:")
    print(l_df[l_df['Status'] == 'HIT'].tail(10).to_string(index=False))
else:
    print("No lari chains found.")
