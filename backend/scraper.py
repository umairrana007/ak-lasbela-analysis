import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json

class LasbelaScraper:
    def __init__(self):
        self.url = "https://dailyaklasbelakarachipk10.com/ak-lasbela/lasbela-record/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_records(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def parse_records(self, html):
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        records = []
        
        # Robust pattern to find date, numbers (any amount), and day
        # Pattern like *_01/01..13.69.32.99.43.35..Thu_*
        pattern = r'\*_(\d{2}/\d{2})\.\.([\d\.]+)\.\.(\w+)\_\*'
        
        all_text = soup.get_text()
        matches = re.finditer(pattern, all_text)
        
        current_year = datetime.now().year
        
        for m in matches:
            date_short = m.group(1)
            numbers_str = m.group(2)
            day = m.group(3)
            
            numbers = numbers_str.split('.')
            numbers = [n for n in numbers if n] # Filter out empty strings
            
            # If there are 6 numbers, the first one is 'bekar' (useless) as per user
            if len(numbers) == 6:
                numbers = numbers[1:]
            
            if len(numbers) == 5:
                # Try to construct a full ISO date.
                day_month = date_short.split('/')
                full_date = f"{current_year}-{day_month[1]}-{day_month[0]}"
                
                record = {
                    "date": full_date,
                    "display_date": date_short,
                    "gm": numbers[0],
                    "ls1": numbers[1],
                    "ak": numbers[2],
                    "ls2": numbers[3],
                    "ls3": numbers[4],
                    "day": day,
                    "timestamp": datetime.now().isoformat()
                }
                records.append(record)
            
        return records

if __name__ == "__main__":
    scraper = LasbelaScraper()
    print("Fetching records from dailyaklasbelakarachipk10.com...")
    html = scraper.fetch_records()
    if html:
        data = scraper.parse_records(html)
        print(f"Found {len(data)} records.")
        # For local testing, we print the first few
        for r in data[:5]:
            print(json.dumps(r, indent=2))
        
        # Save to a local json for debug
        with open('backend/last_fetch.json', 'w') as f:
            json.dump(data, f, indent=2)

