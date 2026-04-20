with open('Records.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Target range (426-429 in 1-based indexing is 425-428 in 0-based)
# We want to replace these 4 lines with 3 clean lines
new_lines = [
    "28/02..71.20.59.57.66..Sat\n",
    "彡༆🧛‍♂️-01-03-2026-🧛‍♂️༆彡\n",
    "01/03..68.89.82.83.48..Sun\n"
]

lines[425:429] = new_lines

with open('Records.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Records.txt fixed successfully via Python.")
