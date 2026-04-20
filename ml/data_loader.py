import pandas as pd
import json
import os
import re
from datetime import datetime
from google.cloud import firestore

def parse_records_txt(file_path):
    if not os.path.exists(file_path):
        return []
    
    records = []
    current_year = 2025
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line: continue
            
            if "2026" in line:
                current_year = 2026
            
            # Flexible regex for 1 or 2 dots: (\d{2}/\d{2})\.*(.*?)\.*(\w+)
            # But we need to be careful with dots between numbers.
            # Updated regex: matches date, then separator, then numbers with dots, then separator, then day.
            match = re.search(r'(\d{2}/\d{2})\.+([\d\.]+)\.+(\w+)', line)
            if match:
                date_short = match.group(1)
                nums_str = match.group(2)
                day = match.group(3)
                
                nums = [n for n in nums_str.split('.') if n]
                
                if len(nums) == 5:
                    day_m = date_short.split('/')
                    full_date = f"{current_year}-{day_m[1]}-{day_m[0]}"
                    records.append({
                        "date": full_date,
                        "gm": nums[0],
                        "ls1": nums[1],
                        "ak": nums[2],
                        "ls2": nums[3],
                        "ls3": nums[4],
                        "day": day
                    })
    return records

def fetch_firestore_data():
    try:
        import glob
        key_files = glob.glob("*.json")
        key_file = next((f for f in key_files if "firebase-adminsdk" in f), None)
        creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        if key_file:
            db = firestore.Client.from_service_account_json(key_file)
        elif creds_json:
            with open("temp_creds.json", "w") as f:
                f.write(creds_json)
            db = firestore.Client.from_service_account_json("temp_creds.json")
        else:
            db = firestore.Client(project='ak-analysis-system-umair')
            
        docs = db.collection('draws').stream()
        records = []
        for doc in docs:
            d = doc.to_dict()
            records.append({
                "date": d.get('date'),
                "gm": d.get('gm'),
                "ls1": d.get('ls1'),
                "ak": d.get('ak'),
                "ls2": d.get('ls2'),
                "ls3": d.get('ls3'),
                "day": d.get('day')
            })
        return records
    except Exception as e:
        print(f"Warning: Failed to fetch from Firestore: {e}")
        return []

def load_all_data():
    all_records = []
    txt_records = parse_records_txt('Records.txt')
    all_records.extend(txt_records)
    
    firestore_records = fetch_firestore_data()
    all_records.extend(firestore_records)
    
    if not all_records:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df = df.drop_duplicates(subset=['date'], keep='last')
    
    targets = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    for col in targets:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['day_of_month'] = df['date'].dt.day
    
    for col in targets:
        df[f'{col}_lag1'] = df[col].shift(1).fillna(0)
        df[f'{col}_lag2'] = df[col].shift(2).fillna(0)
        
    return df

if __name__ == "__main__":
    df = load_all_data()
    if not df.empty:
        print(df.tail())
        print(f"Total records processed: {len(df)}")
        df.to_csv('ml/processed_data.csv', index=False)
