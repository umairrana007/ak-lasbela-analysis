import firebase_admin
from firebase_admin import credentials, firestore

try:
    if not firebase_admin._apps:
        # Try to use default credentials
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': 'ak-analysis-system-umair',
        })
    db = firestore.client()
    print("Successfully connected to Firestore!")
    # Test a simple read
    doc = db.collection('draws').document('2025-01-01').get()
    if doc.exists:
        print(f"Test read successful: {doc.to_dict()}")
    else:
        print("Test read: Document not found, but connection works.")
except Exception as e:
    print(f"Auth failed: {e}")
