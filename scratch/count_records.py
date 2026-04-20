import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/Muhammad.Umair/Desktop/akwebapp/ak-analysis-system-umair-firebase-adminsdk-fbsvc-6eceff3ff0.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def count_records():
    print("Counting records in 'draws' collection...")
    docs = db.collection('draws').stream()
    count = 0
    for doc in docs:
        count += 1
    print(f"Total records found in Firestore: {count}")

if __name__ == "__main__":
    count_records()
