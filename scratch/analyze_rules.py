import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/Muhammad.Umair/Desktop/akwebapp/ak-analysis-system-umair-firebase-adminsdk-fbsvc-6eceff3ff0.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def analyze_patterns():
    # 1. Parse User Rules
    rules = [
        (['21','12'], ['04','40']),
        (['02','20'], ['14','41']),
        (['03','30'], ['19','91','69','96']),
        (['01','10'], ['34','43','47','74']),
        (['18','81'], ['69','96']),
        (['32','29'], ['07','70']),
        (['75','57'], ['16','61']),
        (['73','37'], ['07','70','33','32']),
        (['54','45'], ['09','90','40','04']),
        (['44'], ['13','31']),
        (['56','65'], ['83','38','88']),
        (['13','31'], ['64','46','96','69','49','94']),
        (['42','24'], ['08','80','62','26']),
        (['35','52'], ['07','70','57','75']),
        (['02','20'], ['39','93']),
        (['06','60'], ['34','43','58','85']),
        (['05','50'], ['39','93']),
        (['35','53'], ['03','30','08','80']),
    ]

    # 2. Fetch Data (All)
    print("Fetching historical data from 'draws'...")
    all_docs = db.collection('draws').order_by('date', direction=firestore.Query.ASCENDING).get()
    data = []
    for d in all_docs:
        item = d.to_dict()
        data.append(item)
    
    df = pd.DataFrame(data)
    if df.empty:
        print("No data found!")
        return

    def get_row_numbers(row):
        cols = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
        return [str(row.get(c, '')).strip().zfill(2) for c in cols if row.get(c)]

    print(f"Analyzing {len(df)} records...")
    
    final_report = []
    
    for triggers, targets in rules:
        total_instances = 0
        success_hits = 0
        
        for i in range(len(df) - 10):
            current_nums = get_row_numbers(df.iloc[i])
            found_trigger = any(str(t).zfill(2) in current_nums for t in triggers)
            
            if found_trigger:
                total_instances += 1
                for j in range(i + 1, min(i + 11, len(df))):
                    future_nums = get_row_numbers(df.iloc[j])
                    if any(str(t).zfill(2) in future_nums for t in targets):
                        success_hits += 1
                        break

        accuracy = (success_hits / total_instances * 100) if total_instances > 0 else 0
        final_report.append({
            'Trigger': ",".join(triggers),
            'Target': ",".join(targets),
            'Count': total_instances,
            'Hits': success_hits,
            'Accuracy': f"{round(accuracy, 1)}%"
        })

    print("\n--- PATTERN SUCCESS REPORT ---")
    report_df = pd.DataFrame(final_report).sort_values(by='Count', ascending=False)
    print(report_df.to_string(index=False))

if __name__ == "__main__":
    analyze_patterns()
