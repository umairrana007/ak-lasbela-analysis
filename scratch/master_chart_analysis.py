import pandas as pd
import re
import os

def parse_records():
    file_path = 'Records.txt'
    if not os.path.exists(file_path): return []
    records = []
    current_year = 2025
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if "2026" in line: current_year = 2026
            if "2025" in line: current_year = 2025
            match = re.search(r'(\d{2}/\d{2})\.+([\d\.]+)\.+(\w+)', line)
            if match:
                nums = [n.zfill(2) for n in match.group(2).split('.') if n]
                if len(nums) == 5:
                    records.append({"date": f"{match.group(1)}/{current_year}", "nums": nums})
    return records

def analyze_master_chart():
    data = parse_records()
    raw_rules = """01==96.52
02==62.06
03==16.72
04==82.26
05==36.92
06==02.46
07==56.12
08==22.66
09==76.32
10==43.87
11==97.53
12==63.07
13==17.73
14==83.27
15==37.93
16==03.47
17==57.13
18==23.67
19==77.33
20==44.88
21==98.54
22==64.08
23==18.74
24==84.28
25==38.94
26==04.48
27==58.14
28==24.68
29==78.34
30==45.89
31==99.68
32==65.09
33==19.76
34==85.29
35==39.95
36==05.49
37==59.15
38==25.69
39==79.35
40==46.80
41==90.56
42==66.00
43==10.76
44==86.20
45==30.96
46==06.40
47==50.16
48==26.60
49==70.36
50==47.81
51==91.57
52==67.01
53==11.77
54==87.21
55==31.97
56==07.41
57==51.17
58==27.61
59==71.37
60==48.82
61==92.58
62==68.02
63==12.78
64==88.22
65==32.98
66==08.42
67==52.18
68==28.62
69==72.38
70==49.83
71==93.59
72==69.03
73==13.79
74==89.23
75==33.99
76==09.43
77==53.19
78==29.63
79==73.39
80==40.84
81==94.50
82==60.04
83==14.70
84==80.24
85==34.94
86==00.44
87==54.10
88==20.64
89==74.30
90==41.85
91==95.81
92==61.05
93==15.71
94==81.25
95==35.91
96==01.45
97==55.11
98==21.65
99==75.31
00==42.86"""
    
    rules = []
    for line in raw_rules.strip().split('\n'):
        parts = line.split('==')
        trig = parts[0].zfill(2)
        targets = [t.zfill(2) for t in re.split(r'[\.\s,]', parts[1]) if t]
        rules.append((trig, targets))

    print(f"--- Master Chart Analysis (Total Records: {len(data)}) ---")
    results = []
    for trig, targets in rules:
        count = 0
        hits = 0
        for i in range(len(data) - 10):
            if trig in data[i]['nums']:
                count += 1
                if any(any(t in data[j]['nums'] for t in targets) for j in range(i + 1, i + 11)):
                    hits += 1
        acc = (hits / count * 100) if count > 0 else 0
        results.append({"Number": trig, "Targets": ",".join(targets), "Instances": count, "Hits": hits, "Accuracy": acc})

    df_res = pd.DataFrame(results).sort_values(by='Accuracy', ascending=False)
    print(df_res.head(20).to_string(index=False))
    print("\n--- Summary Statistics ---")
    print(f"Average Accuracy across all 100 numbers: {df_res['Accuracy'].mean():.1f}%")

if __name__ == "__main__":
    analyze_master_chart()
