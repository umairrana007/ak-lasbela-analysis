@echo off
echo ===========================================
echo    AK Lasbela AI Sync & Retrain System
echo ===========================================
echo.
echo 1. Fetching latest data from Firebase...
python ml/data_loader.py
echo.
echo 2. Training Models on latest trends...
python ml/train_model.py
echo.
echo 3. Generating new Predictions...
python ml/predict.py
echo.
echo 4. Uploading to Dashboard...
python backend/upload_to_firestore.py predictions
echo.
echo ===========================================
echo    DONE! Refresh your dashboard now.
echo ===========================================
pause
