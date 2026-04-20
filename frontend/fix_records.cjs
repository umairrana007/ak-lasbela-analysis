const fs = require('fs');
const path = require('path');

const recordsPath = path.join(__dirname, '..', 'Records.txt');
const outputPath = path.join(__dirname, 'src', 'parsed_records.json');

const content = fs.readFileSync(recordsPath, 'utf8');
const lines = content.split('\n');

const results = [];
let currentYear = '2025';

lines.forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed) return;

    // Year detection
    if (trimmed.includes('2026')) { currentYear = '2026'; return; }
    if (trimmed.includes('2025')) { currentYear = '2025'; return; }

    // Improved parsing logic
    // 1. Extract Date (DD/MM)
    const dateMatch = trimmed.match(/^(\d{2})[\/.](\d{2})/);
    if (!dateMatch) return;
    const dayNum = dateMatch[1];
    const monthNum = dateMatch[2];

    // 2. Extract all 2-digit numbers
    // We look for numbers that aren't part of the date
    const remainingText = trimmed.slice(5); // skip the date part "DD/MM"
    const numbers = remainingText.match(/\d{2}/g) || [];
    
    // 3. Extract Day of Week
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Tues', 'Thur', 'Fir'];
    let dayOfWeek = '';
    for (const d of days) {
        if (trimmed.toLowerCase().includes(d.toLowerCase())) {
            dayOfWeek = d;
            break;
        }
    }

    if (numbers.length >= 5) {
        const isoDate = `${currentYear}-${monthNum}-${dayNum}`;
        const displayDate = `${dayNum}/${monthNum}/${currentYear.slice(2)}`;

        results.push({
            date: isoDate,
            display_date: displayDate,
            gm: numbers[0],
            ls1: numbers[1],
            ak: numbers[2],
            ls2: numbers[3],
            ls3: numbers[4],
            day: dayOfWeek,
            isFirebase: false
        });
    }
});

// Sort by date descending
results.sort((a, b) => new Date(b.date) - new Date(a.date));

fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
console.log(`Successfully parsed ${results.length} records into ${outputPath}`);
