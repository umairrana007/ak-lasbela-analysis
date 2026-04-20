const fs = require('fs');
const path = require('path');

const recordsPath = path.join(__dirname, 'Records.txt');
const outputPath = path.join(__dirname, 'frontend', 'src', 'parsed_records.json');

const content = fs.readFileSync(recordsPath, 'utf8');
const lines = content.split('\n');

const results = [];
let currentYear = '2025';

lines.forEach(line => {
    line = line.trim();
    if (!line) return;

    // Detect year changes if any (like ꧁🌹༆ 2026 ༆🌹꧂)
    if (line.includes('2026')) {
        currentYear = '2026';
        return;
    }
    if (line.includes('2025')) {
        currentYear = '2025';
        return;
    }

    // Match patterns like: 01/01..61.46.61.47.64..Wed
    // Regex explanation: 
    // ^(\d{2}/\d{2}) -> Date (DD/MM)
    // \.\. -> double dots
    // (\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2}) -> 5 pairs of digits separated by dots
    // \.\. -> double dots
    // (\w+) -> Day of week
    const match = line.match(/^(\d{2}\/\d{2})\.\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.\.(\w+)/);
    
    if (match) {
        const [_, datePart, v1, v2, v3, v4, v5, day] = match;
        const [dayNum, monthNum] = datePart.split('/');
        
        // Convert to ISO-like date string for Firestore compatibility if needed
        // Format: YYYY-MM-DD
        const isoDate = `${currentYear}-${monthNum}-${dayNum}`;
        const displayDate = `${dayNum}-${monthNum}-${currentYear.slice(2)}`;

        results.push({
            date: isoDate,
            display_date: displayDate,
            values: [v1, v2, v3, v4, v5, '00'], // Assuming 6th value is 00 for now as Records.txt has 5
            day: day
        });
    }
});

fs.writeFileSync(outputPath, JSON.stringify(results.reverse(), null, 2));
console.log(`Successfully parsed ${results.length} records to ${outputPath}`);
