content = open('ml/data_loader.py', 'r', encoding='utf-8').read()

old_block = """    # Load from the verified clean JSON
    json_path = 'frontend/src/parsed_records.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            all_records = json.load(f)
    else:
        # Fallback if not found
        print(f"Warning: {json_path} not found. Trying to parse Records.txt")
        all_records = parse_records_txt('Records.txt')"""

new_block = """    # 1. ALWAYS load from the master source of truth: Records.txt
    txt_records = parse_records_txt('Records.txt')
    all_records.extend(txt_records)
    print(f"Loaded {len(txt_records)} records from Records.txt")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('ml/data_loader.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("data_loader.py patched successfully.")
else:
    # Try a more flexible match if whitespace differs
    print("Literal match failed. Attempting fuzzy match...")
    import re
    pattern = r"# Load from the verified clean JSON.*?all_records = parse_records_txt\('Records.txt'\)"
    content = re.sub(pattern, new_block, content, flags=re.DOTALL)
    with open('ml/data_loader.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("data_loader.py patched via regex.")
