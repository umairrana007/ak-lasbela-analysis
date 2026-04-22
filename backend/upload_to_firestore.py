import json
import os
from google.cloud import firestore
from datetime import datetime

def get_firestore_client():
    try:
        import glob
        key_files = glob.glob("*.json")
        key_file = next((f for f in key_files if "firebase-adminsdk" in f), None)
        creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        if key_file:
            return firestore.Client.from_service_account_json(key_file)
        elif creds_json:
            with open("temp_creds.json", "w") as f:
                f.write(creds_json)
            return firestore.Client.from_service_account_json("temp_creds.json")
        else:
            return firestore.Client(project='ak-analysis-system-umair')
    except Exception as e:
        print(f"Failed to connect to Firestore: {e}")
        return None

def upload_draws():
    db = get_firestore_client()
    if not db: return

    json_path = 'backend/last_fetch.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    print(f"Uploading {len(data)} draw records...")
    
    batch = db.batch()
    count = 0
    for record in data:
        doc_id = record['date']
        doc_ref = db.collection('draws').document(doc_id)
        batch.set(doc_ref, record)
        count += 1
        
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Committed {count} records")

    batch.commit()
    print(f"Finished uploading {count} records to 'draws' collection.")

def upload_predictions():
    db = get_firestore_client()
    if not db: return

    pred_path = 'ml/predictions.json'
    if not os.path.exists(pred_path):
        print(f"Prediction file not found: {pred_path}")
        return

    with open(pred_path, 'r') as f:
        predictions = json.load(f)

    # Add metadata
    predictions['last_updated'] = datetime.now().isoformat()
    
    # Store as 'latest' for the frontend to consume
    db.collection('predictions').document('latest').set(predictions)
    print("Latest predictions uploaded to Firestore.")

    # Also store in history with date as ID
    pred_date = predictions.get('date', datetime.now().strftime('%Y-%m-%d'))
    db.collection('predictions_history').document(pred_date).set(predictions)
    print(f"Prediction history updated for {pred_date}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "predictions":
        upload_predictions()
    else:
        upload_draws()
        upload_predictions()
