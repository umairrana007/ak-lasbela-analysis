import json
from itertools import combinations

def discover_best_set():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    records.sort(key=lambda x: x['date'])

    def get_repeat_chance(target_digits):
        target_digits = set(target_digits)
        hit_days = []
        for i in range(len(records)):
            day_hits = False
            for k in draw_keys:
                val = records[i].get(k)
                if val and val != '--' and val != '??':
                    if all(d in target_digits for d in str(val).zfill(2)):
                        day_hits = True
                        break
            hit_days.append(day_hits)
        
        total_hits = sum(hit_days[:-1])
        repeats = 0
        for i in range(len(hit_days) - 1):
            if hit_days[i] and hit_days[i+1]:
                repeats += 1
        
        return (repeats / total_hits * 100) if total_hits > 0 else 0

    # Test some common sets
    sets_to_test = [
        ('2', '0', '4', '9', '5'), # User's current set
        ('1', '3', '6', '7', '8'), # The remaining digits
        ('1', '2', '3', '4', '5'), # Lower half
        ('6', '7', '8', '9', '0'), # Upper half
        ('1', '6', '2', '7', '3'), # Mirror set 1
        ('4', '9', '5', '0', '1')  # Mirror set 2
    ]

    print("--- Set Performance (Next Day Repeat Chance) ---")
    for s in sets_to_test:
        chance = get_repeat_chance(s)
        print(f"Set {s}: {chance:.2f}%")

if __name__ == "__main__":
    discover_best_set()
