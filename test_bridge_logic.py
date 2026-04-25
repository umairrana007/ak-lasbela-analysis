import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_digits(val):
    val_str = str(val).strip()
    # Handle nan or non-numeric
    if not any(char.isdigit() for char in val_str):
        return None, None
    # Use only digits
    digits = "".join(filter(str.isdigit, val_str))
    if len(digits) == 1:
        digits = "0" + digits
    if len(digits) < 2:
        return None, None
    # Take the last 2 digits if more than 2
    digits = digits[-2:]
    return digits[0], digits[1]

def load_data():
    data_path = "2023-2024-2025-2026 complete data.txt"
    df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
    df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')
    # Filter for Feb - March 2026 as requested "old data"
    start_date = pd.to_datetime('01/01/2026', format='%d/%m/%Y')
    df = df[df['Date_dt'] >= start_date]
    return df

def test_logic():
    df = load_data()
    results = []
    
    game_list = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
    game_next = {
        'GM': 'LS1',
        'LS1': 'AK',
        'AK': 'LS2',
        'LS2': 'LS3',
        'LS3': 'GM'
    }

    # Bridge Pairs to track: [Jodi1, Jodi2, OriginDate, PairType, state, target_jodi, target_games, hit1_date, hit1_game]
    pending_pairs = []

    for idx, row in df.iterrows():
        current_date = row['Date_dt']
        
        day_results = {}
        for g in game_list:
            o, c = get_digits(row[g])
            if o is not None:
                day_results[g] = o + c
        
        # 1. Check for hits in pending pairs
        for pair in pending_pairs[:]:
            if pair[4] == 0:
                j1, j2 = pair[0], pair[1]
                hit_found = False
                for game, val in day_results.items():
                    if val == j1 or val == j1[::-1]:
                        pair[4] = 1 # state
                        pair[5] = j2 # target_jodi
                        pair[6] = [game, game_next[game]] # target_games
                        pair[7] = current_date # hit1_date
                        pair[8] = game # hit1_game
                        hit_found = True
                        break
                    elif val == j2 or val == j2[::-1]:
                        pair[4] = 1 # state
                        pair[5] = j1 # target_jodi
                        pair[6] = [game, game_next[game]] # target_games
                        pair[7] = current_date # hit1_date
                        pair[8] = game # hit1_game
                        hit_found = True
                        break
                
                if not hit_found and (current_date - pair[2]).days > 30:
                    pending_pairs.remove(pair)

            elif pair[4] == 1:
                target_jodi = pair[5]
                target_games = pair[6]
                hit1_date = pair[7]
                
                if (current_date - hit1_date).days == 0:
                    continue # Wait for next day (as per user "next day GM or LS1")
                
                target_hit = False
                for tg in target_games:
                    if tg in day_results:
                        val = day_results[tg]
                        if val == target_jodi or val == target_jodi[::-1]:
                            results.append({
                                'Origin': pair[2].strftime('%d/%m/%Y'),
                                'PairType': pair[3],
                                'Pair': f"{pair[0]}-{pair[1]}",
                                'FirstHitDate': hit1_date.strftime('%d/%m/%Y'),
                                'FirstHitGame': pair[8],
                                'FinalHitDate': current_date.strftime('%d/%m/%Y'),
                                'FinalHitJodi': val,
                                'TargetGames': ",".join(target_games),
                                'Gap': (current_date - hit1_date).days
                            })
                            pending_pairs.remove(pair)
                            target_hit = True
                            break
                
                # Window: User says "4th or 5th day", let's check up to 10 days
                if not target_hit and (current_date - hit1_date).days > 10:
                    pending_pairs.remove(pair)

        # 2. Generate new pairs
        pairs_to_create = [
            ('GM', 'LS1'), ('LS1', 'AK'), ('AK', 'LS2'), ('LS2', 'LS3'), ('LS3', 'GM')
        ]
        
        for g1, g2 in pairs_to_create:
            o1, c1 = get_digits(row[g1])
            o2, c2 = get_digits(row[g2])
            
            if o1 is not None and o2 is not None:
                j1 = o1 + o2
                j2 = c1 + c2
                if j1 != j2 and j1 != j2[::-1]:
                    pending_pairs.append([j1, j2, current_date, f"{g1}-{g2}", 0, None, None, None, None])

    res_df = pd.DataFrame(results)
    print(f"Total Successes: {len(res_df)}")
    if len(res_df) > 0:
        # Sort by gap to see how quickly they hit
        print("\nTop 20 Successes (Shortest Gaps):")
        print(res_df.sort_values('Gap').head(20).to_string())
        
        # Calculate Average Gap
        print(f"\nAverage Gap: {res_df['Gap'].mean():.2f} days")
        
    res_df.to_csv('bridge_logic_results.csv', index=False)

if __name__ == "__main__":
    test_logic()
