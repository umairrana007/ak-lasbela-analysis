import subprocess
import sys
import time
import os

def run_step(name, command):
    print(f"{'='*20}")
    print(f"STEP: {name}")
    print(f"Executing: {command}")
    print(f"{'='*20}")
    
    start_time = time.time()
    try:
        # Use sys.executable to ensure we use the same python environment
        process = subprocess.Popen([sys.executable] + command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            print(f"  {line.strip()}")
            
        process.wait()
        elapsed = time.time() - start_time
        
        if process.returncode == 0:
            print(f"SUCCESS: {name} completed in {elapsed:.2f}s")
            return True
        else:
            print(f"FAILED: {name} exited with code {process.returncode}")
            return False
    except Exception as e:
        print(f"ERROR: {name} failed with exception: {e}")
        return False

def main():
    print("Starting AK Lasbela Automation Pipeline")
    
    # Define steps
    steps = [
        ("Scrape Data", "backend/scraper.py"),
        ("Update Firestore Draws", "backend/upload_to_firestore.py"),
        ("Pre-process Data", "ml/data_loader.py"),
        ("Train Models", "ml/train_model.py"),
        ("Generate Predictions", "ml/predict.py"),
        ("Upload Predictions", "backend/upload_to_firestore.py predictions")
    ]
    
    for name, cmd in steps:
        success = run_step(name, cmd)
        if not success:
            print(f"\n[X] Pipeline stopped due to failure in '{name}'")
            sys.exit(1)
            
    print("\n[V] Pipeline completed successfully!")
    print("All draw data and predictions are now live on the dashboard.")

if __name__ == "__main__":
    main()
