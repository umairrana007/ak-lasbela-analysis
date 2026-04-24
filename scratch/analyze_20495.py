import json

def analyze_patterns():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    target_digits = {'2', '0', '4', '9', '5'}
    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']

    def is_target_pair(val):
        if not val or val == '--' or val == '??':
            return False
        val_str = str(val).zfill(2)
        return all(d in target_digits for d in val_str)

    total_days_with_target = 0
    same_day_followups = 0
    
    total_trigger_instances = 0 # Count of draws that hit a target pair
    subsequent_draw_hits = 0 # Count of times a subsequent draw on the same day hit

    next_day_hits = 0
    days_to_check_next = 0

    # Sort records by date ascending
    records.sort(key=lambda x: x['date'])

    for i, record in enumerate(records):
        day_targets = []
        for k in draw_keys:
            if is_target_pair(record.get(k)):
                day_targets.append(k)
        
        if day_targets:
            total_days_with_target += 1
            
            # Same Day Analysis
            # For each hit, check if there was a hit in a LATER draw
            for idx, draw_key in enumerate(day_targets):
                total_trigger_instances += 1
                # Check draws after this one in the same day
                current_draw_idx = draw_keys.index(draw_key)
                for next_draw_key in draw_keys[current_draw_idx + 1:]:
                    if is_target_pair(record.get(next_draw_key)):
                        subsequent_draw_hits += 1
                        break # Only count the first followup for this specific trigger instance

            # Next Day Analysis
            if i < len(records) - 1:
                days_to_check_next += 1
                next_record = records[i+1]
                hit_next_day = any(is_target_pair(next_record.get(k)) for k in draw_keys)
                if hit_next_day:
                    next_day_hits += 1

    print(f"Total days analyzed: {len(records)}")
    print(f"Days with at least one '20495' jori: {total_days_with_target}")
    
    if total_trigger_instances > 0:
        same_day_pct = (subsequent_draw_hits / total_trigger_instances) * 100
        print(f"Same Day Follow-up Chance: {same_day_pct:.2f}% ({subsequent_draw_hits}/{total_trigger_instances})")
    
    if days_to_check_next > 0:
        next_day_pct = (next_day_hits / days_to_check_next) * 100
        print(f"Next Day Repeat Chance: {next_day_pct:.2f}% ({next_day_hits}/{days_to_check_next})")

if __name__ == "__main__":
    analyze_patterns()
