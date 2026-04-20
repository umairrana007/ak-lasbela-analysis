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
        for line in f:
            if "2026" in line:
                current_year = 2026
            
            match = re.search(r'(\d{2}/\d{2})\.\.([\d\.]+)\.\.(\w+)', line)
            if match:
                date_short = match.group(1)
                nums = match.group(2).split('.')
                nums = [n for n in nums if n]
                day = match.group(3)
                
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
    
    # Load from the verified clean JSON
    json_path = 'frontend/src/parsed_records.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            all_records = json.load(f)
    else:
        # Fallback if not found
        print(f"Warning: {json_path} not found. Trying to parse Records.txt")
        all_records = parse_records_txt('Records.txt')
        
    # Also fetch latest from Firestore to include UI-added records
    print("Fetching latest records from Firestore...")
    firebase_records = fetch_firestore_data()
    if firebase_records:
        all_records.extend(firebase_records)
        print(f"Added {len(firebase_records)} records from Firestore.")
        
    if not all_records:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_records)
    
    # Remove duplicates by date
    df = df.drop_duplicates(subset=['date'])
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['day_of_month'] = df['date'].dt.day
    
    # Convert result columns to numeric
    targets = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    for col in targets:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add lag features
    for col in targets:
        df[f'{col}_lag1'] = df[col].shift(1)
        df[f'{col}_lag2'] = df[col].shift(2)
        
    return df.dropna()

if __name__ == "__main__":
    df = load_all_data()
    
    if not df.empty:
        print(df.tail())
        print(f"Total records processed: {len(df)}")
        
        output_path = 'ml/processed_data.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")
    else:
        print("No data to process.")

