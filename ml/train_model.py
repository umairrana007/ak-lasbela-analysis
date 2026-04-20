import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os
import numpy as np

def train_lottery_models(data_path):
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        return
        
    df = pd.read_csv(data_path)
    
    # We want to predict gm, ls1, ak, ls2, ls3
    targets = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Features: day_of_week, month, day_of_month, and lags
    features = ['day_of_week', 'month', 'day_of_month']
    for t in targets:
        features.extend([f'{t}_lag1', f'{t}_lag2'])
        
    models = {}
    
    for target in targets:
        print(f"Training model for {target}...")
        
        X = df[features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        print(f"{target} RMSE: {rmse:.4f}")
        
        models[target] = model
        
        # Save model
        joblib.dump(model, f'ml/model_{target}.pkl')
        
    print("All models trained and saved.")

def generate_poisson_simulations(df, target_col, num_sims=1000):
    # Calculate the average (lambda) for the target column
    avg = df[target_col].mean()
    
    # Generate poisson distribution
    sims = np.random.poisson(avg, num_sims)
    
    # Get top 5 most frequent numbers in simulation
    unique, counts = np.unique(sims, return_counts=True)
    frequencies = sorted(zip(unique, counts), key=lambda x: x[1], reverse=True)
    
    # Return top numbers that are between 0 and 99
    top_numbers = [int(n[0]) for n in frequencies if 0 <= n[0] <= 99][:5]
    return top_numbers

if __name__ == "__main__":
    csv_path = 'ml/processed_data.csv'
    train_lottery_models(csv_path)
    
    # Simple simulation demo
    df = pd.read_csv(csv_path)
    for t in ['gm', 'ls1', 'ak']:
        sims = generate_poisson_simulations(df, t)
        print(f"Poisson Simulation Top 5 for {t}: {sims}")
