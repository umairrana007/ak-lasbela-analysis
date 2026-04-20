from data_loader import load_all_data
df = load_all_data()
print(f"Total Records: {len(df)}")
print("--- Last 3 Days ---")
print(df.tail(3)[['date', 'gm', 'ls1', 'ak', 'ls2', 'ls3']])
