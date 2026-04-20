import re
import os

def clean_records(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Match pattern like 01/01..13.61.46.61.47.64..Wed
        # or 01/01..61.46.61.47.64..Wed
        match = re.search(r'(\d{2}/\d{2})\.\.([\d\.]+)\.\.(\w+)', line)
        if match:
            date_part = match.group(1)
            numbers_part = match.group(2)
            day_part = match.group(3)
            
            numbers = numbers_part.split('.')
            # Remove empty strings from split
            numbers = [n for n in numbers if n]
            
            if len(numbers) == 6:
                # Remove the first number as per user requirement
                numbers = numbers[1:]
                print(f"Cleaned line: {line.strip()} -> removed first number")
            
            # Reconstruct the line
            new_numbers_part = '.'.join(numbers)
            new_line = f"{date_part}..{new_numbers_part}..{day_part}\n"
            cleaned_lines.append(new_line)
        else:
            cleaned_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Finished cleaning {file_path}")

if __name__ == "__main__":
    clean_records('Records.txt')
