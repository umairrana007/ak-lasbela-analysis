import glob
from google.cloud import firestore

key_files = glob.glob("*.json")
key_file = next((f for f in key_files if "firebase-adminsdk" in f), None)

if not key_file:
    print("Key file not found")
    exit()

db = firestore.Client.from_service_account_json(key_file)
data = {
    'date': '2026-04-14',
    'day': 'Tuesday',
    'gm': '15',
    'ls1': '03',
    'ak': '02',
    'ls2': '02',
    'ls3': '80',
    'display_date': '14/04/26',
    'timestamp': '2026-04-20T11:00:00Z'
}
db.collection('draws').document('2026-04-14').set(data)
print("Record for 14/04 added successfully.")
