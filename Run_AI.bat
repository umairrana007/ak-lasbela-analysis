@echo off
echo ===========================================
echo    AK Lasbela AI Sync
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
echo 4. Uploading results (Local Sync)...
copy frontend\src\predictions.json ml\predictions.json

echo.
echo ===========================================
echo    DONE! Refresh your dashboard now.
echo ===========================================
pause
