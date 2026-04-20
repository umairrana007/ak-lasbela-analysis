from ml.data_loader import fetch_firestore_data
import json

data = fetch_firestore_data()
with open('scratch/firestore_debug.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f"Total records in Firestore: {len(data)}")
for d in data[:5]:
    print(d)
