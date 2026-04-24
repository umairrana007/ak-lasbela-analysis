import re

data = """
01/03..68.89.82.83.48..Sun
02/03..00.87.83.29.87.Mon
03/03..51.19.03.28.49.Tue
04/03..57.54.41.13.55.Wed
05/03..96.22.23.91.41.Thur
06/03.14.89.26.26.91.Fri
07/03..08.13.88.84.03.Sat
08/03..67.14.29.30.72.Sun
09/03..40.85.32.00.91.Mon
10/03..29.85.87.27.58.Tue
11/03..48.48.64.08.38.Wed
12/03..92.68.29.65.87.Thur
13/03.96.29.71.45.07.Fri
14/03..47.04.22.46.76.Sat
15/03..40.66.75.68.26.Sun
16/03..56.03.67.90.46.Mon
17/03..89.56.05.72.07.Tue
18/03..63.91.22.14.63.Wed
19/03.92.23.05.17.68.Thur
20/03.82.40.54.52.21.Fri
23/03..20.25.44.15.87.Sat
24/03..12.12.12.36.08.Sun
25/03..40.06.94.04.45.Mon
26/03..55.87.62.40.51.Thur
27/03..81.99.56.44.43.Fri
28/03..86.16.98.98.95.Sat
29/03..61.12.09.83.61.Sun
30/03..58.92.25.03.06.Mon
31/03..76.55.20.59.44.Wed
01/04.97.92.69.06.23.Thur
02/04..52.46.06.30.76.Fri
03/04..22.63.19.03.56.Fri
04/04..86.88.04.92.96.Sat
05/04..75.53.06.13.96.Sun
06/04..61.76.17.05.79.Mon
07/04..59.16.99.58.93.Tue
08/04..61.81.79.02.49.Wed
09/04.65.62.71.56.45.Thur
10/04..30.17.87.76.63..Fri
19/04..81.56.40.57.37..Sun
"""

records = []
for line in data.strip().split('\n'):
    parts = re.findall(r'\d+', line)
    if len(parts) >= 7:
        date = f"{parts[0]}/{parts[1]}"
        nums = parts[2:7]
        records.append({'date': date, 'nums': nums})

lines_to_check = {
    'Line 1 (7,1,2)': {'7', '1', '2'},
    'Line 2 (7,1,0)': {'7', '1', '0'},
    'Line 3 (7,1,5)': {'7', '1', '5'},
    'Line 4 (7,1,9)': {'7', '1', '9'}
}

columns = ['GM', 'LS1', 'AK', 'LS2', 'LS3']

for line_name, target_digits in lines_to_check.items():
    print(f"\n=== {line_name} ===")
    
    # Check horizontal
    for row in records:
        for i in range(4):
            pair_digits = set(row['nums'][i] + row['nums'][i+1])
            if target_digits.issubset(pair_digits):
                print(f"Horizontal (Aamne-Samne): {row['date']} -> {columns[i]} ({row['nums'][i]}) aur {columns[i+1]} ({row['nums'][i+1]})")
                
    # Check vertical
    for r in range(len(records) - 1):
        for c in range(5):
            pair_digits = set(records[r]['nums'][c] + records[r+1]['nums'][c])
            if target_digits.issubset(pair_digits):
                print(f"Vertical (Uper-Neechay): {records[r]['date']} aur {records[r+1]['date']} -> {columns[c]} main ({records[r]['nums'][c]} aur {records[r+1]['nums'][c]})")
