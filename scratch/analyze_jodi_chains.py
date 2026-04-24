import json
from collections import Counter

def analyze_sequences():
    with open('frontend/src/parsed_records.json', 'r') as f:
        records = json.load(f)

    # Sort records by date (oldest to newest)
    records.sort(key=lambda x: x['date'])

    set1 = {'0', '2', '4', '5', '9'}
    set2 = {'1', '3', '6', '7', '8'}

    def get_set(val):
        if not val or len(val) < 2: return None
        # Checking if BOTH digits are in the same set? 
        # Usually "Set" refers to the individual digits (Haroofs).
        # A jodi like '24' is Set 1 + Set 1.
        # A jodi like '13' is Set 2 + Set 2.
        # A jodi like '21' is Set 1 + Set 2.
        d1, d2 = val[0], val[1]
        if d1 in set1 and d2 in set1: return "S1-S1"
        if d1 in set2 and d2 in set2: return "S2-S2"
        if d1 in set1 and d2 in set2: return "S1-S2"
        if d1 in set2 and d2 in set1: return "S2-S1"
        return "Unknown"

    # We'll track jodi -> next_jodi transitions for all games
    transitions = []
    
    # Flatten games into a sequence
    # Draw order: GM -> LS1 -> AK -> LS2 -> LS3
    draw_sequence = []
    for r in records:
        for key in ['gm', 'ls1', 'ak', 'ls2', 'ls3']:
            if key in r and r[key]:
                draw_sequence.append(r[key])

    # Find common sequences
    pairs = []
    for i in range(len(draw_sequence) - 1):
        pairs.append((draw_sequence[i], draw_sequence[i+1]))

    counter = Counter(pairs)
    most_common = counter.most_common(50)

    print("--- Top 20 Hit Chains (Jodi followed by Jodi) ---")
    for (prev, curr), count in most_common[:20]:
        p_set = get_set(prev)
        c_set = get_set(curr)
        print(f"{prev} ({p_set}) -> {curr} ({c_set}) | Hits: {count}")

    # Set Specific Analysis
    print("\n--- Set 1 to Set 1 Chains ---")
    s1_s1_chains = [p for p in pairs if get_set(p[0]) == "S1-S1" and get_set(p[1]) == "S1-S1"]
    for p, count in Counter(s1_s1_chains).most_common(10):
        print(f"{p[0]} -> {p[1]} | Count: {count}")

    print("\n--- Set 1 to Set 2 (Cross) Chains ---")
    cross_chains = [p for p in pairs if get_set(p[0]) == "S1-S1" and get_set(p[1]) == "S2-S2"]
    for p, count in Counter(cross_chains).most_common(10):
        print(f"{p[0]} -> {p[1]} | Count: {count}")

if __name__ == "__main__":
    analyze_sequences()
